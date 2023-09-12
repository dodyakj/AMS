from odoo import models, fields, api, _
from datetime import datetime, timedelta
import xlwt
from xlsxwriter import *
from cStringIO import StringIO
import base64
from reportlab.pdfgen import canvas
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx


class ComponentRemovalReport(models.Model):
    _name = 'ams.componentremoval.report'
    _description = 'Component Removal'


    date = fields.Date(string='Date', default=datetime.now())
    aircraft_model_id = fields.Many2one('aircraft.type', string='Aircraft Model')
    data_ids = fields.One2many('ams.componentremoval.data','removal_id',string='Data',)
    # year = fields.selection([(y, str(y)) for y in range(1970, (datetime.now().year + 30)+1 )], 'Year')

    @api.onchange('aircraft_model_id','date')
    def _onchange_aircraft_model_id(self):
        data_ids = False
        selected_fleet = []
        for g in self.env['aircraft.acquisition'].search([('aircraft_type_id','=',self.aircraft_model_id.id)]):
            selected_fleet.append(g.id)
        comphis = []
        comp = []

        fleet_before = False
        comp_before = False
        stat_before = False
        year = datetime.strptime(self.date, '%Y-%m-%d').strftime('%Y')
        data = self.env['ams.component_history'].search(['&',('part_id','!=',False),('fleet_id','in',selected_fleet)],order='fleet_id ASC, premature_removal ASC, component_id ASC')
        for i in data:
            if((fleet_before != i.fleet_id) or (comp_before != i.component_id) or (stat_before != i.premature_removal)):
                comphis.append((0, 0,{
                    'ata_id' : i.part_id.ata_code,
                    'product_id' : i.component_id,
                    'fleet_id' : i.fleet_id,
                    'jan' : len(self.env['ams.component_history'].search(['&','&','&',('date','ilike',str(year) + '-01'),('fleet_id' ,'=', i.fleet_id.id),('component_id','=',i.component_id.id),('premature_removal','=',i.premature_removal)])),
                    'feb' : len(self.env['ams.component_history'].search(['&','&','&',('date','ilike',str(year) + '-02'),('fleet_id' ,'=', i.fleet_id.id),('component_id','=',i.component_id.id),('premature_removal','=',i.premature_removal)])),
                    'mar' : len(self.env['ams.component_history'].search(['&','&','&',('date','ilike',str(year) + '-03'),('fleet_id' ,'=', i.fleet_id.id),('component_id','=',i.component_id.id),('premature_removal','=',i.premature_removal)])),
                    'apr' : len(self.env['ams.component_history'].search(['&','&','&',('date','ilike',str(year) + '-04'),('fleet_id' ,'=', i.fleet_id.id),('component_id','=',i.component_id.id),('premature_removal','=',i.premature_removal)])),
                    'mei' : len(self.env['ams.component_history'].search(['&','&','&',('date','ilike',str(year) + '-05'),('fleet_id' ,'=', i.fleet_id.id),('component_id','=',i.component_id.id),('premature_removal','=',i.premature_removal)])),
                    'jun' : len(self.env['ams.component_history'].search(['&','&','&',('date','ilike',str(year) + '-06'),('fleet_id' ,'=', i.fleet_id.id),('component_id','=',i.component_id.id),('premature_removal','=',i.premature_removal)])),
                    'jul' : len(self.env['ams.component_history'].search(['&','&','&',('date','ilike',str(year) + '-07'),('fleet_id' ,'=', i.fleet_id.id),('component_id','=',i.component_id.id),('premature_removal','=',i.premature_removal)])),
                    'agu' : len(self.env['ams.component_history'].search(['&','&','&',('date','ilike',str(year) + '-08'),('fleet_id' ,'=', i.fleet_id.id),('component_id','=',i.component_id.id),('premature_removal','=',i.premature_removal)])),
                    'sep' : len(self.env['ams.component_history'].search(['&','&','&',('date','ilike',str(year) + '-09'),('fleet_id' ,'=', i.fleet_id.id),('component_id','=',i.component_id.id),('premature_removal','=',i.premature_removal)])),
                    'okt' : len(self.env['ams.component_history'].search(['&','&','&',('date','ilike',str(year) + '-10'),('fleet_id' ,'=', i.fleet_id.id),('component_id','=',i.component_id.id),('premature_removal','=',i.premature_removal)])),
                    'nov' : len(self.env['ams.component_history'].search(['&','&','&',('date','ilike',str(year) + '-11'),('fleet_id' ,'=', i.fleet_id.id),('component_id','=',i.component_id.id),('premature_removal','=',i.premature_removal)])),
                    'des' : len(self.env['ams.component_history'].search(['&','&','&',('date','ilike',str(year) + '-12'),('fleet_id' ,'=', i.fleet_id.id),('component_id','=',i.component_id.id),('premature_removal','=',i.premature_removal)])),
                }))
                fleet_before = i.fleet_id
                comp_before = i.component_id
                stat_before = i.premature_removal

        self.data_ids = comphis



    @api.multi
    def print_componentremoval_pdf(self):
        return self.env['report'].get_action(self, 'ams_report.componentremoval_pdf')

        # specomp.append((0, 0,{
        #     'is_subcomp':False,
        #     'installed_at':comp.ac_timeinstallation if slive.unit not in ['year','month','days'] else slive.current_date,
        #     'ata':comp.ata_code.name,
        #     'tsn':comp.tsn if slive.unit not in ['year','month','days'] else '',
        #     'tso':comp.tso if slive.unit not in ['year','month','days'] else '',
        #     'at_installation': comp.comp_timeinstallation if slive.unit not in ['year','month','days'] else '',
        #     'component_id': comp.id,
        #     'expired': self.countDate(self.fleet_id,slive.id) if slive.unit not in ['year','month','days'] else slive.next_date,
        #     'remaining': slive.remaining if slive.unit not in ['year','month','days'] else str(delta.days) + 'days',
        #     'service_life':self.getSliveText(slive.id),
        #     'due_at':slive.value,
        #     'comment':slive.comments,
        # }))
            


class ComponentRemovalData(models.Model):
    _name = 'ams.componentremoval.data'
    _description = 'Removal Data'

    removal_id = fields.Many2one('ams.componentremoval.report',string='Removal Id')
    ata_id = fields.Many2one('ams.ata',string='ATA')
    product_id = fields.Many2one('product.product',string='Product')
    fleet_id = fields.Many2one('aircraft.acquisition',string='REG')

    jan = fields.Integer(string='JAN')
    feb = fields.Integer(string='FEB')
    mar = fields.Integer(string='MAR')
    apr = fields.Integer(string='APR')
    mei = fields.Integer(string='MEI')
    jun = fields.Integer(string='JUN')
    jul = fields.Integer(string='JUL')
    agu = fields.Integer(string='AGU')
    sep = fields.Integer(string='SEP')
    okt = fields.Integer(string='OKT')
    nov = fields.Integer(string='NOV')
    des = fields.Integer(string='DES')
