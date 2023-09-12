# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, _

class Training(models.Model):
    _name = 'ams.training'
    _rec_name = 'crew'
    _description = 'Training'

    crew       = fields.Many2one('hr.employee', string="Crew", required=True)
    type_psw   = fields.Many2one('aircraft.aircraft', string="A/C Type.")
    initial    = fields.Many2one('training.program', string="Initial Training", required=True)
    rec_stat   = fields.Boolean('Recurrent', default=True)
    rec        = fields.Integer('Year', default=2)
    customer   = fields.Char('Customer')
    training   = fields.Date('Training Schedule')


class TrainingProgram(models.Model):
    _name = 'training.program'
    _rec_name = 'name'
    _description = 'Training Program'

    project = fields.Many2one('ams.project', string="Project", required=True)
    name    = fields.Char(string="Training Name")
    man_pos   = fields.Many2one('employee.type', string="Mandatory For Position", default='all')
    # man_pos   = fields.Selection('_get_employee', string="Mandaroty For Position", default='all')
    mandatory = fields.Boolean(string="Mandatory")

    # @api.multi
    # def _get_employee(self):
    #    employee_id = self.env['employee.position'].search([])
    #    lst = [('all','All')]
    #    for employee in employee_id:
    #         lst.append((employee.name, employee.name))
    #    return lst


class EmployeeSetting(models.Model):
    _name = 'employee.setting'
    _rec_name = 'name'
    _description = 'Employee Setting'

    name = fields.Many2one('hr.employee', string="Employee", required=True)
    position = fields.One2many('employee.position', 'emp_id', string="Position")

class EmployeePosition(models.Model):
    _name = 'employee.position'
    _rec_name = 'name'
    _description = 'Employee Position'

    name = fields.Many2one('employee.type', string='Position', required=True)
    type_aircraft = fields.Many2one('aircraft.aircraft', string="Type Aircraft")
    emp_id = fields.Many2one('employee.setting', default=lambda self:self.env.context.get('default_config_id',False))

class JEmployee(models.Model):
    _name = 'employee.type'
    _description = 'Position'

    name = fields.Char('Position', required=True)