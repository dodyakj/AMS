from odoo import models, fields, api, _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import xlwt
from xlsxwriter import *
from cStringIO import StringIO
import base64
from reportlab.pdfgen import canvas
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from calendar import monthrange
import collections
from odoo.exceptions import  ValidationError



class AircraftStatusReport(models.Model):
    _name = 'aircraft.status.report'
    _description = 'Component Removal'


    date = fields.Date('Date',default=fields.Date.today())
    max_date = fields.Integer(string='Max Date',default=31)
    data_ids = fields.One2many('aircraft.status.data','status_id',string='Data')
    maintenance_ids = fields.One2many('aircraft.maintenance.data','status_id',string='Maintenance')
    # year = fields.selection([(y, str(y)) for y in range(1970, (datetime.now().year + 30)+1 )], 'Year')

    @api.onchange('date')
    def _onchange_aircraft_model_id(self):
        max_date = monthrange(int(self.date[:4]), int(self.date[5:-3].lstrip('0')))[1]
        start_month = self.date[:7]+'-01'
        end_month = self.date[:7]+'-'+str(max_date)
        self.max_date = str(max_date)
        data_ids = []
        maintenance_ids = []
        plane = self.env['aircraft.acquisition'].search([],order='category ASC, aircraft_type_id ASC, name ASC')
        
        for g in plane:
            prod_hours = float(0)
            prod_cycles = float(0)
            
            for i in self.env['ams_fml.log'].search(['&','&',('aircraft_id','=',g.id),('date','>=',start_month),('date','<=',end_month)]):
                prod_hours = prod_hours + i.aircraft_hours
                prod_cycles = prod_cycles + i.aircraft_cycles
            
            maintenance = self.env['maintenance.request'].search([('fl_acquisition_id','=',g.id)])
            servicable_status =  {
                'fleet_id' : g.id,
                'prod_hours' : prod_hours,
                'prod_cycles' : prod_cycles,
                'realibility' : 100,
                'total_s' : 0,
                'total_us' : 0,
                'days_1' : 'S',
                'days_2' : 'S',
                'days_3' : 'S',
                'days_4' : 'S',
                'days_5' : 'S',
                'days_6' : 'S',
                'days_7' : 'S',
                'days_8' : 'S',
                'days_9' : 'S',
                'days_10' : 'S',
                'days_11' : 'S',
                'days_12' : 'S',
                'days_13' : 'S',
                'days_14' : 'S',
                'days_15' : 'S',
                'days_16' : 'S',
                'days_17' : 'S',
                'days_18' : 'S',
                'days_19' : 'S',
                'days_20' : 'S',
                'days_21' : 'S',
                'days_22' : 'S',
                'days_23' : 'S',
                'days_24' : 'S',
                'days_25' : 'S',
                'days_26' : 'S',
                'days_27' : 'S',
                'days_28' : 'S',
                'days_29' : 'S',
                'days_30' : 'S',
                'days_31' : 'S',
            }
            for n in maintenance:
                if n.schedule_date:
                    start_maint = n.schedule_date[:10]
                    end_maint = (datetime.strptime(n.schedule_date[:10],'%Y-%m-%d')  + relativedelta(hours=n.duration)).strftime("%Y-%m-%d")
                    if(((start_maint >= start_month) and (start_maint <= end_month)) or ((end_maint >= start_month) and (end_maint <= end_month)) or ((start_maint <= start_month) and (end_maint >= end_month))):
                        maintenance_ids.append((0, 0,{
                            'fleet_id' : g.id,
                            'start_date' : start_maint,
                            'end_date' : end_maint,
                            'maintenance_id' : n.id,
                            'status' : 'US' if n.aircraft_state == 'unserviceable' else 'S',
                            }))
                        # MENENTUKAN START RECORD
                        if(start_maint < start_month):
                            record_start = 1
                        else:
                            record_start = int(start_maint[-2:].lstrip('0'))
                        if(end_maint > end_month):
                            record_end = max_date
                        else:
                            record_end = int(end_maint[-2:].lstrip('0'))
                        if(n.aircraft_state == 'unserviceable'):
                            for o in xrange(record_start,record_end):
                                servicable_status['days_' + str(o)] = 'US'
            # COUNT ALL SERVICEABLE UNSERVICEABLE
            for r in xrange(1,max_date+1):
                if(servicable_status['days_'+str(r)] == 'S'):
                    servicable_status['total_s'] = servicable_status['total_s'] + 1
                else:
                    servicable_status['total_us'] = servicable_status['total_us'] + 1
            
            # print float((float(servicable_status['total_s'])/(max_date)) * 100)
            servicable_status['realibility'] = "%.2f" % ((float(servicable_status['total_s'])/max_date) * 100)
            data_ids.append((0, 0,servicable_status))
        self.data_ids = data_ids
        self.maintenance_ids = maintenance_ids

    @api.multi
    def export_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'aircraft.status.report'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        if context.get('status'):
            return {'type': 'ir.actions.report.xml',
                    'report_name': 'ams_report.aircraft_status_report.xlsx',
                    'datas': datas,
                    'name': 'Aircraft Status'
                    }

    @api.multi
    def print_aircraft_status_reports(self):
        return self.env['report'].get_action(self, 'ams_report.aircraft_status_pdf')




