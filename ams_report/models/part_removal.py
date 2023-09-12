from odoo import models, fields, api, _
from datetime import datetime, timedelta
import xlwt
from xlsxwriter import *
from cStringIO import StringIO
import base64
from reportlab.pdfgen import canvas
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from odoo.exceptions import  ValidationError


class PartRemovalReport(models.Model):
    _name = 'part.removal.report'
    _description = 'Part Removal Report'

    fleet = fields.Many2one('aircraft.acquisition', 'Aircraft')
    part = fields.Many2one('ams.component.part')
    start_date = fields.Date()
    end_date = fields.Date()

    part_id = fields.Many2many('ams.component_history', compute=lambda self: self._onchange_comp())

    @api.multi
    @api.constrains('end_date', 'start_date')
    def date_constrains(self):
        for rec in self:
            if rec.end_date < rec.start_date:
                raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))

    @api.multi
    def export_xls(self):
        self.rendering()
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'part.removal.report'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        if context.get('xls'):
            return {'type': 'ir.actions.report.xml',
                    'report_name': 'ams_report.part_removal.xlsx',
                    'datas': datas,
                    'name': 'Part Removal Report'
                    }

    @api.multi
    def print_part_removal_reports(self):
        return self.env['report'].get_action(self, 'ams_report.part_removal_pdf')

    def rendering(self):
        search_param = []
        no = 0
        search_param.append(('premature_removal','=',True))
        search_param.append(('type','=','replace'))
        if self.fleet:
            search_param.append(('fleet_id','=',self.fleet.id))
        if self.part:
            search_param.append(('part_id','=',self.part.id))
        if self.start_date and self.end_date:
            search_param.append(('date','>=',self.start_date))
            search_param.append(('date','<=',self.end_date))

        part = self.env['ams.component_history'].search(search_param)
        # push_data = []

        # for x in part:
            # push_data.append((0,0,{
                # 'location' : x.base_id.id,
                # 'fleet' : x.fleet_id.id,
                # 'tool' : x.name,
                # 'sn' : x.esn,
                # 'calibration_due' : str(x.gse_nextdue),
            # }))
        self.part_id = part

    @api.onchange('part')
    def _onchange_comp(self):
        self.rendering()
