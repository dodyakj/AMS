from odoo import models, fields, api, _
from datetime import datetime, timedelta
import xlwt
from xlsxwriter import *
from cStringIO import StringIO
import base64
from reportlab.pdfgen import canvas
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx


class AMSFleetwideStatus(models.Model):
    _name = 'ams.fleetwide.report'
    _description = 'Fleetwide Status Report'

    fleetwide = fields.Many2many('aircraft.acquisition', compute=lambda self: self._onchange_comp())
    
    def rendering(self):
        search_param = []
        push_data = self.env['aircraft.acquisition'].search(search_param, order="create_date asc")
        self.fleetwide = push_data

    @api.model
    def _onchange_comp(self):
        self.rendering()
            

    @api.multi
    def print_fleetwide_report(self):
        self.rendering()
        return self.env['report'].get_action(self, 'ams_report.report_fleetwide')            