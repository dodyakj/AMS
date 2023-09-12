# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, _
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import  ValidationError

class componentReliability(models.Model):
    _name = 'ams.component.reliability'
    _description = 'Component Reliability'

    fleet = fields.Many2one('aircraft.acquisition' , 'Aircraft')
    component = fields.Many2one('ams.component.part', domain=lambda self: self._getpremature())

    ch_id = fields.Many2many('ams.component_history', compute=lambda self: self._onchange_fleet())


    @api.model
    def _getpremature(self):
        return {'domain':{'component':[('create_date','>=',datetime.now().strftime('%Y'))]}}


    @api.onchange('fleet')
    def _onchange_fleet(self):
        search_param = []
        search_param.append(('premature_removal','=',True))
        search_param.append(('component_id','!=',False))
        if self.fleet:
            search_param.append(('fleet_id','=',self.fleet.id))
        if self.component:
            search_param.append(('part_id','=',self.component.id))
        component = self.env['ams.component_history'].search(search_param)
        self.ch_id = component


    @api.multi
    def print_comp_reliability(self):
        return self.env['report'].get_action(self, 'ams_reliability.report_comp_reliability')



class engineReliability(models.Model):
    _name = 'ams.engine.reliability'
    _description = 'Engine Reliability'

    engine = fields.Many2one('engine.type' , 'Engine')
    base = fields.Many2one('base.operation')

    cr_id = fields.Many2many('ams.component.replace', compute=lambda self: self._onchange_engine())



    @api.onchange('engine')
    def _onchange_engine(self):
        search_param = []
        if self.engine:
            # search_param.append(('component.engine_id','!=',False))
            search_param.append(('component.engine_id','=', self.engine.id))
            # search_param.append(('engine_id','=',self.engine.id))
        if self.base:
            search_param.append(('warehouse_id','=',self.base.warehouse_id.id))
        component = self.env['ams.component.replace'].search(search_param)
        self.cr_id = component


    @api.multi
    def print_engine_reliability(self):
        return self.env['report'].get_action(self, 'ams_reliability.report_engine_reliability')            

class AmsReliability(models.Model):
    _name           = "ams.reliability"
    _description    =  'Engine reliability'
    

    fleet           = fields.Many2one('aircraft.acquisition' , 'Aircraft', domain="[('category', '=', 'rotary')]")
    action          = fields.Selection([('entry', 'Upload Entry'),('compute', 'Compute from FML')])
    upload_file     = fields.Binary(string="File Upload")
    filename        = fields.Char(String="File Name")   

    @api.multi
    def compute_fml(self):
        return {
            'name': 'Power Assurance Check',
            'type':'ir.actions.act_window',
            'view_mode':'form',
            'view_type': 'form',
            'res_id': False,
            'views': [(False, 'form')],
            'res_model':'ams.pac',
            'target': 'new',
            'context':{
                'fleet_id': self.fleet.id,
            },
         }

class RepetitiveDiscrepencies(models.Model):
    _name = 'ams.repetitive.dicripencies'
    _description = 'Repetitive Discrepencies'

    ac_reg  = fields.Many2one('aircraft.acquisition' , 'Ac. Reg')
    start_date  = fields.Date('Start Date')
    end_date   = fields.Date('End Date')

    dis_id = fields.Many2many('ams.discripencies', compute=lambda self: self._onchange_acreg())

    @api.multi
    @api.constrains('end_date', 'start_date')
    def date_constrains(self):
        for rec in self:
            if rec.end_date < rec.start_date:
                raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))

    @api.onchange('ac_reg')
    def _onchange_acreg(self):
        search_param = []
        if self.ac_reg:
            search_param.append(('fleet_id','=', self.ac_reg.id))
        if self.start_date and self.end_date:
            search_param.append(('create_date','>=',self.start_date))
            search_param.append(('create_date','<=',self.end_date))
        discre = self.env['ams.discripencies'].search(search_param)
        self.dis_id = discre


    @api.multi
    def print_repetitive_dicripencies(self):
        return self.env['report'].get_action(self, 'ams_reliability.report_repetitive_dicripencies')




            





