# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta

# class MELExtention(models.Model):
#     _name = 'document.mel'
#     _description = 'MEL Extention'
#     _rec_name = 'no'

#     no      = fields.Char(string="No.", compute='nama')
#     date    = fields.Date(string="Date", default=datetime.now())
#     ac_type = fields.Many2one('aircraft.type', string="Aircraft Type", related='ac_req.aircraft_type_id')
#     ac_req  = fields.Many2one('aircraft.acquisition', string="Aircraft Registration")
#     ata_mel     = fields.Many2one('ams.ata', string="ATA MEL Number")
#     mel_categ   = fields.Char(string="MEL Category")
#     reason      = fields.Char(string="Reason for Extention")
#     date_became = fields.Date(string="Date/location item became unserviceable")
#     date_schedule   = fields.Date(string="Original date/location of item scheduled for carried out")
#     compliance      = fields.Selection([('draft','Draft'),('onprogress','On Progress'),('notcomply','Not Comply'),('complied','Complied'),], string="Compliance")
#     part_id     = fields.Many2one('product.product', string="Name of item required")
#     part_number = fields.Char(related='part_id.default_code')
#     date_order  = fields.Date(string="Date Part Ordered")
#     date_deliv  = fields.Date(string="Confirmed delivery Date")
#     date_new    = fields.Date(string="New date carried out scheduled")
#     date_dgac   = fields.Date(string="DGAC Representatives notified")
#     date_limit  = fields.Date(string="Time limit valid to")

#     request_by = fields.Many2one('res.partner', string="Request By")
#     qc_by      = fields.Many2one('res.partner', string="Quality Control By")
#     app_by     = fields.Many2one('res.partner', string="Approved by")
#     date_req   = fields.Date(string="Request date")
#     date_qc    = fields.Date(string="Quality Control Date")


#     @api.one
#     @api.model
#     def nama(self):
#             year = datetime.now().strftime('%Y')
#             zero = len(str(self.id))
#             if len(str(self.id)) == zero:
#                 vals = str('00'+str(self.id)+'/MEL/EXT'+'/'+year)
#             elif len(str(self.id)) == zero:
#                 vals = str('0'+str(self.id)+'/MEL/EXT'+'/'+year)
#             else:
#                 vals = str(str(self.id)+'/MEL/EXT'+'/'+year)
#             self.no = vals


class OneTimeInspection(models.Model):
    _name = 'document.oti'
    _description = 'One Time Inspection'
    _rec_name = 'no'

    no      = fields.Char(string="No.", compute='nama')
    date   = fields.Date(string="Date", required=True)
    attend   = fields.Char(string="Attnd", required=True)
    ac_type = fields.Many2one('aircraft.aircraft', string="A/C Type", required=True)
    ac_req  = fields.Many2one('aircraft.acquisition', string="A/C Reg.", required=True)
    ac_sn   = fields.Char(string="A/C S/N", required=True)
    subject = fields.Char(string="Subject", required=True)
    reference   = fields.Char(string="Reference")
    eff_date    = fields.Date(string="Eff. Date")
    system_ata  = fields.Char(string="System/ATA")
    compliance  = fields.Selection([('draft','Draft'),('onprogress','On Progress'),('notcomply','Not Comply'),('complied','Complied'),], string="Compliance")
    text  = fields.Html(string="")
    ce_check = fields.Boolean(string="Chief Engineering")
    cq_check = fields.Boolean(string="Chief Quality")
    qq_check = fields.Boolean(string="QA & QM Manager")
    ata_code =  fields.Char(string="ATA Breakdown")
    compliance_sheet =  fields.Boolean(string="Compliance Sheet")

    file_uploads    = fields.Binary(string="File Uploads")
    filename        = fields.Char(string="Filename")

    @api.one
    @api.model
    def nama(self):
        if self.ac_req.category == 'fixedwing':
            # seq = self.env['ir.sequence'].next_by_code('receiving.inventory')
            year = datetime.now().strftime('%Y')
            if len(str(self.id)) == 1:
                vals = str('OTI/FW/'+'00'+str(self.id)+'/'+year)
            elif len(str(self.id)) == 2:
                vals = str('OTI/FW/'+'0'+str(self.id)+'/'+year)
            else:
                vals = str('OTI/FW/'+str(self.id)+'/'+year)
            self.no = vals
        if self.ac_req.category == 'rotary':
            # seq = self.env['ir.sequence'].next_by_code('receiving.inventory')
            year = datetime.now().strftime('%Y')
            if len(str(self.id)) == 1:
                vals = str('OTI/RW/'+'00'+str(self.id)+'/'+year)
            elif len(str(self.id)) == 2:
                vals = str('OTI/RW/'+'0'+str(self.id)+'/'+year)
            else:
                vals = str('OTI/RW/'+str(self.id)+'/'+year)
            self.no = vals




