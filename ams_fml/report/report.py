# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta
import xlwt
from xlsxwriter import *
from cStringIO import StringIO
import base64
from reportlab.pdfgen import canvas
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from odoo.exceptions import  ValidationError

class report_verify(models.Model):
    _name = 'report_verify.verify_fml'

    type = fields.Selection([('fleet','Aircraft'),('engine','Engine'),('auxiliary','Auxiliary'),('propeller','Propeller')], string='Type', default="fleet", required=True)
    fleet_id = fields.Many2one('aircraft.acquisition', string='Aircraft')
    include_attach = fields.Boolean(string='Include Attached Component')
    engine_id = fields.Many2one('engine.spare', string='Engine')
    auxiliary_id = fields.Many2one('auxiliary.spare', string='Auxiliary')
    start_date = fields.Date(string='Start Date', default= lambda *a:(datetime.now() - timedelta(days=(31))).strftime('%Y-%m-%d'))
    end_date = fields.Date(string='End Date', default= lambda *a:datetime.now().strftime('%Y-%m-%d'))
    fml_id = fields.Many2many('ams_fml.log', string="FML ID", compute="_get_vefify")
    all_fleet = fields.Boolean('All Aircraft')
    all_engine = fields.Boolean('All Engine')
    all_auxiliary = fields.Boolean('All Auxiliary')
    all_propeller = fields.Boolean('All Propeller')
    type_print = fields.Selection([('pdf','PDF'),('xls','Excel')], string='Type Print', default="pdf", required=True)
    order = fields.Selection([('date','Date'),('fleet','A/C Reg'),('fml','Fml Number')], string='Order By', default="date", required=True)

    render_data = fields.One2many('report_verify.verify_fml_table','verify_fml_id',string='Render Data', compute=lambda self: self._onchange_comp())

    @api.multi
    @api.constrains('end_date', 'start_date')
    def date_constrains(self):
        for rec in self:
            if rec.end_date < rec.start_date:
                raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))


    def rendering(self):
        search_param = []
        if(self.type == 'fleet'):
            if(self.all_fleet == False):
                search_param.append('&')
                search_param.append(('aircraft_id','=',self.fleet_id.id))
        elif(self.type == 'engine'):
            if(self.all_engine == False and self.engine_id):
                search_param.append('&')
                search_param.append('|')
                search_param.append('|')
                search_param.append('|')
                search_param.append(('engine1_id','=',self.engine_id.id))
                search_param.append(('engine2_id','=',self.engine_id.id))
                search_param.append(('engine3_id','=',self.engine_id.id))
                search_param.append(('engine4_id','=',self.engine_id.id))
            elif(self.all_engine == False):
                search_param.append('&')
                search_param.append(('id','=',False))


        if(self.start_date and self.end_date):
            search_param.append('&')
            search_param.append('&')
            search_param.append(('date','>=',self.start_date)) # tambahkan substring disini
            search_param.append(('date','<=',self.end_date)) # tambahkan substring disini

        search_param.append(('id','!=',False))
        fml = self.env['ams_fml.log'].search(search_param)

        push_data = []
        no = 0
        if self.type == 'fleet':
            for g in fml:
                    
                push_data.append((0,0,{
                    'date' : g.date,
                    'fleet_id' : g.aircraft_id.id,
                    'fml_id' : g.id,
                    'hours_before' : g.current_aircraft_hours,
                    'hours_added' : g.aircraft_hours,
                    'hours_after' : g.current_aircraft_hours + g.aircraft_hours,
                    'cycles_before' : g.current_aircraft_cycles,
                    'cycles_added' : g.aircraft_cycles,
                    'cycles_after' : g.current_aircraft_cycles + g.aircraft_cycles,
                    'rin_before' : g.current_aircraft_rin,
                    'rin_added' : g.aircraft_rin,
                    'rin_after' : g.current_aircraft_rin + g.aircraft_rin,
                    'engine' : g.aircraft_id.engine_type_id.id,
                    'engine2' : g.aircraft_id.engine2_type_id.id,
                    'engine3' : g.aircraft_id.engine3_type_id.id,
                    'engine4' : g.aircraft_id.engine4_type_id.id,
                }))

                if g.aircraft_id.rin_active == False:
                    push_data[no][2]['rin_before'] = 'Not Active'
                    push_data[no][2]['rin_added'] = 'Not Active'
                    push_data[no][2]['rin_after'] = 'Not Active'
                    # print push_data[no][2]
                    no += 1
        elif self.type == 'engine':
            for g in fml:
                    
                push_data.append((0,0,{
                    'date' : g.date,
                    'fleet_id' : g.aircraft_id.id,
                    'fml_id' : g.id,
                    'hours_before' : g.current_aircraft_hours,
                    'hours_added' : g.aircraft_hours,
                    'hours_after' : g.current_aircraft_hours + g.aircraft_hours,
                    'cycles_before' : g.current_aircraft_cycles,
                    'cycles_added' : g.aircraft_cycles,
                    'cycles_after' : g.current_aircraft_cycles + g.aircraft_cycles,
                    'rin_before' : g.current_aircraft_rin,
                    'rin_added' : g.aircraft_rin,
                    'rin_after' : g.current_aircraft_rin + g.aircraft_rin,
                    'engine' : g.aircraft_id.engine_type_id.id,
                    'engine2' : g.aircraft_id.engine2_type_id.id,
                    'engine3' : g.aircraft_id.engine3_type_id.id,
                    'engine4' : g.aircraft_id.engine4_type_id.id,
                }))

                if g.aircraft_id.rin_active == False:
                    push_data[no][2]['rin_before'] = 'Not Active'
                    push_data[no][2]['rin_added'] = 'Not Active'
                    push_data[no][2]['rin_after'] = 'Not Active'
                    no += 1

        self.render_data = push_data



    @api.multi
    def export_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'ams_fml.log'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        if context.get('xls_export'):
            return {'type': 'ir.actions.report.xml',
                    'report_name': 'ams_fml.verify_fml_xls.xlsx',
                    'datas': datas,
                    'name': 'Verify Flight Time'
                    }


    @api.onchange('type')
    def _onchange_type(self):
        self.rendering()
        self.all_fleet = False
        self.all_engine = False
        self.all_auxiliary = False
        self.all_propeller = False
        self.engine_id = []
        self.fleet_id = []
        self.auxiliary_id = []
        self.env["report_verify.verify_fml"].search([]).unlink()
        

    @api.onchange('all_engine')
    def _onchange_all_engine(self):
        self.rendering()
        if self.all_engine == True:
            self.engine_id = []

    @api.onchange('all_fleet')
    def _onchange_all_fleet(self):
        self.rendering()
        if self.all_fleet == True:
            self.fleet_id = []

    @api.onchange('all_auxiliary')
    def _onchange_all_auxiliary(self):
        self.rendering()
        if self.all_auxiliary == True:
            self.auxiliary_id = []

    @api.onchange('fleet_id','engine_id','auxiliary_id')
    def _onchange_comp(self):
        self.rendering()
            

    @api.model
    def _get_vefify(self):
        if self.type == 'fleet' and self.all_fleet == False:
            all_fml = self.env['ams_fml.log'].search([('aircraft_id', '=', self.fleet_id.ids), ('date', '>=', self.start_date), ('date', '<=', self.end_date)])
        elif self.type == 'fleet' and self.all_fleet == True:
            all_fml = self.env['ams_fml.log'].search([('date', '>=', self.start_date), ('date', '<=', self.end_date)])
        elif self.type == 'engine' and self.all_engine == False:
            all_fml = self.env['ams_fml.log'].search(['|', '|', '|', ('engine1_id_text', 'ilike', self.engine_id.name.name),\
                                                                                     ('engine2_id_text', 'ilike', self.engine_id.name.name),\
                                                                                     ('engine3_id_text', 'ilike', self.engine_id.name.name),\
                                                                                     ('engine4_id_text', 'ilike', self.engine_id.name.name),\
                                                                                     ('date', '>=', self.start_date),\
                                                                                     ('date', '<=', self.end_date)])
        elif self.type == 'engine' and self.all_engine == True:
            all_fml = self.env['ams_fml.log'].search([('date', '>=', self.start_date),\
                                                       ('date', '<=', self.end_date)])

        self.fml_id = all_fml
        # print all_fml


    @api.multi
    def print_verify_pdf(self):
        return self.env['report'].get_action(self, 'ams_fml.report_verify_pdf')

