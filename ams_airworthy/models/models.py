# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SHORTTERMESCALATIONREQUEST(models.Model):
    _name = 'ams.ster'
    _description = 'SHORT TERM ESCALATION REQUEST'
    _rec_name = 'ac_reg'

    ac_reg		= fields.Many2one("aircraft.acquisition", string="A/C Registration")
    ac_model	= fields.Many2one("aircraft.type", string="A/C Make/Model", related="ac_reg.aircraft_type_id")
    type_insp	= fields.Many2one("ams.inspection", string="Type of Inspection")
    engine_pos	= fields.Char(string="Engine Position")
    comp_name	= fields.Many2one("ams.component.part", string="Component Name")
    part_no		= fields.Char(string="Part number", related="comp_name.part_number")
    serial_no	= fields.Many2one("stock.production.lot", string="Serial Number", related="comp_name.serial_number")
    reason		= fields.Char(string="Reason")
    limit		= fields.Char(string="Limit (Hours, Cycles, Calendar Days)")
    req_by		= fields.Many2one('res.partner', string="Requested By")
    req_date	= fields.Char(string="Requested Date")
    date_1		= fields.Char(string="Date")
    concur		= fields.Boolean(string="Concur")
    ste			= fields.Char(string="Short Term Escalation of")
    app_num		= fields.Char(string="Approval Number")
    app_by		= fields.Many2one('res.partner', string="Approved or Disapproved by")
    qa_qm		= fields.Char(string="QA & QM manager")
    DGCA_num	= fields.Char(string="DGCA Approval number")
    date_2		= fields.Char(string="Date")
