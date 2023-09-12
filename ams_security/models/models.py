# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta

class UnderConstruct(models.Model):
    _name = 'under.construct'
    _description = 'Under Construct'

    name = fields.Char('Name', default="Under Construct", readonly=True)