# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api

class Pelita_Inspection(models.Model):
    _name = 'ams.inspection'
    _description = 'Inspection'
    _rec_name = 'inspection_type'

    status = fields.Selection([('uncomplied','Uncomplied'),('failed','Failed'),('complied','Complied')], string='Status', default="uncomplied")
    fleet_id = fields.Many2one('aircraft.acquisition', string='Fleet Id')
    engine_id = fields.Many2one('engine.type', string='Engine Id')
    auxiliary_id = fields.Many2one('auxiliary.type', string='Auxiliary Id')
    propeller_id = fields.Many2one('propeller.type', string='Propeller Id')
    
    inspection_type = fields.Char(string='Inspection Type', required=True)
    desc = fields.Text(string='Description')
    ata_code        = fields.Many2one('ams.ata', string="ATA Code")
    item = fields.Char(string='Item')
    na_reason = fields.Char(string='N/A Reason')
    master_insp_type = fields.Char(string='Master Inspection Type')
    
    one_time_insp  = fields.Boolean(string='One Time Inspection')

    since_insp = fields.Float()
    last_insp = fields.Float()

    install_at = fields.Char(string='Installed Date')

    # hours_on  = fields.Boolean(string='hours')
    # cycles_on  = fields.Boolean(string='cycles')
    # days_on  = fields.Boolean(string='days')
    # months_on  = fields.Boolean(string='months')
    # end_of_month_on  = fields.Boolean(string='end_of_month')

    # hours  = fields.Float(string='hours')
    # cycles  = fields.Float(string='cycles')
    # days  = fields.Float(string='days')
    # months  = fields.Float(string='months')
    # end_of_month  = fields.Float(string='end_of_month')

    serfice_life = fields.One2many('ams.component.servicelife','inspection_id',string='Service Life')


    # show = fields.Boolean(string='show')
    return_uncomplied = fields.Boolean(string='return_uncomplied')
    # hoobs = fields.Float(string='Hoobs')


    employee_id = fields.Many2one('hr.employee', string="Last Inspected by",default=False)
    work_order_id = fields.Many2one('project.project',string='Work Order')

    needed_component_ids = fields.One2many('inspection.component.needed','inspection_id',string='Affected Component')
    attachment_ids = fields.Many2many('ir.attachment', 'class_ir_attachments_rel', 'class_id', 'attachment_id', 'Attachments')

    checklist_id = fields.Many2one('ams.checklist', string='Checklist', context="{'order_display': 'create_date desc' }")

    todo_ids = fields.One2many('ams.checklist.todo','checklist_id',string='To Do',readonly=True,related='checklist_id.todo_ids')
    checklist_desc = fields.Text(string='Description',readonly=True,related='checklist_id.desc')

    file_name = fields.Char('File Name', related='checklist_id.file_name')
    checklist_file = fields.Binary(string='Scan File',readonly=True, related='checklist_id.file')

    # def _upload_name(self):
        # if self.file_name:
            # self.file_name = str(self.inspection_type+".pdf")
        
    #Function
    @api.onchange('employee_id')
    def sortir_checklist(self):
        data_ams_checklist = self.env['ams.checklist'].search([('id','!=', 0)],order='create_date desc')
        if data_ams_checklist:
            ids_ams_checklist = []
            for x in data_ams_checklist:
                ids_ams_checklist.append(x.id)
            self.checklist_id = ids_ams_checklist[0]

class BulletinComponentPartNeeded(models.Model):
    _name = 'inspection.component.needed'
    _description = 'Affected Needed'


    bulletin_inspection_id = fields.Many2one('ams.bulletin', string='Bulletin Id')
    inspection_id = fields.Many2one('ams.inspection', string='Inspection')
    product_id = fields.Many2one('product.product', string='Component Name', required=True)
    part_number = fields.Char(related='product_id.default_code',string="Part Number",readonly=True)
    amount = fields.Integer(string='Amount')
    in_inventory = fields.Integer(string='In Inventory',default='3',readonly=True)
