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

class Manualchanges(models.Model):
    _name = 'ams.manual_changes.report'
    _description = 'Manual Changes Report'

    all_fleet = fields.Boolean('All', default=True)
    all_engine = fields.Boolean('All', default=True)
    all_auxiliary = fields.Boolean('All', default=True)
    all_propeller = fields.Boolean('All', default=True)
    all_part = fields.Boolean('All', default=True)

    none_fleet = fields.Boolean('None')
    none_engine = fields.Boolean('None')
    none_auxiliary = fields.Boolean('None')
    none_propeller = fields.Boolean('None')
    none_part = fields.Boolean('None')


    fleet_id = fields.Many2one('aircraft.acquisition', string='Aircraft')
    engine_id = fields.Many2one('engine.type', string='Engine')
    auxiliary_id = fields.Many2one('auxiliary.type', string='Auxiliary')
    propeller_id = fields.Many2one('propeller.type', string='Propeller')
    part_id = fields.Many2one('ams.component.part', string='Part')

    start_date = fields.Date('Starting Date')
    end_date = fields.Date('Ending Date')

    mc_id = fields.One2many('ams.manual_changes', 'rp_id', compute=lambda self: self._onchange_comp())

    @api.multi
    @api.constrains('end_date', 'start_date')
    def date_constrains(self):
        for rec in self:
            if rec.end_date < rec.start_date:
                raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))

    @api.multi
    def print_manual_changes_reports(self):
        return self.env['report'].get_action(self, 'ams_report.ams_manual_changes_pdf')



    def rendering(self):
        search_param = []
        no = 0 
        no_date = 0 
        if self.none_fleet != True:
            if(self.all_fleet == False):
                search_param.append(('fleet_id','=',self.fleet_id.id))
                no += 1
            else:
                search_param.append(('fleet_id','!=',False))
                no += 1           
                 
        if self.none_engine != True:
            if(self.all_engine == False):
                search_param.append(('engine_id','=',self.engine_id.id))
                no += 1
            else:
                search_param.append(('engine_id','!=',False))
                no += 1

        if self.none_auxiliary != True:
            if(self.all_auxiliary == False):
                search_param.append(('auxiliary_id','=',self.auxiliary_id.id))
                no += 1
            else:
                search_param.append(('auxiliary_id','!=',False))
                no += 1
                
        if self.none_propeller != True:
            if(self.all_propeller == False):
                search_param.append(('propeller_id','=',self.propeller_id.id))
                no += 1
            else:
                search_param.append(('propeller_id','!=',False))
                no += 1

        if self.none_part != True:
            if(self.all_part == False):
                search_param.append(('part_id','=',self.part_id.id))
                no += 1
            else:
                search_param.append(('part_id','!=',False))
                no += 1 
        if self.start_date != False:
            search_param.append('&')
            search_param.append(('create_date','>=',self.start_date))
            no_date += 1
        if self.end_date != False:
            search_param.append(('create_date','<=',self.end_date))
            no_date += 1

        search_domain = []
        for x in xrange(1,no):
            search_domain.append('|')
        if self.start_date != False:
            search_domain.append('&')
        for y in search_param:
            search_domain.append(y)
        manual_changes = self.env['ams.manual_changes'].search(search_domain)

        push_data = []
        for g in manual_changes:
                
            push_data.append((0,0,{
                'fleet_id' : g.fleet_id.id,
                'engine_id' : g.engine_id.id,
                'auxiliary_id' : g.auxiliary_id.id,
                'propeller_id' : g.propeller_id.id,
                'part_id' : g.part_id.id,
                'current_hours' : g.current_hours,
                'current_cycles' : g.current_cycles,
                'current_rin' : g.current_rin,
                'hours' : g.hours,
                'cycles' : g.cycles,
                'rin' : g.rin,
                'timestamp' : g.timestamp,
                'employee' : g.employee.id,

            }))
        self.mc_id = push_data

    @api.onchange('fleet_id','engine_id','auxiliary_id','propeller_id','part_id','all_fleet','all_engine','all_auxiliary','all_propeller','all_part','none_fleet','none_engine','none_auxiliary','none_propeller','none_part')
    def _onchange_comp(self):
        self.rendering()

    @api.onchange('all_fleet','all_engine','all_auxiliary','all_propeller','all_part')
    def _onchange_all(self):
        if self.all_fleet == True:
            self.none_fleet = False
            self.fleet_id = False

        if self.all_engine == True:
            self.none_engine = False

        if self.all_auxiliary == True:
            self.none_auxiliary = False

        if self.all_propeller == True:
            self.none_propeller = False

        if self.all_part == True:
            self.none_part = False

    @api.onchange('none_fleet','none_engine','none_auxiliary','none_propeller','none_part')
    def _onchange_none(self):
        if self.none_fleet == True:
            self.all_fleet = False

        if self.none_engine == True:
            self.all_engine = False

        if self.none_auxiliary == True:
            self.all_auxiliary = False

        if self.none_propeller == True:
            self.all_propeller = False

        if self.none_part == True:
            self.all_part = False



    @api.multi
    def export_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'ams.manual_changes'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        if context.get('xls_export'):
            return {'type': 'ir.actions.report.xml',
                    'report_name': 'ams_report.manual_changes_xls.xlsx',
                    'datas': datas,
                    'name': 'Verify Flight Time'
                    }


class ManualChangesXls(ReportXlsx):
    def get_manual_changes(self, data):
        manual = self.env['ams.manual_changes'].search([('id', 'in', data['form']['mc_id'])])
        return manual

    def generate_xlsx_report(self, workbook, data, lines):
        manual = self.get_manual_changes(data)
        print '################'

        # format1 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'vcenter', 'bold': True})
        # format11 = workbook.add_format({'font_size': 12, 'align': 'center', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True})
        # format21 = workbook.add_format({'font_size': 10, 'align': 'center', 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': True})
        # format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 12})
        # format2 = workbook.add_format({'bottom': True, 'top': False, 'font_size': 12})
        # font_size_8 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8})
        # red_mark = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8,'bg_color': 'red'})
        # justify = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 12})
        # format3.set_align('center')
        # format2.set_align('center')
        # font_size_8.set_align('center')
        # justify.set_align('justify')
        # format1.set_align('center')
        # red_mark.set_align('center')
        # col = 0
        # col1 = 5
        sheet = workbook.add_worksheet('Manual Changes')
        # sheet.merge_range('D1:I2', 'Manual Changes', format1)
        # # sheet.write(0, 0, ' ', format3)
        # # sheet.write(0, 1, 'Previous Value', format3)
        # # sheet.write(0, 2, 'Changes Value', format3)
        # # sheet.write(0, 3, 'Difference', format3)
        # # sheet.write(0, 4, 'Date Time', format3)
        # # sheet.write(0, 5, 'Employee', format3)

ManualChangesXls('report.ams_report.manual_changes_xls.xlsx','ams.manual_changes.report')


class ManualchangesInheritBase(models.Model):
    _inherit = 'ams.manual_changes'

    rp_id = fields.Many2one('ams.manual_changes.report')