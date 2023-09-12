from odoo import models, fields, api, _
import xlwt
from xlsxwriter import *
from cStringIO import StringIO
import base64
from reportlab.pdfgen import canvas
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from datetime import datetime, timedelta
from odoo.exceptions import  ValidationError

class PrematureValue(models.Model):
    _name = 'ams.premature.value.report'
    _description = 'Description'

    component   = fields.Many2one('ams.component.part', 'Component')
    start_date  = fields.Date()
    end_date    = fields.Date()
    ata     = fields.Char('ATA')
    fleet   = fields.Many2one('aircraft.acquisition', 'Aircraft')
    order_by    = fields.Selection([('date','Date'),('component','Component'),('ata','ATA')], default='date')
    premature   = fields.Many2many('ams.component_history', compute=lambda self: self._onchange_comp())

    @api.multi
    @api.constrains('end_date', 'start_date')
    def date_constrains(self):
        for rec in self:
            if rec.end_date < rec.start_date:
                raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))


    @api.multi
    def print_premature_pdf(self):
        return self.env['report'].get_action(self, 'ams_report.premature_pdf')



    def rendering(self):
        search_param = []
        search_param.append(('premature_removal','=',True))
        if self.component:
            search_param.append(('part_id','=',self.component.id))
        if self.start_date and self.end_date:
            search_param.append(('create_date','>=',self.start_date))
            search_param.append(('create_date','<=',self.end_date))
        if self.ata:
            search_param.append(('part_id.ata_code.name','like',self.ata))
        if self.fleet:
            search_param.append(('fleet_id','=',self.fleet.id))

        premature_data = self.env['ams.component_history'].search(search_param, order=str(self.order_by))
        print premature_data
        print search_param
        self.premature = premature_data
        

    @api.onchange('component')
    def _onchange_comp(self):
        self.rendering()
