from datetime import datetime, timedelta, date
import math
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, _

import xlwt
from xlsxwriter import *
from cStringIO import StringIO
import base64
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class MaintenanceDueReport(models.Model):
    _name = 'maintenance.due.report'
    _description = 'Maintenance Due Report'
    _rec_name = 'fleet_id'
    _inherit = ['ir.needaction_mixin']


    type = fields.Selection([('all','All'),('fleet','Aircraft'),('engine','Engine'),('auxiliary','Auxiliary'),('propeller','Propeller')], string='Type', default="fleet", required=True, readonly=True)
    date =  fields.Date(' ', default= lambda *a:datetime.now().strftime('%Y-%m-%d'))
    fleet_id = fields.Many2one('aircraft.acquisition', string='Aircraft', required=True)
    mdr_seq  = fields.Char(string="Number", store=True)
    rin_active = fields.Boolean(string='RIN Active',related='fleet_id.rin_active')
    engine_id = fields.Many2one('engine.spare', string='Engine')
    auxiliary_id = fields.Many2one('auxiliary.spare', string='Auxiliary')
    propeller_id = fields.Many2one('propeller.spare', string='Propeller')
    include_attach = fields.Boolean(string='Include Attached Unit',default=True)
    show_nearly = fields.Boolean(string='Show Nearly Due Component')
    orderby = fields.Selection([('ata','ATA Code'),('due','Due Calendar'),('component','Component Name'),('project','Project Date'),('time','Time Remaining'),('ac_serial','A/C Serial No.')], string='Order By')

    filter_ata = fields.Char('ATA Filter')
    fill_component = fields.Boolean('Component')
    fill_bulletin = fields.Boolean('Bulletin')
    fill_inspection = fields.Boolean('Inspection')

    hour_limit_id = fields.One2many('hour.limit.mdr', 'hour_id', store=True, compute="_get_hour")
    cycle_limit_id = fields.One2many('cycle.limit.mdr', 'cycle_id', store=True, compute="_get_cycle")
    rin_limit_id = fields.One2many('rin.limit.mdr', 'rin_id', store=True, compute="_get_rin")
    calendar_limit_id = fields.One2many('calendar.limit.mdr', 'calendar_id', store=True, compute="_get_calendar")
    certificate_limit_id = fields.One2many('certificate.limit.mdr', 'certificate_id', store=True, compute="_get_certificate")
    set_time_id = fields.Many2many('ams.config', compute='_get_setstime')

    warning_hours = fields.Integer(string="Warning Hours",default=lambda self:self._get_default_hours(), required=True)
    warning_cycles = fields.Integer(string="Warning Cycles",default=lambda self:self._get_default_cycles(), required=True)
    warning_rins = fields.Integer(string="Warning Rin",default=lambda self:self._get_default_rins())
    warning_calendars = fields.Date(string="Warning Calendars", default=datetime.now() + relativedelta(days=90), required=True)

    states = fields.Selection([('create_by','Draft'),('approved_by','Approved'),('done','QC Confirmed'),('expired','Expired')], default="create_by")
    create_by = fields.Many2one('res.partner', readonly=True)
    checked_by = fields.Many2one('res.partner', readonly=True)
    approved_by = fields.Many2one('res.partner', readonly=True)
    qc_by = fields.Many2one('res.partner', string="Quality Control", readonly=True)

    # ADDITIONAL INFORMATION
    create_at            = fields.Date(string='Create At')
    fleet_hours          = fields.Float(string='Fleet Hours On Create')
    fleet_cycles         = fields.Float(string='Fleet Cycles On Create')
    fleet_rins           = fields.Float(string='Fleet RINs On Create')

    engine1_hours        = fields.Float(string='Engine 1 Hours On Create')
    engine1_cycles       = fields.Float(string='Engine 1 Cycles On Create')

    engine2_hours        = fields.Float(string='Engine 2 Hours On Create')
    engine2_cycles       = fields.Float(string='Engine 2 Cycles On Create')

    engine3_hours        = fields.Float(string='Engine 3 Hours On Create')
    engine3_cycles       = fields.Float(string='Engine 3 Cycles On Create')

    engine4_hours        = fields.Float(string='Engine 4 Hours On Create')
    engine4_cycles       = fields.Float(string='Engine 4 Cycles On Create')

    auxiliary1_hours     = fields.Float(string='Auxiliary 1 Hours On Create')
    auxiliary1_cycles    = fields.Float(string='Auxiliary 1 Cycles On Create')

    last_flight          = fields.Date(string='Last Flight')
        
    def _get_default_hours(self):
        return self.env['ams.config'].search([('name','=','warning_hours')],limit=1).int_value

    def _get_default_cycles(self):
        return self.env['ams.config'].search([('name','=','warning_cycles')],limit=1).int_value

    def _get_default_rins(self):
        return self.env['ams.config'].search([('name','=','warning_rins')],limit=1).int_value

    def _get_default_calendars(self):
        return self.env['ams.config'].search([('name','=','warning_calendars')],limit=1).int_value
    
    @api.model
    def _needaction_domain_get(self):
        return [('states', '=', 'create_by')]

    @api.model
    def create(self, value):

        acraft = self.env['aircraft.acquisition'].search([('id','=',value['fleet_id'])])
        partner = self.env.user.partner_id.id
        value['states'] = 'create_by'
        value['create_by'] = partner
        value['create_at'] = datetime.now().strftime("%Y-%m-%d")
        value['last_flight'] = acraft.last_flight

        value['fleet_hours'] = acraft.total_hours
        value['fleet_cycles'] = acraft.total_landings
        value['fleet_rins'] = acraft.total_rins
        value['engine1_hours'] = acraft.engine_type_id.engine_tsn
        value['engine1_cycles'] = acraft.engine_type_id.engine_csn
        value['engine2_hours'] = acraft.engine2_type_id.engine_tsn
        value['engine2_cycles'] = acraft.engine2_type_id.engine_csn
        value['engine3_hours'] = acraft.engine3_type_id.engine_tsn
        value['engine3_cycles'] = acraft.engine3_type_id.engine_csn
        value['engine4_hours'] = acraft.engine4_type_id.engine_tsn
        value['engine4_cycles'] = acraft.engine4_type_id.engine_csn
        value['auxiliary1_hours'] = acraft.auxiliary_type_id.auxiliary_tsn
        value['auxiliary1_cycles'] = acraft.auxiliary_type_id.auxiliary_csn

        # create Sequence 
        default_seq     = self.env['ir.sequence'].next_by_code('mdr_seq')
        if default_seq: 
            fleet_type = None
            if acraft.category == "fixedwing":
                fleet_type = "FW"
            else:
                fleet_type = "RW"

            seq     = str(str(default_seq) + "/" + str(acraft.name) +"/"+ fleet_type +"/"+ str(datetime.strftime(datetime.today(), "%y")))

            value['mdr_seq'] = seq

        rec = super(MaintenanceDueReport, self).create(value)
        return rec

    @api.multi
    def create_by_(self):
        partner = self.env.user.partner_id.id
        self.create_by = partner
        self.states = 'approved_by'
        self.env['maintenance.due.report'].search(['&',('fleet_id','=',self.fleet_id.id),('id','!=',self.id)]).write({'states':'expired'})

    # @api.multi
    # def checked_by_(self):
    #     partner = self.env.user.partner_id.id
    #     self.checked_by = partner
    #     self.states = 'approved_by'

    @api.multi
    def approved_by_(self):
        partner = self.env.user.partner_id.id
        self.approved_by = partner
        # self.date_approved = datetime.now().strftime('%Y-%m-%d')
        self.states = 'done'

    @api.multi
    def qc_by_(self):
        partner = self.env.user.partner_id.id
        self.qc_by = partner
        # self.date_approved = datetime.now().strftime('%Y-%m-%d')
        self.states = 'done'
        

    @api.onchange('type')
    def _onchange_type(self):
        self.engine_id = []
        self.fleet_id = []
        self.auxiliary_id = []
        self.propeller_id = []

        # set Warning type
        if not self.id:
            warning_hours       = self.env['ams.setting'].search([], limit=1, order='create_date DESC').warning_hours
            warning_cycles      = self.env['ams.setting'].search([], limit=1, order='create_date DESC').warning_cycles
            warning_rins        = self.env['ams.setting'].search([], limit=1, order='create_date DESC').warning_rins
            warning_calendars   = self.env['ams.setting'].search([], limit=1, order='create_date DESC').warning_calendars
            
            self.warning_hours  = warning_hours
            self.warning_cycles = warning_cycles
            self.warning_rins   = warning_rins

            timeNow = datetime.now()

            if (warning_calendars != 0):
                self.warning_calendars = timeNow + relativedelta(days=+warning_calendars)
            else:
                self.warning_calendars = timeNow

    @api.multi
    def print_main_due_pdf(self):
        return self.env['report'].get_action(self, 'ams_document.report_maintenance_due')

    @api.multi
    def print_main_due_wizard(self):
        self.hour_limit_id.unlink()
        self.cycle_limit_id.unlink()
        self.rin_limit_id.unlink()
        self.calendar_limit_id.unlink()
        self.certificate_limit_id.unlink()
        if not self.hour_limit_id:
            self._get_hour()
        if not self.cycle_limit_id:
            self._get_cycle()
        if not self.rin_limit_id:
            self._get_rin()
        if not self.calendar_limit_id:
            self._get_calendar()
        if not self.certificate_limit_id:
            self._get_certificate()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'maintenance.due.report.print',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'hour_limit' : self.warning_hours,
                'cycle_limit' : self.warning_cycles,
                'rin_limit' : self.warning_rins,
                'calendar_limit': self.warning_calendars,
                'fleet_id': self.fleet_id.id,
                'id': self.id,
                'create_by': self.create_by.id,
                'approved_by': self.approved_by.id,
            }
        }

    @api.one
    def _get_setstime(self):
        settime = self.env['ams.config'].search([])
        self.set_time_id = settime

    @api.model
    def _get_hour(self):
        self.env["hour.limit.mdr"].search([('hour_id','=',self.id)]).unlink()
        if self.id:
            settime = self.env['ams.config'].search([])
            
            mdr = []
            if self.type == 'fleet':
                if self.fleet_id:
                    data_hour = self.env['aircraft.acquisition'].search([('name','=',self.fleet_id.name)])
                else:
                    data_hour = self.env['aircraft.acquisition'].search([])
            elif self.type == 'engine':
                if self.fleet_id:
                    data_hour = self.env['engine.type'].search([('name','=',self.engine_id.name)])
                else:
                    data_hour = self.env['engine.type'].search([])
            elif self.type == 'auxiliary':
                if self.fleet_id:
                    data_hour = self.env['auxiliary.type'].search([('name','=',self.auxiliary_id.name)])
                else:
                    data_hour = self.env['auxiliary.type'].search([])
            elif self.type == 'propeller':
                if self.fleet_id:
                    data_hour = self.env['propeller.type'].search([('name','=',self.propeller_id.name)])
                else:
                    data_hour = self.env['propeller.type'].search([])

            else:
                fleet = self.env['aircraft.acquisition'].search([])
                engine = self.env['engine.type'].search([])
                auxiliary = self.env['auxiliary.type'].search([])
                propeller = self.env['propeller.type'].search([])
                all = []
                for al in fleet:
                    all.append(al)
                for al in engine:
                    all.append(al)
                for al in auxiliary:
                    all.append(al)
                for al in propeller:
                    all.append(al)
                data_hour = all

            #warning_hours = self.env['ams.setting'].search([],limit=1,order='create_date DESC').warning_hours
                    
            
            warning_hours = self.warning_hours

            

            for reports in data_hour:
                for component in reports.component_ids:
                    for service in component.serfice_life:
                        if (service.remaining <= warning_hours) and (service.unit == 'hours') and (service.action_type != 'oncondition') and (service.action_type != 'conditionmonitoring'):
                            components = {
                                    'data_source' : 'ac',
                                    'data_type' : 'component',
                                    'hour_id':self.id,
                                    'fleet_id': reports.name, 
                                    'name': component.product_id.name, 
                                    'part': component.part_number, 
                                    'serial': component.serial_number.name, 
                                    'ata' : component.ata_code.name, 
                                    'item' : component.item, 
                                    'service' : self.getSliveText(service.id), 
                                    'service_id' :service.id, 
                                    'done' : str(component.ac_timeinstallation), 
                                    'time' : float(service.remaining), 
                                    'remaining' : float(service.remaining), 
                                    'project': (datetime.strptime(self.countDate(self.fleet_id, service.id), '%Y-%m-%d').strftime('%d/%m/%Y') if self.countDate(self.fleet_id, service.id) != False else ''),
                                    'projected_date': self.countDate(self.fleet_id, service.id),
                                    'komen' : service.comments,
                                    }

                            mdr.append(components)
                            # self.hour_limit_id |= self.env['hour.limit.mdr'].create(components)
                            #self.env['hour.limit.mdr.filter'].create(components)
                            
                    for subcomp in component.sub_part_ids:
                        for subservice in subcomp.serfice_life:
                            if (subservice.remaining <= warning_hours) and (subservice.unit == 'hours') and (subservice.action_type != 'oncondition') and (subservice.action_type != 'conditionmonitoring'):
                                subcomponents = {
                                    'data_source' : 'ac',
                                    'data_type' : 'component',
                                    'hour_id':self.id,
                                    'fleet_id': reports.name, 
                                    'name': subcomp.product_id.name, 
                                    'part': subcomp.part_number, 
                                    'serial': subcomp.serial_number.name, 
                                    'ata' : subcomp.ata_code.name, 
                                    'item' : subcomp.item, 
                                    'service' : self.getSliveText(subservice.id), 
                                    'service_id' :subservice.id, 
                                    'done' : str(subcomp.ac_timeinstallation), 
                                    'time' : float(subservice.remaining),
                                    'remaining' : float(subservice.remaining),
                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                    'komen' : subservice.comments,
                                    }
                                # print subcomponents
                                mdr.append(subcomponents)
                                # self.hour_limit_id |= self.env['hour.limit.mdr'].create(subcomponents)
                                # self.env['hour.limit.mdr.filter'].create(subcomponents)

                # AC INSPECTION BY HOURS
                for inspection in reports.inspection_ids:
                    for service in inspection.serfice_life:
                        if (service.remaining <= warning_hours) and (service.unit == 'hours') and (service.action_type != 'oncondition') and (service.action_type != 'conditionmonitoring'):
                            inspections = {
                                    'data_source' : 'ac',
                                    'data_type' : 'inspection',
                                    'hour_id':self.id,
                                    'fleet_id': reports.name, 
                                    'name': inspection.inspection_type, 
                                    'part': '',
                                    'serial': '',
                                    'ata' : inspection.ata_code.name, 
                                    'item' : inspection.item, 
                                    'service' : self.getSliveText(service.id), 
                                    'service_id' :service.id, 
                                    'done' : str(reports.total_hours - service.current), 
                                    'time' : float(service.remaining), 
                                    'remaining' : float(service.remaining), 
                                    'project': (datetime.strptime(self.countDate(self.fleet_id, service.id), '%Y-%m-%d').strftime('%d/%m/%Y') if self.countDate(self.fleet_id, service.id) != False else ''),
                                    'projected_date': self.countDate(self.fleet_id, service.id),
                                    'komen' : service.comments,
                                    }
                            mdr.append(inspections)

                if True:
                    for engnum in xrange(1,4):
                        if(engnum == 1):
                            engine = reports.engine_type_id
                        elif(engnum == 2):
                            engine = reports.engine2_type_id
                        elif(engnum == 3):
                            engine = reports.engine3_type_id
                        elif(engnum == 4):
                            engine = reports.engine4_type_id
                        
                        if(engine):
                            # ENGINE INSPECTION BY HOURS
                            for inspection in engine.inspection_ids:
                                for service in inspection.serfice_life:
                                    if (service.remaining <= warning_hours) and (service.unit == 'hours') and (service.action_type != 'oncondition') and (service.action_type != 'conditionmonitoring'):
                                        inspections = {
                                                'data_source' : 'en'+str(engnum),
                                                'data_type' : 'inspection',
                                                'hour_id':self.id,
                                                'fleet_id': engine.name, 
                                                'name': inspection.inspection_type, 
                                                'part': '',
                                                'serial': '',
                                                'ata' : inspection.ata_code.name, 
                                                'item' : inspection.item, 
                                                'service' : self.getSliveText(service.id), 
                                                'service_id' :service.id, 
                                                'done' : str(reports.total_hours - service.current), 
                                                'time' : float(service.remaining), 
                                                'remaining' : float(service.remaining), 
                                                'project': (datetime.strptime(self.countDate(self.fleet_id, service.id), '%Y-%m-%d').strftime('%d/%m/%Y') if self.countDate(self.fleet_id, service.id) != False else ''),
                                                'projected_date': self.countDate(self.fleet_id, service.id),
                                                'komen' : service.comments,
                                                }
                                        mdr.append(inspections)
                    for propnum in xrange(1,4):
                        if(propnum == 1):
                            propeller = reports.propeller_type_id
                        elif(propnum == 2):
                            propeller = reports.propeller2_type_id
                        elif(propnum == 3):
                            propeller = reports.propeller3_type_id
                        elif(propnum == 4):
                            propeller = reports.propeller4_type_id
                        
                        if(propeller):
                            # PROPELLER INSPECTION BY HOURS
                            for inspection in propeller.inspection_ids:
                                for service in inspection.serfice_life:
                                    if (service.remaining <= warning_hours) and (service.unit == 'hours') and (service.action_type != 'oncondition') and (service.action_type != 'conditionmonitoring'):
                                        inspections = {
                                                'data_source' : 'en'+str(propnum),
                                                'data_type' : 'inspection',
                                                'hour_id':self.id,
                                                'fleet_id': propeller.name, 
                                                'name': inspection.inspection_type, 
                                                'part': '',
                                                'serial': '',
                                                'ata' : inspection.ata_code.name, 
                                                'item' : inspection.item, 
                                                'service' : self.getSliveText(service.id), 
                                                'service_id' :service.id, 
                                                'done' : str(reports.total_hours - service.current), 
                                                'time' : float(service.remaining), 
                                                'remaining' : float(service.remaining), 
                                                'project': (datetime.strptime(self.countDate(self.fleet_id, service.id), '%Y-%m-%d').strftime('%d/%m/%Y') if self.countDate(self.fleet_id, service.id) != False else ''),
                                                'projected_date': self.countDate(self.fleet_id, service.id),
                                                'komen' : service.comments,
                                                }
                                        mdr.append(inspections)

                        if(reports.auxiliary_type_id):
                            # AUXILIARY INSPECTION BY HOURS
                            for inspection in reports.auxiliary_type_id.inspection_ids:
                                for service in inspection.serfice_life:
                                    if (service.remaining <= warning_hours) and (service.unit == 'hours') and (service.action_type != 'oncondition') and (service.action_type != 'conditionmonitoring'):
                                        inspections = {
                                                'data_source' : 'aux',
                                                'data_type' : 'inspection',
                                                'hour_id':self.id,
                                                'fleet_id': reports.auxiliary_type_id.name, 
                                                'name': inspection.inspection_type, 
                                                'part': '',
                                                'serial': '',
                                                'ata' : inspection.ata_code.name, 
                                                'item' : inspection.item, 
                                                'service' : self.getSliveText(service.id), 
                                                'service_id' :service.id, 
                                                'done' : str(reports.total_hours - service.current), 
                                                'time' : float(service.remaining), 
                                                'remaining' : float(service.remaining), 
                                                'project': (datetime.strptime(self.countDate(self.fleet_id, service.id), '%Y-%m-%d').strftime('%d/%m/%Y') if self.countDate(self.fleet_id, service.id) != False else ''),
                                                'projected_date': self.countDate(self.fleet_id, service.id),
                                                'komen' : service.comments,
                                                }
                                        mdr.append(inspections)

                    # if self.include_attach:
                    if reports.engine_type_id:
                        for engine in reports.engine_type_id:
                            for comp in engine.component_ids:
                                for serv in comp.serfice_life:
                                    if (serv.remaining <= warning_hours) and (serv.unit == 'hours') and (serv.action_type != 'oncondition') and (serv.action_type != 'conditionmonitoring'):
                                        comps = {
                                                'data_source' : 'en1',
                                                'data_type' : 'component',
                                                'hour_id':self.id,
                                                'fleet_id': engine.name, 
                                                'name': comp.product_id.name, 
                                                'part': comp.part_number, 
                                                'serial': comp.serial_number.name, 
                                                'ata' : comp.ata_code.name, 
                                                'item' : comp.item, 
                                                'service' : self.getSliveText(serv.id), 
                                                'service_id' :serv.id, 
                                                'done' : str(comp.ac_timeinstallation), 
                                                'time' : float(serv.remaining), 
                                                'remaining' : float(serv.remaining), 
                                                'project': (datetime.strptime(self.countDate(self.fleet_id, serv.id), '%Y-%m-%d').strftime('%d/%m/%Y') if self.countDate(self.fleet_id, serv.id) != False else ''),
                                                'projected_date': self.countDate(self.fleet_id, serv.id),
                                                'komen' : serv.comments,
                                                }
                                        mdr.append(comps)
                                for subcomp in comp.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_hours) and (subservice.unit == 'hours') and (subservice.action_type != 'oncondition') and (subservice.action_type != 'conditionmonitoring'):
                                            subcomps = {
                                                    'data_source' : 'en1',
                                                    'data_type' : 'component',
                                                    'hour_id':self.id,
                                                    'fleet_id': engine.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_timeinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)

                    if reports.engine2_type_id:
                        for engine2 in reports.engine2_type_id:
                            for comp2 in engine2.component_ids:
                                for serv2 in comp2.serfice_life:
                                    if (serv2.remaining <= warning_hours) and (serv2.unit == 'hours') and (serv2.action_type != 'oncondition') and (serv2.action_type != 'conditionmonitoring'):
                                        comps2 = {
                                                'data_source' : 'en2',
                                                'data_type' : 'component',
                                                'hour_id':self.id,
                                                'fleet_id': engine2.name, 
                                                'name': comp2.product_id.name, 
                                                'part': comp2.part_number, 
                                                'serial': comp2.serial_number.name, 
                                                'ata' : comp2.ata_code.name, 
                                                'item' : comp2.item, 
                                                'service' : self.getSliveText(serv2.id), 
                                                'service_id' :serv2.id, 
                                                'done' : str(comp2.ac_timeinstallation), 
                                                'time' : float(serv2.remaining), 
                                                'remaining' : float(serv2.remaining), 
                                                'project': (datetime.strptime(self.countDate(self.fleet_id, serv2.id), '%Y-%m-%d').strftime('%d/%m/%Y') if self.countDate(self.fleet_id, serv2.id) != False else ''),
                                                'projected_date': self.countDate(self.fleet_id, serv2.id),
                                                'komen' : serv2.comments,
                                                }
                                        mdr.append(comps2)
                                for subcomp in comp2.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_hours) and (subservice.unit == 'hours') and (subservice.action_type != 'oncondition') and (subservice.action_type != 'conditionmonitoring'):
                                            subcomps = {
                                                    'data_source' : 'en2',
                                                    'data_type' : 'component',
                                                    'hour_id':self.id,
                                                    'fleet_id': engine2.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_timeinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)
                                    
                    if reports.engine3_type_id:
                        for engine3 in reports.engine3_type_id:
                            for comp3 in engine3.component_ids:
                                for serv3 in comp3.serfice_life:
                                    if (serv3.remaining <= warning_hours) and (serv3.unit == 'hours') and (serv3.action_type != 'oncondition') and (serv3.action_type != 'conditionmonitoring'):
                                        comps3 = {
                                                'data_source' : 'en3',
                                                'data_type' : 'component',
                                                'hour_id':self.id,
                                                'fleet_id': engine3.name, 
                                                'name': comp3.product_id.name, 
                                                'part': comp3.part_number, 
                                                'serial': comp3.serial_number.name, 
                                                'ata' : comp3.ata_code.name, 
                                                'item' : comp3.item, 
                                                'service' : self.getSliveText(serv3.id), 
                                                'service_id' :serv3.id, 
                                                'done' : str(comp3.ac_timeinstallation), 
                                                'time' : float(serv3.remaining), 
                                                'remaining' : float(serv3.remaining), 
                                                'project': (datetime.strptime(self.countDate(self.fleet_id, serv3.id), '%Y-%m-%d').strftime('%d/%m/%Y') if self.countDate(self.fleet_id, serv3.id) != False else '' ),
                                                'projected_date': self.countDate(self.fleet_id, serv3.id),
                                                'komen' : serv3.comments,
                                                }
                                        mdr.append(comps3)
                                for subcomp in comp3.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_hours) and (subservice.unit == 'hours') and (subservice.action_type != 'oncondition') and (subservice.action_type != 'conditionmonitoring'):
                                            subcomps = {
                                                    'data_source' : 'en3',
                                                    'data_type' : 'component',
                                                    'hour_id':self.id,
                                                    'fleet_id': engine3.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_timeinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)

                    if reports.engine4_type_id:
                        for engine4 in reports.engine4_type_id:
                            for comp4 in engine4.component_ids:
                                for serv4 in comp4.serfice_life:
                                    if (serv4.remaining <= warning_hours) and (serv4.unit == 'hours') and (serv4.action_type != 'oncondition') and (serv4.action_type != 'conditionmonitoring'):
                                        comps4 = {
                                                'data_source' : 'en4',
                                                'data_type' : 'component',
                                                'hour_id':self.id,
                                                'fleet_id': engine4.name, 
                                                'name': comp4.product_id.name, 
                                                'part': comp4.part_number, 
                                                'serial': comp4.serial_number.name, 
                                                'ata' : comp4.ata_code.name, 
                                                'item' : comp4.item, 
                                                'service' : self.getSliveText(serv4.id), 
                                                'service_id' :serv4.id, 
                                                'done' : str(comp4.ac_timeinstallation), 
                                                'time' : float(serv4.remaining), 
                                                'remaining' : float(serv4.remaining), 
                                                'project': (datetime.strptime(self.countDate(self.fleet_id, serv4.id), '%Y-%m-%d').strftime('%d/%m/%Y') if self.countDate(self.fleet_id, serv4.id) != False else ''),
                                                'projected_date': self.countDate(self.fleet_id, serv4.id),
                                                'komen' : serv4.comments,
                                                }
                                        mdr.append(comps4)
                                for subcomp in comp4.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_hours) and (subservice.unit == 'hours') and (subservice.action_type != 'oncondition') and (subservice.action_type != 'conditionmonitoring'):
                                            subcomps = {
                                                    'data_source' : 'en4',
                                                    'data_type' : 'component',
                                                    'hour_id':self.id,
                                                    'fleet_id': engine4.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_timeinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)
                    if reports.propeller_type_id:
                        for propeller in reports.propeller_type_id:
                            for comp in propeller.component_ids:
                                for serv in comp.serfice_life:
                                    if (serv.remaining <= warning_hours) and (serv.unit == 'hours') and (serv.action_type != 'oncondition') and (serv.action_type != 'conditionmonitoring'):
                                        comps = {
                                                'data_source' : 'pr1',
                                                'data_type' : 'component',
                                                'hour_id':self.id,
                                                'fleet_id': propeller.name, 
                                                'name': comp.product_id.name, 
                                                'part': comp.part_number, 
                                                'serial': comp.serial_number.name, 
                                                'ata' : comp.ata_code.name, 
                                                'item' : comp.item, 
                                                'service' : self.getSliveText(serv.id), 
                                                'service_id' :serv.id, 
                                                'done' : str(comp.ac_timeinstallation), 
                                                'time' : float(serv.remaining), 
                                                'remaining' : float(serv.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv.id),
                                                'komen' : serv.comments,
                                                }
                                        mdr.append(comps)
                                for subcomp in comp.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_hours) and (subservice.unit == 'hours') and (subservice.action_type != 'oncondition') and (subservice.action_type != 'conditionmonitoring'):
                                            subcomps = {
                                                    'data_source' : 'pr1',
                                                    'data_type' : 'component',
                                                    'hour_id':self.id,
                                                    'fleet_id': propeller.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_timeinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)

                    if reports.propeller2_type_id:
                        for propeller2 in reports.propeller2_type_id:
                            for comp2 in propeller2.component_ids:
                                for serv2 in comp2.serfice_life:
                                    if (serv2.remaining <= warning_hours) and (serv2.unit == 'hours') and (serv2.action_type != 'oncondition') and (serv2.action_type != 'conditionmonitoring'):
                                        comps2 = {
                                                'data_source' : 'pr2',
                                                'data_type' : 'component',
                                                'hour_id':self.id,
                                                'fleet_id': propeller2.name, 
                                                'name': comp2.product_id.name, 
                                                'part': comp2.part_number, 
                                                'serial': comp2.serial_number.name, 
                                                'ata' : comp2.ata_code.name, 
                                                'item' : comp2.item, 
                                                'service' : self.getSliveText(serv2.id), 
                                                'service_id' :serv2.id, 
                                                'done' : str(comp2.ac_timeinstallation), 
                                                'time' : float(serv2.remaining), 
                                                'remaining' : float(serv2.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv2.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv2.id),
                                                'komen' : serv2.comments,
                                                }
                                        mdr.append(comps2)
                                for subcomp in comp2.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_hours) and (subservice.unit == 'hours') and (subservice.action_type != 'oncondition') and (subservice.action_type != 'conditionmonitoring'):
                                            subcomps = {
                                                    'data_source' : 'pr2',
                                                    'data_type' : 'component',
                                                    'hour_id':self.id,
                                                    'fleet_id': propeller2.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_timeinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)
                                    
                    if reports.propeller3_type_id:
                        for propeller3 in reports.propeller3_type_id:
                            for comp3 in propeller3.component_ids:
                                for serv3 in comp3.serfice_life:
                                    if (serv3.remaining <= warning_hours) and (serv3.unit == 'hours') and (serv3.action_type != 'oncondition') and (serv3.action_type != 'conditionmonitoring'):
                                        comps3 = {
                                                'data_source' : 'pr3',
                                                'data_type' : 'component',
                                                'hour_id':self.id,
                                                'fleet_id': propeller3.name, 
                                                'name': comp3.product_id.name, 
                                                'part': comp3.part_number, 
                                                'serial': comp3.serial_number.name, 
                                                'ata' : comp3.ata_code.name, 
                                                'item' : comp3.item, 
                                                'service' : self.getSliveText(serv3.id), 
                                                'service_id' :serv3.id, 
                                                'done' : str(comp3.ac_timeinstallation), 
                                                'time' : float(serv3.remaining), 
                                                'remaining' : float(serv3.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv3.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv3.id),
                                                'komen' : serv3.comments,
                                                }
                                        mdr.append(comps3)
                                for subcomp in comp3.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_hours) and (subservice.unit == 'hours') and (subservice.action_type != 'oncondition') and (subservice.action_type != 'conditionmonitoring'):
                                            subcomps = {
                                                    'data_source' : 'pr3',
                                                    'data_type' : 'component',
                                                    'hour_id':self.id,
                                                    'fleet_id': propeller3.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_timeinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)

                    if reports.propeller4_type_id:
                        for propeller4 in reports.propeller4_type_id:
                            for comp4 in propeller4.component_ids:
                                for serv4 in comp4.serfice_life:
                                    if (serv4.remaining <= warning_hours) and (serv4.unit == 'hours') and (serv4.action_type != 'oncondition') and (serv4.action_type != 'conditionmonitoring'):
                                        comps4 = {
                                                'data_source' : 'pr4',
                                                'data_type' : 'component',
                                                'hour_id':self.id,
                                                'fleet_id': propeller4.name, 
                                                'name': comp4.product_id.name, 
                                                'part': comp4.part_number, 
                                                'serial': comp4.serial_number.name, 
                                                'ata' : comp4.ata_code.name, 
                                                'item' : comp4.item, 
                                                'service' : self.getSliveText(serv4.id), 
                                                'service_id' :serv4.id, 
                                                'done' : str(comp4.ac_timeinstallation), 
                                                'time' : float(serv4.remaining), 
                                                'remaining' : float(serv4.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv4.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv4.id),
                                                'komen' : serv4.comments,
                                                }
                                        mdr.append(comps4)
                                for subcomp in comp4.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_hours) and (subservice.unit == 'hours') and (subservice.action_type != 'oncondition') and (subservice.action_type != 'conditionmonitoring'):
                                            subcomps = {
                                                    'data_source' : 'pr4',
                                                    'data_type' : 'component',
                                                    'hour_id':self.id,
                                                    'fleet_id': propeller4.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_timeinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)
                    if reports.auxiliary_type_id:
                        for auxiliary in reports.auxiliary_type_id:
                            for comp in auxiliary.component_ids:
                                for serv in comp.serfice_life:
                                    if (serv.remaining <= warning_hours) and (serv.unit == 'hours') and (serv.action_type != 'oncondition') and (serv.action_type != 'conditionmonitoring'):
                                        comps4 = {
                                                'data_source' : 'en4',
                                                'data_type' : 'component',
                                                'hour_id':self.id,
                                                'fleet_id': auxiliary.name, 
                                                'name': comp.product_id.name, 
                                                'part': comp.part_number, 
                                                'serial': comp.serial_number.name, 
                                                'ata' : comp.ata_code.name, 
                                                'item' : comp.item, 
                                                'service' : self.getSliveText(serv.id), 
                                                'service_id' :serv.id, 
                                                'done' : str(comp.ac_timeinstallation), 
                                                'time' : float(serv.remaining), 
                                                'remaining' : float(serv.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv.id),
                                                'komen' : serv.comments,
                                                }
                                        mdr.append(comps4)
                                for subcomp in comp.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_hours) and (subservice.unit == 'hours') and (subservice.action_type != 'oncondition') and (subservice.action_type != 'conditionmonitoring'):
                                            subcomps = {
                                                    'data_source' : 'en4',
                                                    'data_type' : 'component',
                                                    'hour_id':self.id,
                                                    'fleet_id': auxiliary.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_timeinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)


            self.hour_limit_id = mdr
       

    @api.model
    def _get_cycle(self):
        if self.env["cycle.limit.mdr"].search([('cycle_id','=',self.id)]):
            self.env["cycle.limit.mdr"].search([('cycle_id','=',self.id)]).unlink()
        if self.id:
            settime = self.env['ams.config'].search([])
            mdr = []
            if self.type == 'fleet':
                if self.fleet_id:
                    data_cycle = self.env['aircraft.acquisition'].search([('name','=',self.fleet_id.name)])
                else:
                    data_cycle = self.env['aircraft.acquisition'].search([])
            elif self.type == 'engine':
                if self.fleet_id:
                    data_cycle = self.env['engine.type'].search([('name','=',self.engine_id.name)])
                else:
                    data_cycle = self.env['engine.type'].search([])
            elif self.type == 'auxiliary':
                if self.fleet_id:
                    data_cycle = self.env['auxiliary.type'].search([('name','=',self.auxiliary_id.name)])
                else:
                    data_cycle = self.env['auxiliary.type'].search([])
            elif self.type == 'propeller':
                if self.fleet_id:
                    data_cycle = self.env['propeller.type'].search([('name','=',self.propeller_id.name)])
                else:
                    data_cycle = self.env['propeller.type'].search([])
            else:
                fleet = self.env['aircraft.acquisition'].search([])
                engine = self.env['engine.type'].search([])
                auxiliary = self.env['auxiliary.type'].search([])
                propeller = self.env['propeller.type'].search([])
                all = []
                for al in fleet:
                    all.append(al)
                for al in engine:
                    all.append(al)
                for al in auxiliary:
                    all.append(al)
                for al in propeller:
                    all.append(al)
                data_cycle = all


            #warning_cycles = self.env['ams.setting'].search([],limit=1,order='create_date DESC').warning_cycles
            warning_cycles = self.warning_cycles
            for reports in data_cycle:
                for component in reports.component_ids:
                    for service in component.serfice_life:
                        if (service.remaining <= warning_cycles) and (service.unit == 'cycles'):
                            components = {
                                    'data_source' : 'ac',
                                    'data_type' : 'component',
                                    'cycle_id':self.id,
                                    'fleet_id': reports.name, 
                                    'name': component.product_id.name, 
                                    'part': component.part_number, 
                                    'serial': component.serial_number.name, 
                                    'ata' : component.ata_code.name, 
                                    'item' : component.item, 
                                    'service' : self.getSliveText(service.id), 
                                    'service_id' :service.id, 
                                    'done' : str(component.cso), 
                                    'time' : float(service.remaining),
                                    'remaining' : float(service.remaining),
                                    'project': (datetime.strptime(self.countDate(self.fleet_id, service.id), '%Y-%m-%d').strftime('%d/%m/%Y') if self.countDate(self.fleet_id, service.id) != False else ''),
                                    'projected_date': self.countDate(self.fleet_id, service.id),
                                    'komen' : service.comments,
                                    }
                            mdr.append(components)
                            # self.cycle_limit_id |= self.env['cycle.limit.mdr'].create(components)

                    for subcomp in component.sub_part_ids:
                        for subservice in subcomp.serfice_life:
                            if (subservice.remaining <= warning_cycles) and (subservice.unit == 'cycles'):
                                subcomponents = {
                                    'data_source' : 'ac',
                                    'data_type' : 'component',
                                    'cycle_id':self.id,
                                    'fleet_id': reports.name, 
                                    'name': subcomp.product_id.name, 
                                    'part': subcomp.part_number, 
                                    'serial': subcomp.serial_number.name, 
                                    'ata' : subcomp.ata_code.name, 
                                    'item' : subcomp.item, 
                                    'service' : self.getSliveText(subservice.id), 
                                    'service_id' :subservice.id, 
                                    'done' : str(subcomp.ac_cyclesinstallation), 
                                    'time' : float(subservice.remaining),
                                    'remaining' : float(subservice.remaining),
                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                    }
                                mdr.append(subcomponents)
                                # self.cycle_limit_id |= self.env['cycle.limit.mdr'].create(subcomponents)

                # AC INSPECTION BY cycles
                for inspection in reports.inspection_ids:
                    for service in inspection.serfice_life:
                        if (service.remaining <= warning_cycles) and (service.unit == 'cycles') and (service.action_type != 'oncondition') and (service.action_type != 'conditionmonitoring'):
                            inspections = {
                                    'data_source' : 'ac',
                                    'data_type' : 'inspection',
                                    'hour_id':self.id,
                                    'fleet_id': reports.name, 
                                    'name': inspection.inspection_type, 
                                    'part': '',
                                    'serial': '',
                                    'ata' : inspection.ata_code.name, 
                                    'item' : inspection.item, 
                                    'service' : self.getSliveText(service.id), 
                                    'service_id' :service.id, 
                                    'done' : str(reports.total_landings - service.current), 
                                    'time' : float(service.remaining), 
                                    'remaining' : float(service.remaining), 
                                    'project': (datetime.strptime(self.countDate(self.fleet_id, service.id), '%Y-%m-%d').strftime('%d/%m/%Y') if self.countDate(self.fleet_id, service.id) != False else ''),
                                    'projected_date': self.countDate(self.fleet_id, service.id),
                                    'komen' : service.comments,
                                    }
                            mdr.append(inspections)

                if True:
                    for engnum in xrange(1,4):
                        if(engnum == 1):
                            engine = reports.engine_type_id
                        elif(engnum == 2):
                            engine = reports.engine2_type_id
                        elif(engnum == 3):
                            engine = reports.engine3_type_id
                        elif(engnum == 4):
                            engine = reports.engine4_type_id
                        
                        if(engine):
                            # ENGINE INSPECTION BY cycles
                            for inspection in engine.inspection_ids:
                                for service in inspection.serfice_life:
                                    if (service.remaining <= warning_cycles) and (service.unit == 'cycles') and (service.action_type != 'oncondition') and (service.action_type != 'conditionmonitoring'):
                                        inspections = {
                                                'data_source' : 'en'+str(engnum),
                                                'data_type' : 'inspection',
                                                'hour_id':self.id,
                                                'fleet_id': engine.name, 
                                                'name': inspection.inspection_type, 
                                                'part': '',
                                                'serial': '',
                                                'ata' : inspection.ata_code.name, 
                                                'item' : inspection.item, 
                                                'service' : self.getSliveText(service.id), 
                                                'service_id' :service.id, 
                                                'done' : str(reports.total_landings - service.current), 
                                                'time' : float(service.remaining), 
                                                'remaining' : float(service.remaining), 
                                                'project': (datetime.strptime(self.countDate(self.fleet_id, service.id), '%Y-%m-%d').strftime('%d/%m/%Y') if self.countDate(self.fleet_id, service.id) != False else ''),
                                                'projected_date': self.countDate(self.fleet_id, service.id),
                                                'komen' : service.comments,
                                                }
                                        mdr.append(inspections)
                    for propnum in xrange(1,4):
                        if(propnum == 1):
                            propeller = reports.propeller_type_id
                        elif(propnum == 2):
                            propeller = reports.propeller2_type_id
                        elif(propnum == 3):
                            propeller = reports.propeller3_type_id
                        elif(propnum == 4):
                            propeller = reports.propeller4_type_id
                        
                        if(propeller):
                            # PROPELLER INSPECTION BY cycles
                            for inspection in propeller.inspection_ids:
                                for service in inspection.serfice_life:
                                    if (service.remaining <= warning_cycles) and (service.unit == 'cycles') and (service.action_type != 'oncondition') and (service.action_type != 'conditionmonitoring'):
                                        inspections = {
                                                'data_source' : 'en'+str(propnum),
                                                'data_type' : 'inspection',
                                                'hour_id':self.id,
                                                'fleet_id': propeller.name, 
                                                'name': inspection.inspection_type, 
                                                'part': '',
                                                'serial': '',
                                                'ata' : inspection.ata_code.name, 
                                                'item' : inspection.item, 
                                                'service' : self.getSliveText(service.id), 
                                                'service_id' :service.id, 
                                                'done' : str(reports.total_landings - service.current), 
                                                'time' : float(service.remaining), 
                                                'remaining' : float(service.remaining), 
                                                'project': (datetime.strptime(self.countDate(self.fleet_id, service.id), '%Y-%m-%d').strftime('%d/%m/%Y') if self.countDate(self.fleet_id, service.id) != False else ''),
                                                'projected_date': self.countDate(self.fleet_id, service.id),
                                                'komen' : service.comments,
                                                }
                                        mdr.append(inspections)

                        if(reports.auxiliary_type_id):
                            # AUXILIARY INSPECTION BY cycles
                            for inspection in reports.auxiliary_type_id.inspection_ids:
                                for service in inspection.serfice_life:
                                    if (service.remaining <= warning_cycles) and (service.unit == 'cycles') and (service.action_type != 'oncondition') and (service.action_type != 'conditionmonitoring'):
                                        inspections = {
                                                'data_source' : 'aux',
                                                'data_type' : 'inspection',
                                                'hour_id':self.id,
                                                'fleet_id': reports.auxiliary_type_id.name, 
                                                'name': inspection.inspection_type, 
                                                'part': '',
                                                'serial': '',
                                                'ata' : inspection.ata_code.name, 
                                                'item' : inspection.item, 
                                                'service' : self.getSliveText(service.id), 
                                                'service_id' :service.id, 
                                                'done' : str(reports.total_landings - service.current), 
                                                'time' : float(service.remaining), 
                                                'remaining' : float(service.remaining), 
                                                'project': (datetime.strptime(self.countDate(self.fleet_id, service.id), '%Y-%m-%d').strftime('%d/%m/%Y') if self.countDate(self.fleet_id, service.id) != False else ''),
                                                'projected_date': self.countDate(self.fleet_id, service.id),
                                                'komen' : service.comments,
                                                }
                                        mdr.append(inspections)


                if True:
                    # if self.include_attach:
                    if reports.engine_type_id:
                        for engine in reports.engine_type_id:
                            for comp in engine.component_ids:
                                for serv in comp.serfice_life:
                                    if (serv.remaining <= warning_cycles) and (serv.unit == 'cycles'):
                                        comps = {
                                                'data_source' : 'en1',
                                                'data_type' : 'component',
                                                'cycle_id':self.id,
                                                'fleet_id': engine.name, 
                                                'name': comp.product_id.name, 
                                                'part': comp.part_number, 
                                                'serial': comp.serial_number.name, 
                                                'ata' : comp.ata_code.name, 
                                                'item' : comp.item, 
                                                'service' : self.getSliveText(serv.id), 
                                                'service_id' :serv.id, 
                                                'done' : str(comp.ac_cyclesinstallation), 
                                                'time' : float(serv.remaining), 
                                                'remaining' : float(serv.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv.id),
                                                'komen' : serv.comments,
                                                }
                                        mdr.append(comps)
                                for subcomp in comp.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_cycles) and (subservice.unit == 'cycles'):
                                            subcomps = {
                                                    'data_source' : 'en1',
                                                    'data_type' : 'component',
                                                    'cycle_id':self.id,
                                                    'fleet_id': engine.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_cyclesinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)

                    if reports.engine2_type_id:
                        for engine2 in reports.engine2_type_id:
                            for comp2 in engine2.component_ids:
                                for serv2 in comp2.serfice_life:
                                    if (serv2.remaining <= warning_cycles) and (serv2.unit == 'cycles'):
                                        comps2 = {
                                                'data_source' : 'en2',
                                                'data_type' : 'component',
                                                'cycle_id':self.id,
                                                'fleet_id': engine2.name, 
                                                'name': comp2.product_id.name, 
                                                'part': comp2.part_number, 
                                                'serial': comp2.serial_number.name, 
                                                'ata' : comp2.ata_code.name, 
                                                'item' : comp2.item, 
                                                'service' : self.getSliveText(serv2.id), 
                                                'service_id' :serv2.id, 
                                                'done' : str(comp2.ac_timeinstallation), 
                                                'time' : float(serv2.remaining), 
                                                'remaining' : float(serv2.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv2.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv2.id),
                                                'komen' : serv2.comments,
                                                }
                                        mdr.append(comps2)
                                for subcomp in comp2.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_cycles) and (subservice.unit == 'cycles'):
                                            subcomps = {
                                                    'data_source' : 'en2',
                                                    'data_type' : 'component',
                                                    'cycle_id':self.id,
                                                    'fleet_id': engine2.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_cyclesinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)
                                    
                    if reports.engine3_type_id:
                        for engine3 in reports.engine3_type_id:
                            for comp3 in engine3.component_ids:
                                for serv3 in comp3.serfice_life:
                                    if (serv3.remaining <= warning_cycles) and (serv3.unit == 'cycles'):
                                        comps3 = {
                                                'data_source' : 'en3',
                                                'data_type' : 'component',
                                                'cycle_id':self.id,
                                                'fleet_id': engine3.name, 
                                                'name': comp3.product_id.name, 
                                                'part': comp3.part_number, 
                                                'serial': comp3.serial_number.name, 
                                                'ata' : comp3.ata_code.name, 
                                                'item' : comp3.item, 
                                                'service' : self.getSliveText(serv3.id), 
                                                'service_id' :serv3.id, 
                                                'done' : str(comp3.ac_timeinstallation), 
                                                'time' : float(serv3.remaining), 
                                                'remaining' : float(serv3.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv3.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv3.id),
                                                'komen' : serv3.comments,
                                                }
                                        mdr.append(comps3)
                                for subcomp in comp3.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_cycles) and (subservice.unit == 'cycles'):
                                            subcomps = {
                                                    'data_source' : 'en3',
                                                    'data_type' : 'component',
                                                    'cycle_id':self.id,
                                                    'fleet_id': engine3.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_cyclesinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)

                    if reports.engine4_type_id:
                        for engine4 in reports.engine4_type_id:
                            for comp4 in engine4.component_ids:
                                for serv4 in comp4.serfice_life:
                                    if (serv4.remaining <= warning_cycles) and (serv4.unit == 'cycles'):
                                        comps4 = {
                                                'data_source' : 'en4',
                                                'data_type' : 'component',
                                                'cycle_id':self.id,
                                                'fleet_id': engine4.name, 
                                                'name': comp4.product_id.name, 
                                                'part': comp4.part_number, 
                                                'serial': comp4.serial_number.name, 
                                                'ata' : comp4.ata_code.name, 
                                                'item' : comp4.item, 
                                                'service' : self.getSliveText(serv4.id), 
                                                'service_id' :serv4.id, 
                                                'done' : str(comp4.ac_timeinstallation), 
                                                'time' : float(serv4.remaining), 
                                                'remaining' : float(serv4.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv4.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv4.id),
                                                'komen' : serv4.comments,
                                                }
                                        mdr.append(comps4)
                                for subcomp in comp4.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_cycles) and (subservice.unit == 'cycles'):
                                            subcomps = {
                                                    'data_source' : 'en4',
                                                    'data_type' : 'component',
                                                    'cycle_id':self.id,
                                                    'fleet_id': engine4.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_cyclesinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)
                    if reports.propeller_type_id:
                        for propeller in reports.propeller_type_id:
                            for comp in propeller.component_ids:
                                for serv in comp.serfice_life:
                                    if (serv.remaining <= warning_cycles) and (serv.unit == 'cycles'):
                                        comps = {
                                                'data_source' : 'pr1',
                                                'data_type' : 'component',
                                                'cycle_id':self.id,
                                                'fleet_id': propeller.name, 
                                                'name': comp.product_id.name, 
                                                'part': comp.part_number, 
                                                'serial': comp.serial_number.name, 
                                                'ata' : comp.ata_code.name, 
                                                'item' : comp.item, 
                                                'service' : self.getSliveText(serv.id), 
                                                'service_id' :serv.id, 
                                                'done' : str(comp.ac_cyclesinstallation), 
                                                'time' : float(serv.remaining), 
                                                'remaining' : float(serv.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv.id),
                                                'komen' : serv.comments,
                                                }
                                        mdr.append(comps)
                                for subcomp in comp.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_cycles) and (subservice.unit == 'cycles'):
                                            subcomps = {
                                                    'data_source' : 'pr1',
                                                    'data_type' : 'component',
                                                    'cycle_id':self.id,
                                                    'fleet_id': propeller.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_cyclesinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)

                    if reports.propeller2_type_id:
                        for propeller2 in reports.propeller2_type_id:
                            for comp2 in propeller2.component_ids:
                                for serv2 in comp2.serfice_life:
                                    if (serv2.remaining <= warning_cycles) and (serv2.unit == 'cycles'):
                                        comps2 = {
                                                'data_source' : 'pr2',
                                                'data_type' : 'component',
                                                'cycle_id':self.id,
                                                'fleet_id': propeller2.name, 
                                                'name': comp2.product_id.name, 
                                                'part': comp2.part_number, 
                                                'serial': comp2.serial_number.name, 
                                                'ata' : comp2.ata_code.name, 
                                                'item' : comp2.item, 
                                                'service' : self.getSliveText(serv2.id), 
                                                'service_id' :serv2.id, 
                                                'done' : str(comp2.ac_timeinstallation), 
                                                'time' : float(serv2.remaining), 
                                                'remaining' : float(serv2.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv2.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv2.id),
                                                'komen' : serv2.comments,
                                                }
                                        mdr.append(comps2)
                                for subcomp in comp2.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_cycles) and (subservice.unit == 'cycles'):
                                            subcomps = {
                                                    'data_source' : 'pr2',
                                                    'data_type' : 'component',
                                                    'cycle_id':self.id,
                                                    'fleet_id': propeller2.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_cyclesinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)
                                    
                    if reports.propeller3_type_id:
                        for propeller3 in reports.propeller3_type_id:
                            for comp3 in propeller3.component_ids:
                                for serv3 in comp3.serfice_life:
                                    if (serv3.remaining <= warning_cycles) and (serv3.unit == 'cycles'):
                                        comps3 = {
                                                'data_source' : 'pr3',
                                                'data_type' : 'component',
                                                'cycle_id':self.id,
                                                'fleet_id': propeller3.name, 
                                                'name': comp3.product_id.name, 
                                                'part': comp3.part_number, 
                                                'serial': comp3.serial_number.name, 
                                                'ata' : comp3.ata_code.name, 
                                                'item' : comp3.item, 
                                                'service' : self.getSliveText(serv3.id), 
                                                'service_id' :serv3.id, 
                                                'done' : str(comp3.ac_cyclesinstallation), 
                                                'time' : float(serv3.remaining), 
                                                'remaining' : float(serv3.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv3.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv3.id),
                                                'komen' : serv3.comments,
                                                }
                                        mdr.append(comps3)
                                for subcomp in comp3.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_cycles) and (subservice.unit == 'cycles'):
                                            subcomps = {
                                                    'data_source' : 'pr3',
                                                    'data_type' : 'component',
                                                    'cycle_id':self.id,
                                                    'fleet_id': propeller3.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_cyclesinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)

                    if reports.propeller4_type_id:
                        for propeller4 in reports.propeller4_type_id:
                            for comp4 in propeller4.component_ids:
                                for serv4 in comp4.serfice_life:
                                    if (serv4.remaining <= warning_cycles) and (serv4.unit == 'cycles'):
                                        comps4 = {
                                                'data_source' : 'pr4',
                                                'data_type' : 'component',
                                                'cycle_id':self.id,
                                                'fleet_id': propeller4.name, 
                                                'name': comp4.product_id.name, 
                                                'part': comp4.part_number, 
                                                'serial': comp4.serial_number.name, 
                                                'ata' : comp4.ata_code.name, 
                                                'item' : comp4.item, 
                                                'service' : self.getSliveText(serv4.id), 
                                                'service_id' :serv4.id, 
                                                'done' : str(comp4.ac_cyclesinstallation), 
                                                'time' : float(serv4.remaining), 
                                                'remaining' : float(serv4.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv4.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv4.id),
                                                'komen' : serv4.comments,
                                                }
                                        mdr.append(comps4)
                                for subcomp in comp4.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_cycles) and (subservice.unit == 'cycles'):
                                            subcomps = {
                                                    'data_source' : 'pr4',
                                                    'data_type' : 'component',
                                                    'cycle_id':self.id,
                                                    'fleet_id': propeller4.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_cyclesinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)

                    if reports.auxiliary_type_id:
                        for auxiliary in reports.auxiliary_type_id:
                            for comp4 in auxiliary.component_ids:
                                for slive in comp4.serfice_life:
                                    if (slive.remaining <= warning_cycles) and (slive.unit == 'cycles'):
                                        comps4 = {
                                                'data_source' : 'aux',
                                                'data_type' : 'component',
                                                'cycle_id':self.id,
                                                'fleet_id': auxiliary.name, 
                                                'name': comp4.product_id.name, 
                                                'part': comp4.part_number, 
                                                'serial': comp4.serial_number.name, 
                                                'ata' : comp4.ata_code.name, 
                                                'item' : comp4.item, 
                                                'service' : self.getSliveText(slive.id), 
                                                'service_id' :slive.id, 
                                                'done' : str(comp4.ac_cyclesinstallation), 
                                                'time' : float(slive.remaining), 
                                                'remaining' : float(slive.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, slive.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, slive.id),
                                                'komen' : slive.comments,
                                                }
                                        mdr.append(comps4)
                                for subcomp in comp4.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_cycles) and (subservice.unit == 'cycles'):
                                            subcomps = {
                                                    'data_source' : 'aux',
                                                    'data_type' : 'component',
                                                    'cycle_id':self.id,
                                                    'fleet_id': auxiliary.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_cyclesinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)

            self.cycle_limit_id = mdr


    @api.model
    def _get_rin(self):
        if self.env["rin.limit.mdr"].search([('rin_id','=',self.id)]):
            self.env["rin.limit.mdr"].search([('rin_id','=',self.id)]).unlink()
        if self.id:
            settime = self.env['ams.config'].search([])
            mdr = []
            if self.type == 'fleet':
                if self.fleet_id:
                    data_rin = self.env['aircraft.acquisition'].search([('name','=',self.fleet_id.name)])
                else:
                    data_rin = self.env['aircraft.acquisition'].search([])
            elif self.type == 'engine':
                if self.fleet_id:
                    data_rin = self.env['engine.type'].search([('name','=',self.engine_id.name)])
                else:
                    data_rin = self.env['engine.type'].search([])
            elif self.type == 'auxiliary':
                if self.fleet_id:
                    data_rin = self.env['auxiliary.type'].search([('name','=',self.auxiliary_id.name)])
                else:
                    data_rin = self.env['auxiliary.type'].search([])
            elif self.type == 'propeller':
                if self.fleet_id:
                    data_rin = self.env['propeller.type'].search([('name','=',self.propeller_id.name)])
                else:
                    data_rin = self.env['propeller.type'].search([])
            else:
                fleet = self.env['aircraft.acquisition'].search([])
                engine = self.env['engine.type'].search([])
                auxiliary = self.env['auxiliary.type'].search([])
                propeller = self.env['propeller.type'].search([])
                all = []
                for al in fleet:
                    all.append(al)
                for al in engine:
                    all.append(al)
                for al in auxiliary:
                    all.append(al)
                for al in propeller:
                    all.append(al)
                data_rin = all


            #warning_rins = self.env['ams.setting'].search([],limit=1,order='create_date DESC').warning_rins
            warning_rins = self.warning_rins
            for reports in data_rin:
                for component in reports.component_ids:
                    for service in component.serfice_life:
                        if (service.remaining <= warning_rins) and (service.unit == 'rins'):
                            components = {
                                    'data_source' : 'ac',
                                    'data_type' : 'component',
                                    'rin_id':self.id,
                                    'fleet_id': reports.name, 
                                    'name': component.product_id.name, 
                                    'part': component.part_number, 
                                    'serial': component.serial_number.name, 
                                    'ata' : component.ata_code.name, 
                                    'item' : component.item, 
                                    'service' : self.getSliveText(service.id), 
                                    'service_id' :service.id, 
                                    'done' : str(reports.total_rins), 
                                    'time' : float(service.remaining),
                                    'remaining' : float(service.remaining),
                                    'project': (datetime.strptime(self.countDate(self.fleet_id, service.id), '%Y-%m-%d').strftime('%d/%m/%Y') if self.countDate(self.fleet_id, service.id) != False else ''),
                                    'projected_date': self.countDate(self.fleet_id, service.id),
                                    'komen' : service.comments,
                                    }
                            mdr.append(components)
                            # self.rin_limit_id |= self.env['rin.limit.mdr'].create(components)

                    for subcomp in component.sub_part_ids:
                        for subservice in subcomp.serfice_life:
                            if (subservice.remaining <= warning_rins) and (subservice.unit == 'rins'):
                                subcomponents = {
                                    'data_source' : 'ac',
                                    'data_type' : 'component',
                                    'rin_id':self.id,
                                    'fleet_id': reports.name, 
                                    'name': subcomp.product_id.name, 
                                    'part': subcomp.part_number, 
                                    'serial': subcomp.serial_number.name, 
                                    'ata' : subcomp.ata_code.name, 
                                    'item' : subcomp.item, 
                                    'service' : self.getSliveText(subservice.id), 
                                    'service_id' :subservice.id, 
                                    'done' : str(reports.total_rins), 
                                    'time' : float(subservice.remaining),
                                    'remaining' : float(subservice.remaining),
                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                    'komen' : subservice.comments,
                                    }
                                mdr.append(subcomponents)
                                # self.rin_limit_id |= self.env['rin.limit.mdr'].create(subcomponents)

                if True:
                    # if self.include_attach:
                    if reports.engine_type_id:
                        for engine in reports.engine_type_id:
                            for comp in engine.component_ids:
                                for serv in comp.serfice_life:
                                    if (serv.remaining <= warning_rins) and (serv.unit == 'rins'):
                                        comps = {
                                                'data_source' : 'en1',
                                                'data_type' : 'component',
                                                'rin_id':self.id,
                                                'fleet_id': engine.name, 
                                                'name': comp.product_id.name, 
                                                'part': comp.part_number, 
                                                'serial': comp.serial_number.name, 
                                                'ata' : comp.ata_code.name, 
                                                'item' : comp.item, 
                                                'service' : self.getSliveText(serv.id), 
                                                'service_id' :serv.id, 
                                                'done' : str(comp.ac_timeinstallation), 
                                                'time' : float(serv.remaining), 
                                                'remaining' : float(serv.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv.id),
                                                'komen' : serv.comments,
                                                }
                                        mdr.append(comps)
                                for subcomp in comp.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_rins) and (subservice.unit == 'rins'):
                                            subcomps = {
                                                    'data_source' : 'en1',
                                                    'data_type' : 'component',
                                                    'rin_id':self.id,
                                                    'fleet_id': engine.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_timeinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)

                    if reports.engine2_type_id:
                        for engine2 in reports.engine2_type_id:
                            for comp2 in engine2.component_ids:
                                for serv2 in comp2.serfice_life:
                                    if (serv2.remaining <= warning_rins) and (serv2.unit == 'rins'):
                                        comps2 = {
                                                'data_source' : 'en2',
                                                'data_type' : 'component',
                                                'rin_id':self.id,
                                                'fleet_id': engine2.name, 
                                                'name': comp2.product_id.name, 
                                                'part': comp2.part_number, 
                                                'serial': comp2.serial_number.name, 
                                                'ata' : comp2.ata_code.name, 
                                                'item' : comp2.item, 
                                                'service' : self.getSliveText(serv2.id), 
                                                'service_id' :serv2.id, 
                                                'done' : str(comp2.ac_timeinstallation), 
                                                'time' : float(serv2.remaining), 
                                                'remaining' : float(serv2.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv2.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv2.id),
                                                'komen' : serv2.comments,
                                                }
                                        mdr.append(comps2)
                                for subcomp in comp2.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_rins) and (subservice.unit == 'rins'):
                                            subcomps = {
                                                    'data_source' : 'en2',
                                                    'data_type' : 'component',
                                                    'rin_id':self.id,
                                                    'fleet_id': engine2.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_timeinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)
                                    
                    if reports.engine3_type_id:
                        for engine3 in reports.engine3_type_id:
                            for comp3 in engine3.component_ids:
                                for serv3 in comp3.serfice_life:
                                    if (serv3.remaining <= warning_rins) and (serv3.unit == 'rins'):
                                        comps3 = {
                                                'data_source' : 'en3',
                                                'data_type' : 'component',
                                                'rin_id':self.id,
                                                'fleet_id': engine3.name, 
                                                'name': comp3.product_id.name, 
                                                'part': comp3.part_number, 
                                                'serial': comp3.serial_number.name, 
                                                'ata' : comp3.ata_code.name, 
                                                'item' : comp3.item, 
                                                'service' : self.getSliveText(serv3.id), 
                                                'service_id' :serv3.id, 
                                                'done' : str(comp3.ac_timeinstallation), 
                                                'time' : float(serv3.remaining), 
                                                'remaining' : float(serv3.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv3.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv3.id),
                                                'komen' : serv3.comments,
                                                }
                                        mdr.append(comps3)
                                for subcomp in comp3.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_rins) and (subservice.unit == 'rins'):
                                            subcomps = {
                                                    'data_source' : 'en3',
                                                    'data_type' : 'component',
                                                    'rin_id':self.id,
                                                    'fleet_id': engine3.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_timeinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)

                    if reports.engine4_type_id:
                        for engine4 in reports.engine4_type_id:
                            for comp4 in engine4.component_ids:
                                for serv4 in comp4.serfice_life:
                                    if (serv4.remaining <= warning_rins) and (serv4.unit == 'rins'):
                                        comps4 = {
                                                'data_source' : 'en4',
                                                'data_type' : 'component',
                                                'rin_id':self.id,
                                                'fleet_id': engine4.name, 
                                                'name': comp4.product_id.name, 
                                                'part': comp4.part_number, 
                                                'serial': comp4.serial_number.name, 
                                                'ata' : comp4.ata_code.name, 
                                                'item' : comp4.item, 
                                                'service' : self.getSliveText(serv4.id), 
                                                'service_id' :serv4.id, 
                                                'done' : str(comp4.ac_timeinstallation), 
                                                'time' : float(serv4.remaining), 
                                                'remaining' : float(serv4.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv4.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv4.id),
                                                'komen' : serv4.comments,
                                                }
                                        mdr.append(comps4)
                                for subcomp in comp4.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_rins) and (subservice.unit == 'rins'):
                                            subcomps = {
                                                    'data_source' : 'en4',
                                                    'data_type' : 'component',
                                                    'rin_id':self.id,
                                                    'fleet_id': engine4.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_timeinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)
                    if reports.propeller_type_id:
                        for propeller in reports.propeller_type_id:
                            for comp in propeller.component_ids:
                                for serv in comp.serfice_life:
                                    if (serv.remaining <= warning_rins) and (serv.unit == 'rins'):
                                        comps = {
                                                'data_source' : 'pr1',
                                                'data_type' : 'component',
                                                'rin_id':self.id,
                                                'fleet_id': propeller.name, 
                                                'name': comp.product_id.name, 
                                                'part': comp.part_number, 
                                                'serial': comp.serial_number.name, 
                                                'ata' : comp.ata_code.name, 
                                                'item' : comp.item, 
                                                'service' : self.getSliveText(serv.id), 
                                                'service_id' :serv.id, 
                                                'done' : str(comp.ac_timeinstallation), 
                                                'time' : float(serv.remaining), 
                                                'remaining' : float(serv.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv.id),
                                                'komen' : serv.comments,
                                                }
                                        mdr.append(comps)
                                for subcomp in comp.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_rins) and (subservice.unit == 'rins'):
                                            subcomps = {
                                                    'data_source' : 'pr1',
                                                    'data_type' : 'component',
                                                    'rin_id':self.id,
                                                    'fleet_id': propeller.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_timeinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)

                    if reports.propeller2_type_id:
                        for propeller2 in reports.propeller2_type_id:
                            for comp2 in propeller2.component_ids:
                                for serv2 in comp2.serfice_life:
                                    if (serv2.remaining <= warning_rins) and (serv2.unit == 'rins'):
                                        comps2 = {
                                                'data_source' : 'pr2',
                                                'data_type' : 'component',
                                                'rin_id':self.id,
                                                'fleet_id': propeller2.name, 
                                                'name': comp2.product_id.name, 
                                                'part': comp2.part_number, 
                                                'serial': comp2.serial_number.name, 
                                                'ata' : comp2.ata_code.name, 
                                                'item' : comp2.item, 
                                                'service' : self.getSliveText(serv2.id), 
                                                'service_id' :serv2.id, 
                                                'done' : str(comp2.ac_timeinstallation), 
                                                'time' : float(serv2.remaining), 
                                                'remaining' : float(serv2.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv2.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv2.id),
                                                'komen' : serv2.comments,
                                                }
                                        mdr.append(comps2)
                                for subcomp in comp2.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_rins) and (subservice.unit == 'rins'):
                                            subcomps = {
                                                    'data_source' : 'pr2',
                                                    'data_type' : 'component',
                                                    'rin_id':self.id,
                                                    'fleet_id': propeller2.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_timeinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)
                                    
                    if reports.propeller3_type_id:
                        for propeller3 in reports.propeller3_type_id:
                            for comp3 in propeller3.component_ids:
                                for serv3 in comp3.serfice_life:
                                    if (serv3.remaining <= warning_rins) and (serv3.unit == 'rins'):
                                        comps3 = {
                                                'data_source' : 'pr3',
                                                'data_type' : 'component',
                                                'rin_id':self.id,
                                                'fleet_id': propeller3.name, 
                                                'name': comp3.product_id.name, 
                                                'part': comp3.part_number, 
                                                'serial': comp3.serial_number.name, 
                                                'ata' : comp3.ata_code.name, 
                                                'item' : comp3.item, 
                                                'service' : self.getSliveText(serv3.id), 
                                                'service_id' :serv3.id, 
                                                'done' : str(comp3.ac_timeinstallation), 
                                                'time' : float(serv3.remaining), 
                                                'remaining' : float(serv3.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv3.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv3.id),
                                                'komen' : serv3.comments,
                                                }
                                        mdr.append(comps3)
                                for subcomp in comp3.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_rins) and (subservice.unit == 'rins'):
                                            subcomps = {
                                                    'data_source' : 'pr3',
                                                    'data_type' : 'component',
                                                    'rin_id':self.id,
                                                    'fleet_id': propeller3.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_timeinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)

                    if reports.propeller4_type_id:
                        for propeller4 in reports.propeller4_type_id:
                            for comp4 in propeller4.component_ids:
                                for serv4 in comp4.serfice_life:
                                    if (serv4.remaining <= warning_rins) and (serv4.unit == 'rins'):
                                        comps4 = {
                                                'data_source' : 'pr4',
                                                'data_type' : 'component',
                                                'rin_id':self.id,
                                                'fleet_id': propeller4.name, 
                                                'name': comp4.product_id.name, 
                                                'part': comp4.part_number, 
                                                'serial': comp4.serial_number.name, 
                                                'ata' : comp4.ata_code.name, 
                                                'item' : comp4.item, 
                                                'service' : self.getSliveText(serv4.id), 
                                                'service_id' :serv4.id, 
                                                'done' : str(comp4.ac_timeinstallation), 
                                                'time' : float(serv4.remaining), 
                                                'remaining' : float(serv4.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv4.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv4.id),
                                                'komen' : serv4.comments,
                                                }
                                        mdr.append(comps4)
                                for subcomp in comp4.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_rins) and (subservice.unit == 'rins'):
                                            subcomps = {
                                                    'data_source' : 'pr4',
                                                    'data_type' : 'component',
                                                    'rin_id':self.id,
                                                    'fleet_id': propeller4.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_timeinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)

                    if reports.auxiliary_type_id:
                        for auxiliary in reports.auxiliary_type_id:
                            for comp in auxiliary.component_ids:
                                for serv in comp.serfice_life:
                                    if (serv.remaining <= warning_rins) and (serv.unit == 'rins'):
                                        comps4 = {
                                                'data_source' : 'aux',
                                                'data_type' : 'component',
                                                'rin_id':self.id,
                                                'fleet_id': auxiliary.name, 
                                                'name': comp.product_id.name, 
                                                'part': comp.part_number, 
                                                'serial': comp.serial_number.name, 
                                                'ata' : comp.ata_code.name, 
                                                'item' : comp.item, 
                                                'service' : self.getSliveText(serv.id), 
                                                'service_id' :serv.id, 
                                                'done' : str(comp.ac_timeinstallation), 
                                                'time' : float(serv.remaining), 
                                                'remaining' : float(serv.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv.id),
                                                'komen' : serv.comments,
                                                }
                                        mdr.append(comps4)
                                for subcomp in comp.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if (subservice.remaining <= warning_rins) and (subservice.unit == 'rins'):
                                            subcomps = {
                                                    'data_source' : 'aux',
                                                    'data_type' : 'component',
                                                    'rin_id':self.id,
                                                    'fleet_id': auxiliary.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : str(subcomp.ac_timeinstallation), 
                                                    'time' : float(subservice.remaining), 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomps)
            self.rin_limit_id = mdr

    @api.model
    def _get_calendar(self):
        if self.env["calendar.limit.mdr"].search([('calendar_id','=',self.id)]):
            self.env["calendar.limit.mdr"].search([('calendar_id','=',self.id)]).unlink()
        if self.id:
            settime = self.env['ams.config'].search([])
            mdr = []
            if self.type == 'fleet':
                if self.fleet_id:
                    data_calendar = self.env['aircraft.acquisition'].search([('name','=',self.fleet_id.name)])
                else:
                    data_calendar = self.env['aircraft.acquisition'].search([])
            elif self.type == 'engine':
                if self.fleet_id:
                    data_calendar = self.env['engine.type'].search([('name','=',self.engine_id.name)])
                else:
                    data_calendar = self.env['engine.type'].search([])
            elif self.type == 'auxiliary':
                if self.fleet_id:
                    data_calendar = self.env['auxiliary.type'].search([('name','=',self.auxiliary_id.name)])
                else:
                    data_calendar = self.env['auxiliary.type'].search([])
            elif self.type == 'propeller':
                if self.fleet_id:
                    data_calendar = self.env['propeller.type'].search([('name','=',self.propeller_id.name)])
                else:
                    data_calendar = self.env['propeller.type'].search([])
            else:
                fleet = self.env['aircraft.acquisition'].search([])
                engine = self.env['engine.type'].search([])
                auxiliary = self.env['auxiliary.type'].search([])
                propeller = self.env['propeller.type'].search([])
                all = []
                for al in fleet:
                    all.append(al)
                for al in engine:
                    all.append(al)
                for al in auxiliary:
                    all.append(al)
                for al in propeller:
                    all.append(al)
                data_calendar = all

            calendar_serv = ['days','month','year']
            #warning_calendars = self.env['ams.setting'].search([],limit=1,order='create_date DESC').warning_calendars
            warning_calendars =  self.warning_calendars
            #print warning_calendars
            # print datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')
            # print datetime.strptime(str(warning_calendars), '%Y-%m-%d')

            # jarak_hari = relativedelta( datetime.strptime(str(datetime.now().date()), '%Y-%m-%d'), datetime.strptime(str(warning_calendars), '%Y-%m-%d'))
            #print jarak_hari,"Ini Jarak Hari"
            # warning_date = datetime.now()+ relativedelta(days=int(str(jarak_hari.days)))
            warning_date = datetime.strptime(self.warning_calendars, "%Y-%m-%d")
            #print warning_date,"__Ini warning date"
            print warning_date
            for reports in data_calendar:
                for component in reports.component_ids:
                    for service in component.serfice_life:
                        if (service.unit in calendar_serv) and ( warning_date >= datetime.strptime(service.next_date, "%Y-%m-%d")):
                            components = {
                                    'data_source' : 'ac',
                                    'data_type' : 'component',
                                    'calendar_id':self.id,
                                    'fleet_id': reports.name, 
                                    'name': component.product_id.name, 
                                    'part': component.part_number, 
                                    'serial': component.serial_number.name, 
                                    'ata' : component.ata_code.name, 
                                    'item' : component.item, 
                                    'service' : self.getSliveText(service.id), 
                                    'service_id' :service.id, 
                                    'done' : datetime.strptime(str(service.current_date), '%Y-%m-%d').strftime('%d/%m/%Y'), 
                                    'time' : str(( datetime.strptime(service.next_date, "%Y-%m-%d") - datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')).days)+" Days", 
                                    'project': (datetime.strptime(self.countDate(self.fleet_id, service.id), '%Y-%m-%d').strftime('%d/%m/%Y') if self.countDate(self.fleet_id, service.id) != False else ''),
                                    'projected_date': self.countDate(self.fleet_id, service.id),
                                    'komen' : service.comments,
                                    }
                            mdr.append(components)
                            # self.calendar_limit_id |= self.env['calendar.limit.mdr'].create(components)

                    for subcomp in component.sub_part_ids:
                        for subservice in subcomp.serfice_life:
                            if subservice.unit in calendar_serv :
                                # if int(abs(datetime.strptime(str(date.today()), "%Y-%m-%d")-datetime.strptime(subcomp.date_installed, "%Y-%m-%d")).days) <= settime[3].int_value:
                                if (subservice.unit in calendar_serv) and ( warning_date >= datetime.strptime(subservice.next_date, "%Y-%m-%d")):
                                    subcomponents = {
                                        'data_source' : 'ac',
                                        'data_type' : 'component',
                                        'calendar_id':self.id,
                                        'fleet_id': reports.name, 
                                        'name': subcomp.product_id.name, 
                                        'part': subcomp.part_number, 
                                        'serial': subcomp.serial_number.name, 
                                        'ata' : subcomp.ata_code.name, 
                                        'item' : subcomp.item, 
                                        'service' : self.getSliveText(subservice.id), 
                                        'service_id' :subservice.id, 
                                        'done' : datetime.strptime(str(subservice.current_date), '%Y-%m-%d').strftime('%d/%m/%Y'), 
                                        'time' : str(( datetime.strptime(subservice.next_date, "%Y-%m-%d") - datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')).days)+ " Days",
                                        'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                        'projected_date': self.countDate(self.fleet_id, subservice.id),
                                        'komen' : subservice.comments,
                                        }
                                    mdr.append(subcomponents)
                                    # self.calendar_limit_id |= self.env['calendar.limit.mdr'].create(subcomponents)

            # AC INSPECTION BY CALENDAR
            for reports in data_calendar:
                for inspection in reports.inspection_ids:
                    for service in inspection.serfice_life:
                        if (service.unit in calendar_serv) and ( warning_date >= datetime.strptime(service.next_date, "%Y-%m-%d")):
                            inspections = {
                                    'data_source' : 'ac',
                                    'data_type' : 'inspection',
                                    'calendar_id':self.id,
                                    'fleet_id': reports.name, 
                                    'name': inspection.inspection_type, 
                                    'part': '', 
                                    'serial': '', 
                                    'ata' : inspection.ata_code.name, 
                                    'item' : inspection.item, 
                                    'service' : self.getSliveText(service.id), 
                                    'service_id' :service.id, 
                                    'done' : datetime.strptime(str(service.current_date), '%Y-%m-%d').strftime('%d/%m/%Y'), 
                                    'time' : str(( datetime.strptime(service.next_date, "%Y-%m-%d") - datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')).days)+" Days", 
                                    'project': (datetime.strptime(self.countDate(self.fleet_id, service.id), '%Y-%m-%d').strftime('%d/%m/%Y') if self.countDate(self.fleet_id, service.id) != False else ''),
                                    'projected_date': self.countDate(self.fleet_id, service.id),
                                    'komen' : service.comments,
                                    }
                            mdr.append(inspections)

            if True:
                for engnum in xrange(1,4):
                    if(engnum == 1):
                        engine = reports.engine_type_id
                    elif(engnum == 2):
                        engine = reports.engine2_type_id
                    elif(engnum == 3):
                        engine = reports.engine3_type_id
                    elif(engnum == 4):
                        engine = reports.engine4_type_id
                    
                    if(engine):
                        # ENGINE INSPECTION BY CALENDAR
                        for inspection in engine.inspection_ids:
                            for service in inspection.serfice_life:
                                if (service.unit in calendar_serv) and ( warning_date >= datetime.strptime(service.next_date, "%Y-%m-%d")):
                                    inspections = {
                                            'data_source' : 'en'+str(engnum),
                                            'data_type' : 'inspection',
                                            'hour_id':self.id,
                                            'fleet_id': engine.name, 
                                            'name': inspection.inspection_type, 
                                            'part': '',
                                            'serial': '',
                                            'ata' : inspection.ata_code.name, 
                                            'item' : inspection.item, 
                                            'service' : self.getSliveText(service.id), 
                                            'service_id' :service.id, 
                                            'done' : str(reports.total_landings - service.current), 
                                            'time' : str(( datetime.strptime(service.next_date, "%Y-%m-%d") - datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')).days)+" Days", 
                                            'remaining' : float(service.remaining), 
                                            'project': (datetime.strptime(self.countDate(self.fleet_id, service.id), '%Y-%m-%d').strftime('%d/%m/%Y') if self.countDate(self.fleet_id, service.id) != False else ''),
                                            'projected_date': self.countDate(self.fleet_id, service.id),
                                            'komen' : service.comments,
                                            }
                                    mdr.append(inspections)
                for propnum in xrange(1,4):
                    if(propnum == 1):
                        propeller = reports.propeller_type_id
                    elif(propnum == 2):
                        propeller = reports.propeller2_type_id
                    elif(propnum == 3):
                        propeller = reports.propeller3_type_id
                    elif(propnum == 4):
                        propeller = reports.propeller4_type_id
                    
                    if(propeller):
                        # PROPELLER INSPECTION BY CALENDAR
                        for inspection in propeller.inspection_ids:
                            for service in inspection.serfice_life:
                                if (service.unit in calendar_serv) and ( warning_date >= datetime.strptime(service.next_date, "%Y-%m-%d")):
                                    inspections = {
                                            'data_source' : 'en'+str(propnum),
                                            'data_type' : 'inspection',
                                            'hour_id':self.id,
                                            'fleet_id': propeller.name, 
                                            'name': inspection.inspection_type, 
                                            'part': '',
                                            'serial': '',
                                            'ata' : inspection.ata_code.name, 
                                            'item' : inspection.item, 
                                            'service' : self.getSliveText(service.id), 
                                            'service_id' :service.id, 
                                            'done' : str(reports.total_landings - service.current), 
                                            'time' : str(( datetime.strptime(service.next_date, "%Y-%m-%d") - datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')).days)+" Days", 
                                            'remaining' : float(service.remaining), 
                                            'project': (datetime.strptime(self.countDate(self.fleet_id, service.id), '%Y-%m-%d').strftime('%d/%m/%Y') if self.countDate(self.fleet_id, service.id) != False else ''),
                                            'projected_date': self.countDate(self.fleet_id, service.id),
                                            'komen' : service.comments,
                                            }
                                    mdr.append(inspections)

                    if(reports.auxiliary_type_id):
                        # AUXILIARY INSPECTION BY CALENDAR
                        for inspection in reports.auxiliary_type_id.inspection_ids:
                            for service in inspection.serfice_life:
                                if (service.unit in calendar_serv) and ( warning_date >= datetime.strptime(service.next_date, "%Y-%m-%d")):
                                    inspections = {
                                            'data_source' : 'aux',
                                            'data_type' : 'inspection',
                                            'hour_id':self.id,
                                            'fleet_id': reports.auxiliary_type_id.name, 
                                            'name': inspection.inspection_type, 
                                            'part': '',
                                            'serial': '',
                                            'ata' : inspection.ata_code.name, 
                                            'item' : inspection.item, 
                                            'service' : self.getSliveText(service.id), 
                                            'service_id' :service.id, 
                                            'done' : str(reports.total_landings - service.current), 
                                            'time' : str(( datetime.strptime(service.next_date, "%Y-%m-%d") - datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')).days)+" Days", 
                                            'remaining' : float(service.remaining), 
                                            'project': (datetime.strptime(self.countDate(self.fleet_id, service.id), '%Y-%m-%d').strftime('%d/%m/%Y') if self.countDate(self.fleet_id, service.id) != False else ''),
                                            'projected_date': self.countDate(self.fleet_id, service.id),
                                            'komen' : service.comments,
                                            }
                                    mdr.append(inspections)

                if True:
                    # if self.include_attach:
                    if reports.engine_type_id:
                        for engine in reports.engine_type_id:
                            for comp in engine.component_ids:
                                for serv in comp.serfice_life:
                                    if (serv.unit in calendar_serv) and ( warning_date >= datetime.strptime(serv.next_date, "%Y-%m-%d")):
                                        comps = {
                                                'data_source' : 'en1',
                                                'data_type' : 'component',
                                                'calendar_id':self.id,
                                                'fleet_id': engine.name, 
                                                'name': comp.product_id.name, 
                                                'part': comp.part_number, 
                                                'serial': comp.serial_number.name, 
                                                'ata' : comp.ata_code.name, 
                                                'item' : comp.item, 
                                                'service' : self.getSliveText(serv.id), 
                                                'service_id' :serv.id, 
                                                'done' : datetime.strptime(str(serv.current_date), '%Y-%m-%d').strftime('%d/%m/%Y'), 
                                                'time' : str(( datetime.strptime(serv.next_date, "%Y-%m-%d") - datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')).days)+" Days", 
                                                'remaining' : float(serv.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv.id),
                                                'komen' : serv.comments,
                                                }
                                        mdr.append(comps)
                                        # self.hour_limit_id |= self.env['hour.limit.mdr'].create(comps)
                                for subcomp in comp.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if subservice.unit in calendar_serv :
                                            if (subservice.unit in calendar_serv) and ( warning_date >= datetime.strptime(subservice.next_date, "%Y-%m-%d")):
                                                subcomponents = {
                                                    'data_source' : 'en1',
                                                    'data_type' : 'component',
                                                    'calendar_id':self.id,
                                                    'fleet_id': engine.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : datetime.strptime(str(subservice.current_date), '%Y-%m-%d').strftime('%d/%m/%Y'), 
                                                    'time' : str(( datetime.strptime(subservice.next_date, "%Y-%m-%d") - datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')).days)+" Days", 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomponents)

                    if reports.engine2_type_id:
                        for engine2 in reports.engine2_type_id:
                            for comp2 in engine2.component_ids:
                                for serv2 in comp2.serfice_life:
                                    if (serv2.unit in calendar_serv) and ( warning_date >= datetime.strptime(serv2.next_date, "%Y-%m-%d")):
                                        comps2 = {
                                                'data_source' : 'en2',
                                                'data_type' : 'component',
                                                'calendar_id':self.id,
                                                'fleet_id': engine2.name, 
                                                'name': comp2.product_id.name, 
                                                'part': comp2.part_number, 
                                                'serial': comp2.serial_number.name, 
                                                'ata' : comp2.ata_code.name, 
                                                'item' : comp2.item, 
                                                'service' : self.getSliveText(serv2.id), 
                                                'service_id' :serv2.id, 
                                                'done' : datetime.strptime(str(serv2.current_date), '%Y-%m-%d').strftime('%d/%m/%Y'), 
                                                'time' : str(( datetime.strptime(serv2.next_date, "%Y-%m-%d") - datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')).days)+" Days",  
                                                'remaining' : float(serv2.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv2.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv2.id),
                                                'komen' : serv2.comments,
                                                }
                                        mdr.append(comps2)
                                for subcomp in comp2.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if subservice.unit in calendar_serv :
                                            if (subservice.unit in calendar_serv) and ( warning_date >= datetime.strptime(subservice.next_date, "%Y-%m-%d")):
                                                subcomponents = {
                                                    'data_source' : 'en1',
                                                    'data_type' : 'component',
                                                    'calendar_id':self.id,
                                                    'fleet_id': engine2.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : datetime.strptime(str(subservice.current_date), '%Y-%m-%d').strftime('%d/%m/%Y'), 
                                                    'time' : str(( datetime.strptime(subservice.next_date, "%Y-%m-%d") - datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')).days)+" Days", 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomponents)
                                        
                    if reports.engine3_type_id:
                        for engine3 in reports.engine3_type_id:
                            for comp3 in engine3.component_ids:
                                for serv3 in comp3.serfice_life:
                                    if (serv3.unit in calendar_serv) and ( warning_date >= datetime.strptime(serv3.next_date, "%Y-%m-%d")):
                                        comps3 = {
                                                'data_source' : 'en3',
                                                'data_type' : 'component',
                                                'calendar_id':self.id,
                                                'fleet_id': engine3.name, 
                                                'name': comp3.product_id.name, 
                                                'part': comp3.part_number, 
                                                'serial': comp3.serial_number.name, 
                                                'ata' : comp3.ata_code.name, 
                                                'item' : comp3.item, 
                                                'service' : self.getSliveText(serv3.id), 
                                                'service_id' :serv3.id, 
                                                'done' : datetime.strptime(str(serv3.current_date), '%Y-%m-%d').strftime('%d/%m/%Y'), 
                                                'time' : str(( datetime.strptime(serv3.next_date, "%Y-%m-%d") - datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')).days)+" Days", 
                                                'remaining' : float(serv3.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv3.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv3.id),
                                                'komen' : serv3.comments,
                                                }
                                        mdr.append(comps3)
                                for subcomp in comp3.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if subservice.unit in calendar_serv :
                                            if (subservice.unit in calendar_serv) and ( warning_date >= datetime.strptime(subservice.next_date, "%Y-%m-%d")):
                                                subcomponents = {
                                                    'data_source' : 'en1',
                                                    'data_type' : 'component',
                                                    'calendar_id':self.id,
                                                    'fleet_id': engine3.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : datetime.strptime(str(subservice.current_date), '%Y-%m-%d').strftime('%d/%m/%Y'), 
                                                    'time' : str(( datetime.strptime(subservice.next_date, "%Y-%m-%d") - datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')).days)+" Days", 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomponents)

                    if reports.engine4_type_id:
                        for engine4 in reports.engine4_type_id:
                            for comp4 in engine4.component_ids:
                                for serv4 in comp4.serfice_life:
                                    if (serv4.unit in calendar_serv) and ( warning_date >= datetime.strptime(serv4.next_date, "%Y-%m-%d")):
                                        comps4 = {
                                                'data_source' : 'en4',
                                                'data_type' : 'component',
                                                'calendar_id':self.id,
                                                'fleet_id': engine4.name, 
                                                'name': comp4.product_id.name, 
                                                'part': comp4.part_number, 
                                                'serial': comp4.serial_number.name, 
                                                'ata' : comp4.ata_code.name, 
                                                'item' : comp4.item, 
                                                'service' : self.getSliveText(serv4.id), 
                                                'service_id' :serv4.id, 
                                                'done' : datetime.strptime(str(serv4.current_date), '%Y-%m-%d').strftime('%d/%m/%Y'), 
                                                'time' : str(( datetime.strptime(serv4.next_date, "%Y-%m-%d") - datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')).days)+" Days", 
                                                'remaining' : float(serv4.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv4.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv4.id),
                                                'komen' : serv4.comments,
                                                }
                                        mdr.append(comps4)
                                for subcomp in comp4.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if subservice.unit in calendar_serv :
                                            if (subservice.unit in calendar_serv) and ( warning_date >= datetime.strptime(subservice.next_date, "%Y-%m-%d")):
                                                subcomponents = {
                                                    'data_source' : 'en1',
                                                    'data_type' : 'component',
                                                    'calendar_id':self.id,
                                                    'fleet_id': engine4.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : datetime.strptime(str(subservice.current_date), '%Y-%m-%d').strftime('%d/%m/%Y'), 
                                                    'time' : str(( datetime.strptime(subservice.next_date, "%Y-%m-%d") - datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')).days)+" Days", 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomponents)
                    if reports.propeller_type_id:
                        for propeller in reports.propeller_type_id:
                            for comp in propeller.component_ids:
                                for serv in comp.serfice_life:
                                    if (serv.unit in calendar_serv) and ( warning_date >= datetime.strptime(serv.next_date, "%Y-%m-%d")):
                                        comps = {
                                                'data_source' : 'pr1',
                                                'data_type' : 'component',
                                                'calendar_id':self.id,
                                                'fleet_id': propeller.name, 
                                                'name': comp.product_id.name, 
                                                'part': comp.part_number, 
                                                'serial': comp.serial_number.name, 
                                                'ata' : comp.ata_code.name, 
                                                'item' : comp.item, 
                                                'service' : self.getSliveText(serv.id), 
                                                'service_id' :serv.id, 
                                                'done' : datetime.strptime(str(serv.current_date), '%Y-%m-%d').strftime('%d/%m/%Y'), 
                                                'time' : str(( datetime.strptime(serv.next_date, "%Y-%m-%d") - datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')).days)+" Days",  
                                                'remaining' : float(serv.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv.id),
                                                'komen' : serv.comments,
                                                }
                                        mdr.append(comps)
                                        # self.hour_limit_id |= self.env['hour.limit.mdr'].create(comps)
                                for subcomp in comp.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if subservice.unit in calendar_serv :
                                            if (subservice.unit in calendar_serv) and ( warning_date >= datetime.strptime(subservice.next_date, "%Y-%m-%d")):
                                                subcomponents = {
                                                    'data_source' : 'pr1',
                                                    'data_type' : 'component',
                                                    'calendar_id':self.id,
                                                    'fleet_id': propeller.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : datetime.strptime(str(subservice.current_date), '%Y-%m-%d').strftime('%d/%m/%Y'), 
                                                    'time' : str(( datetime.strptime(subservice.next_date, "%Y-%m-%d") - datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')).days)+" Days", 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomponents)

                    if reports.propeller2_type_id:
                        for propeller2 in reports.propeller2_type_id:
                            for comp2 in propeller2.component_ids:
                                for serv2 in comp2.serfice_life:
                                    if (serv2.unit in calendar_serv) and ( warning_date >= datetime.strptime(serv2.next_date, "%Y-%m-%d")):
                                        comps2 = {
                                                'data_source' : 'pr2',
                                                'data_type' : 'component',
                                                'calendar_id':self.id,
                                                'fleet_id': propeller2.name, 
                                                'name': comp2.product_id.name, 
                                                'part': comp2.part_number, 
                                                'serial': comp2.serial_number.name, 
                                                'ata' : comp2.ata_code.name, 
                                                'item' : comp2.item, 
                                                'service' : self.getSliveText(serv2.id), 
                                                'service_id' :serv2.id, 
                                                'done' : datetime.strptime(str(serv2.current_date), '%Y-%m-%d').strftime('%d/%m/%Y'), 
                                                'time' : str(( datetime.strptime(serv2.next_date, "%Y-%m-%d") - datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')).days)+" Days", 
                                                'remaining' : float(serv2.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv2.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv2.id),
                                                'komen' : serv2.comments,
                                                }
                                        mdr.append(comps2)
                                for subcomp in comp2.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if subservice.unit in calendar_serv :
                                            if (subservice.unit in calendar_serv) and ( warning_date >= datetime.strptime(subservice.next_date, "%Y-%m-%d")):
                                                subcomponents = {
                                                    'data_source' : 'pr1',
                                                    'data_type' : 'component',
                                                    'calendar_id':self.id,
                                                    'fleet_id': propeller2.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : datetime.strptime(str(subservice.current_date), '%Y-%m-%d').strftime('%d/%m/%Y'), 
                                                    'time' : str(( datetime.strptime(subservice.next_date, "%Y-%m-%d") - datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')).days)+" Days", 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomponents)
                                        
                    if reports.propeller3_type_id:
                        for propeller3 in reports.propeller3_type_id:
                            for comp3 in propeller3.component_ids:
                                for serv3 in comp3.serfice_life:
                                    if (serv3.unit in calendar_serv) and ( warning_date >= datetime.strptime(serv3.next_date, "%Y-%m-%d")):
                                        comps3 = {
                                                'data_source' : 'pr3',
                                                'data_type' : 'component',
                                                'calendar_id':self.id,
                                                'fleet_id': propeller3.name, 
                                                'name': comp3.product_id.name, 
                                                'part': comp3.part_number, 
                                                'serial': comp3.serial_number.name, 
                                                'ata' : comp3.ata_code.name, 
                                                'item' : comp3.item, 
                                                'service' : self.getSliveText(serv3.id), 
                                                'service_id' :serv3.id, 
                                                'done' : datetime.strptime(str(serv3.current_date), '%Y-%m-%d').strftime('%d/%m/%Y'), 
                                                'time' : str(( datetime.strptime(serv3.next_date, "%Y-%m-%d") - datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')).days)+" Days", 
                                                'remaining' : float(serv3.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv3.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv3.id),
                                                'komen' : serv3.comments,
                                                }
                                        mdr.append(comps3)
                                for subcomp in comp3.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if subservice.unit in calendar_serv :
                                            if (subservice.unit in calendar_serv) and ( warning_date >= datetime.strptime(subservice.next_date, "%Y-%m-%d")):
                                                subcomponents = {
                                                    'data_source' : 'pr1',
                                                    'data_type' : 'component',
                                                    'calendar_id':self.id,
                                                    'fleet_id': propeller3.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : datetime.strptime(str(subservice.current_date), '%Y-%m-%d').strftime('%d/%m/%Y'), 
                                                    'time' : str(( datetime.strptime(subservice.next_date, "%Y-%m-%d") - datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')).days)+" Days", 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomponents)

                    if reports.propeller4_type_id:
                        for propeller4 in reports.propeller4_type_id:
                            for comp4 in propeller4.component_ids:
                                for serv4 in comp4.serfice_life:
                                    if (serv4.unit in calendar_serv) and ( warning_date >= datetime.strptime(serv4.next_date, "%Y-%m-%d")):
                                        comps4 = {
                                                'data_source' : 'pr4',
                                                'data_type' : 'component',
                                                'calendar_id':self.id,
                                                'fleet_id': propeller4.name, 
                                                'name': comp4.product_id.name, 
                                                'part': comp4.part_number, 
                                                'serial': comp4.serial_number.name, 
                                                'ata' : comp4.ata_code.name, 
                                                'item' : comp4.item, 
                                                'service' : self.getSliveText(serv4.id), 
                                                'service_id' :serv4.id, 
                                                'done' : datetime.strptime(str(serv4.current_date), '%Y-%m-%d').strftime('%d/%m/%Y'), 
                                                'time' : str(( datetime.strptime(serv4.next_date, "%Y-%m-%d") - datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')).days)+" Days", 
                                                'remaining' : float(serv4.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv4.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv4.id),
                                                'komen' : serv4.comments,
                                                }
                                        mdr.append(comps4)
                                for subcomp in comp4.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if subservice.unit in calendar_serv :
                                            if (subservice.unit in calendar_serv) and ( warning_date >= datetime.strptime(subservice.next_date, "%Y-%m-%d")):
                                                subcomponents = {
                                                    'data_source' : 'pr1',
                                                    'data_type' : 'component',
                                                    'calendar_id':self.id,
                                                    'fleet_id': propeller4.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : datetime.strptime(str(subservice.current_date), '%Y-%m-%d').strftime('%d/%m/%Y'), 
                                                    'time' : str(( datetime.strptime(subservice.next_date, "%Y-%m-%d") - datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')).days)+" Days", 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomponents)
                    if reports.auxiliary_type_id:
                        for auxiliary in reports.auxiliary_type_id:
                            for comp in auxiliary.component_ids:
                                for serv in comp.serfice_life:
                                    if (serv.unit in calendar_serv) and ( warning_date >= datetime.strptime(serv.next_date, "%Y-%m-%d")):
                                        comps = {
                                                'data_source' : 'aux',
                                                'data_type' : 'component',
                                                'calendar_id':self.id,
                                                'fleet_id': auxiliary.name, 
                                                'name': comp.product_id.name, 
                                                'part': comp.part_number, 
                                                'serial': comp.serial_number.name, 
                                                'ata' : comp.ata_code.name, 
                                                'item' : comp.item, 
                                                'service' : self.getSliveText(serv.id), 
                                                'service_id' :serv.id, 
                                                'done' : datetime.strptime(str(serv.current_date), '%Y-%m-%d').strftime('%d/%m/%Y'), 
                                                'time' : str(( datetime.strptime(serv.next_date, "%Y-%m-%d") - datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')).days)+" Days", 
                                                'remaining' : float(serv.remaining), 
                                                'project': datetime.strptime(self.countDate(self.fleet_id, serv.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                'projected_date': self.countDate(self.fleet_id, serv.id),
                                                'komen' : serv.comments,
                                                }
                                        mdr.append(comps)
                                for subcomp in comp.sub_part_ids:
                                    for subservice in subcomp.serfice_life:
                                        if subservice.unit in calendar_serv :
                                            if (subservice.unit in calendar_serv) and ( warning_date >= datetime.strptime(subservice.next_date, "%Y-%m-%d")):
                                                subcomponents = {
                                                    'data_source' : 'aux',
                                                    'data_type' : 'component',
                                                    'calendar_id':self.id,
                                                    'fleet_id': auxiliary.name, 
                                                    'name': subcomp.product_id.name, 
                                                    'part': subcomp.part_number, 
                                                    'serial': subcomp.serial_number.name, 
                                                    'ata' : subcomp.ata_code.name, 
                                                    'item' : subcomp.item, 
                                                    'service' : self.getSliveText(subservice.id), 
                                                    'service_id' :subservice.id, 
                                                    'done' : datetime.strptime(str(subservice.current_date), '%Y-%m-%d').strftime('%d/%m/%Y'), 
                                                    'time' : str(( datetime.strptime(subservice.next_date, "%Y-%m-%d") - datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')).days)+" Days", 
                                                    'remaining' : float(subservice.remaining), 
                                                    'project': datetime.strptime(self.countDate(self.fleet_id, subservice.id), '%Y-%m-%d').strftime('%d/%m/%Y'),
                                                    'projected_date': self.countDate(self.fleet_id, subservice.id),
                                                    'komen' : subservice.comments,
                                                    }
                                            mdr.append(subcomponents)

            # print(sorted(mdr.items(), key=lambda kv:(kv['projected_date'], kv['projected_date']))) 
            self.calendar_limit_id = mdr

    @api.model
    def _get_certificate(self):
        if self.env['certificate.limit.mdr'].search([('certificate_id', '=', self.id )]):
            self.env['certificate.limit.mdr'].search([('certificate_id', '=', self.id)]).unlink()

        if self.id != False:
            mdr = []
            cr_data = self.env['document.certificate'].search([('acquisition_id', '=', self.fleet_id.id ), ('date_expired','<=',self.warning_calendars)])
            
            if cr_data:
                for rec in cr_data:
                    certificate = {
                        'name': rec.document_id.name,
                        'fleet_id': self.fleet_id.name,
                        'due_at': rec.date_expired,
                        'project_date': rec.date_expired, 
                        'remain': str((datetime.strptime(self.warning_calendars, "%Y-%m-%d") - datetime.strptime(rec.date_expired, "%Y-%m-%d")).days) + " Days",

                    }

                    mdr.append(certificate)
            self.certificate_limit_id = mdr

    def getSliveText(self,slive_id):
        slive_name = ''
        slive = self.env['ams.component.servicelife'].search([('id','=',slive_id)])
        slive_name = str(slive.value) 
        slive_name = slive_name.rstrip('0').rstrip('.') if '.' in slive_name else slive_name
        if(slive.unit == 'hours'):
            slive_name = slive_name + ' HR:'
        elif(slive.unit == 'cycles'):
            slive_name = slive_name + ' CY:'
        elif(slive.unit == 'rin'):
            slive_name = slive_name + ' RIN:'
        elif(slive.unit == 'year'):
            slive_name = slive_name + ' YR:'
        elif(slive.unit == 'month'):
            slive_name = slive_name + ' MO:'
        elif(slive.unit == 'days'):
            slive_name = slive_name + ' DY:'

        if(slive.action_type == 'inspection'):
            slive_name = slive_name + 'IN'
        elif(slive.action_type == 'overhaul'):
            slive_name = slive_name + 'OH'
        elif(slive.action_type == 'retirement'):
            slive_name = slive_name + 'RT'
        elif(slive.action_type == 'oncondition'):
            slive_name = 'OC'
        elif(slive.action_type == 'conditionmonitoring'):
            slive_name = slive_name + 'CM'

        return slive_name

    def countDate(self,fleet_id,slive_id):
            service_life = self.env['ams.component.servicelife'].search([('id','=',slive_id)])
            today = datetime.now()
            Remaining = service_life.remaining
            Target = 0

            part_of = False
            fleet_id = fleet_id
            engine_id = False
            auxiliary_id = False
            propeller_id = False
            comp = service_life.part_id
            insp = service_life.inspection_id
            bull = service_life.bulletin_affected_id


            # COMPONENT
            if(comp.id != False):
                if(comp.is_subcomp == True):
                    if (comp.part_id.engine_id.id != False):
                        engine_id = comp.part_id.engine_id
                        part_of = 'E'
                    elif (comp.part_id.auxiliary_id.id != False):
                        auxiliary_id = comp.part_id.auxiliary_id
                        part_of = 'A'
                    elif (comp.part_id.propeller_id.id != False):
                        propeller_id = comp.part_id.propeller_id
                        part_of = 'P'
                    elif (comp.part_id.fleet_id.id != False):
                        # fleet_id = comp.part_id.fleet_id
                        part_of = 'F'
                else:
                    if (comp.engine_id.id != False):
                        engine_id = comp.engine_id
                        part_of = 'E'
                    elif (comp.auxiliary_id.id != False):
                        auxiliary_id = comp.auxiliary_id
                        part_of = 'A'
                    elif (comp.propeller_id.id != False):
                        propeller_id = comp.propeller_id
                        part_of = 'P'
                    elif (comp.fleet_id.id != False):
                        # fleet_id = comp.fleet_id
                        part_of = 'F'
            # INSPEKSI
            elif(insp.id != False):
                if (insp.engine_id.id != False):
                    engine_id = insp.engine_id
                    part_of = 'E'
                elif (insp.auxiliary_id.id != False):
                    auxiliary_id = insp.auxiliary_id
                    part_of = 'A'
                elif (insp.propeller_id.id != False):
                    propeller_id = insp.propeller_id
                    part_of = 'P'
                elif (insp.fleet_id.id != False):
                    # fleet_id = insp.fleet_id
                    part_of = 'F'
            # BULLETIN
            else:
                if (bull.engine_id.id != False):
                    engine_id = bull.engine_id
                    part_of = 'E'
                elif (bull.auxiliary_id.id != False):
                    auxiliary_id = bull.auxiliary_id
                    part_of = 'A'
                elif (bull.propeller_id.id != False):
                    propeller_id = bull.propeller_id
                    part_of = 'P'
                elif (bull.fleet_id.id != False):
                    # fleet_id = bull.fleet_id
                    part_of = 'F'


            daily_utilz = self.env['ams.daily'].search(['&',('fleet_id','=',fleet_id.id),('is_active','=',True)], order="create_date desc", limit=1)
            hours = daily_utilz.aircraft_hours
            cycles = daily_utilz.aircraft_cycles
            rin = daily_utilz.aircraft_rin

            if(part_of == 'E'):
                if(engine_id.id == daily_utilz.engine1_id.id):
                    hours = daily_utilz.engine1_hours
                    cycles = daily_utilz.engine1_cycles
                elif(engine_id.id == daily_utilz.engine2_id.id):
                    hours = daily_utilz.engine2_hours
                    cycles = daily_utilz.engine2_cycles
                elif(engine_id.id == daily_utilz.engine3_id.id):
                    hours = daily_utilz.engine3_hours
                    cycles = daily_utilz.engine3_cycles
                elif(engine_id.id == daily_utilz.engine4_id.id):
                    hours = daily_utilz.engine4_hours
                    cycles = daily_utilz.engine4_cycles
            elif(part_of == 'A'):
                if(auxiliary_id.id == daily_utilz.auxiliary1_id.id):
                    hours = daily_utilz.auxiliary1_hours
                    cycles = daily_utilz.auxiliary1_cycles
                # elif(auxiliary_id.id == daily_utilz.auxiliary2_id.id):
                #     hours = daily_utilz.auxiliary2_hours
                #     cycles = daily_utilz.auxiliary2_cycles
                # elif(auxiliary_id.id == daily_utilz.auxiliary3_id.id):
                #     hours = daily_utilz.auxiliary3_hours
                #     cycles = daily_utilz.auxiliary3_cycles
                # elif(auxiliary_id.id == daily_utilz.auxiliary4_id.id):
                #     hours = daily_utilz.auxiliary4_hours
                #     cycles = daily_utilz.auxiliary4_cycles
            elif(part_of == 'P'):
                if(propeller_id.id == daily_utilz.propeller1_id.id):
                    hours = daily_utilz.propeller1_hours
                    cycles = daily_utilz.propeller1_cycles
                elif(propeller_id.id == daily_utilz.propeller2_id.id):
                    hours = daily_utilz.propeller2_hours
                    cycles = daily_utilz.propeller2_cycles
                elif(propeller_id.id == daily_utilz.propeller3_id.id):
                    hours = daily_utilz.propeller3_hours
                    cycles = daily_utilz.propeller3_cycles
                elif(propeller_id.id == daily_utilz.propeller4_id.id):
                    hours = daily_utilz.propeller4_hours
                    cycles = daily_utilz.propeller4_cycles

            # print fleet_id.name + ' : ' + str(comp.product_id.name)
            # print part_of
            # print hours
            # print cycles


            if service_life.unit == 'hours' :
                if(hours != 0 and hours != False):
                    if(Remaining > 0):
                        daysRemaining = math.floor( (0-Remaining) / hours)
                        dateDue = datetime.strptime(today.strftime("%Y-%m-%d"), '%Y-%m-%d') - timedelta(days=daysRemaining)
                    else:
                        daysRemaining = math.floor(Remaining / hours)
                        dateDue = datetime.strptime(today.strftime("%Y-%m-%d"), '%Y-%m-%d') + timedelta(days=daysRemaining)
                        # dihiting ngikut FML
                    dateDue = dateDue.strftime("%Y-%m-%d")
                    return dateDue
                else:
                    return False
            elif service_life.unit == 'cycles' :
                if(cycles != 0 and cycles != False):
                    if(Remaining > 0):
                        daysRemaining = math.floor( (0-Remaining) / cycles)
                        dateDue = datetime.strptime(today.strftime("%Y-%m-%d"), '%Y-%m-%d') - timedelta(days=daysRemaining)
                    else:
                        daysRemaining = math.floor(Remaining / cycles)
                        dateDue = datetime.strptime(today.strftime("%Y-%m-%d"), '%Y-%m-%d') + timedelta(days=daysRemaining)
                        # dihiting ngikut FML
                    dateDue = dateDue.strftime("%Y-%m-%d")
                    return dateDue
                else:
                    return False
            elif service_life.unit == 'rin' :
                if(rin != 0 and rin != False):
                    if(Remaining > 0):
                        daysRemaining = math.floor( (0-Remaining) / rin)
                        dateDue = datetime.strptime(today.strftime("%Y-%m-%d"), '%Y-%m-%d') - timedelta(days=daysRemaining)
                    else:
                        daysRemaining = math.floor(Remaining / rin)
                        dateDue = datetime.strptime(today.strftime("%Y-%m-%d"), '%Y-%m-%d') + timedelta(days=daysRemaining)
                        # dihiting ngikut FML
                    dateDue = dateDue.strftime("%Y-%m-%d")
                    return dateDue
                else:
                    return False
            elif service_life.unit in ['year','month','days'] :
                return service_life.next_date

            # for g in self.env['ams.daily'].search([('end_date','>',today.strftime("%Y-%m-%d"))], order="end_date asc"):
            #     if g.start_date > today.strftime("%Y-%m-%d"):
            #         ProjectDays = datetime.strptime(g.end_date, '%Y-%m-%d') - datetime.strptime(g.start_date, '%Y-%m-%d')
            #     else:
            #         ProjectDays = datetime.strptime(g.end_date, '%Y-%m-%d') - datetime.strptime(today.strftime("%Y-%m-%d"), '%Y-%m-%d')
            #     ProjectDays = ProjectDays.days
            #     projectHours = g.aircraft_hours * ProjectDays

            #     if (Remaining - projectHours) <= Target:
            #         daysRemaining = math.floor(Remaining / g.aircraft_hours)
            #         dateDue = datetime.strptime(today.strftime("%Y-%m-%d"), '%Y-%m-%d') + timedelta(days=daysRemaining)
            #         dateDue = dateDue.strftime("%Y-%m-%d")
            #         return dateDue
            #     else : 
            #         Remaining = Remaining - projectHours
            return False

class hour_limit_mdr(models.Model):
    _name = 'hour.limit.mdr'
    _description = 'Hours Limit Group'

    data_source = fields.Selection([('ac','Aircraft'),('en1','Engine 1'),('en2','Engine 2'),('en3','Engine 3'),('en4','Engine 4'),('pr1','Propeller 1'),('pr2','Propeller 2'),('pr3','Propeller 3'),('pr4','Propeller 4'),('aux','Auxiliary')])
    data_type = fields.Selection([('component','Component'),('bulletin','Bulletin'),('inspection','Inspection')])
    fleet_id = fields.Char()
    name = fields.Char()
    part = fields.Char()
    serial = fields.Char()
    ata = fields.Char()
    item = fields.Char()
    service = fields.Char()
    done = fields.Char()
    time = fields.Char()
    remaining = fields.Float(string='Remaining')
    projected_date = fields.Date(string='Projected Date')
    project = fields.Char()
    komen = fields.Text()
    service_id = fields.Many2one('ams.component.servicelife')
    due_at_text = fields.Text(string='Due At Text',compute='_compute_due_at')

    hour_id = fields.Many2one('maintenance.due.report')

    @api.one
    def _compute_due_at(self):
        self.due_at_text = self.service_id.next_text
        # if(self.data_source in ['ac','pr1','pr2','pr3','pr4']):
        #     due_at_text = (self.hour_id.fleet_hours + self.remaining if self.remaining > 0 else self.hour_id.fleet_hours - self.remaining) 
        # elif(self.data_source == 'en1'):
        #     due_at_text = (self.hour_id.engine1_hours + self.remaining if self.remaining > 0 else self.hour_id.engine1_hours - self.remaining)
        # elif(self.data_source == 'en2'):
        #     due_at_text = (self.hour_id.engine2_hours + self.remaining if self.remaining > 0 else self.hour_id.engine2_hours - self.remaining)
        # elif(self.data_source == 'en3'):
        #     due_at_text = (self.hour_id.engine3_hours + self.remaining if self.remaining > 0 else self.hour_id.engine3_hours - self.remaining)
        # elif(self.data_source == 'en4'):
        #     due_at_text = (self.hour_id.engine4_hours + self.remaining if self.remaining > 0 else self.hour_id.engine4_hours - self.remaining)
        # elif(self.data_source == 'aux'):
        #     due_at_text = (self.hour_id.auxiliary1_hours + self.remaining if self.remaining > 0 else self.hour_id.auxiliary1_hours - self.remaining) 
        # due_at_text = str(due_at_text)
        # self.due_at_text = due_at_text.rstrip('0').rstrip('.') if '.' in due_at_text else due_at_text

class cycle_limit_mdr(models.Model):
    _name = 'cycle.limit.mdr'
    _description = 'Cycles Limit Group'

    data_source = fields.Selection([('ac','Aircraft'),('en1','Engine 1'),('en2','Engine 2'),('en3','Engine 3'),('en4','Engine 4'),('pr1','Propeller 1'),('pr2','Propeller 2'),('pr3','Propeller 3'),('pr4','Propeller 4'),('aux','Auxiliary')])
    data_type = fields.Selection([('component','Component'),('bulletin','Bulletin'),('inspection','Inspection')])
    fleet_id = fields.Char()
    name = fields.Char()
    part = fields.Char()
    serial = fields.Char()
    ata = fields.Char()
    item = fields.Char()
    service = fields.Char()
    done = fields.Char()
    time = fields.Char()
    remaining = fields.Float(string='Remaining')
    projected_date = fields.Date(string='Projected Date')
    project = fields.Char()
    komen = fields.Text()
    service_id = fields.Many2one('ams.component.servicelife')
    due_at_text = fields.Text(string='Due At Text',compute='_compute_due_at')

    cycle_id = fields.Many2one('maintenance.due.report')

    @api.one
    def _compute_due_at(self):
        self.due_at_text = self.service_id.next_text
        # if(self.data_source in ['ac','pr1','pr2','pr3','pr4']):
        #     due_at_text = (self.cycle_id.fleet_cycles + self.remaining if self.remaining > 0 else self.cycle_id.fleet_cycles - self.remaining) 
        # elif(self.data_source == 'en1'):
        #     due_at_text = (self.cycle_id.engine1_cycles + self.remaining if self.remaining > 0 else self.cycle_id.engine1_cycles - self.remaining)
        # elif(self.data_source == 'en2'):
        #     due_at_text = (self.cycle_id.engine2_cycles + self.remaining if self.remaining > 0 else self.cycle_id.engine2_cycles - self.remaining)
        # elif(self.data_source == 'en3'):
        #     due_at_text = (self.cycle_id.engine3_cycles + self.remaining if self.remaining > 0 else self.cycle_id.engine3_cycles - self.remaining)
        # elif(self.data_source == 'en4'):
        #     due_at_text = (self.cycle_id.engine4_cycles + self.remaining if self.remaining > 0 else self.cycle_id.engine4_cycles - self.remaining)
        # elif(self.data_source == 'aux'):
        #     due_at_text = (self.cycle_id.auxiliary1_cycles + self.remaining if self.remaining > 0 else self.cycle_id.auxiliary1_cycles - self.remaining)  
        # due_at_text = str(due_at_text)
        # self.due_at_text = due_at_text.rstrip('0').rstrip('.') if '.' in due_at_text else due_at_text

class rin_limit_mdr(models.Model):
    _name = 'rin.limit.mdr'
    _description = 'Rins Limit Group'

    data_source = fields.Selection([('ac','Aircraft'),('en1','Engine 1'),('en2','Engine 2'),('en3','Engine 3'),('en4','Engine 4'),('pr1','Propeller 1'),('pr2','Propeller 2'),('pr3','Propeller 3'),('pr4','Propeller 4'),('aux','Auxiliary')])
    data_type = fields.Selection([('component','Component'),('bulletin','Bulletin'),('inspection','Inspection')])
    fleet_id = fields.Char()
    name = fields.Char()
    part = fields.Char()
    serial = fields.Char()
    ata = fields.Char()
    item = fields.Char()
    service = fields.Char()
    done = fields.Char()
    time = fields.Char()
    remaining = fields.Float(string='Remaining')
    projected_date = fields.Date(string='Projected Date')
    project = fields.Char()
    komen = fields.Text()
    service_id = fields.Many2one('ams.component.servicelife')
    due_at_text = fields.Text(string='Due At Text',compute='_compute_due_at')

    rin_id = fields.Many2one('maintenance.due.report')

    @api.one
    def _compute_due_at(self):
        self.due_at_text = self.service_id.next_text
        # if(self.data_source in ['ac','pr1','pr2','pr3','pr4']):
        #     due_at_text = (self.rin_id.fleet_rins + self.remaining if self.remaining > 0 else self.rin_id.fleet_rins - self.remaining) 
        # elif(self.data_source == 'en1'):
        #     due_at_text = (self.rin_id.engine1_rins + self.remaining if self.remaining > 0 else self.rin_id.engine1_rins - self.remaining)
        # elif(self.data_source == 'en2'):
        #     due_at_text = (self.rin_id.engine2_rins + self.remaining if self.remaining > 0 else self.rin_id.engine2_rins - self.remaining)
        # elif(self.data_source == 'en3'):
        #     due_at_text = (self.rin_id.engine3_rins + self.remaining if self.remaining > 0 else self.rin_id.engine3_rins - self.remaining)
        # elif(self.data_source == 'en4'):
        #     due_at_text = (self.rin_id.engine4_rins + self.remaining if self.remaining > 0 else self.rin_id.engine4_rins - self.remaining)
        # elif(self.data_source == 'aux'):
        #     due_at_text = (self.rin_id.auxiliary1_rins + self.remaining if self.remaining > 0 else self.rin_id.auxiliary1_rins - self.remaining)  
        # due_at_text = str(due_at_text)
        # self.due_at_text = due_at_text.rstrip('0').rstrip('.') if '.' in due_at_text else due_at_text

class calendar_limit_mdr(models.Model):
    _name = 'calendar.limit.mdr'
    _description = 'Calendar Limit Group'

    data_source = fields.Selection([('ac','Aircraft'),('en1','Engine 1'),('en2','Engine 2'),('en3','Engine 3'),('en4','Engine 4'),('pr1','Propeller 1'),('pr2','Propeller 2'),('pr3','Propeller 3'),('pr4','Propeller 4'),('aux','Auxiliary')])
    data_type = fields.Selection([('component','Component'),('bulletin','Bulletin'),('inspection','Inspection')])
    fleet_id = fields.Char()
    name = fields.Char()
    part = fields.Char()
    serial = fields.Char()
    ata = fields.Char()
    item = fields.Char()
    service = fields.Char()
    done = fields.Char()
    time = fields.Char()
    remaining = fields.Float(string='Remaining')
    projected_date = fields.Date(string='Projected Date')
    project = fields.Char()
    komen = fields.Text()
    service_id = fields.Many2one('ams.component.servicelife')
    due_at_text = fields.Text(string='Due At Text',compute='_compute_due_at')

    calendar_id = fields.Many2one('maintenance.due.report')

    @api.one
    def _compute_due_at(self):
        self.due_at_text = self.service_id.next_text
        # if(self.data_source in ['ac','pr1','pr2','pr3','pr4']):
        #     due_at_text = (self.calendar_id.fleet_hours + self.remaining if self.remaining > 0 else self.calendar_id.fleet_hours - self.remaining) 
        # elif(self.data_source == 'en1'):
        #     due_at_text = (self.calendar_id.engine1_hours + self.remaining if self.remaining > 0 else self.calendar_id.engine1_hours - self.remaining)
        # elif(self.data_source == 'en2'):
        #     due_at_text = (self.calendar_id.engine2_hours + self.remaining if self.remaining > 0 else self.calendar_id.engine2_hours - self.remaining)
        # elif(self.data_source == 'en3'):
        #     due_at_text = (self.calendar_id.engine3_hours + self.remaining if self.remaining > 0 else self.calendar_id.engine3_hours - self.remaining)
        # elif(self.data_source == 'en4'):
        #     due_at_text = (self.calendar_id.engine4_hours + self.remaining if self.remaining > 0 else self.calendar_id.engine4_hours - self.remaining)
        # elif(self.data_source == 'aux'):
        #     due_at_text = (self.calendar_id.auxiliary1_hours + self.remaining if self.remaining > 0 else self.calendar_id.auxiliary1_hours - self.remaining) 
        # due_at_text = str(due_at_text)
        # self.due_at_text = due_at_text.rstrip('0').rstrip('.') if '.' in due_at_text else due_at_text

class CertifacateLimitMdr(models.Model):
    _name = "certificate.limit.mdr"
    _discription = "certificate Limit Airframe"

    name = fields.Char()
    fleet_id = fields.Char()
    due_at = fields.Date()
    remain = fields.Char(string="Remaining")
    project_date = fields.Date(string='Projected Date')

    certificate_id = fields.Many2one('maintenance.due.report')
        

class WizardPrintMDR(models.Model):
    _name = 'maintenance.due.report.print'
    _description = 'Print Maintenance Due Report'

    orderby = fields.Selection([('ata','ATA Code'),('part','Component Name'),('projected_date','Project Date'),('remaining','Time Remaining')], string='Order By', default='remaining')

    filter_ata = fields.Char('ATA Filter')
    fill_component = fields.Boolean('Component',default=True)
    fill_inspection = fields.Boolean('Inspection',default=True)
    fill_bulletin = fields.Boolean('Bulletin',default=True)
    states = fields.Selection([('create_by','Draft'),('approved_by','Approved'),('done','QC Confirmed'),('expired','Expired')], related='source_id.states')


    fleet_id = fields.Many2one('aircraft.acquisition', default=lambda self: self._context.get('fleet_id', False), store=True)
    source_id = fields.Many2one('maintenance.due.report',string='ID MDR', default=lambda self: self._context.get('id', False))
    mdr_id  = fields.Integer(default=lambda self: self._context.get('id'))

    hour_limit_id = fields.Many2many('hour.limit.mdr', required=True, compute="_get_hour_filter", ondelete="cascade")
    cycle_limit_id = fields.Many2many('cycle.limit.mdr', required=True, compute="_get_cycle_filter", ondelete="cascade")
    rin_limit_id = fields.Many2many('rin.limit.mdr', required=True, compute="_get_rin_filter", ondelete="cascade")
    calendar_limit_id = fields.Many2many('calendar.limit.mdr', required=True, compute="_get_calendar_filter", ondelete="cascade")
    certificate_limit_id = fields.Many2many('certificate.limit.mdr', required=True, compute="_get_certificate_filter", ondelete="cascade")

    warning_hours = fields.Integer(string="Warning Hours",default=lambda self:self._context.get('hour_limit', False))
    warning_cycles = fields.Integer(string="Warning Cycles",default=lambda self:self._context.get('cycle_limit', False))
    warning_rins = fields.Integer(string="Warning Rin",default=lambda self:self._context.get('rin_limit', False))
    warning_calendars = fields.Date(string="Warning Calendars", default=lambda self:self._context.get('calendar_limit', False))

    last_flight = fields.Date(string='Last Flight',compute='get_lastflight')
    create_by = fields.Many2one('res.partner', default=lambda self:self._context.get('create_by', False))
    approved_by = fields.Many2one('res.partner', default=lambda self:self._context.get('approved_by', False))

    header_html = fields.Html(compute='generate_preview')
    footer_html = fields.Html(compute='generate_preview')

    def generate_preview(self):
        rins, engine, engine2, engine3, engine4 = '', '', '', '', ''
        if self.source_id.fleet_id.rin_active:
            rins = '<div class="col-xs-2">Rins: '+str(self.get_float(self.source_id.fleet_rins))+' </div>'
        else:
            rins = ''
        if self.fleet_id.engine_type_id:
            engine = '<div class="row"><div class="col-xs-3">Engine 1 : '+str(self.fleet_id.engine_type_id.name)+'</div><div class="col-xs-3">Hours : '+(self.get_float(self.source_id.engine1_hours))+'</div><div class="col-xs-6">Cycles : '+(self.get_float(self.source_id.engine1_cycles))+'</div></div>'
        if self.fleet_id.engine2_type_id:
            engine2 = '<div class="row"><div class="col-xs-3">Engine 2 : '+str(self.fleet_id.engine2_type_id.name)+'</div><div class="col-xs-3">Hours : '+(self.get_float(self.source_id.engine2_hours))+'</div><div class="col-xs-6">Cycles : '+(self.get_float(self.source_id.engine2_cycles))+'</div></div>'
        if self.fleet_id.engine3_type_id:
            engine3 = '<div class="row"><div class="col-xs-3">Engine 3 : '+str(self.fleet_id.engine3_type_id.name)+'</div><div class="col-xs-3">Hours : '+(self.get_float(self.source_id.engine3_hours))+'</div><div class="col-xs-6">Cycles : '+(self.get_float(self.source_id.engine3_cycles))+'</div></div>'
        if self.fleet_id.engine4_type_id:
            engine4 = '<div class="row"><div class="col-xs-3">Engine 4 : '+str(self.fleet_id.engine4_type_id.name)+'</div><div class="col-xs-3">Hours : '+(self.get_float(self.source_id.engine4_hours))+'</div><div class="col-xs-6">Cycles : '+(self.get_float(self.source_id.engine4_cycles))+'</div></div>'
        header_html = """
                    <h3 class="text-center">Maintenance Due Report</h3>
                            <div class="row">
                                <div class="col-xs-4">
                                </div>
                                <div class="col-xs-4">
                                    <center>
                                        <h4>PT PELITA AIR SERVICE</h4>
                                    </center>
                                </div>
                                <div class="col-xs-4 text-right">
                                    """+str(self.get_date(0))+"""

                                </div>
                            </div>
                            <div class="row">
                                <div class="col-xs-12 text-center">
                                    Cal. Limits: """+str(self.get_date(self.warning_calendars))+""" ,
                                    Non-Calalendar Limits  Based on: """+str(self.warning_hours)+""" A/C Hrs. ,
                                    """+str(self.warning_cycles)+""" A/C Cyc. ,
                                </div>                                
                            </div>
                            <div class="wrapper" style="padding:2px;border:1px solid black;font-weight:bold">
                                <div class="row">
                                    <div class="col-xs-3">
                                        Airframe: """+str(self.fleet_id.name)+""" 
                                    </div>
                                    <div class="col-xs-3">
                                        Hours: """+str(self.get_float(self.source_id.fleet_hours))+""" 
                                    </div>
                                    <div class="col-xs-2">
                                        Cycles: """+str(self.get_float(self.source_id.fleet_cycles))+"""
                                    </div>
                                    """+str(rins)+"""
                                    <div class="col-xs-2">
                                        Last Flight:
                                            """+str(self.last_flight)+"""
                                    </div>
                                </div>
                                    """+str(engine)+"""
                                    """+str(engine2)+"""
                                    """+str(engine3)+"""
                                    """+str(engine4)+"""
                            </div>
                            """
        footer_html = """
                            <div class="text-center">
                                <ul t-if="not company.custom_footer" class="list-inline">
                                    <t t-set="company" t-value="company.sudo()"/>
                                    <li t-if="company.phone">Phone: <span t-field="company.phone"/></li>

                                    <li t-if="company.fax and company.phone">&amp;bull;</li>
                                    <li t-if="company.fax">Fax: <span t-field="company.fax"/></li>

                                    <li t-if="company.email and company.fax or company.email and company.phone">&amp;bull;</li>
                                    <li t-if="company.email">Email: <span t-field="company.email"/></li>

                                    <li t-if="company.website and company.email or company.website and company.fax or company.website and company.phone">&amp;bull;</li>
                                    <li t-if="company.website">Website: <span t-field="company.website"/></li>
                                </ul>

                                <ul t-if="not company.custom_footer" class="list-inline" name="financial_infos">
                                    <li t-if="company.vat">TIN: <span t-field="company.vat"/></li>
                                </ul>

                                <t t-if="company.custom_footer">
                                    <span t-raw="company.rml_footer"/>
                                </t>
                            </div>
                        """
        self.header_html = header_html
        self.footer_html = footer_html


    def get_float(self, number):
        arr = str(number).split('.')
        if len(arr) >= 2:
            get = str(arr[1])
            numbers = str(number)
            if len(get) != 1:
                numbers = str(number)
            else:
                numbers = str(number)+'0'
            return numbers

    def get_date(self, date):
        if date == 0:
            get = datetime.now().strftime('%d/%m/%Y')
        else:
            get = datetime.strptime(date, '%Y-%m-%d').strftime("%d/%m/%Y")
        return get

    @api.model
    def _get_hour_filter(self):
        search_param = [('hour_id','=',self.mdr_id)]
        if self.hour_limit_id:
            self.hour_limit_id.unlink()
        if self.filter_ata:
            search_param.append(('ata','=', self.filter_ata))
        # if self.fill_component:
        #     search_param.append(('part','!=', False))
        # if self.fill_inspection:
        #     search_param.append(('service','not in', ['','False',' ']))
        # if self.fill_bulletin:
        #     search_param.append(('done','not in', ['','False',' ']))
        if self.fill_component == False:
            search_param.append(('data_type','!=', 'component'))
        if self.fill_bulletin == False:
            search_param.append(('data_type','!=', 'bulletin'))
        if self.fill_inspection == False:
            search_param.append(('data_type','!=', 'inspection'))

        if self.orderby:
            hasil_search = self.env['hour.limit.mdr'].search(search_param, order=self.orderby+" asc")
        else:
            hasil_search = self.env['hour.limit.mdr'].search(search_param)
        self.hour_limit_id = hasil_search

    @api.model
    def _get_cycle_filter(self):
        search_param = [('cycle_id','=',self.mdr_id)]
        if self.cycle_limit_id:
            self.cycle_limit_id.unlink()
        if self.filter_ata:
            search_param.append(('ata','like', self.filter_ata))
        # if self.fill_component:
        #     search_param.append(('part','!=', False))
        # if self.fill_inspection:
        #     search_param.append(('service','not in', ['','False',' ']))
        # if self.fill_bulletin:
        #     search_param.append(('done','not in', ['','False',' ']))

        if self.fill_component == False:
            search_param.append(('data_type','!=', 'component'))
        if self.fill_bulletin == False:
            search_param.append(('data_type','!=', 'bulletin'))
        if self.fill_inspection == False:
            search_param.append(('data_type','!=', 'inspection'))

        if self.orderby:
            hasil_search = self.env['cycle.limit.mdr'].search(search_param, order=self.orderby+" asc")
        else:
            hasil_search = self.env['cycle.limit.mdr'].search(search_param)
        self.cycle_limit_id = hasil_search

    @api.model
    def _get_rin_filter(self):
        search_param = [('rin_id','=',self.mdr_id)]
        if self.rin_limit_id:
            self.rin_limit_id.unlink()
        if self.filter_ata:
            search_param.append(('ata','=', self.filter_ata))
        # if self.fill_component:
        #     search_param.append(('part','!=', False))
        # if self.fill_inspection:
        #     search_param.append(('service','not in', ['','False',' ']))
        # if self.fill_bulletin:
        #     search_param.append(('done','not in', ['','False',' ']))

        if self.fill_component == False:
            search_param.append(('data_type','!=', 'component'))
        if self.fill_bulletin == False:
            search_param.append(('data_type','!=', 'bulletin'))
        if self.fill_inspection == False:
            search_param.append(('data_type','!=', 'inspection'))

        if self.orderby:
            hasil_search = self.env['rin.limit.mdr'].search(search_param, order=self.orderby+" asc")
        else:
            hasil_search = self.env['rin.limit.mdr'].search(search_param)
        self.rin_limit_id = hasil_search

    @api.model
    def _get_calendar_filter(self):
        search_param = [('calendar_id','=',self.mdr_id)]
        if self.calendar_limit_id:
            self.calendar_limit_id.unlink()
        if self.filter_ata:
            search_param.append(('ata','=', self.filter_ata))
        if self.fill_component:
            search_param.append(('part','!=', False))
        if self.fill_inspection:
            search_param.append(('service','not in', ['','False',' ']))
        if self.fill_bulletin:
            search_param.append(('done','not in', ['','False',' ']))
        if self.orderby:
            types = 'desc'
            if(self.orderby in ['ata','part']):
                types = 'asc'
            if(self.orderby == 'remaining'):
                types = 'asc'
                order = 'projected_date'
            else:
                order = self.orderby
            hasil_search = self.env['calendar.limit.mdr'].search(search_param, order=order+" "+types)
        else:
            hasil_search = self.env['calendar.limit.mdr'].search(search_param)
        self.calendar_limit_id = hasil_search

    @api.model
    def _get_certificate_filter(self):
        self.certificate_limit_id = self.env['certificate.limit.mdr'].search([('fleet_id','=', self.fleet_id.name)])

    @api.multi
    def get_lastflight(self):
        for rec in self:
            self.last_flight = rec.fleet_id.last_flight

    @api.multi
    def print_main_due_pdf(self):
        return self.env['report'].get_action(self, 'ams_document.report_maintenance_due_print')
    
    @api.multi
    def print_main_due_with_excel(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'ams_document.report_maintenance_due_print'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        datas['form']['lempar_id_mdr'] = context.get('id')
        if context.get('xls_export'):
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'ams_document.mdr_data_xls.xlsx',
                'datas': datas,
                'name': 'Maintenance Due Report',
                }
    

class PrintXlsx(ReportXlsx):

    def get_datas(self, data):
        id_mdr = data['form']['lempar_id_mdr']
        
        data = self.env['maintenance.due.report.print'].search([('mdr_id','=', id_mdr)], order="id desc", limit=1)
        # hasil recordset seperti di bawah jika tidak diberi limit
        # maintenance.due.report.print(56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83)
        return data

    def generate_xlsx_report(self, workbook, data, lines):
        mdr_data_report = self.get_datas(data)

        format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format11 = workbook.add_format({'font_size': 12, 'align': 'center', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True})
        format21 = workbook.add_format({'font_size': 10, 'align': 'center', 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': True})
        format3 = workbook.add_format({'bottom': True, 'top': True, 'left': True , 'right': True, 'font_size': 12})
        format2 = workbook.add_format({'bottom': True, 'top': False, 'left': True , 'right': True, 'font_size': 12})
        font_size_8 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8})
        red_mark = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8,
                                        'bg_color': 'red'})
        justify = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 12})
        format3.set_align('center')
        format2.set_align('center')
        font_size_8.set_align('center')
        justify.set_align('justify')
        format1.set_align('center')
        red_mark.set_align('center')

        


        list_limits = ['hour_limit_id', 'cycle_limit_id', 'rin_limit_id', 'calendar_limit_id']
        list_field_human_readable = ['Reg/Ser','Name','Part #/Insp.Descript.','Serial','ATA','Item/Pos.','Service Life','Last Done/Installed','Time Remaining','Project Date']
        list_field = ['fleet_id','name','part','serial','ata','item','service','done','time','project']

        # region Limit
        for limit_type in list_limits:
            if len(mdr_data_report[limit_type]) >= 0: #ubah operator menjadi > jika tidak ingin menampilkan header yang tidak memiliki detil sama sekali.
                urut_row_table = 2
                if limit_type == 'hour_limit_id':
                    #worksheet.write(urut_row_table-2, 0, "Hour Limit Group", format1)
                    worksheet_hour_limit = workbook.add_worksheet("Hour Limit Group")
                    worksheet_hour_limit.merge_range('A'+str(urut_row_table-1)+':J'+str(urut_row_table), "Hour Limit Group", format1  )
                    worksheet = worksheet_hour_limit
                if limit_type == 'cycle_limit_id':
                    #worksheet.write(urut_row_table-2, 0, "Cycles Limit Group", format1)
                    worksheet_cycles_limit = workbook.add_worksheet("Cycles Limit Group")
                    worksheet_cycles_limit.merge_range('A'+str(urut_row_table-1)+':J'+str(urut_row_table), "Cycles Limit Group", format1  )
                    worksheet = worksheet_cycles_limit
                if limit_type == 'rin_limit_id':
                    #worksheet.write(urut_row_table-2, 0, "Rins Limit Group", format1)
                    worksheet_rins_limit = workbook.add_worksheet("Rins Limit Group")
                    worksheet_rins_limit.merge_range('A'+str(urut_row_table-1)+':J'+str(urut_row_table), "Rins Limit Group", format1  )
                    worksheet = worksheet_rins_limit
                if limit_type == 'calendar_limit_id':
                    #worksheet.write(urut_row_table-2, 0, "Calendar Limit Group", format1)
                    worksheet_calendar_limit = workbook.add_worksheet("Calendar Limit Group")
                    worksheet_calendar_limit.merge_range('A'+str(urut_row_table-1)+':J'+str(urut_row_table), "Calendar Limit Group", format1  )
                    worksheet = worksheet_calendar_limit

                urut_column = 0
                
                for human_readable_field_header in list_field_human_readable:
                    worksheet.write(urut_row_table, urut_column, human_readable_field_header, format11)
                    urut_column += 1

                # Urut Row diIncrement jika kamu pakai hanya 1 Worksheet.
                # urut_row_table += 1
                urut_row_table += 1
                for limit_item in mdr_data_report[limit_type]:
                    for item in limit_item:
                        urut_column = 0
                        for field in list_field:
                            worksheet.write(urut_row_table, urut_column, item[field], format2)
                            urut_column += 1
                    urut_row_table += 1

                # urut_row_table += 3
        # endregion

PrintXlsx('report.ams_document.mdr_data_xls.xlsx','maintenance.due.report.print')