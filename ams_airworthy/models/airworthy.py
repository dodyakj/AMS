# -*- coding: utf-8 -*-
from math import *
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _


class InspectAircraft(models.Model):
    _name = 'airworthy.inspection'
    _description = 'Inspection'
    _rec_name = 'inspection_id'

    fleet_id = fields.Many2one('aircraft.acquisition', string='Aircraft Registration', default=lambda self:self.env.context.get('fleet_id',False))
    engine_id = fields.Many2one('engine.type', string='Engine', default=lambda self:self.env.context.get('engine_id',False))
    propeller_id = fields.Many2one('propeller.type', string='Propeller', default=lambda self:self.env.context.get('propeller_id',False))
    auxiliary_id = fields.Many2one('auxiliary.type', string='Auxiliary', default=lambda self:self.env.context.get('auxiliary_id',False))
    part_id = fields.Many2one('ams.component.part', string='Part', default=lambda self:self.env.context.get('part_id',False))
    
    rin_active = fields.Boolean(string='RIN Active',related="fleet_id.rin_active",readonly=True)
    inspection_id = fields.Many2one('ams.inspection', string='Inspection')
    service_life_id = fields.Many2one('ams.component.servicelife', string='Service Life',required=True)
    unserviceable = fields.Boolean(string='Aircraft is unserviceable during this compliance', default=False)

    current_text = fields.Char(string='Current', related='service_life_id.current_text',readonly=True)
    next_text = fields.Char(string='Next Due', related='service_life_id.next_text',readonly=True)

    date = fields.Date(string='Start Date',required=True,default=fields.Date.today())
    date_finish = fields.Date(string='Finish Date',required=False,default=fields.Date.today())
    
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

    def _upload_name(self):
        if self.date:
            self.file_name = str(self.date+".pdf")

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
            desc = 'Inspection ' + str(part.product_id.name)

        
        cvalue = slive.value
        plavue = 0

        if(part.id != False):
            if(part.part_id.id != False):
                part = part.part_id
            if(part.fleet_id.id != False):
                fleet_id = part.fleet_id
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
                dateDue = datetime.strptime(vals['date'], '%Y-%m-%d') + relativedelta(years=int(floor(cvalue)))
            if slive.unit == 'month':
                dateDue = datetime.strptime(vals['date'], '%Y-%m-%d') + relativedelta(months=int(floor(cvalue)))
            if slive.unit == 'days':
                dateDue = datetime.strptime(vals['date'], '%Y-%m-%d') + relativedelta(days=int(floor(cvalue)))
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


        if(engine.id != False):
            chours = cvalue - (engine.engine_tsn - vals['hours'])
            phours = (engine.engine_tsn - vals['hours'])
            ccycles = cvalue - (engine.engine_csn - vals['cycles'])
            pcycles = (engine.engine_csn - vals['cycles'])
            crin = cvalue - (engine.engine_rsn - vals['rins'])
            prin = (engine.engine_rsn - vals['rins'])
        elif(auxiliary.id != False):
            chours = cvalue - (auxiliary.auxiliary_tsn - vals['hours'])
            phours = (auxiliary.auxiliary_tsn - vals['hours'])
            ccycles = cvalue - (auxiliary.auxiliary_csn - vals['cycles'])
            pcycles = (auxiliary.auxiliary_csn - vals['cycles'])
            crin = cvalue - (auxiliary.auxiliary_rsn - vals['rins'])
            prin = (auxiliary.auxiliary_rsn - vals['rins'])
        else:
            chours = cvalue - (fleet.total_hours - vals['hours'])
            phours = (fleet.total_hours - vals['hours'])
            ccycles = cvalue - (fleet.total_landings - vals['cycles'])
            pcycles = (fleet.total_landings - vals['cycles'])
            crin = cvalue - (fleet.total_rins - vals['rins'])
            prin = (fleet.total_rins - vals['rins'])


        ro = slive.other_service_live
        for g in ro:
            g.service_life_reset_id.reset(g.service_life_reset_id.id,vals['date'],phours,pcycles,prin)

        # Bikin jadwal maintenance 
        # date_format = "%Y-%m-%d"
        # a = datetime.strptime(vals['date'], date_format)
        # b = datetime.strptime(vals['date_finish'], date_format)
        # delta = b - a

        create = super(InspectAircraft, self).create(vals)
        # if fleet:
        #     self.env['maintenance.request'].create({
        #         'name' : str(fleet.name) + ' - ' + str(desc),
        #         'airworthy_inspection_id' : create.id,
        #         'fl_acquisition_id' : fleet.id,
        #         'maintenance_team_id' : self.env['maintenance.team'].search([], limit=1).id,
        #         'reason_maintenance' : desc,
        #         'schedule_date' : vals['date'],
        #         'duration' : (24 * delta.days) - 1,
        #         'aircraft_state' : 'unserviceable' if vals['unserviceable'] == True else 'serviceable',
        #         })
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

class MaintenanceCalendarCorrective(models.Model):
    _inherit = 'maintenance.request'
    
    airworthy_inspection_id = fields.Many2one('airworthy.inspection',string='Inspection')
    airworthy_overhaul_id = fields.Many2one('airworthy.overhaul',string='Overhaul')
    airworthy_service_id = fields.Many2one('airworthy.service',string='Service')

