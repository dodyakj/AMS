# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api 
from datetime import datetime, timedelta


class FleetwideReport(models.Model):
    _name = 'report.fleetwide_bulletin'
    _description = 'Fleetwide Bulletin Report'

    type = fields.Selection([('all','All'),('sb','SB'),('ad','AD'),('stc','STC')], required=True, default='all')
    number_sb = fields.Many2one('ams.bulletin', string="Bulletin Number", domain=[('type','=','SB')])
    number_ad = fields.Many2one('ams.bulletin', string="Bulletin Number", domain=[('type','=','AD')])
    number_stc = fields.Many2one('ams.bulletin', string="Bulletin Number", domain=[('type','=','STC')])
    order_by = fields.Selection([('fleet_id','AC.Reg'),('date','Date'),('name','Numbers')], default='fleet_id')
    sort_by = fields.Selection([('asc','ASC'),('desc','DESC')], default='asc')
    bulletin_number = fields.Char(string="Bulletin Number")
    bulletin_id = fields.Many2many('ams.bulletin', string="Bulletin Number", compute="_get_bulletin")
    bulletin_sb = fields.Many2many('ams.bulletin', string="Bulletin Number", compute="_onchange_comp")
    bulletin_ad = fields.Many2many('ams.bulletin', string="Bulletin Number", compute="_onchange_comp")
    bulletin_stc = fields.Many2many('ams.bulletin', string="Bulletin Number", compute="_onchange_comp")
    date = fields.Date(string='Date', default= lambda *a:datetime.now().strftime('%Y-%m-%d'))

    @api.onchange('type')
    def _onchange_type(self):
        if self.type == 'all':
            self.number_sb = False
            self.number_ad = False
            self.number_stc = False

    @api.model
    def _get_bulletin(self):
        if self.bulletin_number:
            all_bull = self.env['ams.bulletin'].search([('name', 'like', self.bulletin_number)])
        else:
            all_bull = self.env['ams.bulletin'].search([])

        # print self.bulletin_number
        self.bulletin_id = all_bull
      
    @api.multi
    def print_fbr_pdf(self):
        return self.env['report'].get_action(self, 'ams_bulletin.report_fbr')



    def rendering(self):
        search_param_sb = []
        search_param_ad = []
        search_param_stc = []
        search_param_sb.append(('type','=','SB'))
        search_param_ad.append(('type','=','AD'))
        search_param_stc.append(('type','=','STC'))

        if self.number_sb:
            search_param_sb.append(('id','=',self.number_sb.id))
        if self.number_ad:
            search_param_ad.append(('id','=',self.number_ad.id))
        if self.number_stc:
            search_param_stc.append(('id','=',self.number_stc.id))
            

        if self.bulletin_number:
            search_param_sb.append(('name','like',self.bulletin_number))
            search_param_ad.append(('name','like',self.bulletin_number))
            search_param_stc.append(('name','like',self.bulletin_number))
            sb = self.env['ams.bulletin'].search(search_param_sb, order=str(self.order_by+' '+self.sort_by))
            ad = self.env['ams.bulletin'].search(search_param_ad, order=str(self.order_by+' '+self.sort_by))
            stc = self.env['ams.bulletin'].search(search_param_stc, order=str(self.order_by+' '+self.sort_by))
        else:
            sb = self.env['ams.bulletin'].search(search_param_sb, order=str(self.order_by+' '+self.sort_by))
            ad = self.env['ams.bulletin'].search(search_param_ad, order=str(self.order_by+' '+self.sort_by))
            stc = self.env['ams.bulletin'].search(search_param_stc, order=str(self.order_by+' '+self.sort_by))

        self.bulletin_sb = sb
        self.bulletin_ad = ad
        self.bulletin_stc = stc

    @api.onchange('bulletin_number')
    def _onchange_comp(self):
        self.rendering()


class FleetwideReport(models.Model):
    _name = 'bulletin.aircraft.affected.report'
    _description = 'Complied Bulletin Report'

    type = fields.Many2one('aircraft.acquisition', string="Fleet")
    order_by = fields.Selection([('fleet_id','AC.Reg'),('create_date','Date'),('bulletin_id','Bulletin')], default='fleet_id')
    sort_by = fields.Selection([('asc','ASC'),('desc','DESC')], default='asc')
    date = fields.Date(string='Date', default= lambda *a:datetime.now().strftime('%Y-%m-%d'))
    bulletin_id = fields.Many2many('bulletin.aircraft.affected', string="Bulletin Number", compute="_get_complied")

    @api.model
    def _get_complied(self):
        if self.type:
            comple = self.env['bulletin.aircraft.affected'].search([('fleet_id', '=', self.type.id)], order=str(self.order_by+' '+self.sort_by))
        else:
            comple = self.env['bulletin.aircraft.affected'].search([('')], order=str(self.order_by+' '+self.sort_by))
        self.bulletin_id = comple
      
    @api.multi
    def print_complied_bulletin(self):
        return self.env['report'].get_action(self, 'ams_bulletin.report_complied')


class AmsAlterationReport(models.Model):
    _name = 'bulletin.alteration.report'
    _description = 'Modification / Aircraft Alteration Report'

    fleet_id = fields.Many2one('aircraft.acquisition', string='Aircraft')
    date = fields.Date(string='Date Issued')
    number = fields.Char('Alteration Number')
    status  = fields.Selection([('open', 'Open'),('close', 'Close')], string="Status")

    order_by = fields.Selection([('date','Date'),('fleet_id','Aircraft'),('name','Number')], default='date')
    sort_by = fields.Selection([('asc','ASC'),('desc','DESC')], default='asc')

    alteration_id = fields.Many2many('bulletin.alteration', compute=lambda self: self._onchange_comp())

    @api.multi
    def print_alteration(self):
        return self.env['report'].get_action(self, 'ams_bulletin.report_alteration_pdf')

    def rendering(self):
        search_param = []
        search_param.append(('state','=','validate'))
        if self.fleet_id:
            search_param.append(('fleet_id','=',self.fleet_id.id))
        if self.date:
            search_param.append(('date','=',self.date))
        if self.number:
            search_param.append(('name','like',self.number))
        if self.status:
            search_param.append(('status', '=', self.status))
           
        push_data = self.env['bulletin.alteration'].search(search_param, order=str(self.order_by+' '+self.sort_by))
        self.alteration_id = push_data

    @api.onchange('fleet_id')
    def _onchange_comp(self):
        self.rendering()