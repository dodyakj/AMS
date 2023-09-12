# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import  ValidationError

# class VerifyFlight(models.Model):
#     _name = 'verify.flight'

#     verify_flight = fields.Selection([('airframes','Airframes'),('engine','Engine'),('auxiliary','Auxiliary')], string='Print Units', required=False)
#     verify_airframe = fields.Many2one('aircraft.acquisition', string="Airframes")
#     verify_engines = fields.Many2one('maintenance.equipment', string="Engine")
#     verify_auxiliary = fields.Many2one('maintenance.equipment', string="Auxiliary")
#     include	= fields.Boolean('Include Attached Units')
#     verify_print_des = fields.Selection([('screen','Screen'),('printer','Printer'),('printerwithprompt','Printer with Prompt')], string='Print Destination', required=False)
#     start_date = fields.Date('Start Date', default=fields.Date.today)
#     end_date = fields.Date('Start Date', default=fields.Date.today)
#     sort_option = fields.Selection([('flightdate','Flight Date'),('referenceno','Reference No.'),('a/c','A/C Serial No.')], string='Sort Option', required=False)
#     quick_view 	= fields.Char('Quick View By Log No.')
#     quick_desc = fields.Text()


class ManualChanges(models.Model):
    _name = 'verify.manualchange'
    _description = 'Manual Changes'

    all_airframe  = fields.Boolean('All Aircraft', default=True)
    all_engine    = fields.Boolean('All Engine', default=True)
    all_auxiliary = fields.Boolean('All Auxiliary', default=True)

    airframe  = fields.Many2one('aircraft.acquisition', string="Airframes")
    engines   = fields.Many2one('maintenance.equipment', string="Engine")
    auxiliary = fields.Many2one('maintenance.equipment', string="Auxiliary")

    no_airframe  = fields.Boolean('None')
    no_engines   = fields.Boolean('None')
    no_auxiliary = fields.Boolean('None')

    start_date	= fields.Date('Starting Date')
    end_date 	= fields.Date('Ending Date')

    @api.multi
    @api.constrains('end_date', 'start_date')
    def date_constrains(self):
        for rec in self:
            if rec.end_date < rec.start_date:
                raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))

