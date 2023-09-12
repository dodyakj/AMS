# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import  ValidationError

class AmsChecklist(models.Model):
    _name = 'ams.checklist'
    _description = 'Checklist'
    _rec_name = 'number'

    # name = fields.Char(string='Checklist Number',required=True)
    checklist_model_id = fields.Many2one('ams.checklist.type', string='Checklist Number',required=True)
    number = fields.Char(string='Revision Number',required=True)
    # checklist_for = fields.Selection([('ad','AD'),('sb','SB'),('stc','STC'),('wo','WO'),('mwo','MWO'),('inspection','Inspection')],string="Checklist For")
    todo_ids = fields.One2many('ams.checklist.todo','checklist_id',string='To Do')
    desc = fields.Text(string='Description')
    file_name = fields.Char('File Name')
    file = fields.Binary(string='Scan File')


    # @api.multi
    # @api.constrains('file_name', 'file')
    # def date_constrains(self):
    #     for rec in self:
    #         if not rec.file_name.endswith('.DBF'):
    #             raise ValidationError(_('Sorry, File Extension Must PDF'))


    @api.model
    def create(self, values):
        for rec in self:
            if not rec.file_name.endswith('.DBF'):
                raise ValidationError(_('Sorry, File Extension Must PDF'))
        return super(AmsChecklist, self).create(values)


    # @api.one
    # def _compute_name(self):
    #     if self.id:
    #         self.file_name = str(self.number+".pdf")
            

class AmsChecklistTodo(models.Model):
    _name = 'ams.checklist.todo'
    _description = 'Task'

    name = fields.Char(string='Task',required=True)
    checklist_id = fields.Many2one('ams.checklist',string='Checklist')


class AmsChecklistType(models.Model):
    _name = 'ams.checklist.type'
    _description = 'Model ID'

    name = fields.Char(string='Checklist Type')