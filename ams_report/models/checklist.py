from odoo import models, fields, api, _
from datetime import datetime, timedelta
import xlwt
from xlsxwriter import *
from cStringIO import StringIO
import base64
from reportlab.pdfgen import canvas
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx


class AMSChecklistReport(models.Model):
    _name = 'ams.checklist.report'
    _description = 'Checklist Report'

    checklist_model_id = fields.Many2one('ams.checklist.type', string='Checklist Number')

    checklist = fields.Many2many('ams.checklist', compute=lambda self: self._onchange_comp())
    
    @api.one
    def rendering(self):
        search_param = []
        push = []
        avail_ac = []
        if search_param == []:
            push_data = self.env['ams.checklist'].search(search_param, order="create_date desc")
        else:
            push_data = self.env['ams.checklist'].search(search_param, order="create_date desc")

        for x in push_data:
            if(x.checklist_model_id not in avail_ac):
                avail_ac.append(x.checklist_model_id)
                push.append(x.id)

        # print push
        self.checklist = push

    @api.model
    def _onchange_comp(self):
        self.rendering()
            

    @api.multi
    def print_checklist_report(self):
        self.rendering()
        return self.env['report'].get_action(self, 'ams_report.report_checklist')            