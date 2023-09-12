from odoo import models, fields, api, _
import xlwt
from xlsxwriter import *
from cStringIO import StringIO
import base64
from reportlab.pdfgen import canvas
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from odoo.exceptions import  ValidationError


class ReportOTI(models.Model):
    _name = 'document.oti.report'
    _description = 'One Time Inspection'

    ac_type = fields.Many2one('aircraft.acquisition', string="A/C Type")
    start_date = fields.Date('Date Start')
    end_date = fields.Date('Date End')
    ata = fields.Many2one('ams.ata', string="System/ATA")
    compliance  = fields.Selection([('draft','Draft'),('onprogress','On Progress'),('notcomply','Not Comply'),('complied','Complied'),], string="Compliance")
    sort_by = fields.Selection([('asc','ASC'),('desc','DESC')], default='asc')
    order_by = fields.Selection([('id','No'),('date','Date'),('ac_type','A/C Type'),('compliance','Compliance'),('system_ata','ATA')], default='id')

    oti_id = fields.Many2many('document.oti', compute='_onchange_comp')    

    @api.multi
    @api.constrains('end_date', 'start_date')
    def date_constrains(self):
        for rec in self:
            if rec.end_date < rec.start_date:
                raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))

    @api.multi
    def print_oti_pdf_report(self):
        return self.env['report'].get_action(self, 'ams_document.report_oti_report')

    def rendering(self):
        search_param = []
        if self.ac_type:
            search_param.append(('ac_type','=', self.ac_type.id))
        if self.ata:     
            search_param.append(('system_ata','=', self.ata.id))
        if self.compliance:
            search_param.append(('compliance','=', self.compliance))
        if self.start_date and self.end_date :
            search_param.append('&')
            search_param.append(('date','>=', self.start_date))
            search_param.append(('date','<=', self.end_date))


        document = self.env['document.oti'].search(search_param, order=str(self.order_by+' '+self.sort_by))

        self.oti_id = document

    @api.onchange('ac_type')
    def _onchange_comp(self):
        self.rendering()
        


class ReportMI(models.Model):
    _name = 'document.mi.report'
    _description = 'Maintenance Instruction'

    ac_type = fields.Many2one('aircraft.acquisition', string="A/C Type")
    start_date = fields.Date('Date Start')
    end_date = fields.Date('Date End')
    ata = fields.Many2one('ams.ata', string="System/ATA")
    compliance  = fields.Selection([('draft','Draft'),('onprogress','On Progress'),('notcomply','Not Comply'),('complied','Complied'),], string="Compliance")
    sort_by = fields.Selection([('asc','ASC'),('desc','DESC')], default='asc')
    order_by = fields.Selection([('id','No'),('date','Date'),('ac_type','A/C Type'),('compliance','Compliance'),('system_ata','ATA')], default='id')
    
    mi_id = fields.Many2many('document.mi', compute='_onchange_comp')  

    @api.multi
    @api.constrains('end_date', 'start_date')
    def date_constrains(self):
        for rec in self:
            if rec.end_date < rec.start_date:
                raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))  

    @api.multi
    def print_mi_pdf_report(self):
        return self.env['report'].get_action(self, 'ams_document.report_mi_report')

    def rendering(self):
        search_param = []
        if self.ac_type:
            search_param.append(('ac_type','=', self.ac_type.id))
        if self.ata:     
            search_param.append(('system_ata','=', self.ata.id))
        if self.compliance:
            search_param.append(('compliance','=', self.compliance))
        if self.start_date and self.end_date :
            search_param.append('&')
            search_param.append(('date','>=', self.start_date))
            search_param.append(('date','<=', self.end_date))


        document = self.env['document.mi'].search(search_param, order=str(self.order_by+' '+self.sort_by))

        self.mi_id = document

    @api.onchange('ac_type')
    def _onchange_comp(self):
        self.rendering()


class ReportEO(models.Model):
    _name = 'document.eo.report'
    _description = 'Enginering Order'

    ac_type = fields.Many2one('aircraft.acquisition', string="A/C Type")
    start_date = fields.Date('Date Start')
    end_date = fields.Date('Date End')
    # ata = fields.Many2one('ams.ata', string="System/ATA")
    compliance  = fields.Selection([('draft','Draft'),('onprogress','On Progress'),('notcomply','Not Comply'),('complied','Complied'),], string="Compliance")
    sort_by = fields.Selection([('asc','ASC'),('desc','DESC')], default='asc')
    order_by = fields.Selection([('id','E.O. Number'),('eo_tittle','E.O. Tittle'),('aircraft_id','A/C Type'),('create_date','Date'),('compliance','Compliance')], default='id')

    eo_id = fields.Many2many('document.eo', compute='_onchange_comp')    

    @api.multi
    @api.constrains('end_date', 'start_date')
    def date_constrains(self):
        for rec in self:
            if rec.end_date < rec.start_date:
                raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))

    @api.multi
    def print_eo_pdf_report(self):
        return self.env['report'].get_action(self, 'ams_document.report_eo_report')

    def rendering(self):
        search_param = []
        if self.ac_type:
            search_param.append(('aircraft_id','=', self.ac_type.id))
        if self.compliance:
            search_param.append(('compliance','=', self.compliance))
        if self.start_date and self.end_date :
            search_param.append('&')
            search_param.append(('create_date','>=', self.start_date))
            search_param.append(('create_date','<=', self.end_date))


        document = self.env['document.eo'].search(search_param, order=str(self.order_by+' '+self.sort_by))

        self.eo_id = document

        
    @api.onchange('ac_type')
    def _onchange_comp(self):
        self.rendering()

class ReportTI(models.Model):
    _name = 'document.ti.report'
    _description = 'Technical Information'

    ac_type = fields.Many2one('aircraft.acquisition', string="A/C Type")
    start_date = fields.Date('Date Start')
    end_date = fields.Date('Date End')
    ata = fields.Many2one('ams.ata', string="System/ATA")
    compliance  = fields.Selection([('draft','Draft'),('onprogress','On Progress'),('notcomply','Not Comply'),('complied','Complied'),], string="Compliance")
    sort_by = fields.Selection([('asc','ASC'),('desc','DESC')], default='asc')
    order_by = fields.Selection([('id','No'),('date','Date'),('ac_type','A/C Type'),('compliance','Compliance'),('system_ata','ATA')], default='id')

    ti_id = fields.Many2many('document.ti', compute='_onchange_comp')

    @api.multi
    @api.constrains('end_date', 'start_date')
    def date_constrains(self):
        for rec in self:
            if rec.end_date < rec.start_date:
                raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))

    @api.multi
    def print_ti_pdf_report(self):
        return self.env['report'].get_action(self, 'ams_document.report_ti_report')

    def rendering(self):
        search_param = []
        if self.ac_type:
            search_param.append(('ac_type','=', self.ac_type.id))
        if self.ata:     
            search_param.append(('system_ata','=', self.ata.id))
        if self.compliance:
            search_param.append(('compliance','=', self.compliance))
        if self.start_date and self.end_date :
            search_param.append('&')
            search_param.append(('date','>=', self.start_date))
            search_param.append(('date','<=', self.end_date))


        document = self.env['document.ti'].search(search_param, order=str(self.order_by+' '+self.sort_by))

        self.ti_id = document

    @api.onchange('ac_type')
    def _onchange_comp(self):
        self.rendering()
        
