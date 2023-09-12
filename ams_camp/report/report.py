from odoo import models, fields, api, _
from datetime import datetime, timedelta
import xlwt
from xlsxwriter import *
from cStringIO import StringIO
import base64
from reportlab.pdfgen import canvas
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from odoo.exceptions import  ValidationError


class AMSCampReport(models.Model):
    _name = 'ams.camp.report'
    _description = 'Maintenance Program Report'

    aircraft_model_id = fields.Many2one('aircraft.type', string='Aircraft Model')
    start_date = fields.Date('Starting Date Issued')
    end_date = fields.Date('Ending Date Issued')

    cam_id = fields.Many2many('ams.camp', compute=lambda self: self._onchange_comp())
    
    @api.multi
    @api.constrains('end_date', 'start_date')
    def date_constrains(self):
        for rec in self:
            if rec.end_date < rec.start_date:
                raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))


    @api.one
    def rendering(self):
        search_param = []
        push = []
        avail_ac = []
        if search_param == []:
            push_data = self.env['ams.camp'].search(search_param, order="number desc")
        else:
            push_data = self.env['ams.camp'].search(search_param, order="number desc")

        for x in push_data:
            if(x.aircraft_model_id not in avail_ac):
                avail_ac.append(x.aircraft_model_id)
                push.append(x.id)

        # print push
        self.cam_id = push

    @api.onchange('cam_id')
    def _onchange_comp(self):
        self.rendering()
            

    @api.multi
    def print_camp_pdf_report(self):
        self.rendering()
        return self.env['report'].get_action(self, 'ams_camp.report_camp_stat')            