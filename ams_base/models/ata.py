
from odoo import models, fields, api

class AtaDefinition(models.Model):
    _name = 'ams.ata'
    _description = 'Ata Code'
    _order = 'name asc'

    name     = fields.Char('ATA Code', required=True)
    chapter      = fields.Char('ATA Chapter')
    sub_chapter  = fields.Char('Sub-Chapter')
    description  = fields.Text('Description')