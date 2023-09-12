from odoo import models, fields, api, _
from datetime import datetime, timedelta
import xlwt
from xlsxwriter import *
from cStringIO import StringIO
import base64
from reportlab.pdfgen import canvas
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from odoo.exceptions import  ValidationError


class InspectionReport(models.Model):
    _name = 'ams.inspection.report'
    _description = 'Inspection Report'

    type = fields.Selection([('fleet','Aircraft'),('engine','Engine'),('auxiliary','Auxiliary'),('propeller','Propeller')], string='Type', default=lambda self:self.env.context.get('bulletin_type','fleet'), required=True)
    # status = fields.Selection([('mandatory','Mandatory'),('recommended','Recommended'),('optional','Optional')], string='Compliance Type', required=True, default='mandatory')
    start_date = fields.Date()
    end_date = fields.Date()
    ins_id = fields.Many2many('airworthy.inspection', compute=lambda self: self._onchange_comp())

    @api.multi
    @api.constrains('end_date', 'start_date')
    def date_constrains(self):
        for rec in self:
            if rec.end_date < rec.start_date:
                raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))
    
    def rendering(self):
        search_param = []
        if self.type == 'fleet':
            search_param.append(('fleet_id', '!=', False))
        if self.type == 'engine':
            search_param.append(('engine_id', '!=', False))
        if self.type == 'auxiliary':
            search_param.append(('auxiliary_id', '!=', False))
        if self.type == 'propeller':
            search_param.append(('propeller_id', '!=', False))
        if self.start_date and self.end_date:
            search_param.append(('date', '>=', self.start_date))
            search_param.append(('date', '<=', self.end_date))
        push_data = self.env['airworthy.inspection'].search(search_param, order="create_date desc")
        self.ins_id = push_data

    @api.onchange('type')
    def _onchange_comp(self):
        self.rendering()
            

    @api.multi
    def print_ins_reports(self):
        self.rendering()
        return self.env['report'].get_action(self, 'ams_report.report_ins')            