# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ams_codectr(models.Model):
    _name = 'ams_codectr.code'


    name = fields.Char('model',default=lambda self:self.env.context.get('models',False))
    label = fields.Char(string='Label', default=lambda self:self.env.context.get('caption','Value'), readonly=True)
    value = fields.Integer('value',default=lambda self:self._getnext(self.env.context.get('models',False)) )

    # self.env['ir.sequence'].next_by_code('regulation.regulation') or _('/')
    @api.multi
    def save(self):
        #none
        self.env['ir.sequence'].search([('code','=',self.name)]).write({
        	'number_next' : self.value
        	})
        return True

    @api.model
    def _getnext(self,codename):
        sequence = self.env['ir.sequence'].search([('code','=',codename)]).number_next
        return sequence