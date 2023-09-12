from odoo import models, fields, api
import xlwt
from xlsxwriter import *
from cStringIO import StringIO
import base64
from reportlab.pdfgen import canvas
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from datetime import datetime, timedelta

class GeneralToolsReport(models.Model):
    _name = 'general.tool.report'
    _description = 'General Tools Report'

    tool = fields.Many2one('tool.type', 'Tool Name', domain=[('type','=','onground'), ])
    location = fields.Many2one('base.operation', 'Location')
    calibrated = fields.Selection([('all','All'),('need','Need Calibration'),('notneed','Not Need Calibration')], 'Calibrated Status')
    next_calibrated = fields.Date('Next Calibrated Schedule at')
    tool_in = fields.Selection([('all','All'),('inuse','In Use'),('notinuse','Not In Use')], 'Tool in Use')

    gen_tool = fields.One2many('general.tool', 'rep_id', compute=lambda self: self._onchange_comp())



    @api.multi
    def print_general_tool_reports(self):
        return self.env['report'].get_action(self, 'ams_report.general_tool_pdf')


    def rendering(self):
        search_param = []
        search_param_move = []
        no = 0
        search_param_move.append(('status','=','onhand'))
        if self.location:
            search_param.append(('base_id','=',self.location.id))
            # search_param_move.append(('location.name','like',self.location.name))
        if self.tool:
            search_param.append(('id','=',self.tool.id))
            search_param_move.append(('tool','=',self.tool.id))

        if self.calibrated:
            if self.calibrated == 'need':
                search_param.append(('gse_nextdue','>=',datetime.now().strftime('%Y-%m-%d')))
            elif self.calibrated == 'notneed':
                search_param.append(('gse_nextdue','<=',datetime.now().strftime('%Y-%m-%d')))

        # if self.next_calibrated:
        #     search_param.append('&')
        #     search_param.append(('gse_nextdue','>=',self.next_calibrated))
        #     search_param.append(('gse_nextdue','<=',self.next_calibrated))


        tools = self.env['tool.type'].search(search_param)
        tool_move = self.env['tool.movement'].search(search_param_move)
        push_data = []
            



        for x in tools:
            if x.type == 'onground':
                push_data.append((0,0,{
                    'tool' : x.id,
                    'sn' : str(x.esn),
                    'pn' : str(x.part_num),
                    'location' : x.base_id.id,
                    'last_calibration' : str(x.gse_nextdue),
                    'next_calibration' : str(x.gse_lastcb),
                    'status' : 'Available',
                }))
        for y in tool_move:
            if y.refer_sb:
                refer_number = y.refer_sb.name
            if y.refer_ad:
                refer_number = y.refer_ad.name
            if y.refer_stc:
                refer_number = y.refer_stc.name
            if y.refer_ser:
                refer_number = y.refer_ser.name
            if y.refer_eo.eo_number:
                refer_number = y.refer_eo.eo_number
            if y.refer_mi:
                refer_number = y.refer_mi.no
            if y.refer_ti:
                refer_number = y.refer_ti.no
            if y.refer_oti:
                refer_number = y.refer_oti.no
            for c in push_data:
                if c[2]['tool'] == y.tool.id:
                    c[2]['status'] = str('In Used By : '+ y.employee.name+'<br/> For '+y.refer+' No. '+refer_number)
                    no += 1

        data = []
        if self.tool_in:
            if self.tool_in == 'inuse':
                for z in push_data:
                    if z[2]['status'] != 'Available':
                        data.append(z)
                self.gen_tool = data
            elif self.tool_in == 'notinuse':
                for a in push_data:
                    if a[2]['status'] == 'Available':
                        data.append(a)
                self.gen_tool = data
            else:
                self.gen_tool = push_data
        else:
            self.gen_tool = push_data
        

    @api.onchange('tool_in')
    def _onchange_comp(self):
        self.rendering()


class GeneralTools(models.Model):
    _name = 'general.tool'
    _description = 'General Tools'

    tool = fields.Many2one('tool.type', 'Tool Name')
    sn = fields.Char('S/N')
    pn = fields.Char('P/N')
    location = fields.Many2one('base.operation', 'Location')
    last_calibration = fields.Char('Last Calibrated')
    next_calibration = fields.Char('Next Calibrate Due ')
    status = fields.Html('Status')

    rep_id = fields.Many2one('general.tool.report')