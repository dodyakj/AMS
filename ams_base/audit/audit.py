from odoo import fields, models, api

class Audit(models.Model):
    _name = 'audit.audit'
    _description = 'Audit'

    name = fields.Char('Audit', required=True)

class InternalAuditSchedule(models.Model):
    _name = 'internal.audit.schedule'
    _description = 'Internal Audit Schedule'

    # name =  fields.Many2one('audit.audit', string='Schedule')
    name =  fields.Char(string='Schedule Audit', size=64, required=True)
    user_id =  fields.Many2one('res.users', 'Users')
    from_datetime =  fields.Date('From Datetime')
    to_datetime =  fields.Date('To Datetime')

    # user_id 	= fields.Many2one('res.partner', default=lambda self:self.env.user.partner_id.id) 


class CorrectiveActionRequest(models.Model):
    _name = 'internal.audit.car'
    _description = 'Corrective Action Request'

    date  	= fields.Date(string='Date')
    place 	= fields.Many2one('area.operation', string='Place')
    ac_reg 	= fields.Many2one('aircraft.acquisition', string='A/C Registration')
    personel 	= fields.Char(string='Personel Auditor')
    type_audit 	= fields.Selection([('internal','Internal Audit'),('external','External Audit'),('third','Third Party Audit')] , string='Type of Audit / Inspection', readonly=True, default=lambda self:self.env.context.get('audit_type','internal'))
    auditee = fields.Char(string='Auditee')
    car_id = fields.One2many('audit.car', 'tree_id')

class TreeCorrectiveActionRequest(models.Model):
    _name = 'audit.car'
    _description = 'Menu Corrective Action Request'

    tree_id = fields.Many2one('internal.audit.car')
    finding = fields.Html(string='Findings')
    categ 	= fields.Selection([('y','y'),('n','n')] , string='Category')
    system 	= fields.Char(string='System & Root Cause')
    pre_action = fields.Char(string='Preventive Action')
    cor_action = fields.Char(string='Corrective Action')
    status 	   = fields.Selection([('y','y'),('n','n')], string='Status')
    tar_date   = fields.Date(string='Target Date')
    res_person = fields.Char(string='Responsible Person')
    verifi_by  = fields.Many2one('res.users', string='Verified By')
