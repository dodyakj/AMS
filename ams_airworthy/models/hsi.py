# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _

class HsiAircraftPart(models.Model):
    _name = 'airworthy.hsi.part'
    _description = 'Hot Section Inspection Part'

    hsi_id = fields.Many2one('airworthy.hsi', string="Hot Section Inspection Id")
    is_hsi = fields.Boolean(string='Hot Section Inspection')
    part_name = fields.Char(string='Part')
    part_id = fields.Many2one('ams.component.part', string='Part')
    product_id = fields.Many2one('product.product', string='Product', related="part_id.product_id",readonly=True)
    hours = fields.Float(string='Hours',related="part_id.tso",readonly=True)
    cycles = fields.Float(string='Hours',related="part_id.cso",readonly=True)
    old_serial_number = fields.Many2one('stock.production.lot', string='Old Serial Number')
    new_serial_number = fields.Many2one('stock.production.lot', string='New Serial Number')

class HsiAircraft(models.Model):
    _name = 'airworthy.hsi'
    _description = 'Hot Section Inspection'
    _rec_name = 'engine_id'
    
    engine_id  = fields.Many2one('engine.type', string="Engine",readonly=True, default=lambda self:self.env.context.get('engine_id',False))
    part_ids = fields.One2many('airworthy.hsi.part','hsi_id',string='Part', compute=lambda self: self._onchange_engine_id())
    date = fields.Date(string='Start Date', default=fields.Date.today(),required=True)
    finish_date = fields.Date(string='Finish Date', default=fields.Date.today(),required=True)
    work_with = fields.Selection([('wo','Work Order'),('mwo','MWO')],string='Comply With')
    wo_id = fields.Many2one('ams.work.order', string="Work Order",default=False)
    mwo_id = fields.Many2one('ams.mwo', string="MWO",default=False)

    @api.multi 
    def action_save(self):
        #your code
        self.ensure_one()
        #close popup
        return {'type': 'ir.actions.act_window_close'}
        
    @api.onchange('engine_id')
    def _onchange_engine_id(self):
        specomp = []
        engine_id = self.env['engine.type'].search([('id','=',self.env.context.get('engine_id',False))])
        if(engine_id.id != False):
            for g in engine_id.component_ids:
                specomp.append((0, 0,{
                        'is_hsi' : True,
                        'part_name' : g.product_id.name if g.part_id.id == False else ' - '+g.product_id.name ,
                        'part_id' : g.id,
                        'old_serial_number' : g.serial_number.id,
                        'new_serial_number' : False,
                    }))
                for i in g.sub_part_ids:
                    specomp.append((0, 0,{
                        'is_hsi' : True,
                        'part_name' : i.product_id.name if i.part_id.id == False else ' - '+i.product_id.name ,
                        'part_id' : i.id,
                        'old_serial_number' : i.serial_number.id,
                        'new_serial_number' : False,
                    }))
            self.part_ids = specomp

    @api.model
    def create(self, values):
        normal_treat = ['hours','cycles','rin']
        create = super(HsiAircraft, self).create(values)
        if create.engine_id.id != False:
            fleet = self.env['aircraft.acquisition'].search(['|','|','|',('engine_type_id','=',create.engine_id.id),('engine2_type_id','=',create.engine_id.id),('engine3_type_id','=',create.engine_id.id),('engine4_type_id','=',create.engine_id.id)],limit=1) 
            create.engine_id.write({
                'engine_hsi' : create.date,
                'engine_tslsv' : 0,
                'engine_tslsv_hsi' : 0,
                'engine_cslsv' : 0,
                'engine_cslsv_hsi' : 0,
                'total_hours' : 0,
                'total_cycles' : 0,
                'total_rins' : 0,
                })
        for n in create.part_ids:
            # CHANGE S/N
            # CHANGE HOURS & CYCLES
            if n.is_hsi == True:
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
                        plavue = 0
                    elif(r.unit == 'cycles'):
                        cvalue = cvalue - 0
                        plavue = 0
                    elif(r.unit == 'rin'):
                        cvalue = cvalue - 0
                        plavue = 0

                    if(r.unit in normal_treat):
                        r.write({
                            'current' : plavue,
                            'remaining' : cvalue,
                            'current_date' : False,
                            'next_date' : False,
                            'current_text' : plavue,
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
                            'current' : plavue,
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

                    self.env['maintenance.request'].create({
                        'name' : str(fleet.name) + ' - Hot Section Inspection',
                        'airworthy_hsi_id' : create.id,
                        'fl_acquisition_id' : fleet.id,
                        'maintenance_team_id' : self.env['maintenance.team'].search([], limit=1).id,
                        'reason_maintenance' : 'inspection.desc',
                        'schedule_date' : create.date,
                        'duration' : (24 * delta.days) - 1,
                        'aircraft_state' : 'unserviceable',
                        })

        return create
            