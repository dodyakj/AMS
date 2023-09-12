from datetime import datetime, timedelta
from odoo import models, fields, api
from odoo.tools.translate import _

class MaintenanceTracking(models.Model):
    _name = 'maintenance.tracking.report'
    _description = 'Maintenance tracking Report'

    type = fields.Selection([('all','All'),('fleet','Aircraft'),('engine','Engine'),('auxiliary','Auxiliary'),('propeller','Propeller')], string='Type', default="all", required=True)
    date =  fields.Date(' ', default= lambda *a:datetime.now().strftime('%Y-%m-%d'))
    fleet_id = fields.Many2one('aircraft.acquisition', string='Aircraft')
    engine_id = fields.Many2one('engine.spare', string='Engine')
    auxiliary_id = fields.Many2one('auxiliary.spare', string='Auxiliary')
    propeller_id = fields.Many2one('propeller.spare', string='Propeller')
    include_attach = fields.Boolean(string='Include Attached Unit')
    show_nearly = fields.Boolean(string='Show Nearly Tracking Component')
    orderby = fields.Selection([('ata','ATA Code'),('tracking','Tracking Calendar'),('component','Component Name'),('project','Project Date'),('time','Time Remaining'),('ac_serial','A/C Serial No.')], string='Order By')

    filter_ata = fields.Char('ATA Filter')
    fill_component = fields.Boolean('Component')
    fill_bulletin = fields.Boolean('Bulletin')
    fill_inspection = fields.Boolean('Inspection')

    hour_limit_id = fields.One2many('hour.limit.mtr', 'hour_id', required=True, compute="_get_hour")
    calendar_limit_id = fields.One2many('calendar.limit.mtr', 'calendar_id', required=True, compute="_get_calendar")


    @api.onchange('type')
    def _onchange_type(self):
        self.engine_id = []
        self.fleet_id = []
        self.auxiliary_id = []
        self.propeller_id = []
        self.env["maintenance.tracking.report"].search([]).unlink()

    @api.multi
    def print_main_tracking_pdf(self):
        return self.env['report'].get_action(self, 'ams_document.report_maintenance_tracking')

    @api.model
    def _get_hour(self):
        if self.type == 'fleet':
            data_hour = self.env['aircraft.acquisition'].search([('name','=',self.fleet_id.name)])
        else:
            data_hour = self.env['aircraft.acquisition'].search([])

        
        for reports in data_hour:
            for component in reports.component_ids:
                # print 'vvvvvvvvvvvvvvvvvvvvvvvv'
                # print component.sub_part_ids
                # for sub_component in component.sub_part_ids:
                for service in component.serfice_life:
                    params = {
                            'hour_limit_mtr_id':self.id,
                            'fleet_id': reports.name, 
                            'name': component.product_id.id, 
                            'sub_name': component.sub_part_ids.id, 
                            'part': component.part_number, 
                            'serial': component.serial_number.name, 
                            'ata' : component.ata_code.name, 
                            'item' : component.item, 
                            'service' : service.value, 
                            'install' : component.comp_timeinstallation, 
                            'done' : component.comp_timeinstallation, 
                            'time' : component.comp_timeinstallation, 
                            'project': component.date_installed, 
                            }
                    self.hour_limit_id |= self.env['hour.limit.mtr'].create(params)

    @api.model
    def _get_calendar(self):
        if self.type == 'fleet':
            data_calendar = self.env['aircraft.acquisition'].search([('name','=',self.fleet_id.name)])
        else:
            data_calendar = self.env['aircraft.acquisition'].search([])
        for data in data_calendar:
            for comp in data.component_ids:
                for serv in comp.serfice_life:
                    params = {
                            'calendar_limit_mtr':self.id,
                            'fleet_id': data.name, 
                            'name': comp.product_id.id, 
                            'part': comp.part_number, 
                            'serial': comp.serial_number.name, 
                            'ata' : comp.ata_code.name, 
                            'item' : comp.item, 
                            'service' : serv.value, 
                            'install' : comp.comp_timeinstallation, 
                            'done' : comp.comp_timeinstallation, 
                            'time' : comp.comp_timeinstallation, 
                            'project': comp.date_installed,
                            }
                    self.calendar_limit_id |= self.env['calendar.limit.mtr'].create(params)

class hour_limit_mtr(models.Model):
    _name = 'hour.limit.mtr'
    _description = 'Hour Limit Group'

    fleet_id = fields.Char()
    name = fields.Many2one('product.product')
    sub_name = fields.Many2one('ams.component.part')
    part = fields.Char()
    serial = fields.Char()
    ata = fields.Char()
    item = fields.Char()
    service = fields.Char()
    install = fields.Char()
    done = fields.Char()
    time = fields.Char()
    project = fields.Char()

    hour_id = fields.Many2one('maintenance.tracking.report')

class calendar_limit_mtr(models.Model):
    _name = 'calendar.limit.mtr'
    _description = 'Calendar Limit Group'

    fleet_id = fields.Char()
    name = fields.Many2one('product.product')
    sub_name = fields.Many2one('ams.component.part')
    part = fields.Char()
    sub_part = fields.Char()
    serial = fields.Char()
    ata = fields.Char()
    item = fields.Char()
    service = fields.Char()
    install = fields.Char()
    done = fields.Char()
    time = fields.Char()
    project = fields.Char()

    calendar_id = fields.Many2one('maintenance.tracking.report')