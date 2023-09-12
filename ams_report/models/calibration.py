from odoo import models, fields, api, _
import xlwt
from xlsxwriter import *
from cStringIO import StringIO
import base64
from reportlab.pdfgen import canvas
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from datetime import datetime, timedelta
from odoo.exceptions import  ValidationError

class CalibrationReport(models.Model):
    _name = 'tool.calibrated.report'
    _description = 'Calibration Report'

    type = fields.Selection([('all','All'),('onground','Aircraft'),('onboard','On Board')], default='all')
    location = fields.Many2one('base.operation', 'Location')
    fleet = fields.Many2one('aircraft.acquisition', 'Aircraft')
    start_calibrated = fields.Date('Calibrated Start Date')
    end_calibrated = fields.Date('Calibrated End Date')
    calibrated_due = fields.Boolean('Show Calibration Due')

    tool_id = fields.One2many('tool.calibrated', 'rep_id', compute='_onchange_comp')

    @api.multi
    @api.constrains('end_calibrated', 'start_calibrated')
    def date_constrains(self):
        for rec in self:
            if rec.end_calibrated < rec.start_calibrated:
                raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))

                


    @api.multi
    def export_xls(self):
        self.rendering()
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'tool.calibrated.report'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        if context.get('calibrated'):
            return {'type': 'ir.actions.report.xml',
                    'report_name': 'ams_report.calibrated_report.xlsx',
                    'datas': datas,
                    'name': 'Calibrated Report'
                    }

    @api.multi
    def print_calibration_pdf(self):
        return self.env['report'].get_action(self, 'ams_report.calibration_pdf')


    def rendering(self):
        search_param = []
        # search_param_move = []
        no = 0
        # search_param_move.append(('status','=','onhand'))
        if self.location:
            search_param.append(('fleet_id','=',self.location.id))
            # search_param_move.append(('location.name','like',self.location.name))
        if self.fleet and self.type == 'onboard':
            search_param.append(('id','=',self.tool.id))
            # search_param_move.append(('tool','=',self.tool.id))

        if self.start_calibrated and self.end_calibrated:
            search_param.append(('gse_nextdue','>=',self.start_calibrated))
            search_param.append(('gse_nextdue','<=',self.end_calibrated))

        tools = self.env['tool.type'].search(search_param)
        # tool_move = self.env['tool.movement'].search(search_param_move)
        push_data = []

        for x in tools:
            push_data.append((0,0,{
                'location' : x.base_id.id,
                'fleet' : x.fleet_id.id,
                'tool' : x.tool.name,
                'sn' : x.esn,
                'calibration_due' : str(x.gse_nextdue),
                'calibration_last' : str(x.calibrate_last),
                'calibration_next' : str(x.calibrate_next),
            }))
        self.tool_id = push_data
        

    @api.onchange('type')
    def _onchange_comp(self):
        self.rendering()


class Calibration(models.Model):
    _name = 'tool.calibrated'
    _description = 'Calibration'

    location    = fields.Many2one('base.operation', 'Location')
    fleet       = fields.Many2one('aircraft.acquisition', 'Aircraft')
    tool        = fields.Char('Tool Name')
    sn          = fields.Char('S/N')
    calibration_last = fields.Char('Last Calibration')
    calibration_next = fields.Char('Next Calibration')
    calibration_due = fields.Char('Calibration Due')

    rep_id = fields.Many2one('tool.calibrated.report')



class CalibrationReportXls(ReportXlsx):
    def calibratio_data(self, data):
        search_param = []
        if data['form']['location']:
            search_param.append(('fleet_id','=', data['form']['fleet']))
            # search_param_move.append(('location.name','like',self.location.name))
        if data['form']['type'] and data['form']['type'] == 'onboard':
            search_param.append(('base_id','=',data['form']['location']))
            # search_param_move.append(('tool','=',self.tool.id))

        if data['form']['start_calibrated'] and data['form']['end_calibrated']:
            search_param.append(('gse_nextdue','>=',data['form']['start_calibrated']))
            search_param.append(('gse_nextdue','<=',data['form']['end_calibrated']))
        calibration = self.env['tool.type'].search(search_param)
        push_data = []
        # print search_param
        # print data['form']
        # print data['form']['location']
        for x in calibration:
            push_data.append((0,0,{
                'location' : x.base_id.name,
                'fleet' : x.fleet_id.name,
                'tool' : x.tool.name,
                'sn' : x.esn,
                'calibration_due' : str(x.gse_nextdue),
                'calibration_last' : str(x.calibrate_last),
                'calibration_next' : str(x.calibrate_next),
            }))
        # return push_data
        # print calibration
        # print '-----------------'
        # print push_data
        return calibration

    def generate_xlsx_report(self, workbook, data, lines):
        calibration = self.calibratio_data(data)
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
        if data['form']['calibrated_due']:
            sheet2 = workbook.add_worksheet('Special Tool Report')
            sheet2.merge_range('A1:F2', 'Special Tool Report', format1)
            sheet2.write(4, 0, 'No', format11)
            sheet2.write(4, 1, 'Description', format11)
            sheet2.write(4, 2, 'Part Number', format11)
            sheet2.write(4, 3, 'Serial Number', format11)
            sheet2.write(4, 4, 'Qty', format11)
            sheet2.write(4, 5, 'Loc', format11)
            sheet2.write(4, 6, 'Dt of sent', format11)
            for x in calibration:
                col1 = col1 + 1 
                sheet2.write(col1, 0, x.base_id.name, font_size_8)
                sheet2.write(col1, 1, x.fleet_id.name, font_size_8)
                sheet2.write(col1, 2, x.name, font_size_8)
                sheet2.write(col1, 3, x.esn, font_size_8)
                sheet2.write(col1, 4, '', font_size_8)
                sheet2.write(col1, 5, '', font_size_8)
                sheet2.write(col1, 6, x.gse_nextdue, font_size_8)

        sheet = workbook.add_worksheet('Calibrated Report')

        sheet.merge_range('A1:F2', 'Calibrated Report', format1)
        sheet.write(4, 0, 'Location', format11)
        sheet.write(4, 1, 'Aircraft', format11)
        sheet.write(4, 2, 'Tool Name', format11)
        sheet.write(4, 3, 'S/N', format11)
        sheet.write(4, 4, 'Last Calibrated', format11)
        sheet.write(4, 5, 'Next Calibrated', format11)
        
        for x in calibration:
            col1 = col1 + 1 
            sheet.write(col1, 0, x.base_id.name, font_size_8)
            sheet.write(col1, 1, x.fleet_id.name, font_size_8)
            sheet.write(col1, 2, x.name, font_size_8)
            sheet.write(col1, 3, x.esn, font_size_8)
            sheet.write(col1, 4, x.calibrate_last, font_size_8)
            sheet.write(col1, 5, x.calibrate_next, font_size_8)





CalibrationReportXls('report.ams_report.calibrated_report.xlsx','tool.calibrated.report')
