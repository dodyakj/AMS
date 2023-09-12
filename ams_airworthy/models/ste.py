# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SHORTTERMESCALATIONREQUEST(models.Model):
    _name = 'airworthy.ste'
    _description = 'SHORT TERM ESCALATION REQUEST'
    _rec_name = 'fleet_id'

    name    = fields.Char(string='Request Number',required=True)
    date = fields.Date(string='Date', default=fields.Date.today())
    date_limit = fields.Date(string='Limit  Date', default=fields.Date.today())
    value = fields.Integer(string='Request Value')
    reason = fields.Text(string='Reason')
    service_life_id = fields.Many2one("ams.component.servicelife", string="Service Life", default=lambda self:self.env.context.get('serfice_life_id',False),readonly=True)
    part_id = fields.Many2one('ams.component.part', string='Part', related='service_life_id.part_id',readonly=True)
    bulletin_id = fields.Many2one('ams.bulletin', string='AD / SB / STC', compute='_get_bulletin', readonly=True)
    fleet_id    = fields.Many2one("aircraft.acquisition", string="A/C Registration", default=lambda self:self._get_fleet(),readonly=True)
    model_id    = fields.Many2one("aircraft.type", string="A/C Make/Model", related="fleet_id.aircraft_type_id", readonly=True)

    status = fields.Selection([('waiting','Waiting'),('concur','Concur'),('nonconcur','Non-Concur'),('qaapprove','Approve by QA / QM'),('qadisapprove','Dis-Approve by QA / QM'),('dgcaapprove','Approve by DGCA'),('dgcadisapprove','Dis-Approve by DGCA')],string="Status",default="waiting")
    
    concur_date = fields.Date(string='Date', readonly=True)
    qa_approve_date = fields.Date(string='QA / QM Approved/Rejected Date', readonly=True)
    dgca_approve_date = fields.Date(string='DGCA Approved/Rejected Date', readonly=True)
    dgca        = fields.Boolean(string="DGCA")
    

    create_by = fields.Many2one('hr.employee', readonly=True, string="Requested By")
    concur_by = fields.Many2one('hr.employee', readonly=True, string="Approved/Rejected By")
    qa_approval_by = fields.Many2one('hr.employee', readonly=True, string="QA/QM Approved/Rejected By")
    dgca_approval_by = fields.Many2one('hr.employee', readonly=True, string="DGCA Approved/Rejected By")

    @api.multi
    def acc_concur(self):
        self.env['airworthy.ste'].search([('id','=',self.id)]).write({
            'status' : 'concur',
            'concur_date' : fields.Date.today(),
            'concur_by' : self.env['hr.employee'].search([('user_id', '=', self.env.user.id)]).id,
            })
        return True

    @api.multi
    def reject_concur(self):
        self.env['airworthy.ste'].search([('id','=',self.id)]).write({
            'status' : 'nonconcur',
            'concur_date' : fields.Date.today(),
            'concur_by' : self.env['hr.employee'].search([('user_id', '=', self.env.user.id)]).id,
            })
        return True

    @api.multi
    def acc_qa(self):
        self.env['airworthy.ste'].search([('id','=',self.id)]).write({
            'status' : 'qaapprove',
            'qa_approve_date' : fields.Date.today(),
            'qa_approval_by' : self.env['hr.employee'].search([('user_id', '=', self.env.user.id)]).id,
            })
        return True

    @api.multi
    def reject_qa(self):
        self.env['airworthy.ste'].search([('id','=',self.id)]).write({
            'status' : 'qadisapprove',
            'qa_approve_date' : fields.Date.today(),
            'qa_approval_by' : self.env['hr.employee'].search([('user_id', '=', self.env.user.id)]).id,
            })
        return True

    @api.multi
    def acc_dgca(self):
        self.env['airworthy.ste'].search([('id','=',self.id)]).write({
            'status' : 'dgcaapprove',
            'dgca_approve_date' : fields.Date.today(),
            'dgca_approval_by' : self.env['hr.employee'].search([('user_id', '=', self.env.user.id)]).id,
            })
        slive = self.env['ams.component.servicelife'].search([('id','=',self.service_life_id.id)])
        slive.write({
                'extension' : self.value,
                'remaining' : slive.remaining + self.value,
            })
        return True

    @api.multi
    def reject_dgca(self):
        self.env['airworthy.ste'].search([('id','=',self.id)]).write({
            'status' : 'dgcadisapprove',
            'dgca_approve_date' : fields.Date.today(),
            'dgca_approval_by' : self.env['hr.employee'].search([('user_id', '=', self.env.user.id)]).id,
            })
        return True

    def _get_fleet(self):
        slive = self.env['ams.component.servicelife'].search([('id','=',self.env.context.get('serfice_life_id',False))])
        if slive.bulletin_affected_id or slive.part_id:
            if slive.part_id.part_id.id != False:
                return slive.part_id.part_id.fleet_id.id
            elif slive.part_id.fleet_id.id != False:
                return slive.part_id.fleet_id.id
            elif slive.bulletin_affected_id.fleet_id.id != False:
                return slive.bulletin_affected_id.fleet_id.id
            else:
                return False

    @api.depends('service_life_id')
    def _get_bulletin(self):
        if(self.bulletin_id.id != False):
            self.bulletin_id = self.service_life_id.bulletin_affected_id.bulletin_id.id
        

    @api.model
    def create(self, values):
        # TUNGGU ACC
        values['create_by'] = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)]).id
        # slive = self.env['ams.component.servicelife'].search([('id','=',self.env.context.get('serfice_life_id',False))])
        # slive.write({
        #         'extension' : values['value'],
        #         'remaining' : slive.remaining + values['value'],
        #     })
        return super(SHORTTERMESCALATIONREQUEST, self).create(values)


