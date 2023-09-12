from odoo import fields, models, api, _
from datetime import datetime, timedelta, date
import xlwt
from xlsxwriter import *
from cStringIO import StringIO
import base64
import io
from reportlab.pdfgen import canvas
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from odoo.exceptions import ValidationError
from itertools import groupby
from operator import itemgetter


class TrainingReport(models.Model):
    _name = 'report.training'
    _description = 'Report Training'

    initial 	= fields.Many2one('training.program', string="Project", help='Mandatory')
    type_psw   	= fields.Many2one('aircraft.aircraft', string="A/C Type.", required=True)


    @api.multi
    def export_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'ams.training'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        if context.get('xls_export'):
            return {'type': 'ir.actions.report.xml',
                    'report_name': 'ams_training.training_xls.xlsx',
                    'datas': datas,
                    'name': 'MAINTENANCE PERSONNEL MATRIX TRAINING PROGRAM'
                    }


class ReeportTrain(ReportXlsx):
    def get_lst(self, data):
        # data = self.env['report.training'].search([('id', 'in', data['form']['fml_id'])])
        lst = self.env['ams.training'].search([])
        return lst

    def generate_xlsx_report(self, workbook, data, lines):
        lst = self.get_lst(data)
        fleet = self.env['aircraft.aircraft'].search([('id', '=', data['form']['type_psw'])])
        project = self.env['training.program'].search([], order="name asc")
        data_training = self.env['ams.training'].search([('type_psw', '=', data['form']['type_psw'])], order="initial asc")
        if data['form']['initial']:
            project = self.env['training.program'].search([('id', '=', data['form']['initial'])])
            data_training = self.env['ams.training'].search([('initial','=', data['form']['initial']),('type_psw', '=', data['form']['type_psw'])], order="initial asc")

        format1 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'vcenter', 'bold': True})
        format11 = workbook.add_format({'font_size': 12, 'align': 'center', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True})
        donedue = workbook.add_format({'font_size': 12, 'align': 'center', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True})
        format21 = workbook.add_format({'font_size': 10, 'align': 'center', 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': True})
        formatno = workbook.add_format({'font_size': 10, 'align': 'center', 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': False})
        format3 = workbook.add_format({'bottom': False, 'top': False, 'font_size': 12})
        format2 = workbook.add_format({'bottom': False, 'top': False, 'font_size': 14})
        header1 = workbook.add_format({'bottom': False, 'top': True, 'right': True, 'left': True, 'font_size': 10, 'bold': True, 'bg_color': '#bfbfbf'})
        header2 = workbook.add_format({'bottom': True, 'top': False, 'right': True, 'left': True, 'font_size': 10, 'bold': True, 'bg_color': '#bfbfbf'})
        header3 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 10, 'bold': True, 'bg_color': '#bfbfbf', 'align': 'vcenter'})
        header4 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 10, 'bold': True, 'bg_color': '#ffb03a', 'align': 'vcenter'})
        header5 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 10, 'bold': True, 'bg_color': '#F3FD89', 'align': 'vcenter'})
        header6 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 10, 'bold': True, 'bg_color': '#4ECE27', 'align': 'vcenter'})
        red_mark = workbook.add_format({'bottom': True, 'top': False, 'right': True, 'left': True, 'font_size': 8,
                                        'bg_color': 'red'})
        justify = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 12})
        format3.set_align('center')
        format2.set_align('center')
        header1.set_align('center')
        header2.set_align('center')
        justify.set_align('justify')
        format1.set_align('center')
        red_mark.set_align('center')
        col = 0
        col1 = 5
        # sheet = workbook.add_worksheet('ENG-AV ' + fleet.name)
        # sheet.merge_range('A1:M1', 'MAINTENANCE PERSONNEL MATRIX TRAINING PROGRAM', format2)
        # # sheet.merge_range('A2:M2', fleet.name + ' / ' + fleet.aircraft_type_id.name + ' ' + project.name, format3)
        # sheet.merge_range('A3:M3', str('No. Contract      : CA.14012 - No. 045.1/K/PRESDIR/PAS/2014, ACTIVE : 07 Juli 2014'), format3)
        # sheet.merge_range('A4:A5', str('No.'), header3)
        # sheet.merge_range('D4:E4', str('Amel License'), header1)
        # sheet.merge_range('D5:E5', str('No.'), header2)
        # sheet.merge_range('F4:F5', str('Remarks'), header3)
        # sheet.write(3, 1, 'Authority', header1)
        # sheet.write(4, 1, 'Name', header2)
        # sheet.write(3, 2, 'Remarks', header1)
        # sheet.write(4, 2, 'for Row', header2)
        # # sheet.write(3, 5, 'MNF Initial', header1)
        # # sheet.write(4, 5, 'Training', header2)
        # # sheet.write(3, 6, 'MNF Recurrent', header1)
        # # sheet.write(4, 6, 'Training', header2)
        # # sheet.write(3, 7, 'Human Factor', header1)
        # # sheet.write(4, 7, 'Training', header2)
        # # sheet.write(3, 8, 'DG', header1)
        # # sheet.write(4, 8, 'Training', header2)
        # # sheet.write(3, 9, 'Avsec', header1)
        # # sheet.write(4, 9, 'Training', header2)
        # # sheet.write(3, 10, 'Fire', header1)
        # # sheet.write(4, 10, 'Fighting', header2)
        # # sheet.write(3, 11, 'Engine Run up', header1)
        # # sheet.write(4, 11, 'Training', header2)


        # for x in xrange(0,6):
        #     sheet.write(5, x, '', header4)
        #     sheet.write(5, 4, '24 mo', header4)
        #     sheet.write(5, 5, '', format21)
        
        # sheet.write(5, 1, 'CASR', header4)
            

        # for z in xrange(0,6):
        #     sheet.write(6, z, '', header5)
        #     sheet.write(6, 4, '24 mo', header5)
        #     sheet.write(6, 5, '', format21)
        
        # sheet.write(6, 1, 'OGP', header5)
            
           

        # for y in xrange(0,6):
        #     sheet.write(7, y, '', header6)
        #     sheet.write(7, 4, '24 mo', header6)
        #     sheet.write(7, 5, '', format21)
        
        # sheet.write(7, 1, 'CONTRACT', header6)

        # nomor = 1
        # nomor_ = 9
        # last = 8
        # next = 9
        # for data in data_training:
        #     sheet.merge_range(str('A'+str(int(nomor_))+':A'+str(int(nomor_+1))), str(nomor), formatno)
        #     sheet.merge_range(str('B'+str(int(nomor_))+':B'+str(int(nomor_+1))), str(data.crew.name), format21)
        #     sheet.write(last, 2, 'LAST', format21)
        #     sheet.write(next, 2, 'NEXT', format21)
        #     sheet.merge_range(str('D'+str(int(nomor_))+':D'+str(int(nomor_+1))), str(data.crew.license_no), format21)
        #     sheet.write(last, 4, str(data.training), format21)
        #     day = data.rec*365
        #     sheet.write(next, 4, (datetime.strptime(str(data.training),'%Y-%m-%d')+timedelta(days=(day))).strftime('%d-%m-%Y'), format21)
        #     sheet.write(last, 5, '', format21)
        #     sheet.write(next, 5, '', format21)
        #     last += 2
        #     next += 2
        #     nomor_ += 2 
        #     nomor += 1 

        sheet2 = workbook.add_worksheet(str(fleet.name+"-"+fleet.aircraft_type_id.name))
        prog_training = self.env['training.program'].search([])
        image = self.env['res.company'].search([('id', '=', 1)])
        no_char = 68
        no_col = 3
        image_data = io.BytesIO(base64.b64decode(image.logo_web)) # to convert it to base64 file
        sheet2.insert_image('B2', 'company.png', {'image_data': image_data})
        sheet2.merge_range('A5:X5', 'ENGINEER ~ AVIONIC ~ MECHANIC '+ fleet.name + "-" + fleet.aircraft_type_id.name +' TRAINING DATA ', format2)
        sheet2.merge_range('A8:A12', 'NO', format11)
        sheet2.merge_range('B8:B12', 'NAME', format11)
        sheet2.write(7, 2, 'Aircraft Type', format11)
        sheet2.write(8, 2, fleet.name, format11)
        sheet2.merge_range('C10:C12', 'Initial', format11)
        sheet2.merge_range('D8:O8', 'TRAINING TYPE - MANDATORY', format11)
        sheet2.merge_range('D9:O9', 'RECURRENT EVERY 2 YEAR', format11)
        # sheet2.merge_range('D10:E11', fleet.name, format11)
        # sheet2.write(11, 3, 'DONE', format11)
        # sheet2.write(11, 4, 'DUE', format11)
        no_emp = 12
        row_emp = 0
        row_date = 0
        nomor = 1
        crew = []
        row_name = []
        row = str(chr(no_char)+'10'+":"+chr(no_char+1)+'11')
        row_sms = str(chr(no_char+2)+'10'+":"+chr(no_char+2)+'11')
        row_cmm = str(chr(no_char+3)+'10'+":"+chr(no_char+3)+'11')
        row_trow = str(chr(no_char+4)+'10'+":"+chr(no_char+5)+'11')
        row_company = str(chr(no_char+2)+'9'+":"+chr(no_char+5)+'9')
        row_head = str(chr(no_char+2)+'8'+":"+chr(no_char+5)+'8')

        for data in data_training:
            row_name.append((self.env['ams.training'].search([('id','=',data.id)], order="initial asc"),data.initial.id))
            crew.append((self.env['ams.training'].search([('id','=',data.id)], order="initial asc"),data.crew.name))
        result_crew = {}
        result_name = {}
        sortkeyfn = itemgetter(1)
        crew.sort(key=sortkeyfn)
        row_name.sort(key=sortkeyfn)

    
        for key,valuesiter in groupby(crew, key=sortkeyfn):
            result_crew[key] = list(v[0] for v in valuesiter)

        for key2,valuesiter2 in groupby(row_name, key=sortkeyfn):
            result_name[key2] = list(v[0] for v in valuesiter2)

        for d in result_name:
            name = self.env['training.program'].search([('id','=',d)], order="name asc")
            row = str(chr(no_char)+'10'+":"+chr(no_char+1)+'11')
            row_sms = str(chr(no_char+2)+'10'+":"+chr(no_char+2)+'11')
            row_cmm = str(chr(no_char+3)+'10'+":"+chr(no_char+3)+'11')
            row_trow = str(chr(no_char+4)+'10'+":"+chr(no_char+5)+'11')
            row_company = str(chr(no_char+2)+'9'+":"+chr(no_char+5)+'9')
            row_head = str(chr(no_char+2)+'8'+":"+chr(no_char+5)+'8')
            sheet2.merge_range(row, name.name, format11)
            sheet2.write(11, no_col, 'DONE', format11)
            sheet2.write(11, no_col+1, 'DUE', format11)
            no_col +=2
            no_char +=2
        

        """ DATA TRAINING"""
        today = datetime.now()
        formatbiasa = workbook.add_format({'font_size': 12, 'align': 'center', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True})
        formatkuning = workbook.add_format({'font_size': 12, 'align': 'center', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True})
        formatmerah = workbook.add_format({'font_size': 12, 'align': 'center', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True})
        daysRemaining = 90
        remaining = (datetime.strptime(str(date.today()),'%Y-%m-%d') - timedelta(days=daysRemaining)).strftime('%d-%m-%Y')
        listD = len(result_crew)
        deret = 12
        for x in sorted(result_crew):
            sheet2.write(no_emp, row_emp, nomor, format11)
            sheet2.write(no_emp, row_emp+1, x, format11)
            sheet2.write(no_emp, row_emp+2, '-', format11)
            for y in result_crew[x]:
                due  = (datetime.strptime(str(y.training),'%Y-%m-%d')+timedelta(days=int(y.rec*365))).strftime('%d-%m-%Y')
                now  = (datetime.strptime(str(date.today()),'%Y-%m-%d')+timedelta(days=int(1))).strftime('%d-%m-%Y')
                done = (datetime.strptime(str(y.training),'%Y-%m-%d')).strftime('%d-%m-%Y')
                for c in result_name:
                    if y.initial.id == c:
                        if result_crew[x][0].initial.id == y.initial.id:
                            col_deret = 0
                            if done <= remaining :
                                donedue = formatkuning
                            if done >= remaining :
                                donedue = formatmerah
                            if due <= remaining :
                                donedue = formatkuning
                            if due >= remaining :
                                donedue = formatmerah
                            sheet2.write(deret, col_deret+3, done, donedue)
                            sheet2.write(deret, col_deret+4, due, donedue)
                        else:
                            col_deret +=2
                            deret -= 1
                            if done <= remaining :
                                donedue = formatkuning
                            if done >= remaining :
                                donedue = formatmerah
                            if due <= remaining :
                                donedue = formatkuning
                            if due >= remaining :
                                donedue = formatmerah                          
                            sheet2.write(deret, col_deret+3, done, donedue)
                            sheet2.write(deret, col_deret+4, due, donedue)
                        deret += 1
            nomor   += 1
            no_emp  += 1
                            
        sheet2.merge_range(row_head, "", format11)
        sheet2.merge_range(row_company, "COMPANY", format11)
        # sheet2.merge_range(row_sms, "SMS", format11)
        # sheet2.merge_range(row_cmm, "CMM", format11)
        # sheet2.merge_range(row_trow, "Towing \n Pushback", format11)
        # sheet2.write(11, no_col, 'DONE', format11)
        # sheet2.write(11, no_col+1, 'DONE', format11)
        # sheet2.write(11, no_col+2, 'DONE', format11)
        # sheet2.write(11, no_col+3, 'DUE', format11)




ReeportTrain('report.ams_training.training_xls.xlsx','report.training')
