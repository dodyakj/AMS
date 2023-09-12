# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import xlwt
from xlsxwriter import *
from cStringIO import StringIO
import base64
from reportlab.pdfgen import canvas
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from odoo.exceptions import  ValidationError

class ReportToolsMovement(models.Model):
    _name = 'report.tools.movement'
    _description = 'Tools Movement Report'

    date_start = fields.Date()
    date_end = fields.Date()
    all_employee = fields.Boolean('All Employee', default=True)
    all_tool = fields.Boolean('All Tools', default=True)
    employee = fields.Many2one('hr.employee')
    tool = fields.Many2one('tool.type', 'Tool')
    status = fields.Selection([('all','All'),('request','Request'),('onhand','On Hand'),('complete','Complete')], default='all')
    sort_by = fields.Selection([('asc','ASC'),('desc','DESC')], default='asc')
    order_by = fields.Selection([('date','Date'),('tool','Tool'),('employee','Employee'),('status','Status')], default='date')

    tool_id = fields.Many2many('tool.movement', compute='_get_tools')

    @api.multi
    @api.constrains('date_start', 'date_end')
    def date_constrains(self):
        for rec in self:
            if rec.date_end < rec.date_start:
                raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))

    @api.multi
    def export_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'report.tools.movement'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
                
        if context.get('xls_export'):
            print datas
            return {'type': 'ir.actions.report.xml',
                    'report_name': 'ams_report.tool_movement_report.xlsx',
                    'datas': datas,
                    'name': 'Tool Movement Report'
                    }

    # @api.onchange('status')
    @api.model
    def _get_tools(self):
        start_date =  self.date_start
        end_date = self.date_end
        if start_date == False:
            start_date = '1000-10-10'
        if end_date == False:
            end_date = '9999-12-12'
        if self.status == 'all':
            if (self.all_employee == True and self.all_tool == True):
                data = self.env['tool.movement'].search([('date', '>=', start_date), ('date', '<=', end_date)], order=str(self.order_by+' '+self.sort_by))
            elif (self.all_employee == True and self.all_tool == False):
                data = self.env['tool.movement'].search([('tool', '=', self.tool.id), ('date', '>=', start_date), ('date', '<=', end_date)], order=str(self.order_by+' '+self.sort_by))
            elif (self.all_tool == True and self.all_employee == False ):
                data = self.env['tool.movement'].search([('employee', '=', self.employee.id), ('date', '>=', start_date), ('date', '<=', end_date)], order=str(self.order_by+' '+self.sort_by))
            else:
                data = self.env['tool.movement'].search([('tool', '=', self.tool.id), ('employee', '=', self.employee.id), ('date', '>=', start_date), ('date', '<=', end_date)], order=str(self.order_by+' '+self.sort_by))
        else:
            if (self.all_employee == True and self.all_tool == True):
                data = self.env['tool.movement'].search([('status', '=', self.status), ('date', '>=', start_date), ('date', '<=', end_date)], order=str(self.order_by+' '+self.sort_by))
            elif (self.all_employee == True and self.all_tool == False):
                data = self.env['tool.movement'].search([('status', '=', self.status), ('tool', '=', self.tool.id), ('date', '>=', start_date), ('date', '<=', end_date)], order=str(self.order_by+' '+self.sort_by))
            elif (self.all_tool == True and self.all_employee == False ):
                data = self.env['tool.movement'].search([('status', '=', self.status), ('employee', '=', self.employee.id), ('date', '>=', start_date), ('date', '<=', end_date)], order=str(self.order_by+' '+self.sort_by))
            else:
                data = self.env['tool.movement'].search([('status', '=', self.status), ('tool', '=', self.tool.id), ('employee', '=', self.employee.id), ('date', '>=', start_date), ('date', '<=', end_date)], order=str(self.order_by+' '+self.sort_by))
        self.tool_id = data


    @api.multi
    def print_tools_movement_pdf(self):
        return self.env['report'].get_action(self, 'ams_report.report_tool_movement')

class ToolmovementReeport(ReportXlsx):
    def tool_data(self, data):
        tool = self.env['tool.movement'].search([('id', 'in', data['form']['tool_id'])])
        return tool

    def generate_xlsx_report(self, workbook, data, lines):
        tool = self.tool_data(data)
        format1 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'vcenter', 'bold': True})
        format11 = workbook.add_format({'font_size': 12, 'align': 'center', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True})
        format21 = workbook.add_format({'font_size': 10, 'align': 'center', 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': True})
        format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 12})
        format2 = workbook.add_format({'bottom': True, 'top': False, 'font_size': 12})
        font_size_8 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8})
        red_mark = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8, 'bg_color': 'red'})
        justify = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 12})
        format3.set_align('center')
        format2.set_align('center')
        font_size_8.set_align('center')
        justify.set_align('justify')
        format1.set_align('center')
        red_mark.set_align('center')
        col = 0
        col1 = 4
        sheet = workbook.add_worksheet('Tool Movement Report')

        sheet.merge_range('A1:F2', 'Tool Movement Report', format1)
        sheet.write(4, 0, 'Date', format11)
        sheet.write(4, 1, 'Tool', format11)
        sheet.write(4, 2, 'Employee', format11)
        sheet.write(4, 3, 'Reference', format11)
        sheet.write(4, 4, 'Status', format11)
        sheet.write(4, 5, 'Remark', format11)

        for x in tool:
            col1 = col1 + 1 
            if x.remark == False:
                x.remark = ''
            sheet.write(col1, 0, x.date, font_size_8)
            sheet.write(col1, 1, x.tool.tool.name, font_size_8)
            sheet.write(col1, 2, x.employee.name, font_size_8)
            if x.refer == 'SB':
                sheet.write(col1, 3, x.refer_sb.name, font_size_8)
            elif x.refer == 'AD':
                sheet.write(col1, 3, x.refer_ad.name, font_size_8)
            elif x.refer == 'STC':
                sheet.write(col1, 3, x.refer_stc.name, font_size_8)
            elif x.refer == 'SERVICE':
                sheet.write(col1, 3, x.refer_ser.name, font_size_8)
            elif x.refer == 'EO':
                sheet.write(col1, 3, x.refer_eo.eo_number, font_size_8)
            elif x.refer == 'MI':
                sheet.write(col1, 3, x.refer_mi.no, font_size_8)
            elif x.refer == 'TI':
                sheet.write(col1, 3, x.refer_ti.no, font_size_8)
            elif x.refer == 'OTI':
                sheet.write(col1, 3, x.refer_oti.no, font_size_8)
            sheet.write(col1, 4, x.status, font_size_8)
            sheet.write(col1, 5, x.remark, font_size_8)
        
ToolmovementReeport('report.ams_report.tool_movement_report.xlsx','report.tools.movement')
