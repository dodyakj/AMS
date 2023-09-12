# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _

class OverhaulAircraftPart(models.Model):
    _name = 'airworthy.overhaul.part'
    _description = 'Overhaul Part'

    overhaul_id = fields.Many2one('airworthy.overhaul', string="Overhaul Id")
    is_overhaul = fields.Boolean(string='Overhaul')
    part_name = fields.Char(string='Part')
    part_id = fields.Many2one('ams.component.part', string='Part')
    product_id = fields.Many2one('product.product', string='Product', related="part_id.product_id",readonly=True)
    hours = fields.Float(string='Hours',related="part_id.tso",readonly=True)
    cycles = fields.Float(string='Hours',related="part_id.cso",readonly=True)
    old_serial_number = fields.Many2one('stock.production.lot', string='Old Serial Number')
    new_serial_number = fields.Many2one('stock.production.lot', string='New Serial Number')

class OverhaulAircraft(models.Model):
    _name = 'airworthy.overhaul'
    _description = 'Overhaul'
    _rec_name = 'fleet_id'
    
    fleet_id  = fields.Many2one('aircraft.acquisition', string="Aircraft Registration",readonly=True, default=lambda self:self.env.context.get('fleet_id',False))
    engine_id  = fields.Many2one('engine.type', string="Engine",readonly=True, default=lambda self:self.env.context.get('engine_id',False))
    propeller_id  = fields.Many2one('propeller.type', string="Propeller",readonly=True, default=lambda self:self.env.context.get('propeller_id',False))
    auxiliary_id  = fields.Many2one('auxiliary.type', string="Auxiliary",readonly=True, default=lambda self:self.env.context.get('auxiliary_id',False))
    part_id = fields.Many2one('ams.component.part', string='Part',readonly=True, default=lambda self:self.env.context.get('part_id',False))
    

    part_ids = fields.One2many('airworthy.overhaul.part','overhaul_id',string='Part', compute=lambda self: self._part_ids())
    
    current_hours = fields.Float(string='Current Hours', default=lambda self:self._get_vals()['total_hours'], readonly=True)
    current_cycles = fields.Float(string='Current Cycles', default=lambda self:self._get_vals()['total_landings'], readonly=True)
    current_rins = fields.Integer(string='Current RIN', default=lambda self:self._get_vals()['total_rins'], readonly=True)

    overhaul_date = fields.Date(string='Overhaul at', default=fields.Date.today(),required=True)
    overhaul_hours = fields.Float(string='Hours', default=lambda self:self._get_vals()['total_hours'])
    overhaul_cycles = fields.Float(string='Cycles', default=lambda self:self._get_vals()['total_landings'])
    overhaul_rins = fields.Float(string='RIN', default=lambda self:self._get_vals()['total_rins'])
    rin_active = fields.Boolean(string='RIN Active',related="fleet_id.rin_active",readonly=True)

    overhaul_sub = fields.Boolean(string='Reset Sub Component', default=True)
    component_of = fields.Selection([('airframe','Aircraft'),('engine','Engine'),('auxiliary','Auxiliary'),('propeller','Propeller')],string='Component of',default=lambda self:self._get_component_of())

    date = fields.Date(string='Start Date', default=fields.Date.today(),required=True)
    finish_date = fields.Date(string='Finish Date', default=fields.Date.today(),required=True)
    work_with = fields.Selection([('wo','Work Order'),('mwo','MWO')],string='Comply With')
    wo_id = fields.Many2one('ams.work.order', string="Work Order",default=False)
    mwo_id = fields.Many2one('ams.mwo', string="MWO",default=False)

    @api.model
    def _get_component_of(self):
        if(self.env.context.get('fleet_id',False) != False):
            print 'airframe'
            return 'airframe'
        elif(self.env.context.get('propeller_id',False) != False):
            print 'propeller'
            return 'propeller'
        elif(self.env.context.get('engine_id',False) != False):
            print 'engine'
            return 'engine'
        elif(self.env.context.get('auxiliary_id',False) != False):
            print 'auxiliary'
            return 'auxiliary'
        elif(self.env.context.get('part_id',False) != False):
            part_id = self.env['ams.component.part'].search([('id','=',self.env.context.get('part_id',False))],limit=1)
            if(part_id.part_id.id != False):
                part_id = part_id.part_id
            if(part_id.fleet_id.id != False):
                print 'airframe'
                return 'airframe'
            elif(part_id.propeller_id.id != False):
                print 'propeller'
                return 'propeller'
            elif(part_id.engine_id.id != False):
                print 'engine'
                return 'engine'
            elif(part_id.auxiliary_id.id != False):
                print 'auxiliary'
                return 'auxiliary'

    def _get_vals(self):
        
        fleet = self._get_fleet()
        if(self.env.context.get('fleet_id',False) != False):
            return {'total_hours' : fleet.total_hours, 'total_landings' : fleet.total_landings, 'total_rins':fleet.total_rins}
        elif(self.env.context.get('propeller_id',False) != False):
            return {'total_hours' : fleet.total_hours, 'total_landings' : fleet.total_landings, 'total_rins':fleet.total_rins}
        elif(self.env.context.get('engine_id',False) != False):
            engine = self.env['engine.type'].search([('id','=',self.env.context.get('engine_id',False))])
            return {'total_hours' : engine.engine_tsn, 'total_landings' : engine.engine_csn, 'total_rins':engine.engine_rsn}
        elif(self.env.context.get('auxiliary_id',False) != False):
            auxiliary = self.env['auxiliary.type'].search([('id','=',self.env.context.get('auxiliary_id',False))])
            return {'total_hours' : auxiliary.auxiliary_tsn, 'total_landings' : auxiliary.auxiliary_csn, 'total_rins':auxiliary.auxiliary_rsn}
        elif(self.env.context.get('part_id',False) != False):
            part_id = self.env['ams.component.part'].search([('id','=',self.env.context.get('part_id',False))],limit=1)
            if(part_id.part_id.id != False):
                part_id = part_id.part_id
            if(part_id.fleet_id.id != False):
                fleet = self.env['aircraft.acquisition'].search([('id','=',part_id.fleet_id.id)],limit=1) 
                return {'total_hours' : fleet.total_hours, 'total_landings' : fleet.total_landings, 'total_rins':fleet.total_rins}
            elif(part_id.propeller_id.id != False):
                fleet = self.env['aircraft.acquisition'].search([('id','=',part_id.fleet_id.id)],limit=1) 
                return {'total_hours' : fleet.total_hours, 'total_landings' : fleet.total_landings, 'total_rins':fleet.total_rins}
            elif(part_id.engine_id.id != False):
                engine = self.env['engine.type'].search([('id','=',part_id.engine_id.id)])
                return {'total_hours' : engine.engine_tsn, 'total_landings' : engine.engine_csn, 'total_rins':engine.engine_rsn}
            elif(part_id.auxiliary_id.id != False):
                auxiliary = self.env['auxiliary.type'].search([('id','=',part_id.auxiliary_id.id)])
                return {'total_hours' : auxiliary.auxiliary_tsn, 'total_landings' : auxiliary.auxiliary_csn, 'total_rins':auxiliary.auxiliary_rsn}
        return {'total_hours' : 0, 'total_landings' : 0, 'total_rins':0}

    def _get_fleet(self):
        if(self.env.context.get('fleet_id',False) != False):
            fleet_id = self.env['aircraft.acquisition'].search([('id','=',self.env.context.get('fleet_id',False))],limit=1) 
        elif(self.env.context.get('engine_id',False) != False):
            fleet_id = self.env['aircraft.acquisition'].search(['|','|','|',('engine_type_id','=',self.env.context.get('engine_id',False)),('engine2_type_id','=',self.env.context.get('engine_id',False)),('engine3_type_id','=',self.env.context.get('engine_id',False)),('engine4_type_id','=',self.env.context.get('engine_id',False))],limit=1) 
        elif(self.env.context.get('propeller_id',False) != False):
            fleet_id = self.env['aircraft.acquisition'].search(['|','|','|',('propeller_type_id','=',self.env.context.get('propeller_id',False)),('propeller2_type_id','=',self.env.context.get('propeller_id',False)),('propeller3_type_id','=',self.env.context.get('propeller_id',False)),('propeller4_type_id','=',self.env.context.get('propeller_id',False))],limit=1) 
        elif(self.env.context.get('auxiliary_id',False) != False):
            fleet_id = self.env['aircraft.acquisition'].search([('auxiliary_type_id','=',self.env.context.get('auxiliary_id',False))],limit=1) 
        elif(self.env.context.get('part_id',False) != False):
            part_id = self.env['ams.component.part'].search([('id','=',self.env.context.get('part_id',False))],limit=1)
            if(part_id.part_id.id != False):
                part_id = part_id.part_id
            if(part_id.fleet_id.id != False):
                fleet_id = self.env['aircraft.acquisition'].search([('id','=',part_id.fleet_id.id)],limit=1) 
            elif(part_id.engine_id.id != False):
                fleet_id = self.env['aircraft.acquisition'].search(['|','|','|',('engine_type_id','=',part_id.engine_id.id),('engine2_type_id','=',part_id.engine_id.id),('engine3_type_id','=',part_id.engine_id.id),('engine4_type_id','=',part_id.engine_id.id)],limit=1) 
            elif(part_id.propeller_id.id != False):
                fleet_id = self.env['aircraft.acquisition'].search(['|','|','|',('propeller_type_id','=',part_id.propeller_id.id),('propeller2_type_id','=',part_id.propeller_id.id),('propeller3_type_id','=',part_id.propeller_id.id),('propeller4_type_id','=',part_id.propeller_id.id)],limit=1) 
            elif(part_id.auxiliary_id.id != False):
                fleet_id = self.env['aircraft.acquisition'].search([('auxiliary_type_id','=',part_id.auxiliary_id.id)],limit=1) 
        if 'fleet_id' in locals() or 'fleet_id' in globals():
            return fleet_id
        else : 
            return False

    @api.multi 
    def action_save(self):
        #your code
        self.ensure_one()
        #close popup
        return {'type': 'ir.actions.act_window_close'}


    @api.onchange('part_id')
    def _part_ids(self):
        if self.fleet_id:
            self._onchange_fleet_id()
        if self.engine_id:
            self._onchange_engine_id()
        if self.propeller_id:
            self._onchange_propeller_id()
        if self.auxiliary_id:
            self._onchange_auxiliary_id()
        if self.part_id:
            self._onchange_part_id()


    @api.onchange('part_id')
    def _onchange_part_id(self):
        specomp = []
        if(self.part_id.sub_part_ids != []):
            for i in self.part_id.sub_part_ids:
                specomp.append((0, 0,{
                    'is_overhaul' : True,
                    'part_name' : i.product_id.name if i.part_id.id == False else ' - '+i.product_id.name ,
                    'part_id' : i.id,
                    'old_serial_number' : i.serial_number.id,
                    'new_serial_number' : False,
                }))
        self.part_ids = specomp
    
    @api.onchange('fleet_id')
    def _onchange_fleet_id(self):
        specomp = []
        fleet_id = self.env['aircraft.acquisition'].search([('id','=',self.env.context.get('fleet_id',False))])
        if(fleet_id.id != False):
            for g in fleet_id.component_ids:
                specomp.append((0, 0,{
                        'is_overhaul' : True,
                        'part_name' : g.product_id.name if g.part_id.id == False else ' - '+g.product_id.name ,
                        'part_id' : g.id,
                        'old_serial_number' : g.serial_number.id,
                        'new_serial_number' : False,
                    }))
                for i in g.sub_part_ids:
                    specomp.append((0, 0,{
                        'is_overhaul' : True,
                        'part_name' : i.product_id.name if i.part_id.id == False else ' - '+i.product_id.name ,
                        'part_id' : i.id,
                        'old_serial_number' : i.serial_number.id,
                        'new_serial_number' : False,
                    }))
            self.part_ids = specomp

    @api.onchange('propeller_id')
    def _onchange_propeller_id(self):
        specomp = []
        propeller_id = self.env['propeller.type'].search([('id','=',self.env.context.get('propeller_id',False))])
        if(propeller_id.id != False):
            for g in propeller_id.component_ids:
                specomp.append((0, 0,{
                        'is_overhaul' : True,
                        'part_name' : g.product_id.name if g.part_id.id == False else ' - '+g.product_id.name ,
                        'part_id' : g.id,
                        'old_serial_number' : g.serial_number.id,
                        'new_serial_number' : False,
                    }))
                for i in g.sub_part_ids:
                    specomp.append((0, 0,{
                        'is_overhaul' : True,
                        'part_name' : i.product_id.name if i.part_id.id == False else ' - '+i.product_id.name ,
                        'part_id' : i.id,
                        'old_serial_number' : i.serial_number.id,
                        'new_serial_number' : False,
                    }))
            self.part_ids = specomp

    @api.onchange('engine_id')
    def _onchange_engine_id(self):
        specomp = []
        engine_id = self.env['engine.type'].search([('id','=',self.env.context.get('engine_id',False))])
        if(engine_id.id != False):
            for g in engine_id.component_ids:
                specomp.append((0, 0,{
                        'is_overhaul' : True,
                        'part_name' : g.product_id.name if g.part_id.id == False else ' - '+g.product_id.name ,
                        'part_id' : g.id,
                        'old_serial_number' : g.serial_number.id,
                        'new_serial_number' : False,
                    }))
                for i in g.sub_part_ids:
                    specomp.append((0, 0,{
                        'is_overhaul' : True,
                        'part_name' : i.product_id.name if i.part_id.id == False else ' - '+i.product_id.name ,
                        'part_id' : i.id,
                        'old_serial_number' : i.serial_number.id,
                        'new_serial_number' : False,
                    }))
            self.part_ids = specomp

    @api.onchange('auxiliary_id')
    def _onchange_auxiliary_id(self):
        specomp = []
        auxiliary_id = self.env['auxiliary.type'].search([('id','=',self.env.context.get('auxiliary_id',False))])
        if(auxiliary_id.id != False):
            for g in auxiliary_id.component_ids:
                specomp.append((0, 0,{
                        'is_overhaul' : True,
                        'part_name' : g.product_id.name if g.part_id.id == False else ' - '+g.product_id.name ,
                        'part_id' : g.id,
                        'old_serial_number' : g.serial_number.id,
                        'new_serial_number' : False,
                    }))
                for i in g.sub_part_ids:
                    specomp.append((0, 0,{
                        'is_overhaul' : True,
                        'part_name' : i.product_id.name if i.part_id.id == False else ' - '+i.product_id.name ,
                        'part_id' : i.id,
                        'old_serial_number' : i.serial_number.id,
                        'new_serial_number' : False,
                    }))
            self.part_ids = specomp

    
    @api.model
    def create(self, values):
        normal_treat = ['hours','cycles','rin']
        create = super(OverhaulAircraft, self).create(values)
        values['fleet_id'] = self._get_fleet().id
        normal_treat = ['hours','cycles','rin']
        # slive = self.env['ams.component.servicelife'].search([('id','=',values['service_life_id'])])
        
        fleet = self.env['aircraft.acquisition'].search([('id','=',self.env.context.get('fleet_id',values['fleet_id']))], limit=1)
        engine = self.env['engine.type'].search([('id','=',self.env.context.get('engine_id',False))], limit=1)
        auxiliary = self.env['auxiliary.type'].search([('id','=',self.env.context.get('auxiliary_id',False))], limit=1)
        propeller = self.env['propeller.type'].search([('id','=',self.env.context.get('propeller_id',False))], limit=1)
        part = self.env['ams.component.part'].search([('id','=',self.env.context.get('part_id',False))], limit=1)
        # inspection = self.env['ams.inspection'].search([('id','=',values['inspection_id'])], limit=1)
        if(part.id != False):
            if(part.part_id.id != False):
                xpart = part.part_id
            else:
                xpart = part
            if(xpart.fleet_id.id != False):
                fleet = xpart.fleet_id
            if(xpart.engine_id.id != False):
                engine = xpart.engine_id
            if(xpart.auxiliary_id.id != False):
                auxiliary = xpart.auxiliary_id

        if(engine.id != False):
            hours_add = engine.engine_tsn - values['overhaul_hours']
            cycles_add = engine.engine_csn - values['overhaul_cycles']
            rin_add = engine.engine_rsn - values['overhaul_rins']
        elif(auxiliary.id != False):
            hours_add = auxiliary.auxiliary_tsn - values['overhaul_hours']
            cycles_add = auxiliary.auxiliary_csn - values['overhaul_cycles']
            rin_add = auxiliary.auxiliary_rsn - values['overhaul_rins']
        else:
            hours_add = fleet.total_hours - values['overhaul_hours']
            cycles_add = fleet.total_landings - values['overhaul_cycles']
            rin_add = fleet.total_rins - values['overhaul_rins']

        # FOREACH RESET
        if create.part_id.id != False:
            for g in create.part_id.serfice_life:
                self.env['ams.component.servicelife'].reset(g.id,create.overhaul_date,hours_add,cycles_add,rin_add)

            create.part_id.write({
                'is_overhaul' : True,
                'tso' : hours_add,
                'cso' : cycles_add,
                'rso' : rin_add,
                'date_overhaul' : create.overhaul_date,
                })
            # Bikin jadwal maintenance 
            date_format = "%Y-%m-%d"
            a = datetime.strptime(create.date, date_format)
            b = datetime.strptime(create.finish_date, date_format)
            delta = b - a            
            oh_type = ' Component ' + create.part_id.product_id.name + ' '
            # self.env['maintenance.request'].create({
            #     'name' : str(fleet.name) + ' - '+oh_type+'Overhaul',
            #     'airworthy_overhaul_id' : create.id,
            #     'fl_acquisition_id' : fleet.id,
            #     'maintenance_team_id' : self.env['maintenance.team'].search([], limit=1).id,
            #     'reason_maintenance' : 'inspection.desc',
            #     'schedule_date' : create.date,
            #     'duration' : (24 * delta.days) - 1,
            #     'aircraft_state' : 'serviceable',
            #     })

        if create.overhaul_sub == True:
            for i in create.part_ids:
                for n in i.part_id.serfice_life:
                    self.env['ams.component.servicelife'].reset(n.id,create.overhaul_date,hours_add,cycles_add,rin_add)

        return create

    @api.model
    def create_temp(self, values):
        normal_treat = ['hours','cycles','rin']
        create = super(OverhaulAircraft, self).create(values)
        fleet = create.fleet_id
        if fleet.id != False:
            fleet.write({
                'airframe_lastoh' : create.date,
                'total_hours' : 0,
                'total_landings' : 0,
                'total_rins' : 0,
                })
        elif create.engine_id.id != False:
            fleet = self.env['aircraft.acquisition'].search(['|','|','|',('engine_type_id','=',create.engine_id.id),('engine2_type_id','=',create.engine_id.id),('engine3_type_id','=',create.engine_id.id),('engine4_type_id','=',create.engine_id.id)],limit=1) 
            create.engine_id.write({
                'engine_lastoh' : create.date,
                'engine_hsi' : create.date,
                'engine_tslsv' : 0,
                'engine_tslsv_hsi' : 0,
                'engine_cslsv' : 0,
                'engine_cslsv_hsi' : 0,
                'total_hours' : 0,
                'total_cycles' : 0,
                'total_rins' : 0,
                })
        elif create.auxiliary_id.id != False:
            fleet = self.env['aircraft.acquisition'].search([],limit=1) 
            # fleet = self.env['aircraft.acquisition'].search(['|','|','|',('auxiliary_type_id','=',create.auxiliary_id.id),('auxiliary2_type_id','=',create.auxiliary_id.id),('auxiliary3_type_id','=',create.auxiliary_id.id),('auxiliary4_type_id','=',create.auxiliary_id.id)],limit=1) 
            create.auxiliary_id.write({
                'auxiliary_lastoh' : create.date,
                'total_hours' : 0,
                'total_cycles' : 0,
                'total_rins' : 0,
                })
        elif create.propeller_id.id != False:
            fleet = self.env['aircraft.acquisition'].search(['|','|','|',('propeller_type_id','=',create.propeller_id.id),('propeller2_type_id','=',create.propeller_id.id),('propeller3_type_id','=',create.propeller_id.id),('propeller4_type_id','=',create.propeller_id.id)],limit=1) 
            create.propeller_id.write({
                'propeller_lastoh' : create.date,
                'total_hours' : 0,
                'total_cycles' : 0,
                'total_rins' : 0,
                })
        elif create.part_id.id != False:
            if create.part_id.fleet_id.id == False:
                fleet = create.part_id.part_id.fleet_id.id
            else:
                fleet = create.part_id.fleet_id.id
            create.part_id.write({
                'tso' : 0,
                'cso' : 0,
                'rso' : 0,
                })
            for r in create.part_id.serfice_life:
                if(r.action_type == 'overhaul'):
                    cvalue = r.value
                    pvalue = 0
                    if(r.unit == 'hours'):
                        cvalue = cvalue - 0
                        pvalue = 0
                    elif(r.unit == 'cycles'):
                        cvalue = cvalue - 0
                        pvalue = 0
                    elif(r.unit == 'rin'):
                        cvalue = cvalue - 0
                        pvalue = 0

                    if(r.unit in normal_treat):
                        r.write({
                            'current' : pvalue,
                            'remaining' : cvalue,
                            'current_date' : False,
                            'next_date' : False,
                            'current_text' : pvalue,
                            'next_text' : cvalue,
                        })
                    else:
                        if r.unit == 'year':
                            dateDue = datetime.strptime(create.date, '%Y-%m-%d') + relativedelta(years=int(math.floor(cvalue)))
                        if r.unit == 'month':
                            dateDue = datetime.strptime(create.date, '%Y-%m-%d') + relativedelta(months=int(math.floor(cvalue)))
                        if r.unit == 'days':
                            dateDue = datetime.strptime(create.date, '%Y-%m-%d') + relativedelta(days=int(math.floor(cvalue)))
                        dateDue = dateDue.strftime("%Y-%m-%d")

                        r.write({
                            'current' : pvalue,
                            'remaining' : cvalue,
                            'current_date' : create.date,
                            'next_date' : dateDue,
                            'current_text' : create.date,
                            'next_text' : dateDue,
                        })
                    # Bikin jadwal maintenance 
                    date_format = "%Y-%m-%d"
                    a = datetime.strptime(create.date, date_format)
                    b = datetime.strptime(create.finish_date, date_format)
                    delta = b - a

                    oh_type = ' Component ' + create.part_id.product_id.name + ' '

                    # self.env['maintenance.request'].create({
                    #     'name' : str(fleet.name) + ' - '+oh_type+'Overhaul',
                    #     'airworthy_overhaul_id' : create.id,
                    #     'fl_acquisition_id' : fleet.id,
                    #     'maintenance_team_id' : self.env['maintenance.team'].search([], limit=1).id,
                    #     'reason_maintenance' : 'inspection.desc',
                    #     'schedule_date' : create.date,
                    #     'duration' : (24 * delta.days) - 1,
                    #     'aircraft_state' : 'serviceable',
                    #     })


        for n in create.part_ids:
            # CHANGE S/N
            # CHANGE HOURS & CYCLES
            if n.is_overhaul == True:
                n.part_id.write({
                    'no_component' : False,
                    'ac_timeinstallation' : fleet.total_hours,
                    'ac_cyclesinstallation' : fleet.total_landings,
                    'ac_rininstallation' : fleet.total_rins,
                    'serial_number' : n.new_serial_number.id,
                    'tso' : 0,
                    'cso' : 0,
                    'rso' : 0,
                    'comp_timeinstallation' : 0,
                    'comp_cyclesinstallation' : 0,
                    'comp_rininstallation' : 0,
                    })
                # RESET SERVICELIFE
                for r in n.part_id.serfice_life:
                    cvalue = r.value
                    pvalue = 0
                    if(r.unit == 'hours'):
                        cvalue = cvalue - 0
                        pvalue = 0
                    elif(r.unit == 'cycles'):
                        cvalue = cvalue - 0
                        pvalue = 0
                    elif(r.unit == 'rin'):
                        cvalue = cvalue - 0
                        pvalue = 0

                    if(r.unit in normal_treat):
                        r.write({
                            'current' : pvalue,
                            'remaining' : cvalue,
                            'current_date' : False,
                            'next_date' : False,
                            'current_text' : pvalue,
                            'next_text' : cvalue,
                        })
                    else:
                        if r.unit == 'year':
                            dateDue = datetime.strptime(create.date, '%Y-%m-%d') + relativedelta(years=int(math.floor(cvalue)))
                        if r.unit == 'month':
                            dateDue = datetime.strptime(create.date, '%Y-%m-%d') + relativedelta(months=int(math.floor(cvalue)))
                        if r.unit == 'days':
                            dateDue = datetime.strptime(create.date, '%Y-%m-%d') + relativedelta(days=int(math.floor(cvalue)))
                        dateDue = dateDue.strftime("%Y-%m-%d")

                        r.write({
                            'current' : pvalue,
                            'remaining' : cvalue,
                            'current_date' : create.date,
                            'next_date' : dateDue,
                            'current_text' : create.date,
                            'next_text' : dateDue,
                        })
                    # Bikin jadwal maintenance 
                    date_format = "%Y-%m-%d"
                    a = datetime.strptime(create.date, date_format)
                    b = datetime.strptime(create.finish_date, date_format)
                    delta = b - a

                    oh_type = ''
                    if(create.engine_id.id != False):
                        oh_type = 'Engine '
                    if(create.auxiliary_id.id != False):
                        oh_type = 'Auxiliary '
                    if(create.propeller_id.id != False):
                        oh_type = 'Propeller '

                    # self.env['maintenance.request'].create({
                    #     'name' : str(fleet.name) + ' - '+oh_type+'Overhaul',
                    #     'airworthy_overhaul_id' : create.id,
                    #     'fl_acquisition_id' : fleet.id,
                    #     'maintenance_team_id' : self.env['maintenance.team'].search([], limit=1).id,
                    #     'reason_maintenance' : 'inspection.desc',
                    #     'schedule_date' : create.date,
                    #     'duration' : (24 * delta.days) - 1,
                    #     'aircraft_state' : 'serviceable',
                    #     })

        return create
            