class report_verifytable(models.Model):
    _name = 'report_verify.verify_fml_table'

    verify_fml_id = fields.Many2many('report_verify.verify_fml', string="Verify Id")
    
    date = fields.Date(string='Date')
    fleet_id = fields.Many2one('aircraft.acquisition', string='A/C Reg')
    fml_id = fields.Many2one('ams_fml.log', string="Fml Number")

    hours_before = fields.Float(string='Hours Before')
    hours_added = fields.Float(string='Hours Added')
    hours_after = fields.Float(string='Hours After')

    cycles_before = fields.Float(string='Cycles Before')
    cycles_added = fields.Float(string='Cycles Added')
    cycles_after = fields.Float(string='Cycles After')

    rin_before = fields.Char(string='Rin Before')
    rin_added = fields.Char(string='Rin Added')
    rin_after = fields.Char(string='Rin After')

    engine = fields.Many2one('engine.type', 'Engine 1')
    engine2 = fields.Many2one('engine.type', 'Engine 2')
    engine3 = fields.Many2one('engine.type', 'Engine 3')
    engine4 = fields.Many2one('engine.type', 'Engine 4')

class report_verify(models.Model):
    _name = 'report_verify.fleet'

    fleet_id = fields.Many2one('aircraft.acquisition', string='Aircraft')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    
    @api.multi
    @api.constrains('end_date', 'start_date')
    def date_constrains(self):
        for rec in self:
            if rec.end_date < rec.start_date:
                raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))


