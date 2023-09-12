# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AMSCamp(models.Model):
    _name = 'ams.camp'
    _description = 'Maintenance Program'
    _rec_name = 'number'

    aircraft_model_id = fields.Many2one('aircraft.type', string='Aircraft Model', required=True)
    date_issued = fields.Date(string='Date Issued', default=fields.Date.today(), required=True)
    number = fields.Char(string='Revision Number', required=True)
    file_name = fields.Char('File Name')
    file = fields.Binary(string='File Scan')

    # @api.one
    # def _upload_name(self):
    #     if self.id:
    #         self.file_name = str(self.number+".pdf")


    