class AircraftMaintenanceData(models.Model):
    _name = 'aircraft.maintenance.data'
    _description = 'Maintenance Data'

    status_id = fields.Many2one('aircraft.status.report',string='Status Id')
    fleet_id = fields.Many2one('aircraft.acquisition',string='REG')
    start_date = fields.Date('Start Date',default=fields.Date.today())
    end_date = fields.Date('End Date',default=fields.Date.today())
    maintenance_id = fields.Many2one('maintenance.request',string='Maintenance')
    status = fields.Selection([('S','S'),('US','US')], string="Serviceable Status", default="S")

    # @api.multi
    # @api.constrains('end_date', 'start_date')
    # def date_constrains(self):
    #     for rec in self:
    #         if rec.end_date < rec.start_date:
    #             raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))

class AircraftStatusData(models.Model):
    _name = 'aircraft.status.data'
    _description = 'Status Data'

    status_id = fields.Many2one('aircraft.status.report',string='Status Id')
    max_date = fields.Integer(string='Max Date',related='status_id.max_date',readonly=True)
    fleet_id = fields.Many2one('aircraft.acquisition',string='REG')
    # type_id = fields.Many2one('aircraft.type',string='TYPE',related='fleet_id.aircraft_type_id',readonly=True)

    # location_id = fields.Many2one('base.operation',string='Location',related='fleet_id.location',readonly=True)

    prod_hours = fields.Float(string='Prod. in Hours')
    prod_cycles = fields.Float(string='Prod. in Cycles')

    realibility = fields.Float(string='Reliability')

    total_s = fields.Integer(string='Total S')
    total_us = fields.Integer(string='Total US')

    remark = fields.Char('Remark')

    days_1 = fields.Selection([('S','S'),('US','US')], string="1", default="S")
    days_2 = fields.Selection([('S','S'),('US','US')], string="2", default="S")
    days_3 = fields.Selection([('S','S'),('US','US')], string="3", default="S")
    days_4 = fields.Selection([('S','S'),('US','US')], string="4", default="S")
    days_5 = fields.Selection([('S','S'),('US','US')], string="5", default="S")
    days_6 = fields.Selection([('S','S'),('US','US')], string="6", default="S")
    days_7 = fields.Selection([('S','S'),('US','US')], string="7", default="S")
    days_8 = fields.Selection([('S','S'),('US','US')], string="8", default="S")
    days_9 = fields.Selection([('S','S'),('US','US')], string="9", default="S")
    days_10 = fields.Selection([('S','S'),('US','US')], string="10", default="S")
    days_11 = fields.Selection([('S','S'),('US','US')], string="11", default="S")
    days_12 = fields.Selection([('S','S'),('US','US')], string="12", default="S")
    days_13 = fields.Selection([('S','S'),('US','US')], string="13", default="S")
    days_14 = fields.Selection([('S','S'),('US','US')], string="14", default="S")
    days_15 = fields.Selection([('S','S'),('US','US')], string="15", default="S")
    days_16 = fields.Selection([('S','S'),('US','US')], string="16", default="S")
    days_17 = fields.Selection([('S','S'),('US','US')], string="17", default="S")
    days_18 = fields.Selection([('S','S'),('US','US')], string="18", default="S")
    days_19 = fields.Selection([('S','S'),('US','US')], string="19", default="S")
    days_20 = fields.Selection([('S','S'),('US','US')], string="20", default="S")
    days_21 = fields.Selection([('S','S'),('US','US')], string="21", default="S")
    days_22 = fields.Selection([('S','S'),('US','US')], string="22", default="S")
    days_23 = fields.Selection([('S','S'),('US','US')], string="23", default="S")
    days_24 = fields.Selection([('S','S'),('US','US')], string="24", default="S")
    days_25 = fields.Selection([('S','S'),('US','US')], string="25", default="S")
    days_26 = fields.Selection([('S','S'),('US','US')], string="26", default="S")
    days_27 = fields.Selection([('S','S'),('US','US')], string="27", default="S")
    days_28 = fields.Selection([('S','S'),('US','US')], string="28", default="S")
    days_29 = fields.Selection([('S','S'),('US','US')], string="29", default="S")
    days_30 = fields.Selection([('S','S'),('US','US')], string="30", default="S")
    days_31 = fields.Selection([('S','S'),('US','US')], string="31", default="S")