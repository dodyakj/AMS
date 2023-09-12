# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import math
from odoo import fields, models, api

class ComponentPart(models.Model):
    _name = 'ams.component.part'
    _description = 'component'

    # @api.model
    # def _getProductId(self):
    #     return [('product_id.id', '=', self.product_id.id)]

    calm_file = fields.Char()
    calm_id = fields.Char()
    name = fields.Char(related='product_id.name')
    is_subcomp = fields.Boolean(string='Is Sub Component', default=lambda self:self.env.context.get('subcomponent',False)) 
    is_bel = fields.Boolean(string='Is Basic Equipment List', default=lambda self:self.env.context.get('belcomponent',False))
    
    no_component = fields.Boolean(string='No Component Installed', default=False)


    fleet_id = fields.Many2one('aircraft.acquisition', string='Fleet Id')
    engine_id = fields.Many2one('engine.type', string='Engine Id')
    auxiliary_id = fields.Many2one('auxiliary.type', string='Auxiliary Id')
    propeller_id = fields.Many2one('propeller.type', string='Propeller Id')
    part_id = fields.Many2one('ams.component.part', string='Part Id')
    
    product_id = fields.Many2one('product.product', string='Component Name', required=True)
    serial_number = fields.Many2one('stock.production.lot', string='Serial Number')
    serial_number_text = fields.Char(string='Serial Number')
    document_ids = fields.Many2many('stock.production.lot_document',string='Document', compute='get_document')

    date_installed = fields.Date(string='Date Installed', default=fields.Date.today())
    part_number = fields.Char(related='product_id.default_code', string="Part Number")
    part_name = fields.Char(related='product_id.name', string="Part Name")
    ata_code = fields.Many2one('ams.ata',string="Ata Code")
    ata_text = fields.Char(related='ata_code.name',string="ATA",readonly=True)
    item = fields.Char(string='Item')

    csn = fields.Float('Cycles Since New')
    cso = fields.Float('Cycles Since Overhaul')
    tsn = fields.Float('Time Since New')
    tso = fields.Float('Time Since Overhaul')
    rsn = fields.Float('RIN Since New')
    rso = fields.Float('RIN Since Overhaul')

    ac_timeinstallation = fields.Float('A/C Hours at Installation')
    ac_cyclesinstallation = fields.Float('A/C Cycles at Installation')
    ac_rininstallation = fields.Float(string='A/C RIN at Installation')
    comp_timeinstallation = fields.Float('Component Hours at Installation')
    comp_cyclesinstallation = fields.Float('Component Cycles at Installation')
    comp_rininstallation = fields.Float(string='Component RIN at Installation')

    not_follow_parent = fields.Boolean('Not Follow Parent Hours and Cycles', default=False)
    is_overhaul = fields.Boolean('Has been Overhaul', default=False)
    date_overhaul = fields.Date(string='Overhaul Date', default=False)
    unknown_new = fields.Boolean('Unknown TSN / CSN', default=False)

    # inspection_number = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4')], string='Number of Inspection', default="1")

    serfice_life = fields.One2many('ams.component.servicelife','part_id',string='Service Life')

    have_cycles = fields.Boolean(string='Have Cycles in Service Life', compute='_have_cycles')
    have_hours = fields.Boolean(string='Have Hours in Service Life', compute='_have_hours')
    have_rins = fields.Boolean(string='Have Rins in Service Life', compute='_have_rins')
    have_overhaul = fields.Boolean(string='Have Overhaul in Service Life', compute='_have_overhaul')
    have_inspection = fields.Boolean(string='Have Inspection in Service Life', compute='_have_inspection')
    have_service = fields.Boolean(string='Have Service in Service Life', compute='_have_service')

    show_tsn = fields.Boolean(string='Show tsn', compute='_show_param')
    show_csn = fields.Boolean(string='Show csn', compute='_show_param')
    show_tso = fields.Boolean(string='Show tso', compute='_show_param')
    show_cso = fields.Boolean(string='Show cso', compute='_show_param')
    # cycles_on = fields.Boolean('Cycles')
    # inspection_on = fields.Boolean('Inspection')
    # overhaul_on = fields.Boolean('Overhaul')
    # retirement_on = fields.Boolean('Retirement')
    # on_condition_on = fields.Boolean('On Condition')
    # condition_monitored_on = fields.Boolean('Condition Monitored')

    # year_on = fields.Boolean(string='year')
    # months_on = fields.Boolean(string='months')
    # days_on = fields.Boolean(string='days')
    # rin_on = fields.Boolean(string='rin')
    
    # cycles = fields.Float('Cycles')
    # overhaul = fields.Float('Overhaul')
    # retirement = fields.Float('Retirement')
    # on_condition = fields.Float('On Condition',readonly=True,related='tsn')
    # condition_monitored = fields.Float('Condition Monitored',readonly=True,related='tsn')

    # year = fields.Integer(string='year')
    # months = fields.Integer(string='months')
    # days = fields.Integer(string='days')
    # rin = fields.Integer(string='rin')

    # cycles_remaining = fields.Float('Cycles', readonly=True)
    # overhaul_remaining = fields.Float('Overhaul', readonly=True)
    # retirement_remaining = fields.Float('Retirement', readonly=True)
    # on_condition_remaining = fields.Float('On Condition', readonly=True)
    # condition_monitored_remaining = fields.Float('Condition Monitored', readonly=True)

    # year_remaining = fields.Integer(string='year',readonly=True)
    # months_remaining = fields.Integer(string='months',readonly=True)
    # days_remaining = fields.Integer(string='days',readonly=True)
    # rin_remaining = fields.Integer(string='rin',readonly=True)

    # cycles_total = fields.Float('Cycles', readonly=True)
    # overhaul_total = fields.Float('Overhaul', readonly=True)
    # retirement_total = fields.Float('Retirement', readonly=True)
    # on_condition_total = fields.Float('On Condition', readonly=True)
    # condition_monitored_total = fields.Float('Condition Monitored', readonly=True)

    # inspection = fields.Float('Inspection')
    # inspection_remaining = fields.Float('Inspection', readonly=True)
    # inspection_total = fields.Float('Inspection', readonly=True)

    # inspection2 = fields.Float('Inspection #2')
    # inspection2_remaining = fields.Float('Inspection #2', readonly=True)
    # inspection2_total = fields.Float('Inspection #2', readonly=True)

    # inspection3 = fields.Float('Inspection #3')
    # inspection3_remaining = fields.Float('Inspection #3', readonly=True)
    # inspection3_total = fields.Float('Inspection #3', readonly=True)

    # inspection4 = fields.Float('Inspection #4')
    # inspection4_remaining = fields.Float('Inspection #4', readonly=True)
    # inspection4_total = fields.Float('Inspection #4', readonly=True)


    # year_total = fields.Integer(string='year',readonly=True)
    # months_total = fields.Integer(string='months',readonly=True)
    # days_total = fields.Integer(string='days',readonly=True)
    # rin_total = fields.Integer(string='rin',readonly=True)

    merge_mp = fields.Boolean('Major (Show MP)')

    sub_part_ids = fields.One2many('ams.component.part','part_id',string='Sub Components', copy=True)

    some_count = fields.Char(string='',readonly=True)

    # @api.model
    # def return_action_replace(self):
    #     return True

    @api.one
    @api.depends('serfice_life')
    def _show_param(self):
        for rule in self:
            ro = rule.serfice_life
            for g in ro:
                if(g.unit == 'cycles'):
                    rule.show_csn = True
                    if(g.action_type == 'overhaul'):
                        rule.show_cso = True
                if(g.unit == 'hours'):
                    rule.show_tsn = True
                    if(g.action_type == 'overhaul'):
                        rule.show_tso = True            

    @api.one
    @api.depends('serfice_life')
    def _have_cycles(self):
        for rule in self:
            ro = rule.serfice_life
            ret = False
            for g in ro:
                if(g.unit == 'cycles'):
                    ret = True
            rule.have_cycles = ret

    @api.one
    @api.depends('serfice_life')
    def _have_hours(self):
        for rule in self:
            ro = rule.serfice_life
            ret = False
            for g in ro:
                if(g.unit == 'hours'):
                    ret = True
            rule.have_hours = ret

    @api.one
    @api.depends('serfice_life')
    def _have_rins(self):
        for rule in self:
            ro = rule.serfice_life
            ret = False
            for g in ro:
                if(g.unit == 'rin'):
                    ret = True
            rule.have_rins = ret

    @api.one
    @api.depends('serfice_life')
    def _have_overhaul(self):
        for rule in self:
            ro = rule.serfice_life
            ret = False
            for g in ro:
                if(g.action_type == 'overhaul'):
                    ret = True
            rule.have_overhaul = ret

    @api.one
    @api.depends('serial_number')
    def get_document(self):
        ids = []
        docs = self.env['stock.production.lot_document'].search([('lot_id','=',self.serial_number.id)])
        for x in docs:
            ids.append(x.id)
        self.document_ids = ids

    @api.one
    @api.depends('serfice_life')
    def _have_inspection(self):
        for rule in self:
            ro = rule.serfice_life
            ret = False
            for g in ro:
                if(g.action_type == 'inspection'):
                    ret = True
            rule.have_inspection = ret

    @api.one
    @api.depends('serfice_life')
    def _have_service(self):
        for rule in self:
            ro = rule.serfice_life
            ret = False
            for g in ro:
                if(g.action_type == 'service'):
                    ret = True
            rule.have_service = ret

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
            'context': "{'part_id':" + str(self.id) + "}",
        }

    @api.multi
    def do_service(self):
        return {
            'name': 'Service',
            'type': 'ir.actions.act_window',
            'res_model': 'airworthy.service',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': False,
            'views': [(False, 'form')],
            'target': 'new',
            'context': "{'part_id':" + str(self.id) + "}",
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
            'context': "{'part_id':" + str(self.id) + "}",
        }

    @api.multi
    def return_action_upload(self):
        return {
            'name': 'Upload',
            'type': 'ir.actions.act_window',
            'res_model': 'stock.production.lot_document',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': False,
            'views': [(False, 'form')],
            'target': 'new',
            'context': "{'serial_id':" + str(self.serial_number.id) + "}",
        }

    @api.multi
    def name_get(self):
        return [(record.id, '['+str(record.part_number)+'] '+str(record.product_id.name)+' '+str('' if (record.serial_number.name==False) else record.serial_number.name)) for record in self]

    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if(self.is_subcomp == True):
            fleet = self.part_id.fleet_id
        else:
            fleet = self.fleet_id
        self.ac_timeinstallation = fleet.total_hours
        self.ac_cyclesinstallation = fleet.total_landings
        list_serial = []
        serial_installed = self.env['ams.component.part'].search([('product_id','=',self.product_id.id)])
        for x in serial_installed:
            if(x.serial_number != False):
                list_serial.append(x.serial_number.id)
        return {'domain':{'serial_number':['&',('product_id','=',self.product_id.id),('id','not in',list_serial)]}}

    @api.onchange('serial_number')
    def _onchange_serial_number(self):
        sn_search = self.env['stock.production.lot'].search([('id','=',self.serial_number.id)])
        self.comp_timeinstallation = sn_search.tso
        self.comp_cyclesinstallation = sn_search.cso
        self.csn = sn_search.csn
        self.tsn = sn_search.tsn
        self.is_overhaul = sn_search.is_overhaul
        self.unknown_new = sn_search.unknown_new
            

    # PADA SAAT SAVE
    @api.model
    def create(self, vals):
        if(vals['serial_number']):
            vals['tso'] = vals['comp_timeinstallation']
            vals['cso'] = vals['comp_cyclesinstallation']
            self.env['stock.production.lot'].search([('id','=',vals['serial_number'])]).write({
                'csn' : vals['csn'],
                'tsn' : vals['tsn'],
                'tso' : vals['comp_timeinstallation'],
                'cso' : vals['comp_cyclesinstallation'],
                'is_overhaul' : vals['is_overhaul'],
                # 'unknown_new' : vals['unknown_new'],
            })
        create = super(ComponentPart, self).create(vals)
        return create
    
    @api.model
    def write(self, vals):
        if 'tsn' in vals:
            if(vals['tsn'] != self.tsn):
                ro = self.serfice_life
                for g in ro:
                    if(g.unit == 'hours' and g.action_type != 'overhaul'):
                        g.current = g.current + (vals['tsn'] - self.tsn)
                        g.remaining = g.remaining - (vals['tsn'] - self.tsn)
        if 'tso' in vals:
            if(vals['tso'] != self.tso):
                ro = self.serfice_life
                for g in ro:
                    if(g.unit == 'hours' and g.action_type == 'overhaul'):
                        g.current = g.current + (vals['tso'] - self.tso)
                        g.remaining = g.remaining - (vals['tso'] - self.tso)
        if 'csn' in vals:
            if(vals['csn'] != self.csn):
                ro = self.serfice_life
                for g in ro:
                    if(g.unit == 'cycles' and g.action_type != 'overhaul'):
                        g.current = g.current + (vals['csn'] - self.csn)
                        g.remaining = g.remaining - (vals['csn'] - self.csn)
        if 'cso' in vals:
            if(vals['cso'] != self.cso):
                ro = self.serfice_life
                for g in ro:
                    if(g.unit == 'cycles' and g.action_type == 'overhaul'):
                        g.current = g.current + (vals['cso'] - self.cso)
                        g.remaining = g.remaining - (vals['cso'] - self.cso)

        write = super(ComponentPart, self).write(vals)
        return write

