from odoo import models, fields, api, _
import xlwt
from xlsxwriter import *
from cStringIO import StringIO
import base64
import re
from reportlab.pdfgen import canvas
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from datetime import datetime, timedelta, date
from calendar import monthrange
from dateutil.relativedelta import relativedelta
from odoo.exceptions import  ValidationError
import collections

def makehash():
    return collections.defaultdict(makehash)

class OilReport(models.Model):
    _name = 'oil.report'
    _description = 'Oil Report'

    model_ac    = fields.Many2one('aircraft.aircraft', string="Aircraft")
    date       = fields.Date(string="Year", default=datetime.now())
    data_id    = fields.Many2many('ams_fml.log', compute=lambda self: self._compute_data())

    @api.onchange('model_ac')
    def _compute_data(self):
        pesawat = self.env['aircraft.acquisition'].search([('aircraft_name','=', self.model_ac.id)]).ids
        year = self.date.split('-')[0]
        self.data_id = self.env['ams_fml.log'].search([('aircraft_id','in',pesawat),('date', '>=', str(year)+'-01-01'),('date', '<=', str(year)+'-12-30')], order="aircraft_id ASC")


    @api.multi
    def export_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'oil.report'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
                
        if context.get('xls_export'):
            return {'type': 'ir.actions.report.xml',
                    'report_name': 'ams_report.oil_report.xlsx',
                    'datas': datas,
                    'name': 'Oil Report'
                    }