class EngineeringOrder(models.Model):
    _name = 'document.eo'
    _description = 'Engineering Order'
    _rec_name = 'eo_number'

    eo_number   = fields.Char(string="E.O. Number", compute='nama')
    eo_tittle   = fields.Char(string="E.O. Tittle", required=True)
    aircraft_id = fields.Many2one('aircraft.acquisition', string="Aircraft", required=True)
    date_prepared   = fields.Date(string="Date Prepared", readonly=True)
    date_checked    = fields.Date(string="Date Checked", readonly=True)
    date_approved   = fields.Date(string="Date Approved", readonly=True)
    prepared_by = fields.Many2one('res.partner', string="Prepared by", readonly=True)
    checked_by  = fields.Many2one('res.partner', string="Checked by", readonly=True)
    approved_by = fields.Many2one('res.partner', string="Approved by", readonly=True)
    major = fields.Boolean(string="Major")
    minor = fields.Boolean(string="Minor")
    dgca_approval   = fields.Boolean(string="DGCA Approval")
    aircraft_sn     = fields.Char(string="Aircraft SN", readonly=True, compute='_onchange_aircraft_id')
    reg     = fields.Char(string="Reg.", readonly=True, compute='_onchange_aircraft_id')
    desc    = fields.Text(string="Description")
    reason  = fields.Text(string="Reason")
    compliance  = fields.Selection([('draft','Draft'),('onprogress','On Progress'),('notcomply','Not Comply'),('complied','Complied'),], string="Compliance")
    estimated_cost  = fields.Text(string="Estimated Cost")
    drawing_req     = fields.Text(string="Drawing Required")
    estimated_man   = fields.Text(string="Estimated Man hours")
    weight_balance = fields.Selection([('yes','Yes'), ('no','No')] , string="Weight & Balance Affected", default="no")
    weight  = fields.Integer(string="Weight")
    arm     = fields.Char(string="Arm")
    accumulated_weight  = fields.Integer(string="Accumulated Weight Change Record Adjusted By")
    ad_list = fields.Selection([('yes','Yes'), ('no','No')] , string="AD List Affected", default="no")
    publication_aff     = fields.Text(string="Publication Affected")
    part_req    = fields.Text(string="Part Required")
    remark_ref  = fields.Text(string="Remarks & References")
    states = fields.Selection([('prepared_by','Prepared By'),('checked_by','Checked By'),('approved_by','Approved By'),('print','Print')])
    ata_code =  fields.Char(string="ATA Breakdown")
    compliance_sheet =  fields.Boolean(string="Compliance Sheet")

    file_uploads    = fields.Binary(string="File Uploads")
    filename        = fields.Char(string="Filename")

    @api.model
    def create(self,value):
        value['states'] = 'prepared_by'
        value['effectivity'] = '-'
        res = super(EngineeringOrder, self).create(value)
        return res

    @api.onchange('aircraft_id')
    def _onchange_aircraft_id(self):
        self.aircraft_sn = self.aircraft_id.vin_sn
        self.reg = self.aircraft_id.name
        

    @api.multi
    def prepared_by_(self):
        partner = self.env.user.partner_id.id
        self.prepared_by = partner
        self.states = 'checked_by'
        self.date_prepared = datetime.now().strftime('%Y-%m-%d')

    @api.multi
    def checked_by_(self):
        partner = self.env.user.partner_id.id
        self.checked_by = partner
        self.states = 'approved_by'
        self.date_checked = datetime.now().strftime('%Y-%m-%d')

    @api.multi
    def approved_by_(self):
        partner = self.env.user.partner_id.id
        self.approved_by = partner
        self.date_approved = datetime.now().strftime('%Y-%m-%d')
        self.states = 'print'

    @api.multi
    def print_eo_pdf(self):
        return self.env['report'].get_action(self, 'ams_document.report_eo')




    @api.one
    @api.model
    def nama(self):
        if self.aircraft_id.category == 'fixedwing':
            # seq = self.env['ir.sequence'].next_by_code('receiving.inventory')
            year = datetime.now().strftime('%Y')
            if len(str(self.id)) == 1:
                vals = str('EO/FW/'+'00'+str(self.id)+'/'+year)
            elif len(str(self.id)) == 2:
                vals = str('EO/FW/'+'0'+str(self.id)+'/'+year)
            else:
                vals = str('EO/FW/'+str(self.id)+'/'+year)
            self.eo_number = vals
        if self.aircraft_id.category == 'rotary':
            # seq = self.env['ir.sequence'].next_by_code('receiving.inventory')
            year = datetime.now().strftime('%Y')
            if len(str(self.id)) == 1:
                vals = str('EO/RW/'+'00'+str(self.id)+'/'+year)
            elif len(str(self.id)) == 2:
                vals = str('EO/RW/'+'0'+str(self.id)+'/'+year)
            else:
                vals = str('EO/RW/'+str(self.id)+'/'+year)
            self.eo_number = vals




