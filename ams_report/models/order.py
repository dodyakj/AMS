
from odoo import models, fields, api, _
import xlwt
from xlsxwriter import *
from cStringIO import StringIO
import base64
import re
from reportlab.pdfgen import canvas
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from odoo.exceptions import  ValidationError

class WorkOrderReport(models.Model):
    _name = 'ams.work.order.report'
    _description = 'Work Order Report'

    type = fields.Selection([('schedule','Schedule'),('unschedule','Unschedule')], 'Schedule Type', default=lambda self:self.env.context.get('schedule_type','schedule'))
    wo_type = fields.Selection([('all','All'),('material','Inspection'),('inspection','Material')], default='all', string="Work Order Type")
    start_date = fields.Date()
    end_date = fields.Date()
    schedule = fields.Selection([('all','All'),('schedule','Schedule'),('unschedule','Unschedule')], 'Schedule Type')
    aircraft = fields.Many2one('aircraft.acquisition')
    order_by = fields.Selection([('date_issued','Date'),('ac','A/C'),('id','Number')], default='date_issued')
    sort_by  = fields.Selection([('asc','ASC'),('desc','DESC')], default='asc')

    wo_id = fields.Many2many('ams.work.order', compute=lambda self: self._onchange_comp())


    def countId(self, count):
        data =  len(count)
        return data


    def cleanhtml(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    @api.multi
    @api.constrains('end_date', 'start_date')
    def date_constrains(self):
        for rec in self:
            if rec.end_date < rec.start_date:
                raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))

    @api.multi
    def print_wo_pdf(self):
        return self.env['report'].get_action(self, 'ams_report.wo_pdf')



    def rendering(self):
        search_param = []
        if self.type == 'schedule':
            search_param.append(('schedule','=',True))
        else:
            search_param.append(('schedule','=',False))

        if self.aircraft:
            search_param.append(('ac','=',self.aircraft.id))

        if self.wo_type != 'all':
            search_param.append(('wo_type','=',self.wo_type))

        if(self.start_date and self.end_date):
            search_param.append(('date_issued','>=',self.start_date)) # tambahkan substring disini
            search_param.append(('date_issued','<=',self.end_date)) # tambahkan substring disini

        wo_data = self.env['ams.work.order'].search(search_param, order=str(self.order_by+' '+self.sort_by))
        # print wo_data
        self.wo_id = wo_data
        

    # @api.onchange('wo_type')
    @api.multi
    def _onchange_comp(self):
        self.rendering()




class MaintenanceWorkOrderReport(models.Model):
    _name = 'ams.mwo.report'
    _description = 'Maintenance Work Order Report'

    type = fields.Selection([('schedule','Schedule'),('unschedule','Unschedule')], 'Schedule Type', default=lambda self:self.env.context.get('schedule_type','schedule'))
    mwo_type = fields.Selection([('all','All'),('material','Inspection'),('inspection','Material')], default='all', string="Work Order Type")
    start_date = fields.Date()
    end_date = fields.Date()
    schedule = fields.Selection([('all','All'),('schedule','Schedule'),('unschedule','Unschedule')], 'Schedule Type')
    aircraft = fields.Many2one('aircraft.acquisition')
    order_by = fields.Selection([('date','Date'),('ac','A/C'),('id','Number')], default='date')
    sort_by  = fields.Selection([('asc','ASC'),('desc','DESC')], default='asc')
    mwo_id = fields.Many2many('ams.mwo', compute=lambda self: self._onchange_comp())

    def countId(self, count):
        data =  len(count)
        return data
        
    @api.multi
    @api.constrains('end_date', 'start_date')
    def date_constrains(self):
        for rec in self:
            if rec.end_date < rec.start_date:
                raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))

    @api.multi
    def print_mwo_pdf(self):
        return self.env['report'].get_action(self, 'ams_report.mwo_pdf')



    def rendering(self):
        search_param = []
        if self.type == 'schedule':
            search_param.append(('schedule','=',True))
        else:
            search_param.append(('schedule','=',False))
        if self.aircraft:
            search_param.append(('ac','=',self.aircraft.id))
        if self.mwo_type != 'all':
            search_param.append(('mwo_type','=',self.mwo_type))
        if(self.start_date and self.end_date):
            search_param.append(('date','>=',self.start_date)) # tambahkan substring disini
            search_param.append(('date','<=',self.end_date)) # tambahkan substring disini

        mwo_data = self.env['ams.mwo'].search(search_param, order=str(self.order_by+' '+self.sort_by))
        self.mwo_id = mwo_data
        

    @api.onchange('mwo_type')
    def _onchange_comp(self):
        self.rendering()
