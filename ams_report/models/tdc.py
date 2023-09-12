from odoo import models, fields, api, _
from datetime import datetime, timedelta
import xlwt
from xlsxwriter import *
from cStringIO import StringIO
import base64
from reportlab.pdfgen import canvas
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from odoo.exceptions import  ValidationError


class TDCReport(models.Model):
    _name = 'ams.tdc.report'
    _description = 'TDC Report'

    type = fields.Selection([('AD','AD - Airwothiness Directive'),('SB','SB - Service Bulletin')], string='Type', required=True, default=lambda self:self.env.context.get('bulletin_type','SB'))
    # status = fields.Selection([('mandatory','Mandatory'),('recommended','Recommended'),('optional','Optional')], string='Compliance Type', required=True, default='mandatory')
    start_date = fields.Date()
    end_date = fields.Date()
    tdc_id = fields.Many2many('ams.bulletin', compute=lambda self: self._onchange_comp())

    @api.multi
    @api.constrains('end_date', 'start_date')
    def date_constrains(self):
        for rec in self:
            if rec.end_date < rec.start_date:
                raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))
    
    def rendering(self):
        search_param = []
        push = []
        # search_param.append('|')
        if self.type:
            search_param.append(('type','=',self.type))
            # search_param.append(('type','=','SB'))
        if self.start_date and self.end_date:
            search_param.append(('date', '>=', self.start_date))
            search_param.append(('date', '<=', self.end_date))
        push_data = self.env['ams.bulletin'].search(search_param, order="date desc")
        self.tdc_id = push_data

    @api.onchange('tdc_id')
    def _onchange_comp(self):
        self.rendering()
            

    @api.multi
    def print_tdc_reports(self):
        self.rendering()
        return self.env['report'].get_action(self, 'ams_report.report_tdc')            