class OilReportXlxs(ReportXlsx):
    def get_tanggal(self, year, bln, tgl, ac, eng):
        gt = 0
        if eng == 1:
            oil_data = self.env['ams_fml.log'].search(['&','&',('aircraft_id', '=', int(ac)),('oil1_add','=',True),'&',('date', '>=', date(int(year), int(bln), int(tgl)).isoformat()),('date', '<=', date(int(year), int(bln), int(tgl)).isoformat())], order="aircraft_id ASC")
        if eng == 2:
            oil_data = self.env['ams_fml.log'].search(['&','&',('aircraft_id', '=', int(ac)),('oil2_add','=',True),'&',('date', '>=', date(int(year), int(bln), int(tgl)).isoformat()),('date', '<=', date(int(year), int(bln), int(tgl)).isoformat())], order="aircraft_id ASC")
        if eng == 3:
            oil_data = self.env['ams_fml.log'].search(['&','&',('aircraft_id', '=', int(ac)),('oil3_add','=',True),'&',('date', '>=', date(int(year), int(bln), int(tgl)).isoformat()),('date', '<=', date(int(year), int(bln), int(tgl)).isoformat())], order="aircraft_id ASC")
        if eng == 4:
            oil_data = self.env['ams_fml.log'].search(['&','&',('aircraft_id', '=', int(ac)),('oil4_add','=',True),'&',('date', '>=', date(int(year), int(bln), int(tgl)).isoformat()),('date', '<=', date(int(year), int(bln), int(tgl)).isoformat())], order="aircraft_id ASC")
        get = len(oil_data)
        return get


    def fhs_data(self, ac, bln, year):
        tgl = monthrange(int(year), int(bln))[1]
        oil_data = self.env['ams_fml.log'].search([('aircraft_id', '=', int(ac)),'&',('date', '>=', date(int(year), int(bln), int(1)).isoformat()),('date', '<=', date(int(year), int(bln), int(tgl)).isoformat())], order="aircraft_id ASC")
        fh = 0
        for x in oil_data:
            fh += x.aircraft_hours
        return fh


    def oil_data(self, data):
        data_id = {}
        pesawat = self.env['aircraft.acquisition'].search([('aircraft_name','=', data['form']['model_ac'])])
        year = data['form']['date'].split('-')[0]
        oil_data = self.env['ams_fml.log'].search(['|','&',('id', 'in', data['form']['data_id']),('date', '>=', str(year)+'-01-01'),('date', '<=', str(year)+'-12-30')], order="aircraft_id ASC")
        for x in pesawat:
            data_id.update({x.name : []})
            for y in oil_data:
                if x.name == y.aircraft_id.name:
                    data_id[str(x.name)].append({'name' : y.name, 'ac' : y.aircraft_id.id, 'date' : y.date, 'engine1': y.oil1_add,'engine2': y.oil2_add, 'engine3': y.oil3_add, 'engine4': y.oil4_add, 'fh': y.aircraft_hours})
        return data_id

    def generate_xlsx_report(self, workbook, data, lines):
        oil = self.oil_data(data)
        format1 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'vcenter', 'bold': True})
        format11 = workbook.add_format({'font_size': 11, 'align': 'center', 'right': True, 'left': True, 'bottom': True, 'top': True, 'align': 'vcenter', 'bold': True})
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
        format11.set_align('center')
        red_mark.set_align('center')
        col = 0
        year = data['form']['date'].split('-')[0]
        mon_ = data['form']['date'].split('-')[1]
        tgl_ = data['form']['date'].split('-')[2]
        pesawat = self.env['aircraft.aircraft'].search([('id','=', data['form']['model_ac'])])
        ac = self.env['aircraft.acquisition'].search([('aircraft_name','=', data['form']['model_ac'])])
        sheet = makehash()

        for y in oil:
            if oil[y] != []:
                sheet[y] = workbook.add_worksheet(y)
                sheet[y].set_column('A:A', 9)
                sheet[y].set_column('B:B', 6.5)
                sheet[y].set_column('C:C', 4)
                sheet[y].set_column('D:D', 4)
                sheet[y].set_column('E:E', 4)
                sheet[y].set_column('F:F', 4)
                sheet[y].set_column('G:G', 4)
                sheet[y].set_column('H:H', 4)
                sheet[y].set_column('I:I', 4)
                sheet[y].set_column('J:J', 4)
                sheet[y].set_column('K:K', 4)
                sheet[y].set_column('L:L', 4)
                sheet[y].set_column('M:M', 4)
                sheet[y].set_column('N:N', 4)
                sheet[y].set_column('O:O', 4)
                sheet[y].set_column('P:P', 4)
                sheet[y].set_column('Q:Q', 4)
                sheet[y].set_column('R:R', 4)
                sheet[y].set_column('S:S', 4)
                sheet[y].set_column('T:T', 4)
                sheet[y].set_column('U:U', 4)
                sheet[y].set_column('V:V', 4)
                sheet[y].set_column('W:W', 4)
                sheet[y].set_column('X:X', 4)
                sheet[y].set_column('Y:Y', 4)
                sheet[y].set_column('Z:Z', 4)
                sheet[y].set_column('AA:AA', 4)
                sheet[y].set_column('AB:AB', 4)
                sheet[y].set_column('AC:AC', 4)
                sheet[y].set_column('AD:AD', 4)
                sheet[y].set_column('AE:AE', 4)
                sheet[y].set_column('AF:AF', 4)
                sheet[y].set_column('AG:AG', 4)
                sheet[y].set_column('AH:AH', 6)
                sheet[y].set_column('AI:AI', 6)
                sheet[y].set_column('AJ:AJ', 6)
                sheet[y].merge_range('A1:AJ2', str('OIL CONSUMPTION '+str(pesawat.name)+' YEAR '+str(year)), format1)
                
                col1 = 4
                for x in xrange(1,13):
                    mon = ''
                    if x ==1:
                        mon = str('JAN-'+str(year))
                    if x ==2:
                        mon = str('FEB-'+str(year))
                    if x ==3:
                        mon = str('MAR-'+str(year))
                    if x ==4:
                        mon = str('APR-'+str(year))
                    if x ==5:
                        mon = str('MEI-'+str(year))
                    if x ==6:
                        mon = str('JUN-'+str(year))
                    if x ==7:
                        mon = str('JUL-'+str(year))
                    if x ==8:
                        mon = str('AGT-'+str(year))
                    if x ==9:
                        mon = str('SEP-'+str(year))
                    if x ==10:
                        mon = str('OKT-'+str(year))
                    if x ==11:
                        mon = str('NOV-'+str(year))
                    if x ==12:
                        mon = str('DES-'+str(year))
                    sheet[y].write(col1, 0, mon, format11)
                    sheet[y].write(col1+1, 0, 'A/C REG', format11)

                    sheet[y].merge_range('A'+str(col1+3)+':A'+str(col1+6), str(y), format11)
                    sheet[y].write(col1+2, 0, y, font_size_8)
                    sheet[y].write(col1+1, 1, 'ENGINE', format11)
                    ttt = monthrange(int(year), int(x))[1]
                    total_1 = 0
                    total_2 = 0
                    total_3 = 0
                    total_4 = 0
                    ttl = 0
                    ac = self.env['aircraft.acquisition'].search([('name','=',y)], limit=1)
                    fh = self.fhs_data(ac, x, year)
                    for ass in xrange(0,ttt):
                        eng1 = self.get_tanggal(year, x, ass+1, ac, 1)
                        eng2 = self.get_tanggal(year, x, ass+1, ac, 2)
                        eng3 = self.get_tanggal(year, x, ass+1, ac, 3)
                        eng4 = self.get_tanggal(year, x, ass+1, ac, 4)
                        sheet[y].write(col1+1, ass+2, ass+1, format11)
                        sheet[y].write(col1+2, ass+2, eng1, format11)
                        sheet[y].write(col1+3, ass+2, eng2, format11)                            
                        sheet[y].write(col1+4, ass+2, eng3, format11)                                
                        sheet[y].write(col1+5, ass+2, eng4, format11)
                        for l in xrange(1,5):
                            sheet[y].write(col1+1+l, 1, l, format11)
                        ttl = ass+2
                        total_1 += eng1
                        total_2 += eng2
                        total_3 += eng3
                        total_4 += eng4
                    sheet[y].write(col1+1, ttl+1, 'Total', format11)
                    sheet[y].write(col1+2, ttl+1, total_1, format11)
                    sheet[y].write(col1+3, ttl+1, total_2, format11)
                    sheet[y].write(col1+4, ttl+1, total_3, format11)
                    sheet[y].write(col1+5, ttl+1, total_4, format11)
  
                    sheet[y].write(col1+1, ttl+2, 'Fh', format11)
                    sheet[y].write(col1+2, ttl+2, fh, format11)
                    sheet[y].write(col1+3, ttl+2, fh, format11)
                    sheet[y].write(col1+4, ttl+2, fh, format11)
                    sheet[y].write(col1+5, ttl+2, fh, format11)

                    sheet[y].write(col1+1, ttl+3, 'Qt/Hrs', format11)
                    if fh != 0:
                        sheet[y].write(col1+2, ttl+3, (total_1/fh), format11)
                        sheet[y].write(col1+3, ttl+3, (total_2/fh), format11)
                        sheet[y].write(col1+4, ttl+3, (total_3/fh), format11)
                        sheet[y].write(col1+5, ttl+3, (total_4/fh), format11)
                    else:
                        sheet[y].write(col1+2, ttl+3, (0), format11)
                        sheet[y].write(col1+3, ttl+3, (0), format11)
                        sheet[y].write(col1+4, ttl+3, (0), format11)
                        sheet[y].write(col1+5, ttl+3, (0), format11)
                    col1 += 6            

OilReportXlxs('report.ams_report.oil_report.xlsx','report.tools.movement')
