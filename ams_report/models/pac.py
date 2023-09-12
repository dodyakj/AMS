from odoo import models, fields, api, _
from datetime import datetime, timedelta, date
from calendar import monthrange
from dateutil.relativedelta import relativedelta
# import xlwt
# from xlsxwriter import *
# from cStringIO import StringIO
# import base64
# from reportlab.pdfgen import canvas
# from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class PowerAssuranceCheck(models.Model):
    _name = 'ams.pac'
    _description = 'Power Assurance Check'

    fleet 	= fields.Many2one('aircraft.acquisition', default=lambda self:self._context.get('fleet_id', False))
    date 	= fields.Date('Year', default=datetime.now())
    month   = fields.Char('Month', compute=lambda self: self._onchange_date())
    year 	= fields.Char('Year', compute=lambda self: self._onchange_date())
    fml_id  = fields.Many2many('ams_fml.log', compute='_onchange_fleet') 

    @api.onchange('fleet')
    def _onchange_fleet(self):
        if self.fleet:
            month = datetime.strptime(self.date, '%Y-%m-%d').strftime('%m')
            year = datetime.strptime(self.date, '%Y-%m-%d').strftime('%Y')
            max_day = monthrange(int(year), int(month))[1]
            now = datetime.strptime(self.date, "%Y-%m-%d") 
            end = datetime.strptime(str(date(int(year),int(month),max_day)), "%Y-%m-%d")
            fleet = self.env['ams_fml.log'].search([('aircraft_id', '=', self.fleet.id),('date','>=',now),('date','<=',end)], order="date asc")
            self.fml_id = fleet

    @api.onchange('date')
    def _onchange_date(self):
        if self.date:
            year = datetime.strptime(self.date, '%Y-%m-%d').strftime('%Y')
            month = datetime.strptime(self.date, '%Y-%m-%d').strftime('%m')
            now = datetime.strptime(str(date(int(year),int(month),1)), "%Y-%m-%d")
            Months = ['January','February','March','April','May','June','July','August','September','October','November','December']
            self.date = now
            self.year = year
            self.month = Months[int(month)-1].upper()

    @api.multi
    def export_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'ams.pac'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
                
        if context.get('xls_export'):
            print datas
            return {'type': 'ir.actions.report.xml',
                    'report_name': 'ams_report.power_assurance_check.xlsx',
                    'datas': datas,
                    'name': 'Power Assurance Check'
                    }

    @api.multi
    def print_pac_pdf(self):
        return self.env['report'].get_action(self, 'ams_report.pac_pdf')

# class PowerAssuranceCheckXlxs(ReportXlsx):
#     def get_fleet(self, data):
#         fleet = self.env['aircraft.acquisition'].search([('id', '=', data['form']['fleet']),('acquisition_date', 'like', data['form']['year'])])
#         return fleet

#     def generate_xlsx_report(self, workbook, data, lines):
#         fleet = self.get_fleet(data)
#         format1 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'vcenter', 'bold': True})
#         format11 = workbook.add_format({'font_size': 12, 'align': 'center', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True})
#         format21 = workbook.add_format({'font_size': 10, 'align': 'center', 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': True})
#         format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 12})
#         format2 = workbook.add_format({'bottom': True, 'top': False, 'font_size': 12})
#         font_size_8 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8})
#         red_mark = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8, 'bg_color': 'red'})
#         justify = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 12})
#         format3.set_align('center')
#         format2.set_align('center')
#         font_size_8.set_align('center')
#         justify.set_align('justify')
#         format1.set_align('center')
#         red_mark.set_align('center')
#         col = 0
#         col1 = 4
#         sheet = workbook.add_worksheet('Power Assurance Check')
#         bold = workbook.add_format({'bold': 1})

#         # Add the worksheet data that the charts will refer to.
#         headings = ['Number', 'Batch 1', 'Batch 2']
#         data = [
#             [2, 3, 4, 5, 6, 7],
#             [10, 40, 50, 20, 10, 50],
#             [30, 60, 70, 50, 40, 30],
#         ]

#         sheet.write_row('A1', headings, bold)
#         sheet.write_column('A2', data[0])
#         sheet.write_column('B2', data[1])
#         sheet.write_column('C2', data[2])

#         # Create a new chart object. In this case an embedded chart.
#         chart1 = workbook.add_chart({'type': 'line'})

#         # Configure the first series.
#         chart1.add_series({
#             'name':       '=Sheet1!$B$1',
#             'categories': '=Sheet1!$A$2:$A$7',
#             'values':     '=Sheet1!$B$2:$B$7',
#         })

#         # Configure second series. Note use of alternative syntax to define ranges.
#         chart1.add_series({
#             'name':       ['Sheet1', 0, 2],
#             'categories': ['Sheet1', 1, 0, 6, 0],
#             'values':     ['Sheet1', 1, 2, 6, 2],
#         })

#         # Add a chart title and some axis labels.
#         chart1.set_title ({'name': 'Results of sample analysis'})
#         chart1.set_x_axis({'name': 'Test number'})
#         chart1.set_y_axis({'name': 'Sample length (mm)'})

#         # Set an Excel chart style. Colors with white outline and shadow.
#         chart1.set_style(10)

#         # Insert the chart into the sheet (with an offset).
#         sheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10})



# PowerAssuranceCheckXlxs('report.ams_report.power_assurance_check.xlsx','ams.pac')
