# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _

class MELAircraft(models.Model):
    _name = 'ams.mel'
    _description = 'Minimum Equipment List'

    name = fields.Char(string='Type',required=True)
    description = fields.Text(string='Description')


class MELAircraft(models.Model):
    _name = 'airworthy.mel'
    _rec_name = 'no'

    no      = fields.Char(string="No.", compute='nama')
    date    = fields.Date(string="Date", default=datetime.now(),required=True)
    ac_type = fields.Many2one('aircraft.type', string="Aircraft Type", related='ac_req.aircraft_type_id')
    ac_req  = fields.Many2one('aircraft.acquisition', string="Aircraft Registration",required=True)
    ata_mel     = fields.Many2one('ams.ata', string="ATA MEL Number")
    mel_categ   = fields.Many2one('ams.mel', string="MEL Category",required=True)
    reason      = fields.Char(string="Reason for Extention",required=True)
    date_became = fields.Date(string="Date item became unserviceable",required=True)
    date_schedule   = fields.Date(string="Original Date of item scheduled for carried out")
    location_became = fields.Many2one('base.operation',string="Location item became unserviceable",required=True)
    location_schedule   = fields.Many2one('base.operation',string="Original Location of item scheduled for carried out")
    compliance      = fields.Selection([('draft','Draft'),('onprogress','On Progress'),('notcomply','Not Comply'),('complied','Complied'),], string="Compliance")
    part_id     = fields.Many2one('ams.component.part', string="Name of item required")
    part_number = fields.Char(related='part_id.product_id.default_code')
    date_order  = fields.Date(string="Date Part Ordered")
    date_deliv  = fields.Date(string="Confirmed delivery Date")
    date_new    = fields.Date(string="New date carried out scheduled")
    date_dgac   = fields.Date(string="DGAC Representatives notified")
    date_limit  = fields.Date(string="Time limit valid to",required=True)
    dgca        = fields.Boolean(string="DGCA")

    request_by = fields.Many2one('res.partner', string="Request By")
    qc_by      = fields.Many2one('res.partner', string="Quality Control By")
    app_by     = fields.Many2one('res.partner', string="Approved by")
    date_req   = fields.Date(string="Request date")
    date_qc    = fields.Date(string="Quality Control Date")


    @api.one
    @api.model
    def nama(self):
            year = datetime.now().strftime('%Y')
            zero = len(str(self.id))
            if len(str(self.id)) == zero:
                vals = str('00'+str(self.id)+'/MEL/EXT'+'/'+year)
            elif len(str(self.id)) == zero:
                vals = str('0'+str(self.id)+'/MEL/EXT'+'/'+year)
            else:
                vals = str(str(self.id)+'/MEL/EXT'+'/'+year)
            self.no = vals