class VerifyXlsx(ReportXlsx):
    def get_verify(self, data):
        verify = self.env['ams_fml.log'].search([('id', 'in', data['form']['fml_id'])])
        return verify

    def generate_xlsx_report(self, workbook, data, lines):
        verify = self.get_verify(data)
        format1 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'vcenter', 'bold': True})
        format11 = workbook.add_format({'font_size': 12, 'align': 'center', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True})
        format21 = workbook.add_format({'font_size': 10, 'align': 'center', 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': True})
        format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 12})
        format2 = workbook.add_format({'bottom': True, 'top': False, 'font_size': 12})
        font_size_8 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8})
        red_mark = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8,
                                        'bg_color': 'red'})
        justify = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 12})
        format3.set_align('center')
        format2.set_align('center')
        font_size_8.set_align('center')
        justify.set_align('justify')
        format1.set_align('center')
        red_mark.set_align('center')
        col = 0
        col1 = 5
        sheet = workbook.add_worksheet('Verify Flight Time')

        sheet.set_column('B:B', len('All Aircraft'))
        sheet.set_column('C:C', len('Flight Log Number'))
        
        if data['form']['type'] == 'engine':
            sheet.set_column('D:D', len('Serial Number'))

        sheet.merge_range('D1:I2', 'Verify Flight Time', format1)
        sheet.write(0, 0, 'A/C Reg.', format3)

        if data['form']['all_fleet'] == True:
            sheet.write(0, 1, 'All Aircraft', format3)
        elif data['form']['all_fleet'] == False and data['form']['fleet_id'] != False :
            fleet = self.env['aircraft.acquisition'].search([('id', '=', data['form']['fleet_id'])])
            sheet.write(0, 1, fleet.name, format3)        
        elif data['form']['all_engine'] == False and data['form']['engine_id'] != False :
            engine = self.env['engine.spare'].search([('id', '=', data['form']['engine_id'])])
            sheet.write(0, 1, engine.name.name, format3)
        elif data['form']['all_engine'] == True:
            sheet.write(0, 1, 'All Engine', format3)
        elif data['form']['all_auxiliary'] == True:
            sheet.write(0, 1, 'All Auxiliary', format3)
        elif data['form']['all_propeller'] == True:
            sheet.write(0, 1, 'All Propeller', format3)


        sheet.write(1, 0, 'Start Date', format3)
        sheet.write(1, 1, data['form']['start_date'], format3)
        sheet.write(2, 0, 'End Date', format3)
        sheet.write(2, 1, data['form']['end_date'], format3)

        if data['form']['type'] == 'fleet':
            sheet.write(5, 0, 'Flight Date', format2)
            sheet.write(5, 1, 'A/C Reg.', format2)
            # width = len("Flight Log Number")
            # sheet.set_column(5, 2, width)
            sheet.write(5, 2, 'Flight Log Number', format2)
            sheet.merge_range('D5:F5', 'Hours', format2)
            sheet.write(5, 3, 'Before', format2)
            sheet.write(5, 4, 'Added', format2)
            sheet.write(5, 5, 'After', format2)
            sheet.merge_range('G5:I5', 'Cycles', format2)
            sheet.write(5, 6, 'Before', format2)
            sheet.write(5, 7, 'Added', format2)
            sheet.write(5, 8, 'After', format2)
            sheet.merge_range('J5:L5', 'RIN`s', format2)
            sheet.write(5, 9, 'Before', format2)
            sheet.write(5, 10, 'Added', format2)
            sheet.write(5, 11, 'After', format2)

            for obj in verify:
                col =  col + 1
                col1 = col1 + 1
                sheet.write(col1, 0, obj.date, font_size_8)
                sheet.write(col1, 1, str(obj.aircraft_id.name), font_size_8)
                sheet.write(col1, 2, str(obj.name), font_size_8)
                sheet.write(col1, 3, int(obj.aircraft_hours), font_size_8)
                sheet.write(col1, 4, int(0), font_size_8)
                sheet.write(col1, 5, int(obj.aircraft_hours), font_size_8)
                sheet.write(col1, 6, int(obj.aircraft_cycles), font_size_8)
                sheet.write(col1, 7, int(0), font_size_8)
                sheet.write(col1, 8, int(obj.aircraft_cycles), font_size_8)
                sheet.write(col1, 9, int(obj.aircraft_rin), font_size_8)
                sheet.write(col1, 10, int(0), font_size_8)
                sheet.write(col1, 11, int(obj.aircraft_rin), font_size_8)

        elif data['form']['type'] == 'engine':
            sheet.write(5, 0, 'Flight Date', format2)
            sheet.write(5, 1, 'A/C Reg.', format2)
            # width = len("Flight Log Number")
            # sheet.set_column(5, 2, width)
            sheet.write(5, 2, 'Flight Log Number', format2)
            sheet.write(5, 3, 'Serial Number', format2)
            sheet.merge_range('E5:G5', 'Hours', format2)
            sheet.write(5, 4, 'Before', format2)
            sheet.write(5, 5, 'Added', format2)
            sheet.write(5, 6, 'After', format2)
            sheet.merge_range('H5:J5', 'Cycles', format2)
            sheet.write(5, 7, 'Before', format2)
            sheet.write(5, 8, 'Added', format2)
            sheet.write(5, 9, 'After', format2)
            sheet.merge_range('K5:M5', 'RIN`s', format2)
            sheet.write(5, 10, 'Before', format2)
            sheet.write(5, 11, 'Added', format2)
            sheet.write(5, 12, 'After', format2)

            for obj in verify:
                col =  col + 1
                col1 = col1 + 1
                sheet.write(col1, 0, obj.date, font_size_8)
                sheet.write(col1, 1, str(obj.aircraft_id.name), font_size_8)
                sheet.write(col1, 2, str(obj.name), font_size_8)
                sheet.write(col1, 3, int(obj.name), font_size_8)
                sheet.write(col1, 4, int(obj.aircraft_hours), font_size_8)
                sheet.write(col1, 5, int(0), font_size_8)
                sheet.write(col1, 6, int(obj.aircraft_hours), font_size_8)
                sheet.write(col1, 7, int(obj.aircraft_cycles), font_size_8)
                sheet.write(col1, 8, int(0), font_size_8)
                sheet.write(col1, 9, int(obj.aircraft_cycles), font_size_8)
                sheet.write(col1, 10, int(obj.aircraft_rin), font_size_8)
                sheet.write(col1, 11, int(0), font_size_8)
                sheet.write(col1, 12, int(obj.aircraft_rin), font_size_8)


VerifyXlsx('report.ams_fml.verify_fml_xls.xlsx','report_verify.verify_fml')
