from odoo import models, fields, api, _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import xlwt
from xlsxwriter import *
from cStringIO import StringIO
import base64
import math
from reportlab.pdfgen import canvas
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from odoo.exceptions import  ValidationError    
import logging
_logger = logging.getLogger(__name__)

class inheritMaintenanceDueReport(models.Model):
    _inherit = 'maintenance.due.report'

    sumcomp = fields.Integer()
    
class MaintenancePlan(models.Model):
    _name = 'maintenance.plan.report'
    _description = 'ADC Report'

    all         = fields.Boolean(string='All', default=True)
    fleet_id    = fields.Many2one('aircraft.acquisition', string='Aircraft')
    start_date    = fields.Date(string='Start Date' , default=datetime.now(), required=True)
    end_date  = fields.Date(string='End Date', default=datetime.now() + relativedelta(days=365), required=True)
    mp_id       = fields.Many2many('maintenance.due.report', compute='_onchange_fleet_id')

    @api.multi
    @api.constrains('end_date', 'start_date')
    def date_constrains(self):
        for rec in self:
            if rec.end_date < rec.start_date:
                raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))

    @api.onchange('fleet_id')
    def _onchange_fleet_id(self):
        if self.all:
            self.mp_id = self.env['maintenance.due.report'].search([])
        if self.fleet_id:
            self.mp_id = self.env['maintenance.due.report'].search([('fleet_id','=',self.fleet_id.id)])

    @api.multi
    def print_maintenance_planing_reports(self):
        return self.env['report'].get_action(self, 'ams_report.report_maintenance_plan')

    @api.multi
    def export_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'maintenance.plan.report'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        if context.get('xls_export'):
            return {'type': 'ir.actions.report.xml',
                    'report_name': 'ams_report.maintenance_planning_report.xlsx',
                    'datas': datas,
                    'name': 'Maintenance Planning Report'
                    }


