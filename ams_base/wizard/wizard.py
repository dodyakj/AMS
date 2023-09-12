from odoo import models, fields, api
import datetime

class Topupwizard(models.Model):
    _name = 'engine.confirm'

    reason = fields.Char(string='Reason')
