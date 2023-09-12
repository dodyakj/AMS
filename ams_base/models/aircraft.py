# -*- coding: utf-8 -*-
# import json
# from websocket import create_connection
import csv
import base64
import tempfile
import cStringIO
from datetime import date, datetime, timedelta

from odoo import models, fields, api, _

class paiis_corrective_aircraft(models.Model):
    _inherit = 'aircraft.acquisition'



    constra

    aircraft_status = fields.Boolean(string='Aircraft Status',default=True)
    remark = fields.Text('Remark')
    status = fields.Selection([('inservice','In Service'),('available','Available'),('useassubtitution','Use As Subtitution'),('inmaintenance','In Maintenance'),('grounded','Grounded')], default='inservice')
    rent_by = fields.Char(string='Rent By')
    is_deleted = fields.Boolean(default=False)
    last_flight = fields.Date(string='Last Flight', readonly=True, default=False, compute='get_last_flight')

    # location = fields.Char(required=False, string="Location")
    airframe_lastoh = fields.Date(string='Airframe Last Overhaul')
    location = fields.Many2one('base.operation','Location')
    bel_view = fields.Boolean(string='Is Bel',default=lambda self:self.env.context.get('belcomponent',False),readonly=True,store=False)
    rin_active = fields.Boolean(string='Activate Rins')
    license_plate = fields.Char(required=True, string="Aircraft Registration")
    vin_sn = fields.Char(string='Serial Number', copy=False)
    acquisition_date = fields.Date('Acquisition Date')
    car_value = fields.Float(string="Aircraft Value")
    total_hours = fields.Float(string='Total Hours')
    total_landings = fields.Float(string='Total Landings')
    total_rins = fields.Integer(string='Total Rins')
    hoobs = fields.Integer(string='Hoobs')
    
    last_inspection = fields.Char(string='Last Inspection')
    last_inspection_hours = fields.Float(string='Last Inspection at A/C Hours')
    last_inspection_date = fields.Date(string='Last Inspection Date')

    next_inspection = fields.Char(string='Next Inspection')
    next_inspection_at = fields.Char(string='Next Inspection at')

    auxiliary_type_id = fields.Many2one('auxiliary.type', string='Auxiliary Name')
    auxiliary_type_id_before = fields.Many2one('auxiliary.type', string='Auxiliary Before')
    auxiliary_tsn = fields.Float(string='Auxiliary#1 TSN', related='auxiliary_type_id.auxiliary_tsn')
    auxiliary_csn = fields.Float(string='Auxiliary#1 CSN', related='auxiliary_type_id.auxiliary_csn')
    auxiliary_lastoh = fields.Date(string='Auxiliary#1 Last OH', related='auxiliary_type_id.auxiliary_lastoh')
    auxiliary_hsi = fields.Date(string='Auxiliary#1 HSI')

    propeller_type_id = fields.Many2one('propeller.type', string='propeller Name')
    propeller2_type_id = fields.Many2one('propeller.type', string='propeller Name')
    propeller3_type_id = fields.Many2one('propeller.type', string='propeller Name')
    propeller4_type_id = fields.Many2one('propeller.type', string='propeller Name')

    propeller_type_id_before = fields.Many2one('propeller.type', string='Propeller Before')
    propeller2_type_id_before = fields.Many2one('propeller.type', string='Propeller Before')
    propeller3_type_id_before = fields.Many2one('propeller.type', string='Propeller Before')
    propeller4_type_id_before = fields.Many2one('propeller.type', string='Propeller Before')

    propeller_tsn = fields.Float(string='propeller#1 TSN', related='propeller_type_id.propeller_tsn')
    propeller_csn = fields.Float(string='propeller#1 CSN', related='propeller_type_id.propeller_csn')
    propeller_lastoh = fields.Date(string='propeller#1 Last OH', related='propeller_type_id.propeller_lastoh')
    propeller_hsi = fields.Date(string='propeller#1 HSI')

    propeller2_tsn = fields.Float(string='propeller#2 TSN', related='propeller2_type_id.propeller_tsn')
    propeller2_csn = fields.Float(string='propeller#2 CSN', related='propeller2_type_id.propeller_csn')
    propeller2_lastoh = fields.Date(string='propeller#2 Last OH', related='propeller2_type_id.propeller_lastoh')
    propeller2_hsi = fields.Date(string='propeller#2 HSI')

    propeller3_tsn = fields.Float(string='propeller#3 TSN', related='propeller3_type_id.propeller_tsn')
    propeller3_csn = fields.Float(string='propeller#3 CSN', related='propeller3_type_id.propeller_csn')
    propeller3_lastoh = fields.Date(string='propeller#3 Last OH', related='propeller3_type_id.propeller_lastoh')
    propeller3_hsi = fields.Date(string='propeller#3 HSI')

    propeller4_tsn = fields.Float(string='propeller#4 TSN', related='propeller4_type_id.propeller_tsn')
    propeller4_csn = fields.Float(string='propeller#4 CSN', related='propeller4_type_id.propeller_csn')
    propeller4_lastoh = fields.Date(string='propeller#4 Last OH', related='propeller4_type_id.propeller_lastoh')
    propeller4_hsi = fields.Date(string='propeller#4 HSI')

    component_ids = fields.One2many('ams.component.part','fleet_id',string='Component', copy=True)
    inspection_ids = fields.One2many('ams.inspection','fleet_id',string='Inspection', copy=True)
    some_count = fields.Integer(string='Total',default=3)

    engine_change = fields.Boolean(string='Engine 1 Changed',default=False,readonly=True)
    engine2_change = fields.Boolean(string='Engine 2 Changed',default=False,readonly=True)
    engine3_change = fields.Boolean(string='Engine 3 Changed',default=False,readonly=True)
    engine4_change = fields.Boolean(string='Engine 4 Changed',default=False,readonly=True)
    auxiliary_change = fields.Boolean(string='Auxiliary 1 Changed',default=False,readonly=True)
    propeller_change = fields.Boolean(string='Propeller 1 Changed',default=False,readonly=True)
    propeller2_change = fields.Boolean(string='Propeller 2 Changed',default=False,readonly=True)
    propeller3_change = fields.Boolean(string='Propeller 3 Changed',default=False,readonly=True)
    propeller4_change = fields.Boolean(string='Propeller 4 Changed',default=False,readonly=True)

    engine_change_reason = fields.Text(string='Reason')
    engine2_change_reason = fields.Text(string='Reason')
    engine3_change_reason = fields.Text(string='Reason')
    engine4_change_reason = fields.Text(string='Reason')
    
    auxiliary_change_reason = fields.Text(string='Reason')

    propeller_change_reason = fields.Text(string='Reason')
    propeller2_change_reason = fields.Text(string='Reason')
    propeller3_change_reason = fields.Text(string='Reason')
    propeller4_change_reason = fields.Text(string='Reason')

    ac_hours_eng1 = fields.Float(string='Aircraft Hours When Attached')
    ac_cycles_eng1 = fields.Float(string='Aircraft Cycles When Attached')
    en_hours_eng1 = fields.Float(string='Engine Hours When Attached')
    en_cycles_eng1 = fields.Float(string='Engine Cycles When Attached')

    ac_hours_eng2 = fields.Float(string='Aircraft Hours When Attached')
    ac_cycles_eng2 = fields.Float(string='Aircraft Cycles When Attached')
    en_hours_eng2 = fields.Float(string='Engine Hours When Attached')
    en_cycles_eng2 = fields.Float(string='Engine Cycles When Attached')

    ac_hours_eng3 = fields.Float(string='Aircraft Hours When Attached')
    ac_cycles_eng3 = fields.Float(string='Aircraft Cycles When Attached')
    en_hours_eng3 = fields.Float(string='Engine Hours When Attached')
    en_cycles_eng3 = fields.Float(string='Engine Cycles When Attached')

    ac_hours_eng4 = fields.Float(string='Aircraft Hours When Attached')
    ac_cycles_eng4 = fields.Float(string='Aircraft Cycles When Attached')
    en_hours_eng4 = fields.Float(string='Engine Hours When Attached')
    en_cycles_eng4 = fields.Float(string='Engine Cycles When Attached')

    ac_hours_aux1 = fields.Float(string='Aircraft Hours When Attached')
    ac_cycles_aux1 = fields.Float(string='Aircraft Cycles When Attached')
    aux_hours_aux1 = fields.Float(string='Auxiliary Hours When Attached')
    aux_cycles_aux1 = fields.Float(string='Auxiliary Cycles When Attached')

    ac_hours_prop1 = fields.Float(string='Aircraft Hours When Attached')
    ac_cycles_prop1 = fields.Float(string='Aircraft Cycles When Attached')
    pr_hours_prop1 = fields.Float(string='Propeller Hours When Attached')
    pr_cycles_prop1 = fields.Float(string='Propeller Cycles When Attached')

    ac_hours_prop2 = fields.Float(string='Aircraft Hours When Attached')
    ac_cycles_prop2 = fields.Float(string='Aircraft Cycles When Attached')
    pr_hours_prop2 = fields.Float(string='Propeller Hours When Attached')
    pr_cycles_prop2 = fields.Float(string='Propeller Cycles When Attached')

    ac_hours_prop3 = fields.Float(string='Aircraft Hours When Attached')
    ac_cycles_prop3 = fields.Float(string='Aircraft Cycles When Attached')
    pr_hours_prop3 = fields.Float(string='Propeller Hours When Attached')
    pr_cycles_prop3 = fields.Float(string='Propeller Cycles When Attached')

    ac_hours_prop4 = fields.Float(string='Aircraft Hours When Attached')
    ac_cycles_prop4 = fields.Float(string='Aircraft Cycles When Attached')
    pr_hours_prop4 = fields.Float(string='Propeller Hours When Attached')
    pr_cycles_prop4 = fields.Float(string='Propeller Cycles When Attached')

    # @api.model
    # def write(self, vals):
        # if(vals['engine_type_id'] != self.engine_type_id.id):
        #     hist = self.env['ams.component_history'].create({
        #             'engine_id':self.engine_type_id.id,
        #             'fleet_id':self.id,
        #             'type':'attach',
        #         })
        # write = self.write(vals)
        
        # return write
        
    @api.one
    def get_last_flight(self):
        self.last_flight = self.env['ams_fml.log'].search(['&',('aircraft_id','=',self.id),('aircraft_hours','>',0)],order='date desc',limit=1).date
        
    @api.multi
    def do_serviceable(self):
        return {
            'name': 'Unserviceable',
            'type': 'ir.actions.act_window',
            'res_model': 'status.service',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': False,
            'views': [(False, 'form')],
            'target': 'new',
            'context': "{'default_fleet_id':" + str(self.id) + "}, 'default_type': 'S'}",
        }

    @api.multi
    def do_unserviceable(self):
        return {
            'name': 'Serviceable',
            'type': 'ir.actions.act_window',
            'res_model': 'status.service',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': False,
            'views': [(False, 'form')],
            'target': 'new',
            'context': "{'default_fleet_id':" + str(self.id) + ", 'default_type': 'US'}",
        }

    @api.multi
    def do_inspection(self):
        return {
            'name': 'Inspection',
            'type': 'ir.actions.act_window',
            'res_model': 'airworthy.inspection',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': False,
            'views': [(False, 'form')],
            'target': 'new',
            'context': "{'fleet_id':" + str(self.id) + "}",
        }

    @api.multi
    def do_document_check(self):
        return {
            'name': 'Document',
            'type': 'ir.actions.act_window',
            'res_model': 'aircraft.document',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': False,
            'views': [(False, 'form')],
            'target': 'new',
            'context': "{'fleet_id':" + str(self.id) + "}",
        }

    @api.multi
    def do_logbook_check(self):
        return {
            'name': 'Logbook',
            'type': 'ir.actions.act_window',
            'res_model': 'aircraft.logbook',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': False,
            'views': [(False, 'form')],
            'target': 'new',
            'context': "{'fleet_id':" + str(self.id) + "}",
        }

    @api.multi
    def do_overhaul(self):
        return {
            'name': 'Overhaul',
            'type': 'ir.actions.act_window',
            'res_model': 'airworthy.overhaul',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': False,
            'views': [(False, 'form')],
            'target': 'new',
            'context': "{'fleet_id':" + str(self.id) + "}",
        }

    @api.model
    def default_get(self, flds):
        result = super(paiis_corrective_aircraft, self).default_get(flds)
        result['bel_view'] = self.env.context.get('belcomponent',False)
        # self.bel_view = self.env.context.get('belcomponent',False)
        return result

    @api.model
    def check_serviceable(self):
        servicable = True
        # check every part is available
        # A/C Comp
        for ac_comp in self.component_ids:
            if (ac_comp.no_component == True):
                servicable = False
            for ac_subcomp in ac_comp.sub_part_ids:
                if (ac_subcomp.no_component == True):
                    servicable = False
        # Engine Comp
        if(self.engine_type_id):
            if(self.engine_type_id.check_serviceable() == False):
                servicable = False
        if(self.engine2_type_id):
            if(self.engine2_type_id.check_serviceable() == False):
                servicable = False
        if(self.engine3_type_id):
            if(self.engine3_type_id.check_serviceable() == False):
                servicable = False
        if(self.engine4_type_id):
            if(self.engine4_type_id.check_serviceable() == False):
                servicable = False
        # Prop Comp
        if(self.propeller_type_id):
            if(self.propeller_type_id.check_serviceable() == False):
                servicable = False
        if(self.propeller2_type_id):
            if(self.propeller2_type_id.check_serviceable() == False):
                servicable = False
        if(self.propeller3_type_id):
            if(self.propeller3_type_id.check_serviceable() == False):
                servicable = False
        if(self.propeller4_type_id):
            if(self.propeller4_type_id.check_serviceable() == False):
                servicable = False
        # Aux Comp
        if(self.auxiliary_type_id):
            if(self.auxiliary_type_id.check_serviceable() == False):
                servicable = False
        if self.id:
            self.aircraft_status = servicable
        return servicable

    # @api.onchange('id')
    # def _onchange_id(self):
    #     self.bel_view = self.env.context.get('belcomponent',False)
            

    @api.onchange('engine_type_id')
    def _onchange_engine_type_id(self):
        current_id = self.env['aircraft.acquisition'].search([('id','=',self._origin.id)])
        if(self.engine_type_id.id != current_id.engine_type_id.id):
            self.ac_hours_eng1 = current_id.total_hours
            self.ac_cycles_eng1 = current_id.total_landings
            self.en_hours_eng1 = self.engine_type_id.total_hours
            self.en_cycles_eng1 = self.engine_type_id.total_cycles
            self.engine_change = True
            self.engine_type_id_before  = current_id.engine_type_id.id
        else:
            self.ac_hours_eng1 = current_id.ac_hours_eng1
            self.ac_cycles_eng1 = current_id.ac_cycles_eng1
            self.en_hours_eng1 = current_id.en_hours_eng1
            self.en_cycles_eng1 = current_id.en_cycles_eng1
            self.engine_change = False

    @api.onchange('engine2_type_id')
    def _onchange_engine2_type_id(self):
        current_id = self.env['aircraft.acquisition'].search([('id','=',self._origin.id)])
        if(self.engine2_type_id.id != current_id.engine2_type_id.id):
            self.ac_hours_eng2 = current_id.total_hours
            self.ac_cycles_eng2 = current_id.total_landings
            self.en_hours_eng2 = self.engine2_type_id.total_hours
            self.en_cycles_eng2 = self.engine2_type_id.total_cycles
            self.engine2_change = True
            self.engine2_type_id_before  = current_id.engine2_type_id.id
        else:
            self.ac_hours_eng2 = current_id.ac_hours_eng2
            self.ac_cycles_eng2 = current_id.ac_cycles_eng2
            self.en_hours_eng2 = current_id.en_hours_eng2
            self.en_cycles_eng2 = current_id.en_cycles_eng2
            self.engine2_change = False

    @api.onchange('engine3_type_id')
    def _onchange_engine3_type_id(self):
        current_id = self.env['aircraft.acquisition'].search([('id','=',self._origin.id)])
        if(self.engine3_type_id.id != current_id.engine3_type_id.id):
            self.ac_hours_eng3 = current_id.total_hours
            self.ac_cycles_eng3 = current_id.total_landings
            self.en_hours_eng3 = self.engine3_type_id.total_hours
            self.en_cycles_eng3 = self.engine3_type_id.total_cycles
            self.engine3_change = True
            self.engine3_type_id_before  = current_id.engine3_type_id.id
        else:
            self.ac_hours_eng3 = current_id.ac_hours_eng3
            self.ac_cycles_eng3 = current_id.ac_cycles_eng3
            self.en_hours_eng3 = current_id.en_hours_eng3
            self.en_cycles_eng3 = current_id.en_cycles_eng3
            self.engine3_change = False

    @api.onchange('engine4_type_id')
    def _onchange_engine4_type_id(self):
        current_id = self.env['aircraft.acquisition'].search([('id','=',self._origin.id)])
        if(self.engine4_type_id.id != current_id.engine4_type_id.id):
            self.ac_hours_eng4 = current_id.total_hours
            self.ac_cycles_eng4 = current_id.total_landings
            self.en_hours_eng4 = self.engine4_type_id.total_hours
            self.en_cycles_eng4 = self.engine4_type_id.total_cycles
            self.engine4_change = True
            self.engine4_type_id_before  = current_id.engine4_type_id.id
        else:
            self.ac_hours_eng4 = current_id.ac_hours_eng4
            self.ac_cycles_eng4 = current_id.ac_cycles_eng4
            self.en_hours_eng4 = current_id.en_hours_eng4
            self.en_cycles_eng4 = current_id.en_cycles_eng4
            self.engine4_change = False

    @api.onchange('propeller_type_id')
    def _onchange_propeller_type_id(self):
        current_id = self.env['aircraft.acquisition'].search([('id','=',self._origin.id)])
        if(self.propeller_type_id.id != current_id.propeller_type_id.id):
            self.ac_hours_prop1 = current_id.total_hours
            self.ac_cycles_prop1 = current_id.total_landings
            self.pr_hours_prop1 = self.propeller_type_id.total_hours
            self.pr_cycles_prop1 = self.propeller_type_id.total_cycles
            self.propeller_change = True
            self.propeller_type_id_before  = current_id.propeller_type_id.id
        else:
            self.ac_hours_prop1 = current_id.ac_hours_prop1
            self.ac_cycles_prop1 = current_id.ac_cycles_prop1
            self.pr_hours_prop1 = current_id.pr_hours_prop1
            self.pr_cycles_prop1 = current_id.pr_cycles_prop1
            self.propeller_change = False

    @api.onchange('propeller2_type_id')
    def _onchange_propeller2_type_id(self):
        current_id = self.env['aircraft.acquisition'].search([('id','=',self._origin.id)])
        if(self.propeller2_type_id.id != current_id.propeller2_type_id.id):
            self.ac_hours_prop2 = current_id.total_hours
            self.ac_cycles_prop2 = current_id.total_landings
            self.pr_hours_prop2 = self.propeller2_type_id.total_hours
            self.pr_cycles_prop2 = self.propeller2_type_id.total_cycles
            self.propeller2_change = True
            self.propeller2_type_id_before  = current_id.propeller2_type_id.id
        else:
            self.ac_hours_prop2 = current_id.ac_hours_prop2
            self.ac_cycles_prop2 = current_id.ac_cycles_prop2
            self.pr_hours_prop2 = current_id.pr_hours_prop2
            self.pr_cycles_prop2 = current_id.pr_cycles_prop2
            self.propeller2_change = False

    @api.onchange('propeller3_type_id')
    def _onchange_propeller3_type_id(self):
        current_id = self.env['aircraft.acquisition'].search([('id','=',self._origin.id)])
        if(self.propeller3_type_id.id != current_id.propeller3_type_id.id):
            self.ac_hours_prop3 = current_id.total_hours
            self.ac_cycles_prop3 = current_id.total_landings
            self.pr_hours_prop3 = self.propeller3_type_id.total_hours
            self.pr_cycles_prop3 = self.propeller3_type_id.total_cycles
            self.propeller3_change = True
            self.propeller3_type_id_before  = current_id.propeller3_type_id.id
        else:
            self.ac_hours_prop3 = current_id.ac_hours_prop3
            self.ac_cycles_prop3 = current_id.ac_cycles_prop3
            self.pr_hours_prop3 = current_id.pr_hours_prop3
            self.pr_cycles_prop3 = current_id.pr_cycles_prop2
            self.propeller3_change = False

    @api.onchange('propeller4_type_id')
    def _onchange_propeller4_type_id(self):
        current_id = self.env['aircraft.acquisition'].search([('id','=',self._origin.id)])
        if(self.propeller4_type_id.id != current_id.propeller4_type_id.id):
            self.ac_hours_prop4 = current_id.total_hours
            self.ac_cycles_prop4 = current_id.total_landings
            self.pr_hours_prop4 = self.propeller4_type_id.total_hours
            self.pr_cycles_prop4 = self.propeller4_type_id.total_cycles
            self.propeller4_change = True
            self.propeller4_type_id_before  = current_id.propeller4_type_id.id
        else:
            self.ac_hours_prop4 = current_id.ac_hours_prop4
            self.ac_cycles_prop4 = current_id.ac_cycles_prop4
            self.pr_hours_prop4 = current_id.pr_hours_prop4
            self.pr_cycles_prop4 = current_id.pr_cycles_prop4
            self.propeller4_change = False

    @api.onchange('auxiliary_type_id')
    def _onchange_auxiliary_type_id(self):
        current_id = self.env['aircraft.acquisition'].search([('id','=',self._origin.id)])
        if(self.auxiliary_type_id.id != current_id.auxiliary_type_id.id):
            self.ac_hours_aux1 = current_id.total_hours
            self.ac_cycles_aux1 = current_id.total_landings
            self.aux_hours_aux1 = self.auxiliary_type_id.total_hours
            self.aux_cycles_aux1 = self.auxiliary_type_id.total_cycles
            self.auxiliary_change = True
            self.auxiliary_type_id_before  = current_id.auxiliary_type_id.id
        else:
            self.ac_hours_aux1 = current_id.ac_hours_aux1
            self.ac_cycles_aux1 = current_id.ac_cycles_aux1
            self.aux_hours_aux1 = current_id.aux_hours_aux1
            self.aux_cycles_aux1 = current_id.aux_cycles_aux1
            self.auxiliary_change = False
       
    @api.multi
    def return_action_to_open(self):
        return False

    # GAK DIPAKAI, CHECK SERVICEABLE LOG
    # @api.multi
    # def toggle_active(self):
    #     if(self.aircraft_status == True):
    #         self.aircraft_status = False
    #     else:
    #         self.aircraft_status = True
    #     ws = create_connection("ws://paiis.pelita-air.com:8000/dashboard")
    #     ws.send(json.dumps({"platform": "dashboard", "method": "refresh","message":"Refresh"}))
    #     result =  ws.recv()
    #     ws.close()

    def part_change(self,types,fleet_id,prev_id,replacement_id):
        if(types == 'engine'):
            if(prev_id):
                self.env['engine.type'].search([('id','=',prev_id)]).write({
                    'fleet_id' : False,
                    })
            if(replacement_id):
                self.env['engine.type'].search([('id','=',replacement_id)]).write({
                    'fleet_id' : fleet_id,
                    })
        if(types == 'auxiliary'):
            if(prev_id):
                self.env['auxiliary.type'].search([('id','=',prev_id)]).write({
                    'fleet_id' : False,
                    })
            if(replacement_id):
                self.env['auxiliary.type'].search([('id','=',replacement_id)]).write({
                    'fleet_id' : fleet_id,
                    })
        if(types == 'propeller'):
            if(prev_id):
                self.env['propeller.type'].search([('id','=',prev_id)]).write({
                    'fleet_id' : False,
                    })
            if(replacement_id):
                self.env['propeller.type'].search([('id','=',replacement_id)]).write({
                    'fleet_id' : fleet_id,
                    })

    @api.multi
    def write(self, vals):
        if('total_hours' in vals or 'total_landings' in vals or 'total_rins' in vals):
            if(self.env.context.get('manual_edit',False) == True) :
                self.env['ams.manual_changes'].create({
                    'fleet_id' : self.id,
                    'current_hours' : self.total_hours if ('total_hours' in vals) else False,
                    'current_cycles' : self.total_landings if ('total_landings' in vals) else False,
                    'current_rin' : self.total_rins if ('total_rins' in vals) else False,
                    'hours' : vals['total_hours'] if ('total_hours' in vals) else False,
                    'cycles' : vals['total_landings'] if ('total_landings' in vals) else False,
                    'rin' : vals['total_rins'] if ('total_rins' in vals) else False,
                    })

        if 'engine_type_id' in vals:
            if(vals['engine_type_id'] != self.engine_type_id.id):
                if(vals['engine_type_id'] == False):
                    hist = self.env['ams.component_history'].create({
                            'engine_id':self.engine_type_id.id,
                            'engine_replacement_id':False, 
                            'fleet_id':self.id,
                            'type':'detach',
                            'reason':vals['engine_change_reason'] if 'engine_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_eng1'] if 'ac_hours_eng1' in vals else 0,
                            'ac_cycles':vals['ac_cycles_eng1'] if 'ac_cycles_eng1' in vals else 0,
                            'hours':vals['en_hours_eng1'] if 'en_hours_eng1' in vals else 0,
                            'cycles':vals['en_cycles_eng1'] if 'en_cycles_eng1' in vals else 0,
                        })
                    self.part_change('engine',self.id,self.engine_type_id.id,False)
                elif(self.engine_type_id == False):
                    hist = self.env['ams.component_history'].create({
                            'engine_id':False,
                            'engine_replacement_id':vals['engine_type_id'], 
                            'fleet_id':self.id,
                            'type':'attach',
                            'reason':vals['engine_change_reason'] if 'engine_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_eng1'] if 'ac_hours_eng1' in vals else 0,
                            'ac_cycles':vals['ac_cycles_eng1'] if 'ac_cycles_eng1' in vals else 0,
                            'hours':vals['en_hours_eng1'] if 'en_hours_eng1' in vals else 0,
                            'cycles':vals['en_cycles_eng1'] if 'en_cycles_eng1' in vals else 0,
                        })
                    self.part_change('engine',self.id,False,vals['engine_type_id'])
                else:
                    hist = self.env['ams.component_history'].create({
                            'engine_id':self.engine_type_id.id,
                            'engine_replacement_id':vals['engine_type_id'], 
                            'fleet_id':self.id,
                            'type':'replace',
                            'reason':vals['engine_change_reason'] if 'engine_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_eng1'] if 'ac_hours_eng1' in vals else 0,
                            'ac_cycles':vals['ac_cycles_eng1'] if 'ac_cycles_eng1' in vals else 0,
                            'hours':vals['en_hours_eng1'] if 'en_hours_eng1' in vals else 0,
                            'cycles':vals['en_cycles_eng1'] if 'en_cycles_eng1' in vals else 0,
                        })
                    hist = self.env['ams.component_history'].create({
                            'engine_id':vals['engine_type_id'],
                            'engine_replacement_id':self.engine_type_id.id, 
                            'fleet_id':self.id,
                            'type':'attach',
                            'reason':vals['engine_change_reason'] if 'engine_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_eng1'] if 'ac_hours_eng1' in vals else 0,
                            'ac_cycles':vals['ac_cycles_eng1'] if 'ac_cycles_eng1' in vals else 0,
                            'hours':vals['en_hours_eng1'] if 'en_hours_eng1' in vals else 0,
                            'cycles':vals['en_cycles_eng1'] if 'en_cycles_eng1' in vals else 0,
                        })
                    self.part_change('engine',self.id,self.engine_type_id.id,vals['engine_type_id'])

        if 'engine2_type_id' in vals:
            if(vals['engine2_type_id'] != self.engine2_type_id.id):
                if(vals['engine2_type_id'] == False):
                    hist = self.env['ams.component_history'].create({
                            'engine_id':self.engine2_type_id.id,
                            'engine_replacement_id':False, 
                            'fleet_id':self.id,
                            'type':'detach',
                            'reason':vals['engine2_change_reason'] if 'engine2_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_eng2'] if 'ac_hours_eng2' in vals else 0,
                            'ac_cycles':vals['ac_cycles_eng2'] if 'ac_cycles_eng2' in vals else 0,
                            'hours':vals['en_hours_eng2'] if 'en_hours_eng2' in vals else 0,
                            'cycles':vals['en_cycles_eng2'] if 'en_cycles_eng2' in vals else 0,
                        })
                    self.part_change('engine',self.id,self.engine2_type_id.id,False)
                elif(self.engine2_type_id == False):
                    hist = self.env['ams.component_history'].create({
                            'engine_id':False,
                            'engine_replacement_id':vals['engine2_type_id'], 
                            'fleet_id':self.id,
                            'type':'attach',
                            'reason':vals['engine2_change_reason'] if 'engine2_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_eng2'] if 'ac_hours_eng2' in vals else 0,
                            'ac_cycles':vals['ac_cycles_eng2'] if 'ac_cycles_eng2' in vals else 0,
                            'hours':vals['en_hours_eng2'] if 'en_hours_eng2' in vals else 0,
                            'cycles':vals['en_cycles_eng2'] if 'en_cycles_eng2' in vals else 0,
                        })
                    self.part_change('engine',self.id,False,vals['engine2_type_id'])
                else:
                    hist = self.env['ams.component_history'].create({
                            'engine_id':self.engine2_type_id.id,
                            'engine_replacement_id':vals['engine2_type_id'], 
                            'fleet_id':self.id,
                            'type':'replace',
                            'reason':vals['engine2_change_reason'] if 'engine2_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_eng2'] if 'ac_hours_eng2' in vals else 0,
                            'ac_cycles':vals['ac_cycles_eng2'] if 'ac_cycles_eng2' in vals else 0,
                            'hours':vals['en_hours_eng2'] if 'en_hours_eng2' in vals else 0,
                            'cycles':vals['en_cycles_eng2'] if 'en_cycles_eng2' in vals else 0,
                        })
                    hist = self.env['ams.component_history'].create({
                            'engine_id':vals['engine2_type_id'],
                            'engine_replacement_id':self.engine2_type_id.id, 
                            'fleet_id':self.id,
                            'type':'attach',
                            'reason':vals['engine2_change_reason'] if 'engine2_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_eng2'] if 'ac_hours_eng2' in vals else 0,
                            'ac_cycles':vals['ac_cycles_eng2'] if 'ac_cycles_eng2' in vals else 0,
                            'hours':vals['en_hours_eng2'] if 'en_hours_eng2' in vals else 0,
                            'cycles':vals['en_cycles_eng2'] if 'en_cycles_eng2' in vals else 0,
                        })
                    self.part_change('engine',self.id,self.engine2_type_id.id,vals['engine2_type_id'])
        if 'engine3_type_id' in vals:
            if(vals['engine3_type_id'] != self.engine3_type_id.id):
                if(vals['engine3_type_id'] == False):
                    hist = self.env['ams.component_history'].create({
                            'engine_id':self.engine3_type_id.id,
                            'engine_replacement_id':False, 
                            'fleet_id':self.id,
                            'type':'detach',
                            'reason':vals['engine3_change_reason'] if 'engine3_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_eng3'] if 'ac_hours_eng3' in vals else 0,
                            'ac_cycles':vals['ac_cycles_eng3'] if 'ac_cycles_eng3' in vals else 0,
                            'hours':vals['en_hours_eng3'] if 'en_hours_eng3' in vals else 0,
                            'cycles':vals['en_cycles_eng3'] if 'en_cycles_eng3' in vals else 0,
                        })
                    self.part_change('engine',self.id,self.engine3_type_id.id,False)
                elif(self.engine3_type_id == False):
                    hist = self.env['ams.component_history'].create({
                            'engine_id':False,
                            'engine_replacement_id':vals['engine3_type_id'], 
                            'fleet_id':self.id,
                            'type':'attach',
                            'reason':vals['engine3_change_reason'] if 'engine3_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_eng3'] if 'ac_hours_eng3' in vals else 0,
                            'ac_cycles':vals['ac_cycles_eng3'] if 'ac_cycles_eng3' in vals else 0,
                            'hours':vals['en_hours_eng3'] if 'en_hours_eng3' in vals else 0,
                            'cycles':vals['en_cycles_eng3'] if 'en_cycles_eng3' in vals else 0,
                        })
                    self.part_change('engine',self.id,False,vals['engine3_type_id'])
                else:
                    hist = self.env['ams.component_history'].create({
                            'engine_id':self.engine3_type_id.id,
                            'engine_replacement_id':vals['engine3_type_id'], 
                            'fleet_id':self.id,
                            'type':'replace',
                            'reason':vals['engine3_change_reason'] if 'engine3_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_eng3'] if 'ac_hours_eng3' in vals else 0,
                            'ac_cycles':vals['ac_cycles_eng3'] if 'ac_cycles_eng3' in vals else 0,
                            'hours':vals['en_hours_eng3'] if 'en_hours_eng3' in vals else 0,
                            'cycles':vals['en_cycles_eng3'] if 'en_cycles_eng3' in vals else 0,
                        })
                    hist = self.env['ams.component_history'].create({
                            'engine_id':vals['engine3_type_id'],
                            'engine_replacement_id':self.engine3_type_id.id, 
                            'fleet_id':self.id,
                            'type':'attach',
                            'reason':vals['engine3_change_reason'] if 'engine3_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_eng3'] if 'ac_hours_eng3' in vals else 0,
                            'ac_cycles':vals['ac_cycles_eng3'] if 'ac_cycles_eng3' in vals else 0,
                            'hours':vals['en_hours_eng3'] if 'en_hours_eng3' in vals else 0,
                            'cycles':vals['en_cycles_eng3'] if 'en_cycles_eng3' in vals else 0,
                        })
                    self.part_change('engine',self.id,self.engine3_type_id.id,vals['engine3_type_id'])
        if 'engine4_type_id' in vals:
            if(vals['engine4_type_id'] != self.engine4_type_id.id):
                if(vals['engine4_type_id'] == False):
                    hist = self.env['ams.component_history'].create({
                            'engine_id':self.engine4_type_id.id,
                            'engine_replacement_id':False, 
                            'fleet_id':self.id,
                            'type':'detach',
                            'reason':vals['engine4_change_reason'] if 'engine4_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_eng4'] if 'ac_hours_eng4' in vals else 0,
                            'ac_cycles':vals['ac_cycles_eng4'] if 'ac_cycles_eng4' in vals else 0,
                            'hours':vals['en_hours_eng4'] if 'en_hours_eng4' in vals else 0,
                            'cycles':vals['en_cycles_eng4'] if 'en_cycles_eng4' in vals else 0,
                        })
                    self.part_change('engine',self.id,self.engine4_type_id.id,False)
                elif(self.engine4_type_id == False):
                    hist = self.env['ams.component_history'].create({
                            'engine_id':False,
                            'engine_replacement_id':vals['engine4_type_id'], 
                            'fleet_id':self.id,
                            'type':'attach',
                            'reason':vals['engine4_change_reason'] if 'engine4_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_eng4'] if 'ac_hours_eng4' in vals else 0,
                            'ac_cycles':vals['ac_cycles_eng4'] if 'ac_cycles_eng4' in vals else 0,
                            'hours':vals['en_hours_eng4'] if 'en_hours_eng4' in vals else 0,
                            'cycles':vals['en_cycles_eng4'] if 'en_cycles_eng4' in vals else 0,
                        })
                    self.part_change('engine',self.id,False,vals['engine4_type_id'])
                else:
                    hist = self.env['ams.component_history'].create({
                            'engine_id':self.engine4_type_id.id,
                            'engine_replacement_id':vals['engine4_type_id'], 
                            'fleet_id':self.id,
                            'type':'replace',
                            'reason':vals['engine4_change_reason'] if 'engine4_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_eng4'] if 'ac_hours_eng4' in vals else 0,
                            'ac_cycles':vals['ac_cycles_eng4'] if 'ac_cycles_eng4' in vals else 0,
                            'hours':vals['en_hours_eng4'] if 'en_hours_eng4' in vals else 0,
                            'cycles':vals['en_cycles_eng4'] if 'en_cycles_eng4' in vals else 0,
                        })
                    hist = self.env['ams.component_history'].create({
                            'engine_id':vals['engine4_type_id'],
                            'engine_replacement_id':self.engine4_type_id.id, 
                            'fleet_id':self.id,
                            'type':'attach',
                            'reason':vals['engine4_change_reason'] if 'engine4_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_eng4'] if 'ac_hours_eng4' in vals else 0,
                            'ac_cycles':vals['ac_cycles_eng4'] if 'ac_cycles_eng4' in vals else 0,
                            'hours':vals['en_hours_eng4'] if 'en_hours_eng4' in vals else 0,
                            'cycles':vals['en_cycles_eng4'] if 'en_cycles_eng4' in vals else 0,
                        })
                    self.part_change('engine',self.id,self.engine4_type_id.id,vals['engine4_type_id'])
        if 'auxiliary_type_id' in vals:
            if(vals['auxiliary_type_id'] != self.auxiliary_type_id.id):
                if(vals['auxiliary_type_id'] == False):
                    hist = self.env['ams.component_history'].create({
                            'auxiliary_id':self.auxiliary_type_id.id,
                            'auxiliary_replacement_id':False, 
                            'fleet_id':self.id,
                            'type':'detach',
                            'reason':vals['auxiliary_change_reason'] if 'auxiliary_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_aux1'] if 'ac_hours_aux1' in vals else 0,
                            'ac_cycles':vals['ac_cycles_aux1'] if 'ac_cycles_aux1' in vals else 0,
                            'hours':vals['aux_hours_aux1'] if 'aux_hours_aux1' in vals else 0,
                            'cycles':vals['aux_cycles_aux1'] if 'aux_cycles_aux1' in vals else 0,
                        })
                    self.part_change('auxiliary',self.id,self.auxiliary_type_id.id,False)
                elif(self.auxiliary_type_id == False):
                    hist = self.env['ams.component_history'].create({
                            'auxiliary_id':False,
                            'auxiliary_replacement_id':vals['auxiliary_type_id'], 
                            'fleet_id':self.id,
                            'type':'attach',
                            'reason':vals['auxiliary_change_reason'] if 'auxiliary_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_aux1'] if 'ac_hours_aux1' in vals else 0,
                            'ac_cycles':vals['ac_cycles_aux1'] if 'ac_cycles_aux1' in vals else 0,
                            'hours':vals['aux_hours_aux1'] if 'aux_hours_aux1' in vals else 0,
                            'cycles':vals['aux_cycles_aux1'] if 'aux_cycles_aux1' in vals else 0,
                        })
                    self.part_change('auxiliary',self.id,False,vals['auxiliary_type_id'])
                else:
                    hist = self.env['ams.component_history'].create({
                            'auxiliary_id':self.auxiliary_type_id.id,
                            'auxiliary_replacement_id':vals['auxiliary_type_id'], 
                            'fleet_id':self.id,
                            'type':'replace',
                            'reason':vals['auxiliary_change_reason'] if 'auxiliary_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_aux1'] if 'ac_hours_aux1' in vals else 0,
                            'ac_cycles':vals['ac_cycles_aux1'] if 'ac_cycles_aux1' in vals else 0,
                            'hours':vals['aux_hours_aux1'] if 'aux_hours_aux1' in vals else 0,
                            'cycles':vals['aux_cycles_aux1'] if 'aux_cycles_aux1' in vals else 0,
                        })
                    hist = self.env['ams.component_history'].create({
                            'auxiliary_id':vals['auxiliary_type_id'],
                            'auxiliary_replacement_id':self.auxiliary_type_id.id, 
                            'fleet_id':self.id,
                            'type':'attach',
                            'reason':vals['auxiliary_change_reason'] if 'auxiliary_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_aux1'] if 'ac_hours_aux1' in vals else 0,
                            'ac_cycles':vals['ac_cycles_aux1'] if 'ac_cycles_aux1' in vals else 0,
                            'hours':vals['aux_hours_aux1'] if 'aux_hours_aux1' in vals else 0,
                            'cycles':vals['aux_cycles_aux1'] if 'aux_cycles_aux1' in vals else 0,
                        })
                    self.part_change('auxiliary',self.id,self.auxiliary_type_id.id,vals['auxiliary_type_id'])
        if 'propeller_type_id' in vals:
            if(vals['propeller_type_id'] != self.propeller_type_id.id):
                if(vals['propeller_type_id'] == False):
                    hist = self.env['ams.component_history'].create({
                            'propeller_id':self.propeller_type_id.id,
                            'propeller_replacement_id':False, 
                            'fleet_id':self.id,
                            'type':'detach',
                            'reason':vals['propeller_change_reason'] if 'propeller_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_prop1'] if 'ac_hours_prop1' in vals else 0,
                            'ac_cycles':vals['ac_cycles_prop1'] if 'ac_cycles_prop1' in vals else 0,
                            'hours':vals['pr_hours_prop1'] if 'pr_hours_prop1' in vals else 0,
                            'cycles':vals['pr_cycles_prop1'] if 'pr_cycles_prop1' in vals else 0,
                        })
                    self.part_change('propeller',self.id,self.propeller_type_id.id,False)
                elif(self.propeller_type_id == False):
                    hist = self.env['ams.component_history'].create({
                            'propeller_id':False,
                            'propeller_replacement_id':vals['propeller_type_id'], 
                            'fleet_id':self.id,
                            'type':'attach',
                            'reason':vals['propeller_change_reason'] if 'propeller_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_prop1'] if 'ac_hours_prop1' in vals else 0,
                            'ac_cycles':vals['ac_cycles_prop1'] if 'ac_cycles_prop1' in vals else 0,
                            'hours':vals['pr_hours_prop1'] if 'pr_hours_prop1' in vals else 0,
                            'cycles':vals['pr_cycles_prop1'] if 'pr_cycles_prop1' in vals else 0,
                        })
                    self.part_change('propeller',self.id,False,vals['propeller_type_id'])
                else:
                    hist = self.env['ams.component_history'].create({
                            'propeller_id':self.propeller_type_id.id,
                            'propeller_replacement_id':vals['propeller_type_id'], 
                            'fleet_id':self.id,
                            'type':'replace',
                            'reason':vals['propeller_change_reason'] if 'propeller_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_prop1'] if 'ac_hours_prop1' in vals else 0,
                            'ac_cycles':vals['ac_cycles_prop1'] if 'ac_cycles_prop1' in vals else 0,
                            'hours':vals['pr_hours_prop1'] if 'pr_hours_prop1' in vals else 0,
                            'cycles':vals['pr_cycles_prop1'] if 'pr_cycles_prop1' in vals else 0,
                        })
                    hist = self.env['ams.component_history'].create({
                            'propeller_id':vals['propeller_type_id'],
                            'propeller_replacement_id':self.propeller_type_id.id, 
                            'fleet_id':self.id,
                            'type':'attach',
                            'reason':vals['propeller_change_reason'] if 'propeller_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_prop1'] if 'ac_hours_prop1' in vals else 0,
                            'ac_cycles':vals['ac_cycles_prop1'] if 'ac_cycles_prop1' in vals else 0,
                            'hours':vals['pr_hours_prop1'] if 'pr_hours_prop1' in vals else 0,
                            'cycles':vals['pr_cycles_prop1'] if 'pr_cycles_prop1' in vals else 0,
                        })
                    self.part_change('propeller',self.id,self.propeller_type_id.id,vals['propeller_type_id'])
        if 'propeller2_type_id' in vals:
            if(vals['propeller2_type_id'] != self.propeller2_type_id.id):
                if(vals['propeller2_type_id'] == False):
                    hist = self.env['ams.component_history'].create({
                            'propeller_id':self.propeller2_type_id.id,
                            'propeller_replacement_id':False, 
                            'fleet_id':self.id,
                            'type':'detach',
                            'reason':vals['propeller2_change_reason'] if 'propeller2_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_prop2'] if 'ac_hours_prop2' in vals else 0,
                            'ac_cycles':vals['ac_cycles_prop2'] if 'ac_cycles_prop2' in vals else 0,
                            'hours':vals['pr_hours_prop2'] if 'pr_hours_prop2' in vals else 0,
                            'cycles':vals['pr_cycles_prop2'] if 'pr_cycles_prop2' in vals else 0,
                        })
                    self.part_change('propeller',self.id,self.propeller2_type_id.id,False)
                elif(self.propeller2_type_id == False):
                    hist = self.env['ams.component_history'].create({
                            'propeller_id':False,
                            'propeller_replacement_id':vals['propeller2_type_id'], 
                            'fleet_id':self.id,
                            'type':'attach',
                            'reason':vals['propeller2_change_reason'] if 'propeller2_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_prop2'] if 'ac_hours_prop2' in vals else 0,
                            'ac_cycles':vals['ac_cycles_prop2'] if 'ac_cycles_prop2' in vals else 0,
                            'hours':vals['pr_hours_prop2'] if 'pr_hours_prop2' in vals else 0,
                            'cycles':vals['pr_cycles_prop2'] if 'pr_cycles_prop2' in vals else 0,
                        })
                    self.part_change('propeller',self.id,False,vals['propeller2_type_id'])
                else:
                    hist = self.env['ams.component_history'].create({
                            'propeller_id':self.propeller2_type_id.id,
                            'propeller_replacement_id':vals['propeller2_type_id'], 
                            'fleet_id':self.id,
                            'type':'replace',
                            'reason':vals['propeller2_change_reason'] if 'propeller2_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_prop2'] if 'ac_hours_prop2' in vals else 0,
                            'ac_cycles':vals['ac_cycles_prop2'] if 'ac_cycles_prop2' in vals else 0,
                            'hours':vals['pr_hours_prop2'] if 'pr_hours_prop2' in vals else 0,
                            'cycles':vals['pr_cycles_prop2'] if 'pr_cycles_prop2' in vals else 0,
                        })
                    hist = self.env['ams.component_history'].create({
                            'propeller_id':vals['propeller2_type_id'],
                            'propeller_replacement_id':self.propeller2_type_id.id, 
                            'fleet_id':self.id,
                            'type':'attach',
                            'reason':vals['propeller2_change_reason'] if 'propeller2_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_prop2'] if 'ac_hours_prop2' in vals else 0,
                            'ac_cycles':vals['ac_cycles_prop2'] if 'ac_cycles_prop2' in vals else 0,
                            'hours':vals['pr_hours_prop2'] if 'pr_hours_prop2' in vals else 0,
                            'cycles':vals['pr_cycles_prop2'] if 'pr_cycles_prop2' in vals else 0,
                        })
                    self.part_change('propeller',self.id,self.propeller2_type_id.id,vals['propeller2_type_id'])
        if 'propeller3_type_id' in vals:
            if(vals['propeller3_type_id'] != self.propeller3_type_id.id):
                if(vals['propeller3_type_id'] == False):
                    hist = self.env['ams.component_history'].create({
                            'propeller_id':self.propeller3_type_id.id,
                            'propeller_replacement_id':False, 
                            'fleet_id':self.id,
                            'type':'detach',
                            'reason':vals['propeller3_change_reason'] if 'propeller3_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_prop3'] if 'ac_hours_prop3' in vals else 0,
                            'ac_cycles':vals['ac_cycles_prop3'] if 'ac_cycles_prop3' in vals else 0,
                            'hours':vals['pr_hours_prop3'] if 'pr_hours_prop3' in vals else 0,
                            'cycles':vals['pr_cycles_prop3'] if 'pr_cycles_prop3' in vals else 0,
                        })
                    self.part_change('propeller',self.id,self.propeller3_type_id.id,False)
                elif(self.propeller3_type_id == False):
                    hist = self.env['ams.component_history'].create({
                            'propeller_id':False,
                            'propeller_replacement_id':vals['propeller3_type_id'], 
                            'fleet_id':self.id,
                            'type':'attach',
                            'reason':vals['propeller3_change_reason'] if 'propeller3_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_prop3'] if 'ac_hours_prop3' in vals else 0,
                            'ac_cycles':vals['ac_cycles_prop3'] if 'ac_cycles_prop3' in vals else 0,
                            'hours':vals['pr_hours_prop3'] if 'pr_hours_prop3' in vals else 0,
                            'cycles':vals['pr_cycles_prop3'] if 'pr_cycles_prop3' in vals else 0,
                        })
                    self.part_change('propeller',self.id,False,vals['propeller3_type_id'])
                else:
                    hist = self.env['ams.component_history'].create({
                            'propeller_id':self.propeller3_type_id.id,
                            'propeller_replacement_id':vals['propeller3_type_id'], 
                            'fleet_id':self.id,
                            'type':'replace',
                            'reason':vals['propeller3_change_reason'] if 'propeller3_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_prop3'] if 'ac_hours_prop3' in vals else 0,
                            'ac_cycles':vals['ac_cycles_prop3'] if 'ac_cycles_prop3' in vals else 0,
                            'hours':vals['pr_hours_prop3'] if 'pr_hours_prop3' in vals else 0,
                            'cycles':vals['pr_cycles_prop3'] if 'pr_cycles_prop3' in vals else 0,
                        })
                    hist = self.env['ams.component_history'].create({
                            'propeller_id':vals['propeller3_type_id'],
                            'propeller_replacement_id':self.propeller3_type_id.id, 
                            'fleet_id':self.id,
                            'type':'attach',
                            'reason':vals['propeller3_change_reason'] if 'propeller3_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_prop3'] if 'ac_hours_prop3' in vals else 0,
                            'ac_cycles':vals['ac_cycles_prop3'] if 'ac_cycles_prop3' in vals else 0,
                            'hours':vals['pr_hours_prop3'] if 'pr_hours_prop3' in vals else 0,
                            'cycles':vals['pr_cycles_prop3'] if 'pr_cycles_prop3' in vals else 0,
                        })
                    self.part_change('propeller',self.id,self.propeller3_type_id.id,vals['propeller3_type_id'])
        if 'propeller4_type_id' in vals:
            if(vals['propeller4_type_id'] != self.propeller4_type_id.id):
                if(vals['propeller4_type_id'] == False):
                    hist = self.env['ams.component_history'].create({
                            'propeller_id':self.propeller4_type_id.id,
                            'propeller_replacement_id':False, 
                            'fleet_id':self.id,
                            'type':'detach',
                            'reason':vals['propeller4_change_reason'] if 'propeller4_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_prop4'] if 'ac_hours_prop4' in vals else 0,
                            'ac_cycles':vals['ac_cycles_prop4'] if 'ac_cycles_prop4' in vals else 0,
                            'hours':vals['pr_hours_prop4'] if 'pr_hours_prop4' in vals else 0,
                            'cycles':vals['pr_cycles_prop4'] if 'pr_cycles_prop4' in vals else 0,
                        })
                    self.part_change('propeller',self.id,self.propeller4_type_id.id,False)
                elif(self.propeller4_type_id == False):
                    hist = self.env['ams.component_history'].create({
                            'propeller_id':False,
                            'propeller_replacement_id':vals['propeller4_type_id'], 
                            'fleet_id':self.id,
                            'type':'attach',
                            'reason':vals['propeller4_change_reason'] if 'propeller4_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_prop4'] if 'ac_hours_prop4' in vals else 0,
                            'ac_cycles':vals['ac_cycles_prop4'] if 'ac_cycles_prop4' in vals else 0,
                            'hours':vals['pr_hours_prop4'] if 'pr_hours_prop4' in vals else 0,
                            'cycles':vals['pr_cycles_prop4'] if 'pr_cycles_prop4' in vals else 0,
                        })
                    self.part_change('propeller',self.id,False,vals['propeller4_type_id'])
                else:
                    hist = self.env['ams.component_history'].create({
                            'propeller_id':self.propeller4_type_id.id,
                            'propeller_replacement_id':vals['propeller4_type_id'], 
                            'fleet_id':self.id,
                            'type':'replace',
                            'reason':vals['propeller4_change_reason'] if 'propeller4_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_prop4'] if 'ac_hours_prop4' in vals else 0,
                            'ac_cycles':vals['ac_cycles_prop4'] if 'ac_cycles_prop4' in vals else 0,
                            'hours':vals['pr_hours_prop4'] if 'pr_hours_prop4' in vals else 0,
                            'cycles':vals['pr_cycles_prop4'] if 'pr_cycles_prop4' in vals else 0,
                        })
                    hist = self.env['ams.component_history'].create({
                            'propeller_id':vals['propeller4_type_id'],
                            'propeller_replacement_id':self.propeller4_type_id.id, 
                            'fleet_id':self.id,
                            'type':'attach',
                            'reason':vals['propeller4_change_reason'] if 'propeller4_change_reason' in vals else '',
                            'ac_hours':vals['ac_hours_prop4'] if 'ac_hours_prop4' in vals else 0,
                            'ac_cycles':vals['ac_cycles_prop4'] if 'ac_cycles_prop4' in vals else 0,
                            'hours':vals['pr_hours_prop4'] if 'pr_hours_prop4' in vals else 0,
                            'cycles':vals['pr_cycles_prop4'] if 'pr_cycles_prop4' in vals else 0,
                        })
                    self.part_change('propeller',self.id,self.propeller4_type_id.id,vals['propeller4_type_id'])
        vals['engine_change'] = False
        vals['engine2_change'] = False
        vals['engine3_change'] = False
        vals['engine4_change'] = False
        vals['engine_change_reason'] = False
        vals['engine2_change_reason'] = False
        vals['engine3_change_reason'] = False
        vals['engine4_change_reason'] = False
        vals['auxiliary_change'] = False
        vals['auxiliary_change_reason'] = False
        write = super(paiis_corrective_aircraft, self).write(vals)
        # if vals.get('twitter_api_key') or vals.get('twitter_api_secret') or vals.get('twitter_screen_name'):
            # self._check_twitter_authorization()
        return write

    @api.model
    def create(self, vals):
        acquisition = super(paiis_corrective_aircraft, self).create(vals)
        if ('engine_type_id' in vals) and vals.get('engine_type_id'):
            self.part_change('engine',acquisition.id,False,vals['engine_type_id'])
        if ('engine2_type_id' in vals) and vals.get('engine2_type_id'):
            self.part_change('engine',acquisition.id,False,vals['engine2_type_id'])
        if ('engine3_type_id' in vals) and vals.get('engine3_type_id'):
            self.part_change('engine',acquisition.id,False,vals['engine3_type_id'])
        if ('engine4_type_id' in vals) and vals.get('engine4_type_id'):
            self.part_change('engine',acquisition.id,False,vals['engine4_type_id'])
        if ('auxiliary_type_id' in vals) and vals.get('auxiliary_type_id'):
            self.part_change('auxiliary',acquisition.id,False,vals['auxiliary_type_id'])
        if ('propeller_type_id' in vals) and vals.get('propeller_type_id'):
            self.part_change('propeller',acquisition.id,False,vals['propeller_type_id'])
        if ('propeller2_type_id' in vals) and vals.get('propeller2_type_id'):
            self.part_change('propeller',acquisition.id,False,vals['propeller2_type_id'])
        if ('propeller3_type_id' in vals) and vals.get('propeller3_type_id'):
            self.part_change('propeller',acquisition.id,False,vals['propeller3_type_id'])
        if ('propeller4_type_id' in vals) and vals.get('propeller4_type_id'):
            self.part_change('propeller',acquisition.id,False,vals['propeller4_type_id'])

        product_categ = self.env['product.category']
        if ('aircraft_name' in vals) and vals.get('aircraft_name'): #('product_tmpl_ok' in vals) and vals['product_tmpl_ok'] and
            aircraft = self.env['aircraft.aircraft'].browse(vals.get('aircraft_name'))
            exist_categ = product_categ.search([('name', 'like', '%' + str(aircraft.aircraft_categ).title() + '%')], limit=1)
            if not exist_categ:
                parent_categ = product_categ.search([('name', 'like', '%PAS%')], limit=1)
                categ_id = product_categ.create({'name': str(aircraft.aircraft_categ).title(),  'type': 'normal',
                                                 'parent_id': parent_categ and parent_categ.id}).id
            else:
                categ_id = exist_categ.id or False
            if (vals.get('name') or acquisition.name):  #aircraft.aircraft_code: aircraft.name and
                uom_ids = self.env['product.uom'].search(['|',('name','like','%Hour%'),('name','like','%Hour(s)%')], limit=1)
                product_tmpl_id = self.env['product.template'].create({
                    'name': aircraft.name,
                    'default_code': vals.get('name') or acquisition.name,  #aircraft.aircraft_code,
                    'type': 'service',
                    'categ_id': categ_id or 1,
                    'sale_ok': True,
                    'purchase_ok': False,
                    'uom_id': uom_ids and uom_ids.id or 1,
                    'uom_po_id': uom_ids and uom_ids.id or 1,
                    'aircraft_ok': True,
                    'aircraft_state': 'serviceable',
                    'availability_aircraft': 'available',
                })
                if product_tmpl_id:
                    acquisition.write({'product_tmpl_id': product_tmpl_id.id})
        return acquisition

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.id:
                rec.is_deleted = True

    @api.multi
    def restore(self):
        for rec in self:
            if rec.id:
                rec.is_deleted = False

    @api.multi
    def reset_component(self):
        for rec in self:
            if rec.id:
                # component
                for comp in rec.component_ids:
                    comp.serial_number_text = comp.serial_number.name
                    comp.serial_number = False
                    for subcomp in comp.sub_part_ids:
                        subcomp.serial_number_text = subcomp.serial_number.name
                        subcomp.serial_number = False
                
                for comp in rec.engine_type_id.component_ids:
                    comp.serial_number_text = comp.serial_number.name
                    comp.serial_number = False
                    for subcomp in comp.sub_part_ids:
                        subcomp.serial_number_text = subcomp.serial_number.name
                        subcomp.serial_number = False

                for comp in rec.engine2_type_id.component_ids:
                    comp.serial_number_text = comp.serial_number.name
                    comp.serial_number = False
                    for subcomp in comp.sub_part_ids:
                        subcomp.serial_number_text = subcomp.serial_number.name
                        subcomp.serial_number = False

                for comp in rec.engine3_type_id.component_ids:
                    comp.serial_number_text = comp.serial_number.name
                    comp.serial_number = False
                    for subcomp in comp.sub_part_ids:
                        subcomp.serial_number_text = subcomp.serial_number.name
                        subcomp.serial_number = False

                for comp in rec.engine4_type_id.component_ids:
                    comp.serial_number_text = comp.serial_number.name
                    comp.serial_number = False
                    for subcomp in comp.sub_part_ids:
                        subcomp.serial_number_text = subcomp.serial_number.name
                        subcomp.serial_number = False

                for comp in rec.auxiliary_type_id.component_ids:
                    comp.serial_number_text = comp.serial_number.name
                    comp.serial_number = False
                    for subcomp in comp.sub_part_ids:
                        subcomp.serial_number_text = subcomp.serial_number.name
                        subcomp.serial_number = False

                for comp in rec.propeller_type_id.component_ids:
                    comp.serial_number_text = comp.serial_number.name
                    comp.serial_number = False
                    for subcomp in comp.sub_part_ids:
                        subcomp.serial_number_text = subcomp.serial_number.name
                        subcomp.serial_number = False

                for comp in rec.propeller2_type_id.component_ids:
                    comp.serial_number_text = comp.serial_number.name
                    comp.serial_number = False
                    for subcomp in comp.sub_part_ids:
                        subcomp.serial_number_text = subcomp.serial_number.name
                        subcomp.serial_number = False

                for comp in rec.propeller3_type_id.component_ids:
                    comp.serial_number_text = comp.serial_number.name
                    comp.serial_number = False
                    for subcomp in comp.sub_part_ids:
                        subcomp.serial_number_text = subcomp.serial_number.name
                        subcomp.serial_number = False

                for comp in rec.propeller4_type_id.component_ids:
                    comp.serial_number_text = comp.serial_number.name
                    comp.serial_number = False
                    for subcomp in comp.sub_part_ids:
                        subcomp.serial_number_text = subcomp.serial_number.name
                        subcomp.serial_number = False

    @api.multi
    def check_import_csv(self):
        return{
            'type': 'ir.actions.act_window',
            'name': 'Check Import CSV',
            'res_model': 'wizard.check.import.csv',
            'view_mode': 'form',
            'target': 'new',
            'context':{
                'acraft': self.id,
            },
        }

