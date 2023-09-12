
from odoo import models, fields, api

class AmsBin(models.Model):
    _name = 'ams.bin'
    _description = 'Inventory Location'

    code     = fields.Char('Location Code', default='KOTA', required=True)
    name     = fields.Char('Location Name',required=True)
    base_id = fields.Many2one('base.operation', string="Location")
    desc 	= fields.Text('Description')
    