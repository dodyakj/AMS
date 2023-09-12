
from odoo import models, fields, api
from lxml import html
from lxml.html.clean import clean_html
import re

class AmsLog(models.Model):
    _name = 'ams.log'
    _description = 'Logbook'

    name      = fields.Char('Subject', related="aircraft_id.name", readonly=True)
    aircraft_id = fields.Many2one('aircraft.acquisition', string="Airframes", required=True, ondelete="cascade")
    
    hours = fields.Float(string='Hours')
    cycles = fields.Float(string='Cycles')
    rin = fields.Float(string='RIN')

    date = fields.Date(string='Date')

    ata = fields.Many2one('ams.ata', string="ATA Code")

    description = fields.Text('Description')
    wo_id = fields.Many2one('ams.work.order', string="W/O Reference")
    mwo_id = fields.Many2one('ams.mwo', string="MWO Reference")


    # @api.model
    # def create(self, values):
    #     if values[]:
    #         for x in values:
    #             print type(values[x])
    #             print values[x]
    #             # if type(values[x]) is str:
    #             #     print clean_html(values[x])
