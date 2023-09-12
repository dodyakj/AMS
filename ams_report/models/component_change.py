# from odoo import models, fields, api
# import xlwt
# from xlsxwriter import *
# from cStringIO import StringIO
# import base64
# from reportlab.pdfgen import canvas
# from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
# from datetime import datetime, timedelta

# class CalibrationReport(models.Model):
#     _name = 'tool.calibrated.report'
#     _description = 'Calibration Report'

#     type = fields.Selection([('all','All'),('onground','Aircraft'),('onboard','On Board')])
#     location = fields.Many2one('base.operation', 'Location')
#     fleet = fields.Many2one('aircraft.acquisition', 'Aircraft')
#     start_calibrated = fields.Date('Calibrated Start Date')
#     end_calibrated = fields.Date('Calibrated End Date')
#     calibrated_due = fields.Boolean('Show Calibration Due')

#     tool_id = fields.One2many('tool.calibrated', 'rep_id', compute=lambda self: self._onchange_comp())

#     @api.multi
#     def print_calibration_reports(self):
#         return self.env['report'].get_action(self, 'ams_report.calibration_pdf')


#     def rendering(self):
#         search_param = []
#         # search_param_move = []
#         no = 0
#         # search_param_move.append(('status','=','onhand'))
#         if self.location:
#             search_param.append(('fleet_id','=',self.location.id))
#             # search_param_move.append(('location.name','like',self.location.name))
#         if self.fleet and self.type == 'onboard':
#             search_param.append(('id','=',self.tool.id))
#             # search_param_move.append(('tool','=',self.tool.id))

#         if self.start_calibrated and self.end_calibrated:
#             search_param.append(('gse_nextdue','>=',self.start_calibrated))
#             search_param.append(('gse_nextdue','<=',self.end_calibrated))

#         tools = self.env['tool.type'].search(search_param)
#         # tool_move = self.env['tool.movement'].search(search_param_move)
#         push_data = []

#         for x in tools:
#             push_data.append((0,0,{
#                 'location' : x.base_id.id,
#                 'fleet' : x.fleet_id.id,
#                 'tool' : x.name,
#                 'sn' : x.esn,
#                 'calibration_due' : str(x.gse_nextdue),
#             }))
#         self.tool_id = push_data
        

#     @api.onchange('tool')
#     def _onchange_comp(self):
#         self.rendering()


# class Calibration(models.Model):
#     _name = 'tool.calibrated'
#     _description = 'Calibration'

#     location    = fields.Many2one('base.operation', 'Location')
#     fleet       = fields.Many2one('aircraft.acquisition', 'Aircraft')
#     tool        = fields.Char('Tool Name')
#     sn          = fields.Char('S/N')
#     calibration_due = fields.Char('Calibration Due')

#     rep_id = fields.Many2one('tool.calibrated.report')