class ComponentOverride(models.Model):
    _name = "ams.component.override"
    _description = "Component Value Override"

    component = fields.Many2one('ams.component.part', string='Component', default=lambda self:self.env.context.get('default_config_id',False), readonly=True)
    current_serial = fields.Many2one('stock.production.lot', string='Current Serial Number', related="component.serial_number",readonly=True)
    rin_enable = fields.Boolean(string='RIN Enable', default=False)

    comp_timeinstallation = fields.Float('Current Hours', related='component.tso', readonly=True)
    comp_cyclesinstallation = fields.Float('Current Cycles', related='component.cso', readonly=True)
    comp_rininstallation = fields.Float('Current RIN', related='component.rso', readonly=True)

    timeinstallation = fields.Float('Component Hours',default= lambda self: self.env['ams.component.part'].search([('id','=',self.env.context.get('default_config_id',False))]).tso)
    cyclesinstallation = fields.Float('Component Cycles',default= lambda self: self.env['ams.component.part'].search([('id','=',self.env.context.get('default_config_id',False))]).cso)
    rininstallation = fields.Float('Component RIN',default= lambda self: self.env['ams.component.part'].search([('id','=',self.env.context.get('default_config_id',False))]).rso)


    def override(self):
        addition_hours = self.timeinstallation - self.component.tso
        addition_cycles = self.cyclesinstallation - self.component.cso
        addition_rins = self.rininstallation - self.component.rso
        self.env['ams.manual_changes'].create({
            'part_id' : self.component.id,
            'current_hours' : self.comp_timeinstallation,
            'current_cycles' : self.comp_cyclesinstallation,
            'current_rin' : self.comp_rininstallation,
            'hours' : self.timeinstallation,
            'cycles' : self.cyclesinstallation,
            'rin' : self.rininstallation,
            })
        self.component.write({
            'tsn' : self.component.tsn + addition_hours,
            'tso' : self.component.tso + addition_hours,
            'csn' : self.component.csn + addition_cycles,
            'cso' : self.component.cso + addition_cycles,
            'rsn' : self.component.rsn + addition_rins,
            'rso' : self.component.rso + addition_rins,
            })

