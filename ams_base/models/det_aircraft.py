# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, tools, api, _
from odoo.exceptions import ValidationError, except_orm

class AircraftDetails(models.Model):
    _inherit = 'aircraft.acquisition'


        # image: all image fields are base64 encoded and PIL-supported
    image = fields.Binary()


    """ AIRFIELDS PERFORMANCE """

    seat_cap 		= fields.Integer('Seat Capacity')
    type_engine 	= fields.Many2one('engine.type', string='Type of Engine')
    takeoff_power 	= fields.Integer('Take off Power')
    max_continuous	= fields.Integer('Max Continuous')
    max_climb		= fields.Integer('Max Climb')
    max_cruise		= fields.Integer('Max Cruise')
    type_propeller  = fields.Char('Type Of Propeller')
    blades_diameter = fields.Char('Blades Diameter')
    
    """ WEIGHTS """

    max_takeoff 		= fields.Char('Maximum Take off Weight')
    max_landing 		= fields.Char('Maximum Landing Weight')
    max_zero 			= fields.Char('Maximum Zero Fuel Weight')
    operational_empt 	= fields.Char('Operational empty Weight')

    avionic_id = fields.One2many('aircraft.detail.avionic', 'ad_id', string='Avionic System', copy=True)

class AvionicSystem(models.Model):
    _name = 'aircraft.detail.avionic'
    _description = 'Avionic System'

    designation = fields.Many2one('ams.component.part', 'Designation')
    manufacture = fields.Boolean('Manufacture',compute=lambda self: self._onchange_designation())
    part_number = fields.Char('Part Number',compute=lambda self: self._onchange_designation())
    qty 		= fields.Float('Qty')

    ad_id = fields.Many2one('aircraft.acquisition')

    @api.onchange('designation')
    def _onchange_designation(self):
        des = self.designation 
        # self.manufacture = des.product_id.route_ids
        self.part_number = des.product_id.default_code
        # self.qty = des.product_id.qty      

            