# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime, timedelta
from odoo import fields, models, api

class GSEType(models.Model):
	_name = 'gse.type'
	_description = 'Ground Service Equipment'

	name = fields.Char( string='Ground Service Equipment Name')
	category = fields.Selection([('fixedwing','Fixed Wing'),('rotary','Rotary')],'Category')
	ownership = fields.Selection([('leasing','Leasing'),('owner','Owner')],string='Ownership')
	delivery_date = fields.Date('Delivery date')
	date_manufacture = fields.Date('Date of Manufacture')
	propeller_type_id = fields.Many2one('propeller.type','Propeller Type')
	esn = fields.Char(string='S/N')
	rgb = fields.Char(string='RGB S/N')
	propeller = fields.Char(string='Propeller S/N')
	tsn = fields.Char(string='TSN')
	csn = fields.Char(string='CSN')
	tslsv = fields.Char(string='TSLSV')
	cslsv = fields.Char(string='CSLSV')
	lessor = fields.Char(string='Lessor')
	start_lease = fields.Date('Start Lease')
	normal_termination = fields.Date('Normal Termination')
	gse_lastcb = fields.Date(string='Last Calibrated')
	gse_nextdue = fields.Date(string='Next Calibrate Due')
	vendors = fields.Many2one('res.partner', string='Vendor')
	gse_hsi = fields.Date(string='Ground Service Equipment#1 HSI')
	gse_tsn = fields.Float(string='TSN')
	gse_csn = fields.Float(string='GSE CSN')
	gse_tslsvcb = fields.Float(string='GSE TSLSV Calibrated')
	gse_tslsv_hsi = fields.Float(string='GSE TSLSV HSI')
	gse_cslsv = fields.Float(string='GSE CSLSV Calibrated')
	gse_cslsv_hsi = fields.Float(string='GSE CSLSV HSI')
	propeller_tsn = fields.Float(string='Propeller TSN')
	propeller_tslsv = fields.Float(string='Propeller TSLSV')
	propeller_lastoh =fields.Date(string='Propeller Last Calibrated')
	aircraft_status = fields.Boolean(string='Engine Status',default=True)
	total_hours = fields.Float(string='Total Hours')
	total_cycles = fields.Float(string='Total Cycles')
	special_ratio_counting = fields.Boolean(string='Special ratio Counting')
	component_ids = fields.One2many('ams.component.part','engine_id',string='Component')
	inspection_ids = fields.One2many('ams.inspection','engine_id',string='Inspection')
	history_line = fields.One2many('ams.component_history','engine_id',string='History')
	some_count = fields.Integer(string='Total',default=3)

	# type = fields.Selection([('onboard','On Board'),('onground','On Ground')], required=True)
	fleet_id = fields.Many2one('aircraft.acquisition', string="Location")
	base_id = fields.Many2one('base.operation', string="Location")
	count_calibrate =  fields.Integer(default=1 , readonly=True)


	@api.onchange('type')
	def _associate_account(self):
		if (self.id):
			data = self.env['gse.calibrated'].search_count([('gse_id.id','=',self.id)])
			self.count_calibrate = data

	def true(self):
		return True

	@api.multi
	def return_action_to_open(self):
		return False


class Calibrated(models.Model):
	_name = 'gse.calibrated'
	_description = 'Calibrated'

	calibrate_last = fields.Date(string='Last Calibrated')
	calibrate_next = fields.Date(string='Next Calibrate Due')
	gse_id = fields.Many2one('gse.type', default=lambda self:self.env.context.get('default_config_id',False))