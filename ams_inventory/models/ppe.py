from odoo import models, fields, api
from odoo.tools.translate import _
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class MasterPP(models.Model):
    _inherit = 'product.product'
    # _name = 'ppe.master'
    # _description = 'PPE'

    # date = fields.Date('Date', default=datetime.now())
    is_ppe = fields.Boolean('PPE')
    # stocked_id = fields.Many2one('res.partner', 'Stocked By', default=lambda self: self.env.user.partner_id.id)
    # location_id = fields.Many2one('base.operation', ' Loocation')

    # ppe_id = fields.One2many('ppe.stock', 'm_ppe')

    @api.model
    def create(self,value):
        value['is_ppe'] = True
        res = super(MasterPP, self).create(value)
        return res

    @api.multi
    def write(self, vals):
        for rec in self:
            if rec.is_ppe == False:
                vals['is_ppe'] = True
        return super(MasterPP, self).write(vals)


class MasterPPE(models.Model):
    # _inherit = 'product.product'
    _name = 'ppe.master'
    _description = 'PPE'


    date = fields.Date('Date', default=datetime.now())
    is_ppe = fields.Boolean('PPE')
    stocked_id = fields.Many2one('res.partner', 'Stocked By', default=lambda self: self.env.user.partner_id.id)
    location_id = fields.Many2one('base.operation', ' Loocation')

    ppe_id = fields.One2many('ppe.stock', 'm_ppe', copy=True)

    @api.model
    def create(self,value):
        value['is_ppe'] = True
        res = super(MasterPPE, self).create(value)
        return res

    @api.multi
    def write(self, vals):
        for rec in self:
            if rec.is_ppe == False:
                vals['is_ppe'] = True
        return super(MasterPPE, self).write(vals)

    # @api.one
    # @api.onchange('ppe_id')
    # def _onchange_ppe_id(self):
    #     if self.ppe_id:
    #         self.ppe_id.stocked_id = self.stocked_id.id
    #         self.ppe_id.location_id = self.location_id.id
    #         print self.ppe_id.location_id
    #         print self.ppe_id.stocked_id
        
            

class StockPPE(models.Model):
    _name = 'ppe.stock'
    _description = 'Stock'

    name = fields.Many2one('product.product', 'PPE', domain=[('is_ppe','=',True)])
    date = fields.Date('Date', default=datetime.now())
    amount = fields.Float('Amount')
    stocked_id = fields.Many2one('res.partner', 'Stocked By', compute=lambda self: self._onchange_name())
    location_id = fields.Many2one('base.operation', ' Loocation', compute=lambda self: self._onchange_name())
    # stock_type = fields.Selection([('M','m'),('U','u')], compute=lambda self: self._onchange_name())
    m_ppe = fields.Many2one('ppe.master')
    u_ppe = fields.Many2one('ppe.usage')

    @api.onchange('name')
    def _onchange_name(self):
        self.stocked_id = self.m_ppe.stocked_id.id 
        self.location_id = self.m_ppe.location_id.id 
        self.amount = 1
        # if self.m_ppe:
        #     self.stock_type  = 'M'
        # elif self.u_ppe:
        #     self.stock_type  = 'U'

class UsagePPE(models.Model):
    # _inherit = ["ppe.stock"]
    _name = 'ppe.usage'
    _description = 'Usage PPE'

    date = fields.Date('Date', default=datetime.now())
    is_ppe = fields.Boolean('PPE', default=True)
    employee_id = fields.Many2one('res.partner', 'Stocked By', default=lambda self: self.env.user.partner_id.id)
    location_id = fields.Many2one('base.operation', ' Loocation')
    use = fields.Boolean(default=True)


    ppe_id = fields.One2many('ppe.stock', 'u_ppe', copy=True)

    @api.model
    def create(self, values):
        search_param = []
        if self.ppe_id:
            for x in self.ppe_id:
                search_param.append(('id','=',x.id))
        ppe = self.env['ppe.stock'].search(search_param)
        if ppe:
            ppe.unlink()
        res = super(UsagePPE, self).create(values)
        return res

