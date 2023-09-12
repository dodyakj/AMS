# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ams_fml(models.Model):
    _inherit = 'ams_fml.log'

    fuel_lines_fw = fields.One2many('fuel_fw','fml_log', string="Fuel Lines")
    fuel_lines_rw = fields.One2many('fuel_rw','fml_log', string="Fuel Lines")
    oil_lines_engine_1 = fields.One2many('oil_engine_1','fml_log', string="Oil Lines")
    oil_lines_engine_2 = fields.One2many('oil_engine_2','fml_log', string="Oil Lines")
    oil_lines_engine_3 = fields.One2many('oil_engine_3','fml_log', string="Oil Lines")
    oil_lines_engine_4 = fields.One2many('oil_engine_4','fml_log', string="Oil Lines")

class FuelAircraftFw(models.Model):
    _name = 'fuel_fw'

    fml_log = fields.Many2one('ams_fml.log', string="FML Log")

    uplift = fields.Float('Uplift')
    uplift_uom = fields.Many2one('product.uom',string="Unit")
    total_fw = fields.Float('Total')
    total_fw_uom = fields.Many2one('product.uom',string="Unit")
    cons = fields.Float('Cons')
    cons_uom = fields.Many2one('product.uom',string="Unit")
    rem = fields.Float('Rem')
    rem_uom = fields.Many2one('product.uom',string="Unit")

class FuelAircraftRw(models.Model):
    _name = 'fuel_rw'

    fml_log = fields.Many2one('ams_fml.log', string="FML Log")

    added = fields.Float('Added')
    added_uom = fields.Many2one('product.uom',string="Unit")
    total_rw = fields.Float('Total')
    total_rw_uom = fields.Many2one('product.uom',string="Unit")

class OilAircraftEngine1(models.Model):
    _name = 'oil_engine_1'

    fml_log = fields.Many2one('ams_fml.log', string="FML Log")

    engine_number = fields.Selection([('engine_1','Engine 1'),('engine_2','Engine 2'),('engine_3','Engine 3'),('engine_4','Engine 4')], default=lambda self:self._context.get('engine_number', False))

    added = fields.Float(string='Added')
    added_uom = fields.Many2one('product.uom',string='Unit')

class OilAircraftEngine2(models.Model):
    _name = 'oil_engine_2'

    fml_log = fields.Many2one('ams_fml.log', string="FML Log")

    engine_number = fields.Selection([('engine_1','Engine 1'),('engine_2','Engine 2'),('engine_3','Engine 3'),('engine_4','Engine 4')], default=lambda self:self._context.get('engine_number', False))

    added = fields.Float(string='Added')
    added_uom = fields.Many2one('product.uom',string='Unit')

class OilAircraftEngine3(models.Model):
    _name = 'oil_engine_3'

    fml_log = fields.Many2one('ams_fml.log', string="FML Log")

    engine_number = fields.Selection([('engine_1','Engine 1'),('engine_2','Engine 2'),('engine_3','Engine 3'),('engine_4','Engine 4')], default=lambda self:self._context.get('engine_number', False))

    added = fields.Float(string='Added')
    added_uom = fields.Many2one('product.uom',string='Unit')

class OilAircraftEngine4(models.Model):
    _name = 'oil_engine_4'

    fml_log = fields.Many2one('ams_fml.log', string="FML Log")

    engine_number = fields.Selection([('engine_1','Engine 1'),('engine_2','Engine 2'),('engine_3','Engine 3'),('engine_4','Engine 4')], default=lambda self:self._context.get('engine_number', False))

    added = fields.Float(string='Added')
    added_uom = fields.Many2one('product.uom',string='Unit')