class MPReportXls(ReportXlsx):
    def get_data(self, data):
        search_param = []
        if data['form']['all'] == False:
            search_param.append(('fleet_id', '=', data['form']['fleet_id']))
        if data['form']['start_date'] and data['form']['end_date']:
            search_param.append(('create_date', '>=', data['form']['start_date']))
            search_param.append(('create_date', '<=', data['form']['end_date']))            
        mp_data = self.env['maintenance.due.report'].search(search_param)
        push_data = []
        pesawat_id = []
        for x in mp_data:
            pesawat_id.append(x.fleet_id.id)
            push_data.append((0,0,{
                'fleet'         : x.fleet_id,
                'aux'           : x.fleet_id.auxiliary_type_id,
                'date_man'      : x.fleet_id.date_manufacture,
                'ac_tot'        : x.fleet_id.total_landings,
                'engine'        : x.fleet_id.engine_type_id,
                'engine_tt'     : x.fleet_id.engine_type_id.engine_tsn,
                'propeller'     : x.fleet_id.propeller_type_id,
                'engine2'       : x.fleet_id.engine2_type_id,
                'engine2_tt'    : x.fleet_id.engine2_type_id.engine_tsn,
                'propeller2'    : x.fleet_id.propeller2_type_id,
                'engine3'       : x.fleet_id.engine3_type_id,
                'engine3_tt'    : x.fleet_id.engine3_type_id.engine_tsn,
                'propeller3'    : x.fleet_id.propeller3_type_id,
                'engine4'       : x.fleet_id.engine4_type_id,
                'engine4_tt'    : x.fleet_id.engine4_type_id.engine_tsn,
                'propeller4'    : x.fleet_id.propeller4_type_id,
            }))
        AC = self.env['aircraft.acquisition'].search([('id','in',pesawat_id)])
        if data['form']['all'] == False:
            AC = self.env['aircraft.acquisition'].search([('id','in',pesawat_id),('id','=',data['form']['fleet_id']),('create_date', '>=', data['form']['start_date']),('create_date', '<=', data['form']['end_date'])])
        _logger.warning(AC)
        return AC
    
    def __datetime(self, date_str):
        return datetime.strptime(date_str, "%d/%m/%Y")

    def generate_xlsx_report(self, workbook, data, lines):
        mp_data = self.get_data(data)
        format1 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'vcenter', 'bold': True})
        format11 = workbook.add_format({'font_size': 12, 'align': 'top', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True, 'text_wrap': True})
        format12 = workbook.add_format({'font_size': 12, 'align': 'left', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': False})
        formatdate = workbook.add_format({'font_size': 12, 'align': 'left', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': False, 'num_format': 'dd/mm/yyyyy'})
        format21 = workbook.add_format({'font_size': 13, 'align': 'center', 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': True})
        format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 12})
        format2 = workbook.add_format({'bottom': True, 'top': False, 'font_size': 12})
        font_size_8 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8})
        green_mark = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8, 'bg_color': 'green'})
        justify = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 12})
        format3.set_align('center')
        format2.set_align('center')
        font_size_8.set_align('center')
        justify.set_align('justify')
        format1.set_align('center')
        green_mark.set_bg_color('#76B76A')
        col = 0
        col1 = 4
        sheet = workbook.add_worksheet('Maintenance Planning Report')
        sheet.set_column('A:A', 21)
        sheet.set_column('B:B', 21)
        sheet.set_column('C:C', 7)
        sheet.set_column('D:D', 7)
        sheet.set_column('E:E', 10)
        sheet.set_column('F:F', 12)
        sheet.set_column('G:G', 4)
        sheet.set_column('H:H', 4)
        sheet.set_column('I:I', 4)
        sheet.set_column('J:J', 4)
        sheet.set_column('K:K', 4)
        sheet.set_column('L:L', 4)
        sheet.set_column('M:M', 4)
        sheet.set_column('N:N', 4)
        sheet.set_column('O:O', 4)
        sheet.set_column('P:P', 4)
        sheet.set_column('Q:Q', 4)
        sheet.set_column('R:R', 4)

        sheet.merge_range('A1:R2', 'Maintenance Planning Report', format1)
        sheet.merge_range('A3:A4', 'A/C REG.', format21)
        sheet.merge_range('B3:B4', 'DESCIPTION', format21)
        sheet.merge_range('C3:C4', 'DUE AT', format21)
        sheet.merge_range('D3:D4', 'REM.', format21)
        sheet.merge_range('E3:E4', 'EST.DATE', format21)
        sheet.merge_range('F3:F4', 'REM. BY DAY', format21)
        sheet.merge_range('G3:R3', str(datetime.today().strftime('%d/%m/%Y')), format21)
        sheet.write(3, 6,  'JAN', format21)
        sheet.write(3, 7,  'FEB', format21)
        sheet.write(3, 8,  'MAR', format21)
        sheet.write(3, 9,  'APR', format21)
        sheet.write(3, 10, 'MEI', format21)
        sheet.write(3, 11, 'JUN', format21)
        sheet.write(3, 12, 'JUL', format21)
        sheet.write(3, 13, 'AUG', format21)
        sheet.write(3, 14, 'SEP', format21)
        sheet.write(3, 15, 'OKT', format21)
        sheet.write(3, 16, 'NOV', format21)
        sheet.write(3, 17, 'DES', format21)
        
        today = datetime.now()
        row = 6
        no1 = 4
        first_row = 4
        # ro = self.env['aircraft.acquisition'].search([])
        # for g in ro:
        #     # get fleet utilz
        #     daily_utilz = self.env['ams.daily'].search(['&',('fleet_id','=',g.id),('is_active','=',True)])
        #     for i in g.mapped('component_ids'):
        #         last_date = False
        #         for n in i.mapped('serfice_life'):
        #             if(n.is_major and n.action_type not in ['oncondition','conditionmonitoring']):
        #                 if(n.unit in ['days','month','year']):
        #                     due_date = n.next_date
        #                 elif(n.unit == 'hours'):
        #                     daysRemaining = math.floor( (0-n.remaining) / daily_utilz.aircraft_hours)
        #                     due_date = datetime.strptime(today.strftime("%Y-%m-%d"), '%Y-%m-%d') - timedelta(days=daysRemaining)
        #                 elif(n.unit == 'cycles'):
        #                     daysRemaining = math.floor( (0-n.remaining) / daily_utilz.aircraft_cycles)
        #                     due_date = datetime.strptime(today.strftime("%Y-%m-%d"), '%Y-%m-%d') - timedelta(days=daysRemaining)
        #                 elif(n.unit == 'rin'):
        #                     daysRemaining = math.floor( (0-n.remaining) / daily_utilz.aircraft_rin)
        #                     due_date = datetime.strptime(today.strftime("%Y-%m-%d"), '%Y-%m-%d') - timedelta(days=daysRemaining)
                        
        #                 if(last_date == False or last_date > due_date):
        #                     last_date = due_date

        #         if(last_date != False):
        #             # for x in xrange(2,18):
        #             #     sheet.write(no1, x, '', format11)
        #             # sheet.write(no1, int(est_date.split('/')[1])+5, '\n', green_mark)

        #             sheet.write(no1, 1, i.product_id.name, format12)
        #             sheet.write(no1, 2, n.next_text, format12)
        #             sheet.write(no1, 3, n.remaining, format12)
        #             sheet.write(no1, 4, str(due_date), formatdate)
        #             sheet.write(no1, 5, str(str((datetime.strptime(str(due_date), '%Y-%m-%d') - datetime.strptime(today.strftime("%Y-%m-%d"), '%Y-%m-%d')).days)+' Days'), format12)
        #             no1 +=1
        #     if(no1 > first_row+1):
        #         sheet.merge_range('A'+str(first_row+1)+':A'+str(no1), g.name, format11)
        #     first_row = no1


        ac = mp_data


        for x in ac:
            if len(x.component_ids) != 0:
                if x.date_manufacture:
                    date_man = datetime.strptime(x.date_manufacture, '%Y-%m-%d').strftime('%d/%m/%Y')
                else:
                    date_man = 'None'

                sheet.merge_range('A'+str(no1+1)+':A'+str(no1+7), \
                                ''+str(x.name)+''\
                                +'\n Date : '+str(date_man)\
                                +'\n A/C TT  : '+str(x.total_landings)\
                                +'\n ENG#1 TT  : '+str(x.engine_type_id.engine_tsn)\
                                +'\n ENG#2 TT  : '+str(x.engine2_type_id.engine_tsn)\
                                +'\n ENG#3 TT  : '+str(x.engine3_type_id.engine_tsn)\
                                +'\n ENG#4 TT  : '+str(x.engine4_type_id.engine_tsn)\
                                , format11)
                """ COMPONENT """

                for cm in x.component_ids:
                    for sv in cm.serfice_life:
                        if sv.is_major:
                            est_date = datetime.strptime(self.env['ams.mtr'].countDate(x.id, sv.id), '%Y-%m-%d').strftime("%d/%m/%Y")
                            rem_date = self.__datetime(str(est_date)) - self.__datetime(str(datetime.today().strftime('%d/%m/%Y')))
                            for a in xrange(2,18):
                                sheet.write(no1, a, '', format11)
                            sheet.write(no1, int(est_date.split('/')[1])+5, '\n', green_mark)
                            sheet.write(no1, 1, cm.product_id.name, format12)
                            sheet.write(no1, 2, sv.next_text, format12)
                            sheet.write(no1, 3, sv.remaining, format12)
                            sheet.write(no1, 4, str(est_date), formatdate)
                            sheet.write(no1, 5, str(str(rem_date.days)+' Days'), format12)
                            no1 += 1
                        for scm in cm.sub_part_ids:
                            for ssv in scm.serfice_life:
                                if ssv.is_major:
                                    est_date = datetime.strptime(self.env['ams.mtr'].countDate(x.id, ssv.id), '%Y-%m-%d').strftime("%d/%m/%Y")
                                    rem_date = self.__datetime(str(est_date)) - self.__datetime(str(datetime.today().strftime('%d/%m/%Y')))
                                    for a in xrange(2,18):
                                        sheet.write(no1, a, '', format11)
                                    sheet.write(no1, int(est_date.split('/')[1])+5, '\n', green_mark)
                                    sheet.write(no1, 1, scm.product_id.name, format12)
                                    sheet.write(no1, 2, ssv.next_text, format12)
                                    sheet.write(no1, 3, ssv.remaining, format12)
                                    sheet.write(no1, 4, str(est_date), formatdate)
                                    sheet.write(no1, 5, str(str(rem_date.days)+' Days'), format12)
                                    no1 += 1

                """ Engine """
                for eng1 in x.engine_type_id:
                    sheet.write(no1, 1, eng1.name, format11)
                    no1 += 1
                    for cm in eng1.component_ids:
                        for sv in cm.serfice_life:
                            if sv.is_major:
                                est_date = datetime.strptime(self.env['ams.mtr'].countDate(x.id, sv.id), '%Y-%m-%d').strftime("%d/%m/%Y")
                                rem_date = self.__datetime(str(est_date)) - self.__datetime(str(datetime.today().strftime('%d/%m/%Y')))
                                for a in xrange(2,18):
                                    sheet.write(no1, a, '', format11)
                                sheet.write(no1, int(est_date.split('/')[1])+5, '\n', green_mark)
                                sheet.write(no1, 1, cm.product_id.name+' '+eng1.name, format12)
                                sheet.write(no1, 2, sv.next_text, format12)
                                sheet.write(no1, 3, sv.remaining, format12)
                                sheet.write(no1, 4, str(est_date), formatdate)
                                sheet.write(no1, 5, str(str(rem_date.days)+' Days'), format12)
                                no1 += 1
                            for scm in cm.sub_part_ids:
                                for ssv in scm.serfice_life:
                                    if ssv.is_major:
                                        est_date = datetime.strptime(self.env['ams.mtr'].countDate(x.id, ssv.id), '%Y-%m-%d').strftime("%d/%m/%Y")
                                        rem_date = self.__datetime(str(est_date)) - self.__datetime(str(datetime.today().strftime('%d/%m/%Y')))
                                        for a in xrange(2,18):
                                            sheet.write(no1, a, '', format11)
                                        sheet.write(no1, int(est_date.split('/')[1])+5, '\n', green_mark)
                                        sheet.write(no1, 1, scm.product_id.name, format12)
                                        sheet.write(no1, 2, ssv.next_text, format12)
                                        sheet.write(no1, 3, ssv.remaining, format12)
                                        sheet.write(no1, 4, str(est_date), formatdate)
                                        sheet.write(no1, 5, str(str(rem_date.days)+' Days'), format12)
                                        no1 += 1    
                """ Engine """
                for eng2 in x.engine2_type_id:
                    sheet.write(no1, 1, eng2.name, format11)
                    no1 += 1
                    for cm in eng2.component_ids:
                        for sv in cm.serfice_life:
                            if sv.is_major:
                                est_date = datetime.strptime(self.env['ams.mtr'].countDate(x.id, sv.id), '%Y-%m-%d').strftime("%d/%m/%Y")
                                rem_date = self.__datetime(str(est_date)) - self.__datetime(str(datetime.today().strftime('%d/%m/%Y')))
                                for a in xrange(2,18):
                                    sheet.write(no1, a, '', format11)
                                sheet.write(no1, int(est_date.split('/')[1])+5, '\n', green_mark)
                                sheet.write(no1, 1, cm.product_id.name+' '+eng2.name, format12)
                                sheet.write(no1, 2, sv.next_text, format12)
                                sheet.write(no1, 3, sv.remaining, format12)
                                sheet.write(no1, 4, str(est_date), formatdate)
                                sheet.write(no1, 5, str(str(rem_date.days)+' Days'), format12)
                                no1 += 1
                            for scm in cm.sub_part_ids:
                                for ssv in scm.serfice_life:
                                    if ssv.is_major:
                                        est_date = datetime.strptime(self.env['ams.mtr'].countDate(x.id, ssv.id), '%Y-%m-%d').strftime("%d/%m/%Y")
                                        rem_date = self.__datetime(str(est_date)) - self.__datetime(str(datetime.today().strftime('%d/%m/%Y')))
                                        for a in xrange(2,18):
                                            sheet.write(no1, a, '', format11)
                                        sheet.write(no1, int(est_date.split('/')[1])+5, '\n', green_mark)
                                        sheet.write(no1, 1, scm.product_id.name, format12)
                                        sheet.write(no1, 2, ssv.next_text, format12)
                                        sheet.write(no1, 3, ssv.remaining, format12)
                                        sheet.write(no1, 4, str(est_date), formatdate)
                                        sheet.write(no1, 5, str(str(rem_date.days)+' Days'), format12)
                                        no1 += 1    
                """ Engine """
                for eng3 in x.engine3_type_id:
                    sheet.write(no1, 1, eng3.name, format11)
                    no1 += 1
                    for cm in eng3.component_ids:
                        for sv in cm.serfice_life:
                            if sv.is_major:
                                est_date = datetime.strptime(self.env['ams.mtr'].countDate(x.id, sv.id), '%Y-%m-%d').strftime("%d/%m/%Y")
                                rem_date = self.__datetime(str(est_date)) - self.__datetime(str(datetime.today().strftime('%d/%m/%Y')))
                                for a in xrange(2,18):
                                    sheet.write(no1, a, '', format11)
                                sheet.write(no1, int(est_date.split('/')[1])+5, '\n', green_mark)
                                sheet.write(no1, 1, cm.product_id.name+' '+eng3.name, format12)
                                sheet.write(no1, 2, sv.next_text, format12)
                                sheet.write(no1, 3, sv.remaining, format12)
                                sheet.write(no1, 4, str(est_date), formatdate)
                                sheet.write(no1, 5, str(str(rem_date.days)+' Days'), format12)
                                no1 += 1
                            for scm in cm.sub_part_ids:
                                for ssv in scm.serfice_life:
                                    if ssv.is_major:
                                        est_date = datetime.strptime(self.env['ams.mtr'].countDate(x.id, ssv.id), '%Y-%m-%d').strftime("%d/%m/%Y")
                                        rem_date = self.__datetime(str(est_date)) - self.__datetime(str(datetime.today().strftime('%d/%m/%Y')))
                                        for a in xrange(2,18):
                                            sheet.write(no1, a, '', format11)
                                        sheet.write(no1, int(est_date.split('/')[1])+5, '\n', green_mark)
                                        sheet.write(no1, 1, scm.product_id.name, format12)
                                        sheet.write(no1, 2, ssv.next_text, format12)
                                        sheet.write(no1, 3, ssv.remaining, format12)
                                        sheet.write(no1, 4, str(est_date), formatdate)
                                        sheet.write(no1, 5, str(str(rem_date.days)+' Days'), format12)
                                        no1 += 1    
                """ Engine """
                for eng4 in x.engine4_type_id:
                    sheet.write(no1, 1, eng4.name, format11)
                    no1 += 1
                    for cm in eng4.component_ids:
                        for sv in cm.serfice_life:
                            if sv.is_major:
                                est_date = datetime.strptime(self.env['ams.mtr'].countDate(x.id, sv.id), '%Y-%m-%d').strftime("%d/%m/%Y")
                                rem_date = self.__datetime(str(est_date)) - self.__datetime(str(datetime.today().strftime('%d/%m/%Y')))
                                for a in xrange(2,18):
                                    sheet.write(no1, a, '', format11)
                                sheet.write(no1, int(est_date.split('/')[1])+5, '\n', green_mark)
                                sheet.write(no1, 1, cm.product_id.name+' '+eng4.name, format12)
                                sheet.write(no1, 2, sv.next_text, format12)
                                sheet.write(no1, 3, sv.remaining, format12)
                                sheet.write(no1, 4, str(est_date), formatdate)
                                sheet.write(no1, 5, str(str(rem_date.days)+' Days'), format12)
                                no1 += 1
                            for scm in cm.sub_part_ids:
                                for ssv in scm.serfice_life:
                                    if ssv.is_major:
                                        est_date = datetime.strptime(self.env['ams.mtr'].countDate(x.id, ssv.id), '%Y-%m-%d').strftime("%d/%m/%Y")
                                        rem_date = self.__datetime(str(est_date)) - self.__datetime(str(datetime.today().strftime('%d/%m/%Y')))
                                        for a in xrange(2,18):
                                            sheet.write(no1, a, '', format11)
                                        sheet.write(no1, int(est_date.split('/')[1])+5, '\n', green_mark)
                                        sheet.write(no1, 1, scm.product_id.name, format12)
                                        sheet.write(no1, 2, ssv.next_text, format12)
                                        sheet.write(no1, 3, ssv.remaining, format12)
                                        sheet.write(no1, 4, str(est_date), formatdate)
                                        sheet.write(no1, 5, str(str(rem_date.days)+' Days'), format12)
                                        no1 += 1                    
                """ Propeller """
                for prop1 in x.propeller_type_id:
                    sheet.write(no1, 1, prop1.name, format11)
                    no1 += 1
                    for cm in prop1.component_ids:
                        for sv in cm.serfice_life:
                            if sv.is_major:
                                est_date = datetime.strptime(self.env['ams.mtr'].countDate(x.id, sv.id), '%Y-%m-%d').strftime("%d/%m/%Y")
                                rem_date = self.__datetime(str(est_date)) - self.__datetime(str(datetime.today().strftime('%d/%m/%Y')))
                                for a in xrange(2,18):
                                    sheet.write(no1, a, '', format11)
                                sheet.write(no1, int(est_date.split('/')[1])+5, '\n', green_mark)
                                sheet.write(no1, 1, cm.product_id.name, format12)
                                sheet.write(no1, 2, sv.next_text, format12)
                                sheet.write(no1, 3, sv.remaining, format12)
                                sheet.write(no1, 4, str(est_date), formatdate)
                                sheet.write(no1, 5, str(str(rem_date.days)+' Days'), format12)
                                no1 += 1
                            for scm in cm.sub_part_ids:
                                for ssv in scm.serfice_life:
                                    if ssv.is_major:
                                        est_date = datetime.strptime(self.env['ams.mtr'].countDate(x.id, ssv.id), '%Y-%m-%d').strftime("%d/%m/%Y")
                                        rem_date = self.__datetime(str(est_date)) - self.__datetime(str(datetime.today().strftime('%d/%m/%Y')))
                                        for a in xrange(2,18):
                                            sheet.write(no1, a, '', format11)
                                        sheet.write(no1, int(est_date.split('/')[1])+5, '\n', green_mark)
                                        sheet.write(no1, 1, scm.product_id.name, format12)
                                        sheet.write(no1, 2, ssv.next_text, format12)
                                        sheet.write(no1, 3, ssv.remaining, format12)
                                        sheet.write(no1, 4, str(est_date), formatdate)
                                        sheet.write(no1, 5, str(str(rem_date.days)+' Days'), format12)
                                        no1 += 1    
                """ Propeller """
                for prop2 in x.propeller2_type_id:
                    sheet.write(no1, 1, prop2.name, format11)
                    no1 += 1
                    for cm in prop2.component_ids:
                        for sv in cm.serfice_life:
                            if sv.is_major:
                                est_date = datetime.strptime(self.env['ams.mtr'].countDate(x.id, sv.id), '%Y-%m-%d').strftime("%d/%m/%Y")
                                rem_date = self.__datetime(str(est_date)) - self.__datetime(str(datetime.today().strftime('%d/%m/%Y')))
                                for a in xrange(2,18):
                                    sheet.write(no1, a, '', format11)
                                sheet.write(no1, int(est_date.split('/')[1])+5, '\n', green_mark)
                                sheet.write(no1, 1, cm.product_id.name, format12)
                                sheet.write(no1, 2, sv.next_text, format12)
                                sheet.write(no1, 3, sv.remaining, format12)
                                sheet.write(no1, 4, str(est_date), formatdate)
                                sheet.write(no1, 5, str(str(rem_date.days)+' Days'), format12)
                                no1 += 1
                            for scm in cm.sub_part_ids:
                                for ssv in scm.serfice_life:
                                    if ssv.is_major:
                                        est_date = datetime.strptime(self.env['ams.mtr'].countDate(x.id, ssv.id), '%Y-%m-%d').strftime("%d/%m/%Y")
                                        rem_date = self.__datetime(str(est_date)) - self.__datetime(str(datetime.today().strftime('%d/%m/%Y')))
                                        for a in xrange(2,18):
                                            sheet.write(no1, a, '', format11)
                                        sheet.write(no1, int(est_date.split('/')[1])+5, '\n', green_mark)
                                        sheet.write(no1, 1, scm.product_id.name, format12)
                                        sheet.write(no1, 2, ssv.next_text, format12)
                                        sheet.write(no1, 3, ssv.remaining, format12)
                                        sheet.write(no1, 4, str(est_date), formatdate)
                                        sheet.write(no1, 5, str(str(rem_date.days)+' Days'), format12)
                                        no1 += 1    
                """ Propeller """
                for prop3 in x.propeller3_type_id:
                    sheet.write(no1, 1, prop3.name, format11)
                    no1 += 1
                    for cm in prop3.component_ids:
                        for sv in cm.serfice_life:
                            if sv.is_major:
                                est_date = datetime.strptime(self.env['ams.mtr'].countDate(x.id, sv.id), '%Y-%m-%d').strftime("%d/%m/%Y")
                                rem_date = self.__datetime(str(est_date)) - self.__datetime(str(datetime.today().strftime('%d/%m/%Y')))
                                for a in xrange(2,18):
                                    sheet.write(no1, a, '', format11)
                                sheet.write(no1, int(est_date.split('/')[1])+5, '\n', green_mark)
                                sheet.write(no1, 1, cm.product_id.name, format12)
                                sheet.write(no1, 2, sv.next_text, format12)
                                sheet.write(no1, 3, sv.remaining, format12)
                                sheet.write(no1, 4, str(est_date), formatdate)
                                sheet.write(no1, 5, str(str(rem_date.days)+' Days'), format12)
                                no1 += 1
                            for scm in cm.sub_part_ids:
                                for ssv in scm.serfice_life:
                                    if ssv.is_major:
                                        est_date = datetime.strptime(self.env['ams.mtr'].countDate(x.id, ssv.id), '%Y-%m-%d').strftime("%d/%m/%Y")
                                        rem_date = self.__datetime(str(est_date)) - self.__datetime(str(datetime.today().strftime('%d/%m/%Y')))
                                        for a in xrange(2,18):
                                            sheet.write(no1, a, '', format11)
                                        sheet.write(no1, int(est_date.split('/')[1])+5, '\n', green_mark)
                                        sheet.write(no1, 1, scm.product_id.name, format12)
                                        sheet.write(no1, 2, ssv.next_text, format12)
                                        sheet.write(no1, 3, ssv.remaining, format12)
                                        sheet.write(no1, 4, str(est_date), formatdate)
                                        sheet.write(no1, 5, str(str(rem_date.days)+' Days'), format12)
                                        no1 += 1    
                """ Propeller """
                for prop4 in x.propeller4_type_id:
                    sheet.write(no1, 1, prop4.name, format11)
                    no1 += 1
                    for cm in prop4.component_ids:
                        for sv in cm.serfice_life:
                            if sv.is_major:
                                est_date = datetime.strptime(self.env['ams.mtr'].countDate(x.id, sv.id), '%Y-%m-%d').strftime("%d/%m/%Y")
                                rem_date = self.__datetime(str(est_date)) - self.__datetime(str(datetime.today().strftime('%d/%m/%Y')))
                                for a in xrange(2,18):
                                    sheet.write(no1, a, '', format11)
                                sheet.write(no1, int(est_date.split('/')[1])+5, '\n', green_mark)
                                sheet.write(no1, 1, cm.product_id.name, format12)
                                sheet.write(no1, 2, sv.next_text, format12)
                                sheet.write(no1, 3, sv.remaining, format12)
                                sheet.write(no1, 4, str(est_date), formatdate)
                                sheet.write(no1, 5, str(str(rem_date.days)+' Days'), format12)
                                no1 += 1
                            for scm in cm.sub_part_ids:
                                for ssv in scm.serfice_life:
                                    if ssv.is_major:
                                        est_date = datetime.strptime(self.env['ams.mtr'].countDate(x.id, ssv.id), '%Y-%m-%d').strftime("%d/%m/%Y")
                                        rem_date = self.__datetime(str(est_date)) - self.__datetime(str(datetime.today().strftime('%d/%m/%Y')))
                                        for a in xrange(2,18):
                                            sheet.write(no1, a, '', format11)
                                        sheet.write(no1, int(est_date.split('/')[1])+5, '\n', green_mark)
                                        sheet.write(no1, 1, scm.product_id.name, format12)
                                        sheet.write(no1, 2, ssv.next_text, format12)
                                        sheet.write(no1, 3, ssv.remaining, format12)
                                        sheet.write(no1, 4, str(est_date), formatdate)
                                        sheet.write(no1, 5, str(str(rem_date.days)+' Days'), format12)
                                        no1 += 1                    

                """ Auxiliary """
                for aux in x.auxiliary_type_id:
                    sheet.write(no1, 1, aux.name, format11)
                    no1 += 1
                    for cm in aux.component_ids:
                        for sv in cm.serfice_life:
                            if sv.is_major:
                                est_date = datetime.strptime(self.env['ams.mtr'].countDate(x.id, sv.id), '%Y-%m-%d').strftime("%d/%m/%Y")
                                rem_date = self.__datetime(str(est_date)) - self.__datetime(str(datetime.today().strftime('%d/%m/%Y')))
                                for a in xrange(2,18):
                                    sheet.write(no1, a, '', format11)
                                sheet.write(no1, int(est_date.split('/')[1])+5, '\n', green_mark)
                                sheet.write(no1, 1, cm.product_id.name, format12)
                                sheet.write(no1, 2, sv.next_text, format12)
                                sheet.write(no1, 3, sv.remaining, format12)
                                sheet.write(no1, 4, str(est_date), formatdate)
                                sheet.write(no1, 5, str(str(rem_date.days)+' Days'), format12)
                                no1 += 1
                            for scm in cm.sub_part_ids:
                                for ssv in scm.serfice_life:
                                    if ssv.is_major:
                                        est_date = datetime.strptime(self.env['ams.mtr'].countDate(x.id, ssv.id), '%Y-%m-%d').strftime("%d/%m/%Y")
                                        rem_date = self.__datetime(str(est_date)) - self.__datetime(str(datetime.today().strftime('%d/%m/%Y')))
                                        for a in xrange(2,18):
                                            sheet.write(no1, a, '', format11)
                                        sheet.write(no1, int(est_date.split('/')[1])+5, '\n', green_mark)
                                        sheet.write(no1, 1, scm.product_id.name, format12)
                                        sheet.write(no1, 2, ssv.next_text, format12)
                                        sheet.write(no1, 3, ssv.remaining, format12)
                                        sheet.write(no1, 4, str(est_date), formatdate)
                                        sheet.write(no1, 5, str(str(rem_date.days)+' Days'), format12)
                                        no1 += 1                    

MPReportXls('report.ams_report.maintenance_planning_report.xlsx','maintenance.plan.report')