class MaintenanceInstruction(models.Model):
    _name = 'document.mi'
    _description = 'Maintenance Instruction'
    _rec_name = 'no'

    no      = fields.Char(string="No.", compute='nama')
    date   = fields.Date(string="Date", required=True)
    attend   = fields.Char(string="Attnd", required=True)
    ac_type = fields.Many2one('aircraft.aircraft', string="A/C Type", required=True)
    ac_req  = fields.Many2one('aircraft.acquisition', string="A/C Reg.", required=True)
    ac_sn   = fields.Char(string="A/C S/N", related='ac_req.vin_sn')
    subject = fields.Char(string="Subject", required=True)
    reference   = fields.Char(string="Reference")
    eff_date    = fields.Date(string="Eff. Date")
    system_ata  = fields.Char(string="System/ATA")
    compliance  = fields.Selection([('draft','Draft'),('onprogress','On Progress'),('notcomply','Not Comply'),('complied','Complied'),], string="Compliance")
    text  = fields.Html(string="")
    ce_check = fields.Boolean(string="Chief Engineering")
    cq_check = fields.Boolean(string="Chief Quality")
    qq_check = fields.Boolean(string="QA & QM Manager")
    ata_code =  fields.Char(string="ATA Breakdown")
    compliance_sheet =  fields.Boolean(string="Compliance Sheet")
    remark_ref          = fields.Text(string="Remark")

    file_uploads    = fields.Binary(string="File Uploads")
    filename        = fields.Char(string="Filename")



    @api.one
    @api.model
    def nama(self):
        if self.ac_req.category == 'fixedwing':
            # seq = self.env['ir.sequence'].next_by_code('receiving.inventory')
            year = datetime.now().strftime('%Y')
            if len(str(self.id)) == 1:
                vals = str('MI/FW/'+'00'+str(self.id)+'/'+year)
            elif len(str(self.id)) == 2:
                vals = str('MI/FW/'+'0'+str(self.id)+'/'+year)
            else:
                vals = str('MI/FW/'+str(self.id)+'/'+year)
            self.no = vals
        if self.ac_req.category == 'rotary':
            # seq = self.env['ir.sequence'].next_by_code('receiving.inventory')
            year = datetime.now().strftime('%Y')
            if len(str(self.id)) == 1:
                vals = str('MI/RW/'+'00'+str(self.id)+'/'+year)
            elif len(str(self.id)) == 2:
                vals = str('MI/RW/'+'0'+str(self.id)+'/'+year)
            else:
                vals = str('MI/RW/'+str(self.id)+'/'+year)
            self.no = vals



class TechnicalInformation(models.Model):
    _name = 'document.ti'
    _description = 'Technical Information'
    _rec_name = 'no'

    no      = fields.Char(string="No.", compute='nama')
    date   = fields.Date(string="Date", required=True)
    attend   = fields.Char(string="Attnd", required=True)
    ac_type = fields.Many2one('aircraft.aircraft', string="A/C Type", required=True)
    ac_req  = fields.Many2one('aircraft.acquisition', string="A/C Reg.", required=True)
    ac_sn   = fields.Char(string="A/C S/N", required=True)
    subject = fields.Char(string="Subject", required=True)
    reference   = fields.Char(string="Reference")
    eff_date    = fields.Date(string="Eff. Date")
    system_ata  = fields.Char(string="System/ATA")
    compliance  = fields.Selection([('draft','Draft'),('onprogress','On Progress'),('notcomply','Not Comply'),('complied','Complied'),], string="Compliance")
    text  = fields.Html(string="")
    ce_check = fields.Boolean(string="Chief Engineering")
    cq_check = fields.Boolean(string="Chief Quality")
    qq_check = fields.Boolean(string="QA & QM Manager")
    ata_code =  fields.Char(string="ATA Breakdown")
    compliance_sheet =  fields.Boolean(string="Compliance Sheet")

    file_uploads    = fields.Binary(string="File Uploads")
    filename        = fields.Char(string="Filename")


    @api.one
    @api.model
    def nama(self):
        if self.ac_req.category == 'fixedwing':
            # seq = self.env['ir.sequence'].next_by_code('receiving.inventory')
            year = datetime.now().strftime('%Y')
            if len(str(self.id)) == 1:
                vals = str('TI/FW/'+'00'+str(self.id)+'/'+year)
            elif len(str(self.id)) == 2:
                vals = str('TI/FW/'+'0'+str(self.id)+'/'+year)
            else:
                vals = str('TI/FW/'+str(self.id)+'/'+year)
            self.no = vals
        if self.ac_req.category == 'rotary':
            # seq = self.env['ir.sequence'].next_by_code('receiving.inventory')
            year = datetime.now().strftime('%Y')
            if len(str(self.id)) == 1:
                vals = str('TI/RW/'+'00'+str(self.id)+'/'+year)
            elif len(str(self.id)) == 2:
                vals = str('TI/RW/'+'0'+str(self.id)+'/'+year)
            else:
                vals = str('TI/RW/'+str(self.id)+'/'+year)
            self.no = vals

class DocumentInheritToolMovement(models.Model):
    _inherit = 'tool.movement'

    refer_eo = fields.Many2one('document.eo', string="Ref. Numbers")
    refer_mi = fields.Many2one('document.mi', string="Ref. Numbers")
    refer_ti = fields.Many2one('document.ti', string="Ref. Numbers")
    refer_oti = fields.Many2one('document.oti', string="Ref. Numbers")