class WizardCsvImport(models.Model):
    _name   = 'wizard.check.import.csv'

    file        = fields.Binary('File')
    filename    = fields.Char(string="Filename")
    fleet_id = fields.Many2one('aircraft.acquisition', string='Aircraft', default=lambda self:self._context.get('acraft', False))
        
    @api.multi
    def get_action_wizard(self, comptype='M'):

        acraft = self.fleet_id.id
        print acraft

        if(acraft != False):
            self.fleet_id.component_ids.unlink()
            self.fleet_id.inspection_ids.unlink()
            self.env.cr.commit()
            filedata = base64.b64decode(self.file)
            input = cStringIO.StringIO(filedata)
            input.seek(0)
       
            (fileno, fp_name) = tempfile.mkstemp('.csv', 'openerp_')
            file = open(fp_name, "w")
            file.write(filedata)
            file.close()
               
            ro = list(csv.reader(open(fp_name,"rb"), delimiter=';'))
            # head = ro.next()[0].split(';')
            print 'Hihihihihi'
            if len(ro) >= 1:
                if ro[0][155] == 'CALMID':
                    part_name = 0
                    last_time_insp = 94
                    rhll = 82
                    since_time_insp = 93
                    part_desc = 95
                    part_no = 1
                    serial = 2
                    ata_1 = 3
                    ata_2 = 4
                    ata_3 = 5
                    rank = 68
                    inst_date = 6
                    item = 90
                    calm_id = 155
                    delete = 156

                    cycle_on_install = 8
                    csn = 9
                    cso = 11

                    on_condition = 26
                    U2TT = 48
                    on_condition_hours = 49
                    on_aircraft_hours = 47
                    on_comp_hours = 46

                    comment = 79

                    retirement = 33
                    retirement_hours = 34
                    retirement_aircraft_hours = 36
                    retirement_comp_hours = 35
                    retirement_comp_attach_at = 37
                    retirement_current = 37

                    overhaul = 27
                    overhaul_hours = 28
                    overhaul_aircraft_hours = 30
                    overhaul_comp_hours = 29
                    overhaul_comp_attach_at = 31
                    overhaul_current = 32

                    inspection = 16
                    inspection_hours = 17
                    inspection_aircraft_hours = 19
                    inspection_comp_hours = 18
                    inspection_comp_attach_at = 20
                    inspection_current = 21

                    cycles_on = 7
                    cycles_type = 159
                    cycles_value = 8
                    cycles_current = 11
                    aircraft_cycles = 10
                    comp_cycles = 9
                    comp_cycles_attach_at = 11

                    month_on = 22
                    month_type = 24
                    month_value = 23
                    month_date = 25

                    days_on = 12
                    days_type = 14
                    days_value = 13
                    days_date = 15
                elif ro[0][165] == 'CALMID':
                    part_name = 0
                    last_time_insp = 94
                    rhll = 82
                    since_time_insp = 93
                    part_desc = 95
                    part_no = 1
                    serial = 2
                    ata_1 = 3
                    ata_2 = 4
                    ata_3 = 5
                    rank = 68
                    inst_date = 6
                    item = 90
                    calm_id = 165
                    delete = 166
                    ste_hr = 172
                    ste_cy = 173
                    ste_overhaul = 174
                    ste_retire = 175

                    cycle_on_install = 8
                    csn = 9
                    cso = 11

                    on_condition = 26
                    U2TT = 48
                    on_condition_hours = 49
                    on_aircraft_hours = 47
                    on_comp_hours = 46

                    comment = 79

                    retirement = 33
                    retirement_hours = 34
                    retirement_aircraft_hours = 36
                    retirement_comp_hours = 35
                    retirement_comp_attach_at = 37
                    retirement_current = 37

                    overhaul = 27
                    overhaul_hours = 28
                    overhaul_aircraft_hours = 30
                    overhaul_comp_hours = 29
                    overhaul_comp_attach_at = 31
                    overhaul_current = 32

                    inspection = 16
                    inspection_hours = 17
                    inspection_aircraft_hours = 19
                    inspection_comp_hours = 18
                    inspection_comp_attach_at = 20
                    inspection_current = 21

                    cycles_on = 7
                    cycles_type = 169
                    cycles_value = 8
                    cycles_current = 11
                    aircraft_cycles = 10
                    comp_cycles = 9
                    comp_cycles_attach_at = 11

                    month_on = 22
                    month_type = 24
                    month_value = 23
                    month_date = 25

                    days_on = 12
                    days_type = 14
                    days_value = 13
                    days_date = 15

                ro.pop(0)
                ro.sort(key=lambda elem: elem[rank])
                for g in ro:
                    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                    # IF COMPONENT ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                    if(str(g[rank][:1]) == 'M' or str(g[rank][:1]) == 'S'):
                        print str(g[part_name])
                        comptype = str(g[rank][:1])
                        if g[part_no].strip() == "":
                            product_id = self.env['product.product'].search([('name', '=', str(g[part_name]))],limit=1)
                        else:
                            product_id = self.env['product.product'].search([('default_code', '=', g[part_no])],limit=1)

                        if(product_id.id == False):
                            product_id = self.env['product.product'].create({
                                'qmap':False,
                                'is_part':True,
                                'name':str(g[part_name]),
                                'short_name':str(g[part_name]),
                                'default_code':str(g[part_no]),
                                'purchase_ok':True,
                                'categ_id':self.env.ref('ib_base_pelita.product_category_pas').id,
                                'type':'product',
                                'tracking':'none',
                                'invoice_policy':'order',
                                'purchase_method':'receive',
                            })
                            self.env.cr.commit()
                        else:
                            product_id.update({
                                'is_part':True,
                                'categ_id':self.env.ref('ib_base_pelita.product_category_pas').id,
                                })
                            self.env.cr.commit()

                        ata_id = self.env['ams.ata'].search([('name', '=', 'xx-xx-xx')])
                        if(g[ata_1] != '' or g[ata_2] != '' or g[ata_3] != ''):
                            ata_string = g[ata_1].zfill(2) + '-' + g[ata_2].zfill(2) + '-' + g[ata_3].zfill(2)
                            ata_id = self.env['ams.ata'].search([('name', '=', ata_string)])
                            if(ata_id.id == False):
                                ata_id = self.env['ams.ata'].create({
                                    'name' : ata_string,
                                    'chapter' : g[ata_1].zfill(2),
                                    'sub_chapter' : g[ata_2].zfill(2),
                                    'description' : 'ATA ' + ata_string,
                                    })
                                self.env.cr.commit()
                        if(g[serial] != ''):
                            serial_id = self.env['stock.production.lot'].search(['&',('product_id','=',product_id.id),('name','=',g[serial])])
                            if(serial_id.id == False):
                                serial_id = self.env['stock.production.lot'].create({
                                    'product_id':product_id.id,
                                    'name':g[serial],
                                })
                            self.env.cr.commit()
                            serial_number = serial_id.id
                        else:
                            serial_number = False

                        if(comptype == 'M'):
                            comp = self.env['ams.component.part'].search(['&',('serial_number','=',serial_number),'&',('fleet_id','=',acraft),('calm_id','=',g[rank])])
                        else:
                            comp = self.env['ams.component.part'].search(['&',('serial_number','=',serial_number),'&',('fleet_id','=',acraft),('calm_id','=',g[rank]+g[part_no])])
                        
                        if(comp.id == False):
                            if comptype != 'M':
                                get_calm_id = self.env['ams.component.part'].search(['&',('fleet_id','=',acraft),('calm_id','=',g[rank].replace('S','M'))])
                            comp = self.env['ams.component.part'].create({
                                'calm_file' : self.filename,
                                'calm_id' : g[rank] if comptype == 'M' else g[rank]+g[part_no],
                                'ata_code' : ata_id.id,
                                'is_subcomp' : True if comptype == 'S' else False,
                                'part_id' : False if comptype == 'M' else get_calm_id.id,
                                'fleet_id': False if comptype != 'M' else acraft,
                                'product_id':product_id.id,
                                'serial_number':serial_number,
                                'comp_timeinstallation' : 0,
                                'comp_cyclesinstallation' : 0,
                                'date_installed' : g[inst_date] if (g[inst_date] != '') else False,
                                'csn' : 0,
                                'tsn' : 0,
                                'is_overhaul' : False,
                                # 'unknown_new' : False,
                                'item' : g[item],
                            })
                            self.env.cr.commit()
                        else:
                            comp.update({
                                'product_id':product_id.id,
                                'serial_number':serial_number,
                                'date_installed' : g[inst_date] if (g[inst_date] != '') else False,
                            })

                        # SERVICE LIFE
                        # ON CONDITION
                        if(g[on_condition].upper() == 'TRUE'):
                            comp.update({
                                'tsn' : ((float(self.fleet_id.total_hours) - float(g[on_aircraft_hours])) + float(g[U2TT])),
                                # 'tso': (float(self.fleet_id.total_hours) - float(g[on_aircraft_hours])) + float(g[on_comp_hours]),
                                'comp_timeinstallation' : g[U2TT],
                                'ac_timeinstallation' : g[on_aircraft_hours],
                                'unknown_new' : False,
                            })

                            # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',g[calm_id]),('file','=',g[rank]),('fleet_id','=',self.fleet_id.id)])
                            # if calm_data.id == False:
                            # AIRFRAME ON-CONDITION ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                            # slive = self.env['ams.component.servicelife'].search(['&',('value','=',0),'&',('unit','=','hours'),'&',('part_id','=',comp.id),('action_type','=','oncondition')])
                            if(True):
                                slive = self.env['ams.component.servicelife'].create({
                                    'at_install' : float(g[U2TT]),
                                    'part_id' : comp.id,
                                    'action_type' : 'oncondition',
                                    'unit' : 'hours',
                                    'value' : 0,
                                    'current' : (float(self.fleet_id.total_hours) - float(g[on_aircraft_hours])) + float(g[U2TT]), 
                                    'comments' : g[comment],
                                })
                                self.env.cr.commit()
                                # self.env['calm.dict'].create({
                                #     'file' : g[rank],
                                #     'fleet_id' : self.fleet_id.id,
                                #     'part_id' : comp.id,
                                #     'sequence' : g[calm_id],
                                #     'service_life_id' : slive.id,
                                # })
                                # self.env.cr.commit()
                            else :
                                slive.write({
                                    'at_install' : float(g[U2TT]),
                                    'part_id' : comp.id,
                                    'action_type' : 'oncondition',
                                    'unit' : 'hours',
                                    'value' : 0,
                                    'current' : (float(self.fleet_id.total_hours) - float(g[on_aircraft_hours])) + float(g[U2TT]),
                                    'comments' : g[comment],    
                                })
                                self.env.cr.commit()
                        # RETIREMENT
                        if(g[retirement].upper() == 'TRUE'):
                            tsn = (float(self.fleet_id.total_hours) - float(g[retirement_aircraft_hours]) + float(g[retirement_comp_hours])) if comp.tsn < (float(self.fleet_id.total_hours) - float(g[retirement_aircraft_hours]) + float(g[retirement_comp_hours])) else comp.tsn
                            if(tsn > comp.tsn):
                                comp.update({
                                    # 'unknown_new' : False,
                                    'tsn': tsn,
                                    # 'tso': (float(self.fleet_id.total_hours) - float(g[retirement_aircraft_hours]) + float(g[retirement_comp_hours])),
                                    'comp_timeinstallation' : float(g[retirement_comp_hours]),
                                    'ac_timeinstallation' : float(g[retirement_aircraft_hours]),
                                })

                            # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',g[calm_id]),('file','=',g[rank]),('fleet_id','=',self.fleet_id.id)])
                            # if calm_data.id == False:
                            if(True):
                                slive = self.env['ams.component.servicelife'].create({
                                    'at_install' : float(g[retirement_comp_hours]),
                                    'part_id' : comp.id,
                                    'is_major' : True,
                                    'action_type' : 'retirement',
                                    'unit' : 'hours',
                                    'value' : float(g[retirement_hours]),
                                    'current' : (float(self.fleet_id.total_hours) - float(g[retirement_aircraft_hours])) + float(g[retirement_comp_hours]), 
                                    'comments' : g[comment],
                                })
                                # if len(g) > 165:
                                #     if(g[ste_retire] != '0' and g[ste_retire] != ''):
                                #         if (calm_data.service_life_id.id != False):
                                #             self.env['airworthy.ste'].create({
                                #                 'service_life_id' : calm_data.service_life_id.id,
                                #                 'value' : float(g[ste_retire])/float(100) * g[retirement_hours],
                                #                 'status' : 'dgcaapprove',
                                #                 })
                                self.env.cr.commit()
                                # self.env['calm.dict'].create({
                                #     'file' : g[rank],
                                #     'fleet_id' : self.fleet_id.id,
                                #     'part_id' : comp.id,
                                #     'sequence' : g[calm_id],
                                #     'service_life_id' : slive.id,
                                # })
                                # self.env.cr.commit()
                            else :
                                # slive = calm_data.service_life_id,
                                # slive.write({
                                #     'at_install' : float(g[retirement_comp_hours]),
                                #     'part_id' : comp.id,
                                #     'is_major' : True,
                                #     'action_type' : 'retirement',
                                #     'unit' : 'hours',
                                #     'value' : g[retirement_hours],
                                #     'current' : (float(self.fleet_id.total_hours) - float(g[retirement_comp_attach_at])) + float(g[retirement_comp_hours]),
                                #     'comments' : g[comment],    
                                # })
                                self.env.cr.commit()
                        # OVERHAUL
                        if(g[overhaul].upper() == 'TRUE'):
                            tsn = ((float(g[overhaul_comp_attach_at]) + float(g[overhaul_current]) + float(g[overhaul_comp_hours])) if float(comp.tsn) < float(float(g[overhaul_comp_attach_at]) + float(g[overhaul_current]) + float(g[overhaul_comp_hours])) else float(comp.tsn))
                            is_overhaul = (True if tsn > (float(self.fleet_id.total_hours) - float(g[overhaul_aircraft_hours]) + float(g[overhaul_comp_hours])) else False)
                            comp.update({
                                'unknown_new' : False,
                                'is_overhaul' : is_overhaul,
                                'tsn': tsn if (tsn > comp.tsn) else comp.tsn,
                                'tso': (float(self.fleet_id.total_hours) - float(g[overhaul_aircraft_hours]) + float(g[overhaul_comp_hours])),
                                'comp_timeinstallation' : float(g[overhaul_comp_hours]),
                                'ac_timeinstallation' : float(g[overhaul_aircraft_hours]),
                            })

                            # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',g[calm_id]),('file','=',g[rank]),('fleet_id','=',self.fleet_id.id)])
                            # if calm_data.id == False:
                            if(True):
                                slive = self.env['ams.component.servicelife'].create({
                                    'at_install' : float(g[overhaul_comp_hours]),
                                    'part_id' : comp.id,
                                    'is_major' : True,
                                    'action_type' : 'overhaul',
                                    'unit' : 'hours',
                                    'value' : float(g[overhaul_hours]),
                                    'overhaul_comp_attach_at' : float(g[overhaul_comp_attach_at]),
                                    'current' : (float(self.fleet_id.total_hours) - float(g[overhaul_aircraft_hours])) + float(g[overhaul_comp_hours]), 
                                    'comments' : g[comment],
                                })
                                # if len(g) > 165:
                                #     if(g[ste_overhaul] != '0' and g[ste_overhaul] != ''):
                                #         if (calm_data.service_life_id.id != False):
                                #             self.env['airworthy.ste'].create({
                                #                 'service_life_id' : calm_data.service_life_id.id,
                                #                 'value' : float(g[ste_overhaul])/float(100) * g[overhaul_hours],
                                #                 'status' : 'dgcaapprove',
                                #                 })
                                self.env.cr.commit()
                                # self.env['calm.dict'].create({
                                #     'file' : g[rank],
                                #     'fleet_id' : self.fleet_id.id,
                                #     'part_id' : comp.id,
                                #     'sequence' : g[calm_id],
                                #     'service_life_id' : slive.id,
                                # })
                                # self.env.cr.commit()
                            else :
                                # slive = calm_data.service_life_id,
                                # slive.write({
                                #     'at_install' : float(g[overhaul_comp_hours]),
                                #     'part_id' : comp.id,
                                #     'is_major' : True,
                                #     'action_type' : 'overhaul',
                                #     'unit' : 'hours',
                                #     'value' : g[overhaul_hours],
                                #     'current' : (float(self.fleet_id.total_hours) - float(g[overhaul_comp_attach_at])) + float(g[overhaul_comp_hours]),
                                #     'comments' : g[comment],    
                                # })
                                self.env.cr.commit()
                        # INSPECTION
                        if(g[inspection].upper() == 'TRUE'):
                            tsn = (float(self.fleet_id.total_hours) - float(g[inspection_aircraft_hours]) + float(g[inspection_comp_hours])) if comp.tsn < (float(self.fleet_id.total_hours) - float(g[inspection_aircraft_hours]) + float(g[inspection_comp_hours])) else comp.tsn
                            if(tsn > comp.tsn):
                                comp.update({
                                    # 'unknown_new' : False,
                                    'tsn': tsn,
                                    # 'tso': (float(self.fleet_id.total_hours) - float(g[inspection_aircraft_hours]) + float(g[inspection_comp_hours])),
                                    'comp_timeinstallation' : float(g[inspection_comp_hours]),
                                    'ac_timeinstallation' : float(g[inspection_aircraft_hours]),
                                })

                            # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',g[calm_id]),('file','=',g[rank]),('fleet_id','=',self.fleet_id.id)])
                            # if calm_data.id == False:
                            if(True):
                                slive = self.env['ams.component.servicelife'].create({
                                    'at_install' : float(g[inspection_comp_hours]),
                                    'part_id' : comp.id,
                                    'action_type' : 'inspection',
                                    'unit' : 'hours',
                                    'value' : float(g[inspection_hours]),
                                    'current' : (float(self.fleet_id.total_hours) - float(g[inspection_aircraft_hours])) + float(g[inspection_comp_hours]), 
                                    'comments' : g[comment],
                                })
                                # if len(g) > 165:
                                #     if(g[ste_hr] != '0' and g[ste_hr] != ''):
                                #         if (calm_data.service_life_id.id != False):
                                #             self.env['airworthy.ste'].create({
                                #                 'service_life_id' : calm_data.service_life_id.id,
                                #                 'value' : float(g[ste_hr])/float(100) * g[inspection_hours],
                                #                 'status' : 'dgcaapprove',
                                #                 })
                                self.env.cr.commit()
                                # self.env['calm.dict'].create({
                                #     'file' : g[rank],
                                #     'fleet_id' : self.fleet_id.id,
                                #     'part_id' : comp.id,
                                #     'sequence' : g[calm_id],
                                #     'service_life_id' : slive.id,
                                # })
                                # self.env.cr.commit()
                            else :
                                # slive = calm_data.service_life_id,
                                # slive.write({
                                #     'at_install' : float(g[inspection_comp_hours]),
                                #     'part_id' : comp.id,
                                #     'action_type' : 'inspection',
                                #     'unit' : 'hours',
                                #     'value' : g[inspection_hours],
                                #     'current' : (float(self.fleet_id.total_hours) - float(g[inspection_comp_attach_at])) + float(g[inspection_comp_hours]),
                                #     'comments' : g[comment],    
                                # })
                                self.env.cr.commit()

                        # CYCLES
                        if(g[cycles_on].upper() == 'TRUE'):
                            if(g[cycles_type] == '1'):
                                slive_type = 'retirement'
                            elif(g[cycles_type] == '2'):
                                slive_type = 'service'
                            elif(g[cycles_type] == '3'):
                                slive_type = 'inspection'
                            elif(g[cycles_type] == '4'):
                                slive_type = 'overhaul'

                            csn = (float(self.fleet_id.total_landings) - float(g[cycle_on_install]) + float(g[comp_cycles])) if comp.tsn < (float(self.fleet_id.total_landings) - float(g[cycle_on_install]) + float(g[comp_cycles])) else comp.csn
                            comp.update({
                                'unknown_new' : False,
                                'csn': (float(csn)),
                                'cso': (float(g[cso])),
                                'comp_cyclesinstallation' : float(g[comp_cycles]),
                                'ac_cyclesinstallation' : float(g[aircraft_cycles]),
                            })

                            # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',g[calm_id]),('file','=',g[rank]),('fleet_id','=',self.fleet_id.id)])
                            # if calm_data.id == False:
                            if(True):
                                print g[comp_cycles] , ' <=> CYCLES'
                                slive = self.env['ams.component.servicelife'].create({
                                    'at_install' : float(g[comp_cycles]),
                                    'part_id' : comp.id,
                                    'action_type' : slive_type,
                                    'unit' : 'cycles',
                                    'value' : float(g[cycles_value]),
                                    'current' : float(g[cycles_current]) + float(g[comp_cycles]),  
                                    'comments' : g[comment],
                                })
                                # if len(g) > 165:
                                #     if(g[ste_cy] != '0' and g[ste_cy] != ''):
                                #         if (calm_data.service_life_id.id != False):
                                #             self.env['airworthy.ste'].create({
                                #                 'service_life_id' : calm_data.service_life_id.id,
                                #                 'value' : float(g[ste_cy])/float(100) * g[cycles_value],
                                #                 'status' : 'dgcaapprove',
                                #                 })
                                self.env.cr.commit()
                                # self.env['calm.dict'].create({
                                #     'file' : g[rank],
                                #     'fleet_id' : self.fleet_id.id,
                                #     'part_id' : comp.id,
                                #     'sequence' : g[calm_id],
                                #     'service_life_id' : slive.id,
                                # })
                                # self.env.cr.commit()
                            else :
                                # slive = calm_data.service_life_id,
                                # print g[comp_cycles] , ' <=> CYCLES'
                                # slive.write({
                                #     'at_install' : float(g[comp_cycles]),
                                #     'part_id' : comp.id,
                                #     'action_type' : slive_type,
                                #     'unit' : 'cycles',
                                #     'value' : g[cycles_value],
                                #     'current' : float(g[cycles_current]) + float(g[comp_cycles]),
                                #     'comments' : g[comment],    
                                # })
                                self.env.cr.commit()
                        # MONTH
                        if(g[month_on].upper() == 'TRUE'):
                            if(g[month_type] == '1'):
                                slive_type = 'inspection'
                            elif(g[month_type] == '2'):
                                slive_type = 'overhaul'
                            elif(g[month_type] == '3'):
                                slive_type = 'retirement'
                            elif(g[month_type] == '4'):
                                slive_type = 'service'
                           
                            if g[month_date] != '':
                                d = str(g[month_date]).split('/')
                                if len(d) == 3:
                                    comp.update({
                                        # 'unknown_new' : False,
                                        'date_installed' : datetime.strptime(g[month_date], '%m/%d/%Y').strftime("%Y-%m-%d")
                                    })
                                else:
                                    comp.update({
                                        # 'unknown_new' : False,
                                        'date_installed' : datetime.strptime(g[month_date], '%Y-%m-%d').strftime("%Y-%m-%d")
                                    })

                            date_val = g[month_date]
                            if(date_val == ''):
                                date_val = g[inst_date]
                            if(date_val != ''):
                                # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',g[calm_id]),('file','=',g[rank]),('fleet_id','=',self.fleet_id.id)])
                                # if calm_data.id == False:
                                if(True):
                                    slive = self.env['ams.component.servicelife'].create({
                                        'part_id' : comp.id,
                                        'action_type' : slive_type,
                                        'unit' : 'month',
                                        'value' : float(g[month_value]),
                                        'current' : False,
                                        'current_date' : date_val, 
                                        'comments' : g[comment],
                                    })
                                    self.env.cr.commit()
                                    # self.env['calm.dict'].create({
                                    #     'file' : g[rank],
                                    #     'fleet_id' : self.fleet_id.id,
                                    #     'part_id' : comp.id,
                                    #     'sequence' : g[calm_id],
                                    #     'service_life_id' : slive.id,
                                    # })
                                    # self.env.cr.commit()
                                else :
                                    # slive = calm_data.service_life_id,
                                    # slive.write({
                                    #     'part_id' : comp.id,
                                    #     'action_type' : slive_type,
                                    #     'unit' : 'month',
                                    #     'value' : g[month_value],
                                    #     'current' : False,
                                    #     'current_date' : date_val,
                                    #     'comments' : g[comment],    
                                    # })
                                    self.env.cr.commit()
                        # DAYS
                        if(g[days_on].upper() == 'TRUE'):
                            if(g[days_type] == '1'):
                                slive_type = 'inspection'
                            elif(g[days_type] == '2'):
                                slive_type = 'overhaul'
                            elif(g[days_type] == '3'):
                                slive_type = 'retirement'
                            elif(g[days_type] == '4'):
                                slive_type = 'service'

                            if g[days_date] != '':
                                d = str(g[days_date]).split('/')
                                if len(d) == 3:
                                    comp.update({
                                        # 'unknown_new' : False,
                                        'date_installed' : datetime.strptime(g[days_date], '%m/%d/%Y').strftime("%Y-%m-%d")
                                    })
                                else:
                                    comp.update({
                                        # 'unknown_new' : False,
                                        'date_installed' : datetime.strptime(g[days_date], '%Y-%m-%d').strftime("%Y-%m-%d")
                                    })

                            date_val = g[days_date]
                            if(date_val == ''):
                                date_val = g[inst_date]
                            if(date_val != ''):
                                # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',g[calm_id]),('file','=',g[rank]),('fleet_id','=',self.fleet_id.id)])
                                # if calm_data.id == False:
                                if(True):
                                    slive = self.env['ams.component.servicelife'].create({
                                        'part_id' : comp.id,
                                        'action_type' : slive_type,
                                        'unit' : 'days',
                                        'value' : float(g[days_value]),
                                        'current' : False,
                                        'current_date' : date_val, 
                                        'comments' : g[comment],
                                    })
                                    self.env.cr.commit()
                                    # self.env['calm.dict'].create({
                                    #     'file' : g[rank],
                                    #     'fleet_id' : self.fleet_id.id,
                                    #     'part_id' : comp.id,
                                    #     'sequence' : g[calm_id],
                                    #     'service_life_id' : slive.id,
                                    # })
                                    # self.env.cr.commit()
                                else :
                                    # slive = calm_data.service_life_id,
                                    # slive.write({
                                    #     'part_id' : comp.id,
                                    #     'action_type' : slive_type,
                                    #     'unit' : 'days',
                                    #     'value' : g[days_value],
                                    #     'current' : False,
                                    #     'current_date' : date_val,
                                    #     'comments' : g[comment],    
                                    # })
                                    self.env.cr.commit()


                    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                    # IF INSPECTION :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                    else:
                        if len(g) > 155:
                            print 'inspection ::' + str(g[part_name]) + ' desc : ' + str(g[part_desc])+ ' last : ' + str(g[rhll])+ ' since : ' + str(g[since_time_insp])
                            if(str(g[delete]).upper() == 'FALSE' and g[rank] == ''):
                                # PERHITUNGAN
                                comp_tso = 0
                                comp_cso = 0
                                comp_tsn = 0
                                comp_csn = 0
                                slive_type = 'inspection'

                                ata_id = self.env['ams.ata'].search([('name', '=', 'xx-xx-xx')])
                                if(g[ata_1] != '' or g[ata_2] != '' or g[ata_3] != ''):
                                    ata_string = g[ata_1].zfill(2) + '-' + g[ata_2].zfill(2) + '-' + g[ata_3].zfill(2)
                                    ata_id = self.env['ams.ata'].search([('name', '=', ata_string)])
                                    if(ata_id.id == False):
                                        ata_id = self.env['ams.ata'].create({
                                            'name' : ata_string,
                                            'chapter' : g[ata_1].zfill(2),
                                            'sub_chapter' : g[ata_2].zfill(2),
                                            'description' : 'ATA ' + ata_string,
                                            })
                                        self.env.cr.commit()

                                insp = self.env['ams.inspection'].create({
                                    'fleet_id' : self.fleet_id.id,
                                    'inspection_type' : str(g[part_name]),
                                    'desc' : str(g[part_desc]),
                                    'ata_code' : ata_id.id,
                                    'one_time_insp' : False,
                                    'last_insp' : g[rhll],
                                    'since_insp' : g[since_time_insp],
                                    'install_at' : g[inst_date],
                                })
                                self.env.cr.commit()

                                # SERVICE LIFE
                                # INSPECTION
                                if(g[inspection].upper() == 'TRUE'):
                                    slive = self.env['ams.component.servicelife'].create({
                                        'inspection_id' : insp.id,
                                        'action_type' : 'inspection',
                                        'unit' : 'hours',
                                        'value' : float(g[inspection_hours]),
                                        'current' : float(self.fleet_id.total_hours) - float(g[rhll]), 
                                        'comments' : g[comment],
                                    })
                                    self.env.cr.commit()

                                # CYCLES
                                if(g[cycles_on].upper() == 'TRUE'):
                                    if(g[cycles_type] == '1'):
                                        slive_type = 'retirement'
                                    elif(g[cycles_type] == '2'):
                                        slive_type = 'service'
                                    elif(g[cycles_type] == '3'):
                                        slive_type = 'inspection'
                                    elif(g[cycles_type] == '4'):
                                        slive_type = 'overhaul'

                                    slive = self.env['ams.component.servicelife'].create({
                                        'inspection_id' : insp.id,
                                        'action_type' : slive_type,
                                        'unit' : 'cycles',
                                        'value' : float(g[cycles_value]),
                                        'current' : float(g[cycles_current]) + float(g[comp_cycles]), 
                                        'comments' : g[comment],
                                    })
                                    self.env.cr.commit()
                                # MONTH
                                if(g[month_on].upper() == 'TRUE'):
                                    if(g[month_type] == '1'):
                                        slive_type = 'inspection'
                                    elif(g[month_type] == '2'):
                                        slive_type = 'overhaul'
                                    elif(g[month_type] == '3'):
                                        slive_type = 'retirement'
                                    elif(g[month_type] == '4'):
                                        slive_type = 'service'

                                    date_val = g[month_date]
                                    if(date_val == ''):
                                        date_val = g[inst_date]
                                    if(date_val != ''):
                                        slive = self.env['ams.component.servicelife'].create({
                                            'inspection_id' : insp.id,
                                            'action_type' : slive_type,
                                            'unit' : 'month',
                                            'value' : float(g[month_value]),
                                            'current' : False,
                                            'current_date' : date_val, 
                                            'comments' : g[comment],
                                        })
                                        self.env.cr.commit()
                                # DAYS
                                if(g[days_on].upper() == 'TRUE'):
                                    if(g[days_type] == '1'):
                                        slive_type = 'inspection'
                                    elif(g[days_type] == '2'):
                                        slive_type = 'overhaul'
                                    elif(g[days_type] == '3'):
                                        slive_type = 'retirement'
                                    elif(g[days_type] == '4'):
                                        slive_type = 'service'

                                    date_val = g[days_date]
                                    if(date_val == ''):
                                        date_val = g[inst_date]
                                    if(date_val != ''):
                                        slive = self.env['ams.component.servicelife'].create({
                                            'inspection_id' : insp.id,
                                            'action_type' : slive_type,
                                            'unit' : 'days',
                                            'value' : float(g[days_value]),
                                            'current' : False,
                                            'current_date' : date_val, 
                                            'comments' : g[comment],
                                        })
                                        self.env.cr.commit()
