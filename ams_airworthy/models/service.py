# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _

class ServiceAircraftPart(models.Model):
    _name = 'airworthy.service.part'
    _description = 'Service Part'

    service_id = fields.Many2one('airworthy.service', string="Service Id")
    is_service = fields.Boolean(string='Service')
    part_name = fields.Char(string='Part')
    part_id = fields.Many2one('ams.component.part', string='Part')
    product_id = fields.Many2one('product.product', string='Product', related="part_id.product_id",readonly=True)
    hours = fields.Float(string='Hours',related="part_id.tso",readonly=True)
    cycles = fields.Float(string='Hours',related="part_id.cso",readonly=True)
    old_serial_number = fields.Many2one('stock.production.lot', string='Old Serial Number')
    new_serial_number = fields.Many2one('stock.production.lot', string='New Serial Number')

class ServiceAircraft(models.Model):
    _name = 'airworthy.service'
    _description = 'Service'
    _rec_name = 'fleet_id'
    
    fleet_id  = fields.Many2one('aircraft.acquisition', string="Aircraft Registration",readonly=True, default=lambda self:self.env.context.get('fleet_id',False))
    engine_id  = fields.Many2one('engine.type', string="Engine",readonly=True, default=lambda self:self.env.context.get('engine_id',False))
    propeller_id  = fields.Many2one('propeller.type', string="Propeller",readonly=True, default=lambda self:self.env.context.get('propeller_id',False))
    auxiliary_id  = fields.Many2one('auxiliary.type', string="Auxiliary",readonly=True, default=lambda self:self.env.context.get('auxiliary_id',False))
    part_id = fields.Many2one('ams.component.part', string='Part',readonly=True, default=lambda self:self.env.context.get('part_id',False))
    
    rin_active = fields.Boolean(string='RIN Active',related="fleet_id.rin_active",readonly=True)
    inspection_id = fields.Many2one('ams.inspection', string='Inspection')
    service_life_id = fields.Many2one('ams.component.servicelife', string='Service Life',required=True)
    unserviceable = fields.Boolean(string='Aircraft is unserviceable during this compliance', default=False)

    current_text = fields.Char(string='Current', related='service_life_id.current_text',readonly=True)
    next_text = fields.Char(string='Next Due', related='service_life_id.next_text',readonly=True)

    date = fields.Date(string='Start Date',required=True,default=fields.Date.today())
    date_finish = fields.Date(string='Finish Date',required=True,default=fields.Date.today())
    
    current_hours = fields.Float(string='Current Hours', default=lambda self:self._get_vals()['total_hours'], readonly=True)
    current_cycles = fields.Float(string='Current Cycles', default=lambda self:self._get_vals()['total_landings'], readonly=True)
    current_rins = fields.Integer(string='Current RIN', default=lambda self:self._get_vals()['total_rins'], readonly=True)

    hours = fields.Float(string='Aircraft Hours',required=True,default=lambda self:self._get_vals()['total_hours'])
    cycles = fields.Float(string='Aircraft Cycles',required=True,default=lambda self:self._get_vals()['total_landings'])
    rins = fields.Integer(string='Aircraft RIN',required=True,default=lambda self:self._get_vals()['total_rins'])

    employee_id = fields.Many2one('hr.employee', string="Inspected by",default=False)

    checklist_id = fields.Many2one('ams.checklist', string='Checklist', readonly=True,related='inspection_id.checklist_id')

    work_with = fields.Selection([('wo','Work Order'),('mwo','MWO')],string='Comply With')
    wo_id = fields.Many2one('ams.work.order', string="Work Order",default=False)
    mwo_id = fields.Many2one('ams.mwo', string="MWO",default=False)

    todo_ids = fields.One2many('ams.checklist.todo','checklist_id',string='To Do',readonly=True,related='inspection_id.checklist_id.todo_ids')
    desc = fields.Text(string='Description',readonly=True,related='inspection_id.checklist_id.desc')

    file_name = fields.Char('File Name', related='inspection_id.checklist_id.file_name')
    file = fields.Binary(string='Scan File',readonly=True,related='inspection_id.checklist_id.file')

    component_of = fields.Selection([('airframe','Aircraft'),('engine','Engine'),('auxiliary','Auxiliary'),('propeller','Propeller')],string='Component of',default=lambda self:self._get_component_of())
    
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
    
    @api.onchange('fleet_id')
    def _onchange_fleet_id(self):
        specomp = []
        fleet_id = self.env['aircraft.acquisition'].search([('id','=',self.env.context.get('fleet_id',False))])
        if(fleet_id.id != False):
            for g in fleet_id.component_ids:
                specomp.append((0, 0,{
                        'is_service' : True,
                        'part_name' : g.product_id.name if g.part_id.id == False else ' - '+g.product_id.name ,
                        'part_id' : g.id,
                        'old_serial_number' : g.serial_number.id,
                        'new_serial_number' : False,
                    }))
                for i in g.sub_part_ids:
                    specomp.append((0, 0,{
                        'is_service' : True,
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
                        'is_service' : True,
                        'part_name' : g.product_id.name if g.part_id.id == False else ' - '+g.product_id.name ,
                        'part_id' : g.id,
                        'old_serial_number' : g.serial_number.id,
                        'new_serial_number' : False,
                    }))
                for i in g.sub_part_ids:
                    specomp.append((0, 0,{
                        'is_service' : True,
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
                        'is_service' : True,
                        'part_name' : g.product_id.name if g.part_id.id == False else ' - '+g.product_id.name ,
                        'part_id' : g.id,
                        'old_serial_number' : g.serial_number.id,
                        'new_serial_number' : False,
                    }))
                for i in g.sub_part_ids:
                    specomp.append((0, 0,{
                        'is_service' : True,
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
                        'is_service' : True,
                        'part_name' : g.product_id.name if g.part_id.id == False else ' - '+g.product_id.name ,
                        'part_id' : g.id,
                        'old_serial_number' : g.serial_number.id,
                        'new_serial_number' : False,
                    }))
                for i in g.sub_part_ids:
                    specomp.append((0, 0,{
                        'is_service' : True,
                        'part_name' : i.product_id.name if i.part_id.id == False else ' - '+i.product_id.name ,
                        'part_id' : i.id,
                        'old_serial_number' : i.serial_number.id,
                        'new_serial_number' : False,
                    }))
            self.part_ids = specomp

    # @api.model
    # def create(self, values):
    #     normal_treat = ['hours','cycles','rin']
    #     create = super(ServiceAircraft, self).create(values)
    #     fleet = create.fleet_id
    #     if fleet.id != False:
    #         fleet.write({
    #             'airframe_lastoh' : create.date,
    #             'total_hours' : 0,
    #             'total_landings' : 0,
    #             'total_rins' : 0,
    #             })
    #     elif create.engine_id.id != False:
    #         fleet = self.env['aircraft.acquisition'].search(['|','|','|',('engine_type_id','=',create.engine_id.id),('engine2_type_id','=',create.engine_id.id),('engine3_type_id','=',create.engine_id.id),('engine4_type_id','=',create.engine_id.id)],limit=1) 
    #         create.engine_id.write({
    #             'engine_lastoh' : create.date,
    #             'engine_hsi' : create.date,
    #             'engine_tslsv' : 0,
    #             'engine_tslsv_hsi' : 0,
    #             'engine_cslsv' : 0,
    #             'engine_cslsv_hsi' : 0,
    #             'total_hours' : 0,
    #             'total_cycles' : 0,
    #             'total_rins' : 0,
    #             })
    #     elif create.auxiliary_id.id != False:
    #         fleet = self.env['aircraft.acquisition'].search(['|','|','|',('auxiliary_type_id','=',create.auxiliary_id.id),('auxiliary2_type_id','=',create.auxiliary_id.id),('auxiliary3_type_id','=',create.auxiliary_id.id),('auxiliary4_type_id','=',create.auxiliary_id.id)],limit=1) 
    #         create.auxiliary_id.write({
    #             'auxiliary_lastoh' : create.date,
    #             'total_hours' : 0,
    #             'total_cycles' : 0,
    #             'total_rins' : 0,
    #             })
    #     elif create.propeller_id.id != False:
    #         fleet = self.env['aircraft.acquisition'].search(['|','|','|',('propeller_type_id','=',create.propeller_id.id),('propeller2_type_id','=',create.propeller_id.id),('propeller3_type_id','=',create.propeller_id.id),('propeller4_type_id','=',create.propeller_id.id)],limit=1) 
    #         create.propeller_id.write({
    #             'propeller_lastoh' : create.date,
    #             'total_hours' : 0,
    #             'total_cycles' : 0,
    #             'total_rins' : 0,
    #             })
    #     elif create.part_id.id != False:
    #         if create.part_id.fleet_id.id == False:
    #             fleet = create.part_id.part_id.fleet_id.id
    #         else:
    #             fleet = create.part_id.fleet_id.id
    #         create.part_id.write({
    #             'tso' : 0,
    #             'cso' : 0,
    #             'rso' : 0,
    #             })
    #         for r in create.part_id.serfice_life:
    #             if(r.action_type == 'service'):
    #                 cvalue = r.value
    #                 pvalue = 0
    #                 if(r.unit == 'hours'):
    #                     cvalue = cvalue - 0
    #                     plavue = 0
    #                 elif(r.unit == 'cycles'):
    #                     cvalue = cvalue - 0
    #                     plavue = 0
    #                 elif(r.unit == 'rin'):
    #                     cvalue = cvalue - 0
    #                     plavue = 0

    #                 if(r.unit in normal_treat):
    #                     r.write({
    #                         'current' : plavue,
    #                         'remaining' : cvalue,
    #                         'current_date' : False,
    #                         'next_date' : False,
    #                         'current_text' : plavue,
    #                         'next_text' : cvalue,
    #                     })
    #                 else:
    #                     if r.unit == 'year':
    #                         dateDue = datetime.strptime(create.date, '%Y-%m-%d') + relativedelta(years=int(math.floor(cvalue)))
    #                     if r.unit == 'month':
    #                         dateDue = datetime.strptime(create.date, '%Y-%m-%d') + relativedelta(months=int(math.floor(cvalue)))
    #                     if r.unit == 'days':
    #                         dateDue = datetime.strptime(create.date, '%Y-%m-%d') + relativedelta(days=int(math.floor(cvalue)))
    #                     dateDue = dateDue.strftime("%Y-%m-%d")

    #                     r.write({
    #                         'current' : plavue,
    #                         'remaining' : cvalue,
    #                         'current_date' : create.date,
    #                         'next_date' : dateDue,
    #                         'current_text' : create.date,
    #                         'next_text' : dateDue,
    #                     })
    #                 # Bikin jadwal maintenance 
    #                 date_format = "%Y-%m-%d"
    #                 a = datetime.strptime(create.date, date_format)
    #                 b = datetime.strptime(create.finish_date, date_format)
    #                 delta = b - a

    #                 oh_type = ' Component ' + create.part_id.product_id.name + ' '

    #                 self.env['maintenance.request'].create({
    #                     'name' : str(fleet.name) + ' - '+oh_type+'Service',
    #                     'airworthy_service_id' : create.id,
    #                     'fl_acquisition_id' : fleet.id,
    #                     'maintenance_team_id' : self.env['maintenance.team'].search([], limit=1).id,
    #                     'reason_maintenance' : 'inspection.desc',
    #                     'schedule_date' : create.date,
    #                     'duration' : (24 * delta.days) - 1,
    #                     'aircraft_state' : 'unserviceable',
    #                     })


    #     for n in create.part_ids:
    #         # CHANGE S/N
    #         # CHANGE HOURS & CYCLES
    #         if n.is_service == True:
    #             n.part_id.write({
    #                 'no_component' : False,
    #                 'ac_timeinstallation' : fleet.total_hours,
    #                 'ac_cyclesinstallation' : fleet.total_landings,
    #                 'ac_rininstallation' : fleet.total_rins,
    #                 'serial_number' : n.new_serial_number.id,
    #                 'tso' : 0,
    #                 'cso' : 0,
    #                 'rso' : 0,
    #                 'comp_timeinstallation' : 0,
    #                 'comp_cyclesinstallation' : 0,
    #                 'comp_rininstallation' : 0,
    #                 })
    #             # RESET SERVICELIFE
    #             for r in n.part_id.serfice_life:
    #                 cvalue = r.value
    #                 pvalue = 0
    #                 if(r.unit == 'hours'):
    #                     cvalue = cvalue - 0
    #                     plavue = 0
    #                 elif(r.unit == 'cycles'):
    #                     cvalue = cvalue - 0
    #                     plavue = 0
    #                 elif(r.unit == 'rin'):
    #                     cvalue = cvalue - 0
    #                     plavue = 0

    #                 if(r.unit in normal_treat):
    #                     r.write({
    #                         'current' : plavue,
    #                         'remaining' : cvalue,
    #                         'current_date' : False,
    #                         'next_date' : False,
    #                         'current_text' : plavue,
    #                         'next_text' : cvalue,
    #                     })
    #                 else:
    #                     if r.unit == 'year':
    #                         dateDue = datetime.strptime(create.date, '%Y-%m-%d') + relativedelta(years=int(math.floor(cvalue)))
    #                     if r.unit == 'month':
    #                         dateDue = datetime.strptime(create.date, '%Y-%m-%d') + relativedelta(months=int(math.floor(cvalue)))
    #                     if r.unit == 'days':
    #                         dateDue = datetime.strptime(create.date, '%Y-%m-%d') + relativedelta(days=int(math.floor(cvalue)))
    #                     dateDue = dateDue.strftime("%Y-%m-%d")

    #                     r.write({
    #                         'current' : plavue,
    #                         'remaining' : cvalue,
    #                         'current_date' : create.date,
    #                         'next_date' : dateDue,
    #                         'current_text' : create.date,
    #                         'next_text' : dateDue,
    #                     })
    #                 # Bikin jadwal maintenance 
    #                 date_format = "%Y-%m-%d"
    #                 a = datetime.strptime(create.date, date_format)
    #                 b = datetime.strptime(create.finish_date, date_format)
    #                 delta = b - a

    #                 oh_type = ''
    #                 if(create.engine_id.id != False):
    #                     oh_type = 'Engine '
    #                 if(create.auxiliary_id.id != False):
    #                     oh_type = 'Auxiliary '
    #                 if(create.propeller_id.id != False):
    #                     oh_type = 'Propeller '

    #                 self.env['maintenance.request'].create({
    #                     'name' : str(fleet.name) + ' - '+oh_type+'Service',
    #                     'airworthy_service_id' : create.id,
    #                     'fl_acquisition_id' : fleet.id,
    #                     'maintenance_team_id' : self.env['maintenance.team'].search([], limit=1).id,
    #                     'reason_maintenance' : 'inspection.desc',
    #                     'schedule_date' : create.date,
    #                     'duration' : (24 * delta.days) - 1,
    #                     'aircraft_state' : 'unserviceable',
    #                     })

    #     return create

    @api.model
    def create(self, vals):
        vals['fleet_id'] = self._get_fleet().id
        normal_treat = ['hours','cycles','rin']
        slive = self.env['ams.component.servicelife'].search([('id','=',vals['service_life_id'])])
        
        fleet = self.env['aircraft.acquisition'].search([('id','=',self.env.context.get('fleet_id',vals['fleet_id']))], limit=1)
        engine = self.env['engine.type'].search([('id','=',self.env.context.get('engine_id',False))], limit=1)
        auxiliary = self.env['auxiliary.type'].search([('id','=',self.env.context.get('auxiliary_id',False))], limit=1)
        propeller = self.env['propeller.type'].search([('id','=',self.env.context.get('propeller_id',False))], limit=1)
        part = self.env['ams.component.part'].search([('id','=',self.env.context.get('part_id',False))], limit=1)
        inspection = self.env['ams.inspection'].search([('id','=',vals['inspection_id'])], limit=1)

        desc = inspection.desc
        if(desc == False or desc == ''):
            desc = 'Inspection ' + part.product_id.name

        
        cvalue = slive.value
        pvalue = 0

        if(part.id != False):
            if(part.part_id.id != False):
                part = part.part_id
            if(part.engine_id.id != False):
                engine = part.engine_id
            if(part.auxiliary_id.id != False):
                auxiliary = part.auxiliary_id

        if(engine.id != False):
            if(slive.unit == 'hours'):
                cvalue = cvalue - (engine.engine_tsn - vals['hours'])
                plavue = (engine.engine_tsn - vals['hours'])
            elif(slive.unit == 'cycles'):
                cvalue = cvalue - (engine.engine_csn - vals['cycles'])
                plavue = (engine.engine_csn - vals['cycles'])
            elif(slive.unit == 'rin'):
                cvalue = cvalue - (engine.engine_rsn - vals['rins'])
                plavue = (engine.engine_rsn - vals['rins'])
        elif(auxiliary.id != False):
            if(slive.unit == 'hours'):
                cvalue = cvalue - (auxiliary.auxiliary_tsn - vals['hours'])
                plavue = (auxiliary.auxiliary_tsn - vals['hours'])
            elif(slive.unit == 'cycles'):
                cvalue = cvalue - (auxiliary.auxiliary_csn - vals['cycles'])
                plavue = (auxiliary.auxiliary_csn - vals['cycles'])
            elif(slive.unit == 'rin'):
                cvalue = cvalue - (auxiliary.auxiliary_rsn - vals['rins'])
                plavue = (auxiliary.auxiliary_rsn - vals['rins'])
        else:
            if(slive.unit == 'hours'):
                cvalue = cvalue - (fleet.total_hours - vals['hours'])
                plavue = (fleet.total_hours - vals['hours'])
            elif(slive.unit == 'cycles'):
                cvalue = cvalue - (fleet.total_landings - vals['cycles'])
                plavue = (fleet.total_landings - vals['cycles'])
            elif(slive.unit == 'rin'):
                cvalue = cvalue - (fleet.total_rins - vals['rins'])
                plavue = (fleet.total_rins - vals['rins'])

        if(slive.unit in normal_treat):
            slive.write({
                'current' : plavue,
                'extension' : 0,
                'remaining' : cvalue,
                'current_date' : False,
                'next_date' : False,
                'current_text' : plavue,
                'next_text' : cvalue,
            })
        else:
            if slive.unit == 'year':
                dateDue = datetime.strptime(vals['date'], '%Y-%m-%d') + relativedelta(years=int(math.floor(cvalue)))
            if slive.unit == 'month':
                dateDue = datetime.strptime(vals['date'], '%Y-%m-%d') + relativedelta(months=int(math.floor(cvalue)))
            if slive.unit == 'days':
                dateDue = datetime.strptime(vals['date'], '%Y-%m-%d') + relativedelta(days=int(math.floor(cvalue)))
            dateDue = dateDue.strftime("%Y-%m-%d")

            slive.write({
                'current' : plavue,
                'extension' : 0,
                'remaining' : cvalue,
                'current_date' : vals['date'],
                'next_date' : dateDue,
                'current_text' : vals['date'],
                'next_text' : dateDue,
            })
        # Bikin jadwal maintenance 
        date_format = "%Y-%m-%d"
        a = datetime.strptime(vals['date'], date_format)
        b = datetime.strptime(vals['date_finish'], date_format)
        delta = b - a

        create = super(ServiceAircraft, self).create(vals)
        if fleet:
            self.env['maintenance.request'].create({
                'name' : str(fleet.name) + ' - ' + str(desc),
                'airworthy_service_id' : create.id,
                'fl_acquisition_id' : fleet.id,
                'maintenance_team_id' : self.env['maintenance.team'].search([], limit=1).id,
                'reason_maintenance' : desc,
                'schedule_date' : vals['date'],
                'duration' : (24 * delta.days) - 1,
                'aircraft_state' : 'unserviceable' if vals['unserviceable'] == True else 'serviceable',
                })
        # CREATE INVENTORY REQUEST
        # if(create.needed_component_ids != []):
        #     reqcomp = []
        #     for g in create.needed_component_ids:
        #         reqcomp.append((0,0,{
        #                 'part_name' : g.product_id.id,
        #                 'quantity' : g.amount,
        #             }))
        #     id_reqcomp = self.env['request.inventory'].create({
        #         'ref_type' : 'inspection',
        #         'base_id' : False,
        #         'part_line' : reqcomp,
        #         })
        #     create.inventory_request_id = id_reqcomp.id
        return create

    @api.multi 
    def action_save(self):
        #your code
        self.ensure_one()
        #close popup
        return {'type': 'ir.actions.act_window_close'}

            