class ComponentReplacement(models.Model):
    _name = "ams.component.replace"
    _description = "Component Replacement"

    no_component = fields.Boolean(string='Only Remove this Component', default=False)
    component = fields.Many2one('ams.component.part', string='Component', default=lambda self:self.env.context.get('default_config_id',False), readonly=True)
    show_tsn = fields.Boolean(string='Show tsn', related='component.show_tsn')
    show_csn = fields.Boolean(string='Show csn', related='component.show_csn')
    show_tso = fields.Boolean(string='Show tso', related='component.show_tso')
    show_cso = fields.Boolean(string='Show cso', related='component.show_cso')

    current_serial = fields.Many2one('stock.production.lot', string='Serial Number OFF', related="component.serial_number",readonly=True)
    sn_us = fields.Boolean(string='This Component is unserviceable', default=False)

    product_id = fields.Many2one('product.product', string='Component Name', required=True)
    serial_number = fields.Many2one('stock.production.lot', string='Serial Number ON')
    date_installed = fields.Date(string='Date Installed', default=fields.Date.today(),required=True)
    
    rin_enable = fields.Boolean(string='RIN Enable', default=False)

    ac_timeinstallation = fields.Float('A/C Hours at Installation', default=lambda self:self._get_vals()['total_hours'])
    ac_cyclesinstallation = fields.Float('A/C Cycles at Installation', default=lambda self:self._get_vals()['total_landings'])
    ac_rininstallation = fields.Float('A/C RIN at Installation', default=lambda self:self._get_vals()['total_rins'])
    comp_timeinstallation = fields.Float('Component TSO')
    comp_cyclesinstallation = fields.Float('Component CSO')
    comp_rininstallation = fields.Float('Component RIN')

    csn = fields.Float('Component CSN')
    tsn = fields.Float('Component TSN')

    unknown_new = fields.Boolean('Unknown TSN / CSN', default=False)
    premature = fields.Boolean('Premature Replacement', default=False)
    is_overhaul = fields.Boolean('Has been Overhaul', default=False)
    reason = fields.Text(string='Reason')

    warehouse_id = fields.Many2one('ams.bin', string='Warehouse Location')

    component_of = fields.Selection([('airframe','Aircraft'),('engine','Engine'),('auxiliary','Auxiliary'),('propeller','Propeller')],string='Component of',default=lambda self:self._get_component_of())
    current_hours = fields.Float(string='Current Hours', default=lambda self:self._get_vals()['total_hours'], readonly=True)
    current_cycles = fields.Float(string='Current Cycles', default=lambda self:self._get_vals()['total_landings'], readonly=True)
    current_rins = fields.Integer(string='Current RIN', default=lambda self:self._get_vals()['total_rins'], readonly=True)    

    @api.model
    def _get_component_of(self):
        part_id = self.env['ams.component.part'].search([('id','=',self.env.context.get('default_config_id',False))],limit=1)
        if(part_id.part_id.id != False):
            part_id = part_id.part_id
        if(part_id.fleet_id.id != False):
            return 'airframe'
        elif(part_id.propeller_id.id != False):
            return 'propeller'
        elif(part_id.engine_id.id != False):
            return 'engine'
        elif(part_id.auxiliary_id.id != False):
            return 'auxiliary'

    def _get_vals(self):    
        fleet = self._get_fleet()
        if(self.env.context.get('default_config_id',False) != False):
            part_id = self.env['ams.component.part'].search([('id','=',self.env.context.get('default_config_id',False))],limit=1)
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
        if(self.env.context.get('default_config_id',False) != False):
            part_id = self.env['ams.component.part'].search([('id','=',self.env.context.get('default_config_id',False))],limit=1)
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

    @api.onchange('serial_number')
    def _onchange_serial_number(self):
        sn_search = self.env['stock.production.lot'].search([('id','=',self.serial_number.id)])
        self.comp_timeinstallation = sn_search.tso
        self.comp_cyclesinstallation = sn_search.cso
        self.csn = sn_search.csn
        self.tsn = sn_search.tsn
        self.is_overhaul = sn_search.is_overhaul
        # self.unknown_new = sn_search.unknown_new

    # @api.onchange('component')
    # def _onchange_component(self):
    #     if(self.component.is_subcomp == True):
    #         fleet = self.component.part_id.fleet_id
    #     else:
    #         fleet = self.component.fleet_id
    #     self.product_id = self.component.product_id.id
    #     self.ac_timeinstallation = self._get_vals()['total_hours']
    #     self.ac_cyclesinstallation = self._get_vals()['total_landings']
    #     self.ac_rininstallation = self._get_vals()['total_rins']
    #     self.rin_enable = False
    #     for g in self.component.serfice_life:
    #         if(g.unit == 'rin'):
    #             self.rin_enable = True
            
    @api.onchange('product_id')
    def _onchange_product_id(self):
        forbid = []
        ro = self.env['ams.component.part'].search([('product_id','=',self.product_id.id)])
        for record in ro:
            forbid.append(record.serial_number.id)
        return {'domain':{'serial_number':['&',('product_id','=',self.product_id.id),('id','not in',forbid)]}}

    # def replace(self):
    #     # PENGURANGAN COMPONENT
    #     if(self.no_component == False):
    #         stock_by_ref = self.env['ams.stock'].search([('product_id','=',self.product_id.id),('bin_id','=',self.warehouse_id.id)])
    #         stock_by_ref.write({
    #             'stock_on_hand' : stock_by_ref.stock_on_hand - 1,
    #             'stock_scrap' : stock_by_ref.stock_scrap + 1,
    #             })
    #     self.component.no_component = self.no_component

    #     if(self.component.is_subcomp == True):
    #         fleet = self.component.part_id.fleet_id
    #         engine = self.component.part_id.engine_id
    #         auxiliary = self.component.part_id.auxiliary_id
    #         propeller = self.component.part_id.propeller_id
    #     else:
    #         fleet = self.component.fleet_id
    #         engine = self.component.engine_id
    #         auxiliary = self.component.auxiliary_id
    #         propeller = self.component.propeller_id

    #     if (fleet.id == False):
    #         if (engine):
    #             fleet = self.env['aircraft.acquisition'].search(['|','|','|',('engine_type_id.id','=',engine.id),('engine2_type_id.id','=',engine.id),('engine3_type_id.id','=',engine.id),('engine4_type_id.id','=',engine.id)], limit=1)
    #         elif (auxiliary):
    #             fleet = self.env['aircraft.acquisition'].search([('auxiliary_type_id.id','=',auxiliary.id)], limit=1)
    #         elif (propeller):
    #             fleet = self.env['aircraft.acquisition'].search(['|','|','|',('propeller_type_id.id','=',propeller.id),('propeller2_type_id.id','=',propeller.id),('propeller3_type_id.id','=',propeller.id),('propeller4_type_id.id','=',propeller.id)], limit=1)

    #     recomp_min_hours = self._get_vals()['total_hours'] - self.ac_timeinstallation
    #     recomp_min_cycles = self._get_vals()['total_landings'] - self.ac_cyclesinstallation
    #     recomp_min_rins = self._get_vals()['total_rins'] - self.ac_rininstallation

    #     newcomp_plus_hours = self._get_vals()['total_hours'] - self.ac_timeinstallation
    #     newcomp_plus_cycles = self._get_vals()['total_landings'] - self.ac_cyclesinstallation
    #     newcomp_plus_rins = self._get_vals()['total_rins'] - self.ac_rininstallation

    #     # cek recent component by serial
    #     if(self.current_serial):
    #         self.env['stock.production.lot'].search([('id','=',self.current_serial.id)]).write({
    #             'csn' : self.component.csn - recomp_min_cycles,
    #             'tsn' : self.component.tsn - recomp_min_hours,
    #             'tso' : self.component.tso - recomp_min_hours,
    #             'cso' : self.component.cso - recomp_min_cycles,
    #         })

    #     # cek new component by serial
    #     if(self.serial_number):
    #         self.env['stock.production.lot'].search([('id','=',self.serial_number.id)]).write({
    #             'csn' : self.component.csn + newcomp_plus_cycles,
    #             'tsn' : self.component.tsn + newcomp_plus_hours,
    #             'tso' : self.component.tso + newcomp_plus_hours,
    #             'cso' : self.component.cso + newcomp_plus_cycles,
    #         })
    #     # pengurangan dan penambahan hours cycles component sesuai dengan pemasangan
    #     comp = self.env['ams.component.part'].search([('id','=',self.component.id)])
    #     comp.write({
    #         'product_id' : self.product_id.id,
    #         'serial_number' : self.serial_number.id,
    #         'date_installed' : self.date_installed,
    #         'csn' : self.csn + newcomp_plus_cycles,
    #         'cso' : self.comp_timeinstallation + newcomp_plus_cycles,
    #         'tsn' : self.tsn + newcomp_plus_hours,
    #         'tso' : self.comp_cyclesinstallation + newcomp_plus_hours,
    #         'ac_timeinstallation' : self.ac_timeinstallation,
    #         'ac_cyclesinstallation' : self.ac_cyclesinstallation,
    #         'ac_rininstallation' : self.ac_rininstallation,
    #         'comp_timeinstallation' : self.comp_timeinstallation + newcomp_plus_hours,
    #         'comp_cyclesinstallation' : self.comp_cyclesinstallation + newcomp_plus_cycles,
    #         'comp_rininstallation' : self.comp_rininstallation + newcomp_plus_rins,
    #         'is_overhaul' : self.is_overhaul,
    #         'unknown_new' : self.unknown_new,
    #         })
    #     if(self.no_component):
    #         # add history
    #         hist = self.env['ams.component_history'].create({
    #             'fleet_id' : fleet.id,
    #             'engine_id' : engine.id,
    #             'auxiliary_id' : auxiliary.id,
    #             'propeller_id' : propeller.id,
    #             'part_id' : self.component.id,
    #             'component_id' : self.product_id.id,
    #             'component_replacement_id' : False,
    #             'serial_id' : self.current_serial.id,
    #             'serial_replacement_id' : False,
    #             'ac_hours' : self.ac_timeinstallation,
    #             'ac_cycles' : self.ac_cyclesinstallation,
    #             'hours' : self.comp_timeinstallation + newcomp_plus_hours,
    #             'cycles' : self.comp_cyclesinstallation + newcomp_plus_cycles,
    #             'type' : 'detach',
    #             'reason' : self.reason,
    #             'premature_removal' : self.premature,
    #             'date' : False,
    #             })
    #     else:
    #         # add history
    #         hist = self.env['ams.component_history'].create({
    #             'fleet_id' : fleet.id,
    #             'engine_id' : engine.id,
    #             'auxiliary_id' : auxiliary.id,
    #             'propeller_id' : propeller.id,
    #             'part_id' : self.component.id,
    #             'component_id' : self.product_id.id,
    #             'component_replacement_id' : self.component.product_id.id,
    #             'serial_id' : self.current_serial.id,
    #             'serial_replacement_id' : self.serial_number.id,
    #             'ac_hours' : self.ac_timeinstallation,
    #             'ac_cycles' : self.ac_cyclesinstallation,
    #             'hours' : self.comp_timeinstallation + newcomp_plus_hours,
    #             'cycles' : self.comp_cyclesinstallation + newcomp_plus_cycles,
    #             'type' : 'replace',
    #             'reason' : self.reason,
    #             'premature_removal' : self.premature,
    #             'date' : self.date_installed,
    #             })
    #     # reset perlakuan servicelife
    #     normal_treat = ['hours','cycles','rin']

    #     for slive in self.component.serfice_life:
    #         cvalue = slive.value
    #         pvalue = 0
    #         if(slive.unit == 'hours'):
    #             cvalue = cvalue + newcomp_plus_hours
    #             plavue = newcomp_plus_hours
    #         elif(slive.unit == 'cycles'):
    #             cvalue = cvalue + newcomp_plus_cycles
    #             plavue = newcomp_plus_cycles
    #         elif(slive.unit == 'rin'):
    #             cvalue = cvalue + newcomp_plus_rins
    #             plavue = newcomp_plus_rins

    #         if(slive.unit in normal_treat):
    #             slive.write({
    #                 'extension' : 0,
    #                 'current' : plavue,
    #                 'remaining' : cvalue,
    #                 'current_date' : False,
    #                 'next_date' : False,
    #                 'current_text' : plavue,
    #                 'next_text' : cvalue,
    #             })
    #         else:
    #             if slive.unit == 'year':
    #                 dateDue = datetime.strptime(self.date_installed, '%Y-%m-%d') + relativedelta(years=int(math.floor(cvalue)))
    #             if slive.unit == 'month':
    #                 dateDue = datetime.strptime(self.date_installed, '%Y-%m-%d') + relativedelta(months=int(math.floor(cvalue)))
    #             if slive.unit == 'days':
    #                 dateDue = datetime.strptime(self.date_installed, '%Y-%m-%d') + relativedelta(days=int(math.floor(cvalue)))
    #             dateDue = dateDue.strftime("%Y-%m-%d")

    #             slive.write({
    #                 'extension' : 0,
    #                 'current' : plavue,
    #                 'remaining' : cvalue,
    #                 'current_date' : self.date_installed,
    #                 'next_date' : dateDue,
    #                 'current_text' : self.date_installed,
    #                 'next_text' : dateDue,
    #             })

    #     # change A/C status
    #     if engine.id != False:
    #         engine.check_serviceable()
    #         acraft = self.env['aircraft.acquisition'].search(['|','|','|',('engine_type_id.id','=',engine.id),('engine2_type_id.id','=',engine.id),('engine3_type_id.id','=',engine.id),('engine4_type_id.id','=',engine.id)])
    #         for g in acraft:
    #             g.check_serviceable()
    #     if propeller.id != False:
    #         propeller.check_serviceable()
            
    #     if auxiliary.id != False:
    #         auxiliary.check_serviceable()
            
    #     fleet.check_serviceable()
    #     return True