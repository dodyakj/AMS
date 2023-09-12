# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ComponentHistory(models.Model):
    _name = 'ams.component_history'

    engine_id = fields.Many2one('engine.type', string='Engine')
    auxiliary_id = fields.Many2one('auxiliary.type', string='Auxiliary')
    propeller_id = fields.Many2one('propeller.type', string='Propeller')
    fleet_id = fields.Many2one('aircraft.acquisition', string='Aircraft')
    engine_replacement_id = fields.Many2one('engine.type', string='Replacement Engine')

    auxiliary_id = fields.Many2one('auxiliary.type', string='Auxiliary')
    auxiliary_replacement_id = fields.Many2one('auxiliary.type', string='Replacement Auxiliary')

    propeller_id = fields.Many2one('propeller.type', string='Propeller')
    propeller_replacement_id = fields.Many2one('propeller.type', string='Replacement Propeller')

    part_id = fields.Many2one('ams.component.part', string='Part')
    component_id = fields.Many2one('product.product', string='Component')
    component_replacement_id = fields.Many2one('product.product', string='Replacement Component')
    serial_id = fields.Many2one('stock.production.lot', string='Serial', domain=lambda self: self._getserial())
    serial_replacement_id = fields.Many2one('stock.production.lot', string='Replacement Serial')

    ac_hours = fields.Float(string='A/C Hours')
    ac_cycles = fields.Float(string='A/C Cycles')
    hours = fields.Float(string='Hours')
    cycles = fields.Float(string='Cycles')

    type = fields.Selection([('attach','Attach'),('detach','Detach'),('replace','Replace')], string='Action')

    date = fields.Date(string='Date')

    reason = fields.Text(string='Reason')

    premature_removal = fields.Boolean(string='Premature Removal',default=True)

    @api.onchange('component_id')
    def _getserial(self):
        return {'domain':{'serial_id':[('product_id','=',self.component_id.id)]}}
        # return [('product_id', '=', self.component_id.id)]

class DocumentHistoryLot(models.Model):
    _inherit = 'stock.production.lot'

    document_ids = fields.One2many('stock.production.lot_document','lot_id',string='Document')
    unserviceable = fields.Boolean(string='Unserviceable', default=False)

class DocumentHistory(models.Model):
    _name = 'stock.production.lot_document'

    lot_id = fields.Many2one('stock.production.lot',string='Serial Number', default=lambda self:self.env.context.get('serial_id',False), readonly=True)
    file = fields.Binary(string='File Scan')
    file_name = fields.Char('File Name')

class ComponentHistory(models.Model):
    _name = 'ams.manual_changes'

    fleet_id = fields.Many2one('aircraft.acquisition', string='Aircraft')
    engine_id = fields.Many2one('engine.type', string='Engine')
    auxiliary_id = fields.Many2one('auxiliary.type', string='Auxiliary')
    propeller_id = fields.Many2one('propeller.type', string='Propeller')
    part_id = fields.Many2one('ams.component.part', string='Part')

    current_hours = fields.Float(string='Hours',default=False)
    current_cycles = fields.Float(string='Cycles',default=False)
    current_rin = fields.Integer(string='RIN',default=False)

    hours = fields.Float(string='Hours',default=False)
    cycles = fields.Float(string='Cycles',default=False)
    rin = fields.Integer(string='RIN',default=False)

    timestamp = fields.Datetime(string='Timestamp', default=fields.datetime.now())
    employee = fields.Many2one('res.partner', default=lambda self: self.env.user.partner_id.id)
    


    # ONCREATE CEK PERLAKUAN KOMPONENT

    # @api.model
    # def create(self, vals):

    #     acraft = self.env['aircraft.acquisition'].search([('id','=',vals['fleet_id'])])
    #     egine = self.env['engine.type'].search([('id','=',vals['engine_id'])])
        
    #     vals['ac_hours'] = acraft.total_hours
    #     vals['ac_cycles'] = acraft.total_landings

    #     vals['hours'] = egine.total_hours
    #     vals['cycles'] = egine.total_cycles

    #     create = super(ComponentHistory, self).create(vals)
    #     return create

    