# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api

class AircraftAircraftPropeller(models.Model):
    _name = 'propeller.propeller'
    
    name = fields.Char(string="Name", required=True)

class PropellerType(models.Model):
    _inherit = 'propeller.type'

    name = fields.Char( string='Propeller Name', required=True)
    
    propeller_model = fields.Many2one('propeller.propeller', string='Propeller Model')
    serial_number = fields.Char( string='Serial Number')
    document_ids = fields.One2many('document.certificate','propeller_id', string="Document Certificate", copy=True)
    bel_view = fields.Boolean(string='Is Bel',default=lambda self:self.env.context.get('belcomponent',False),readonly=True,store=False)
    propeller_lastoh = fields.Date(string='Last Overhaul')
    aircraft_status = fields.Boolean(string='Propeller Status',default=True)
    fleet_id = fields.Many2one('aircraft.acquisition', string='Fleet Id')
    propeller_tsn = fields.Float(string='TSN')
    propeller_tso = fields.Float(string='TSO')
    propeller_csn = fields.Float(string='CSN')
    propeller_cso = fields.Float(string='CSO')
    propeller_rsn = fields.Float(string='RIN Since New')
    propeller_rso = fields.Float(string='RIN Since Overhaul')
    total_hours = fields.Float(string='Hours', required=True, default=0)
    total_cycles = fields.Float(string='Cycles', required=True, default=0)
    total_rins = fields.Integer(string='Total Rins')
    special_ratio_counting = fields.Boolean(string='Special ratio Counting')
    component_ids = fields.One2many('ams.component.part','propeller_id',string='Component', copy=True)
    inspection_ids = fields.One2many('ams.inspection','propeller_id',string='Inspection', copy=True)
    history_line = fields.One2many('ams.component_history','propeller_id',string='History', copy=True)

    is_deleted = fields.Boolean(default=False)

    some_count = fields.Integer(string='Total',default=3)
    @api.multi
    def return_action_to_open(self):
        return False

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
            'context': "{'propeller_id':" + str(self.id) + "}",
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
            'context': "{'propeller_id':" + str(self.id) + "}",
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
            'context': "{'propeller_id':" + str(self.id) + "}",
        }

    @api.multi
    def write(self, vals):
        if('total_hours' in vals or 'total_cycles' in vals or 'total_rins' in vals):
            if(self.env.context.get('manual_edit',False) == True) :
                self.env['ams.manual_changes'].create({
                    # 'auxiliary_id' : self.id,
                    'current_hours' : self.total_hours if ('total_hours' in vals) else False,
                    'current_cycles' : self.total_cycles if ('total_cycles' in vals) else False,
                    'current_rin' : self.total_rins if ('total_rins' in vals) else False,
                    'hours' : vals['total_hours'] if ('total_hours' in vals) else False,
                    'cycles' : vals['total_cycles'] if ('total_cycles' in vals) else False,
                    'rin' : vals['total_rins'] if ('total_rins' in vals) else False,
                    })
        write = super(PropellerType, self).write(vals)
        return write

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

    @api.model
    def check_serviceable(self):
        servicable = True
        # check every part is available
        # A/C Comp
        for prop_comp in self.component_ids:
            if (prop_comp.no_component == True):
                servicable = False
            for ac_subcomp in prop_comp.sub_part_ids:
                if (ac_subcomp.no_component == True):
                    servicable = False
        self.aircraft_status = servicable
        return servicable

class PropellerSpare(models.Model):
    _name = 'propeller.spare'

    name = fields.Many2one('propeller.type','Propeller Spare')
    acquisition_id = fields.Many2one('engine.type',string ='Propeller Spare for')
    description = fields.Text('Description')
    date_pemasangan = fields.Date('Tanggal Pemasangan')
    date_penurunan = fields.Date('Tanggal Penurunan')
    propeller_type_id = fields.Many2one('propeller.type','Propeller Type')
    esn = fields.Char(string='ESN')
    rgb = fields.Char(string='RGB S/N')
    propeller = fields.Char(string='Propeller S/N')
    propeller_tsn = fields.Char(string='TSN')
    propeller_csn = fields.Char(string='CSN')
    tslsv = fields.Char(string='TSLSV')
    cslsv = fields.Char(string='CSLSV')
    lessor = fields.Char(string='Lessor')
    start_lease = fields.Date('Start Lease')
    normal_termination = fields.Date('Normal Termination')
