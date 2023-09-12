from odoo import models, fields, api
import xlwt
from xlsxwriter import *
from cStringIO import StringIO
import base64
from reportlab.pdfgen import canvas
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from datetime import datetime, timedelta

class OnBoardReport(models.Model):
    _name = 'on.board.report'
    _description = 'On Board Report'

    tool = fields.Many2one('tool.type', 'Tool Name', domain=[('type','=','onboard'), ])
    location = fields.Many2one('aircraft.acquisition', 'Aircraft')
    calibrated = fields.Selection([('all','All'),('need','Need Calibration'),('notneed','Not Need Calibration')], 'Calibrated Status')
    next_calibrated = fields.Date('Next Calibrated Schedule at')
    # tool_in = fields.Selection([('all','All'),('inuse','In Use'),('notinuse','Not In Use')], 'Tool in Use')

    tool_id = fields.One2many('on.board', 'rep_id', compute=lambda self: self._onchange_comp())



    @api.multi
    def print_on_board_reports(self):
        return self.env['report'].get_action(self, 'ams_report.on_board_pdf')


    def rendering(self):
        search_param = []
        search_param_move = []
        no = 0
        # search_param_move.append(('status','=','onhand'))
        if self.location:
            search_param.append(('fleet_id','=',self.location.id))
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
            if x.type == 'onboard':
                push_data.append((0,0,{
                    'tool' : x.id,
                    'sn' : str(x.esn),
                    'pn' : str(x.part_num),
                    'location' : x.fleet_id.id,
                    'last_calibration' : str(x.gse_nextdue),
                    'next_calibration' : str(x.gse_lastcb),
                }))
        self.tool_id = push_data
        

    @api.onchange('tool')
    def _onchange_comp(self):
        self.rendering()


class GeneralTools(models.Model):
    _name = 'on.board'
    _description = 'On Board'

    tool = fields.Many2one('tool.type', 'Tool Name')
    sn = fields.Char('S/N')
    pn = fields.Char('P/N')
    location = fields.Many2one('aircraft.acquisition', 'Aircraft')
    last_calibration = fields.Char('Last Calibrated')
    next_calibration = fields.Char('Next Calibrate Due ')

    rep_id = fields.Many2one('on.board.report')