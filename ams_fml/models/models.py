# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime, timedelta
from odoo import exceptions, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class ams_fml(models.Model):
    _name = 'ams_fml.log'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Char(string="FML Number", required=True, track_visibility="onchange")
    log_id = fields.Many2one('flight.maintenance.log',string='Log Id')
    log_id_text = fields.Char(string='Log Id',related='log_id.name')
    date = fields.Date(string='Date', default=datetime.today(), track_visibility="onchange")
    status = fields.Selection([('unverified','Unverified'),('verified','Verified')],"Status", default="unverified", track_visibility="onchange")

    aircraft_type = fields.Selection(string='Aircraft Type', readonly=True, related="log_id.aircraft_type")
    date_lt = fields.Date('Date (LT)', readonly=True, related="log_id.date_lt")
    etd = fields.Datetime('ETD (Local Time)', readonly=True, related="log_id.etd")
    eta = fields.Datetime('ETA (Local Time)', readonly=True, related="log_id.eta")
    flight_schedule_id = fields.Many2one('flight.schedule','Flight Schedule', readonly=True, related="log_id.flight_schedule_id")
    flight_number = fields.Char('Flight Number', readonly=True, related="log_id.flight_number")
    flight_order_number = fields.Char('Flight Order Number', readonly=True, related="log_id.flight_order_number")
    location_id = fields.Many2one('base.operation', 'Location', readonly=True, related="log_id.location_id")
    customer_id = fields.Many2one('res.partner', string='Customer',readonly=True, related="log_id.customer_id")
    schedule_commercial_id = fields.Many2one('schedule.commercial','Schedule Commercial', readonly=True, related="log_id.schedule_commercial_id")
    flight_category = fields.Selection([('domestic','Domestic'), ('international','International')],'Flight Category',readonly=True, related="log_id.flight_category")
    flight_type = fields.Selection([('commercial','Commercial'), ('noncommercial','Non-Commercial')], string='Flight Type',readonly=True, related="log_id.flight_type")
    internal_flight_type_id = fields.Many2one('internal.flight.type','Internal Flight Type', readonly=True, related="log_id.internal_flight_type_id")
    schedule_date = fields.Date('Schedule Date',readonly=True, related="log_id.schedule_date")

    issued_by   = fields.Many2one('res.users', 'Issued By', readonly=True, default=lambda self:self.env.user.id)
    
    maintenance_rotary_ids = fields.One2many('maintenance.rotary', 'rotary_id', string='Maintenance Rotary',readonly=True, related="log_id.maintenance_rotary_ids")
    maintenance_fixed_ids = fields.One2many('maintenance.fixedwing','fixedwing_id', string='Maintenance Fixed Wing',readonly=True, related="log_id.maintenance_fixed_ids")

    aircraft_id = fields.Many2one('aircraft.acquisition', string='Aircraft Registration', default=lambda self:self._context.get('aircraft_id',False))
    ac_type     = fields.Selection([('fixedwing', 'Fixed Wing'),('rotary', 'Rotary Wing')], related="aircraft_id.category")
    rin_active = fields.Boolean(string='RIN Active',related='aircraft_id.rin_active')
    aircraft_hours = fields.Float(string='Hours', track_visibility="onchange")
    aircraft_cycles = fields.Float(string='Cycles', track_visibility="onchange")
    aircraft_rin = fields.Float(string='RIN', track_visibility="onchange")
    contextable = fields.Float(string='Contextable', store=False, default=lambda self:self._context.get('aircraft_id',False))

    aircraft_comp_ids = fields.One2many('ams_fml.component.airframe','ac_fml_id',string='Aircraft Component', track_visibility="onchange")

    engine1_id = fields.Many2one('engine.type', string='Engine #1')
    engine1_id_text = fields.Char(string='Engine #1',related='engine1_id.name',readonly=True)
    engine1_reason_change  = fields.Boolean(string="Engine Change", default=False)
    engine1_reason  = fields.Text(string="Reason")
    engine1_total_hour  = fields.Float(string="Total Hours", track_visibility="onchange")
    engine1_total_cycle  = fields.Float(string="Total Cycles", track_visibility="onchange")
    engine2_id = fields.Many2one('engine.type', string='Engine #2')
    engine2_id_text = fields.Char(string='Engine #2',related='engine2_id.name',readonly=True)
    engine2_reason_change  = fields.Boolean(string="Engine Change", default=False)
    engine2_reason  = fields.Text(string="Reason")
    engine2_total_hour  = fields.Float(string="Total Hours", track_visibility="onchange")
    engine2_total_cycle  = fields.Float(string="Total Cycles", track_visibility="onchange")
    engine3_id = fields.Many2one('engine.type', string='Engine #3')
    engine3_id_text = fields.Char(string='Engine #3',related='engine3_id.name',readonly=True)
    engine3_reason_change  = fields.Boolean(string="Engine Change", default=False)
    engine3_reason  = fields.Text(string="Reason")
    engine3_total_hour  = fields.Float(string="Total Hours", track_visibility="onchange")
    engine3_total_cycle  = fields.Float(string="Total Cycles", track_visibility="onchange")
    engine4_id = fields.Many2one('engine.type', string='Engine #4')
    engine4_id_text = fields.Char(string='Engine #4',related='engine4_id.name',readonly=True)
    engine4_reason_change  = fields.Boolean(string="Engine Change", default=False)
    engine4_reason  = fields.Text(string="Reason")
    engine4_total_hour  = fields.Float(string="Total Hours", track_visibility="onchange")
    engine4_total_cycle  = fields.Float(string="Total Cycles", track_visibility="onchange")

    auxiliary1_id = fields.Many2one('auxiliary.type', string='Auxiliary #1')
    auxiliary1_id_text = fields.Char(string='Auxiliary #1',related='auxiliary1_id.name',readonly=True)
    # auxiliary2_id = fields.Many2one('auxiliary.type', string='Auxiliary #2')
    # auxiliary2_id_text = fields.Char(string='Auxiliary #2',related='auxiliary2_id.name',readonly=True)
    # auxiliary3_id = fields.Many2one('auxiliary.type', string='Auxiliary #3')
    # auxiliary3_id_text = fields.Char(string='Auxiliary #3',related='auxiliary3_id.name',readonly=True)
    # auxiliary4_id = fields.Many2one('auxiliary.type', string='Auxiliary #4')
    # auxiliary4_id_text = fields.Char(string='Auxiliary #4',related='auxiliary4_id.name',readonly=True)

    propeller1_id = fields.Many2one('propeller.type', string='Propeller #1')
    propeller1_id_text = fields.Char(string='Propeller #1',related='propeller1_id.name',readonly=True)
    propeller2_id = fields.Many2one('propeller.type', string='Propeller #2')
    propeller2_id_text = fields.Char(string='Propeller #2',related='propeller2_id.name',readonly=True)
    propeller3_id = fields.Many2one('propeller.type', string='Propeller #3')
    propeller3_id_text = fields.Char(string='Propeller #3',related='propeller3_id.name',readonly=True)
    propeller4_id = fields.Many2one('propeller.type', string='Propeller #4')
    propeller4_id_text = fields.Char(string='Propeller #4',related='propeller4_id.name',readonly=True)

    engine_comp_text = fields.Text(compute='text_comp_fml')
    auxiliary_comp_text = fields.Text(compute='text_comp_fml')
    propeller_comp_text = fields.Text(compute='text_comp_fml')



    engine1_hours = fields.Float(string='Hours Added', track_visibility="onchange")
    engine1_cycles = fields.Float(string='Cycles Added', track_visibility="onchange")
    engine1_hours_before_flight = fields.Float(string="Hours Before", readonly=True, store=True, track_visibility="onchange")
    engine1_cycles_before_flight = fields.Float(string="Cycles Before", readonly=True, store=True, track_visibility="onchange")
    engine1_hours_added = fields.Float(string="Hours After", compute='text_comp_fml')
    engine1_cycles_added = fields.Float(string="Cycles After", compute='text_comp_fml')
    engine1_power = fields.Float(string='Power Assurance Check', track_visibility="onchange")
    engine1_torque = fields.Float(string='Torque', track_visibility="onchange")
    engine1_comp_ids = fields.One2many('ams_fml.component.airframe','eng1_fml_id',string='Engine #1 Component', track_visibility="onchange")

    engine2_hours = fields.Float(string='Hours Added', track_visibility="onchange")
    engine2_cycles = fields.Float(string='Cycles Added', track_visibility="onchange")
    engine2_hours_before_flight = fields.Float(string="Hours Before", readonly=True, store=True, track_visibility="onchange")
    engine2_cycles_before_flight = fields.Float(string="Cycles Before", readonly=True, store=True, track_visibility="onchange")
    engine2_hours_added = fields.Float(string="Hours After", compute='text_comp_fml')
    engine2_cycles_added = fields.Float(string="Cycles After", compute='text_comp_fml')
    engine2_power = fields.Float(string='Power Assurance Check',store=True, track_visibility="onchange")
    engine2_torque = fields.Float(string='Torque', track_visibility="onchange")
    engine2_comp_ids = fields.One2many('ams_fml.component.airframe','eng2_fml_id',string='Engine #2 Component', track_visibility="onchange")

    engine3_hours = fields.Float(string='Hours Added', track_visibility="onchange")
    engine3_cycles = fields.Float(string='Cycles Added', track_visibility="onchange")
    engine3_hours_before_flight = fields.Float(string="Hours Before", readonly=True, store=True, track_visibility="onchange")
    engine3_cycles_before_flight = fields.Float(string="Cycles Before", readonly=True, store=True, track_visibility="onchange")
    engine3_hours_added = fields.Float(string="Hours After", compute='text_comp_fml')
    engine3_cycles_added = fields.Float(string="Cycles After", compute='text_comp_fml')
    engine3_power = fields.Float(string='Power Assurance Check', track_visibility="onchange")
    engine3_torque = fields.Float(string='Torque', track_visibility="onchange")
    engine3_comp_ids = fields.One2many('ams_fml.component.airframe','eng3_fml_id',string='Engine #3 Component', track_visibility="onchange")

    engine4_hours = fields.Float(string='Hours Added', track_visibility="onchange")
    engine4_cycles = fields.Float(string='Cycles Added', track_visibility="onchange")
    engine4_hours_before_flight = fields.Float(string="Hours Before", readonly=True, store=True, track_visibility="onchange")
    engine4_cycles_before_flight = fields.Float(string="Cycles Before", readonly=True, store=True, track_visibility="onchange")
    engine4_hours_added = fields.Float(string="Hours After", compute='text_comp_fml')
    engine4_cycles_added = fields.Float(string="Cycles After", compute='text_comp_fml')
    engine4_power = fields.Float(string='Power Assurance Check', track_visibility="onchange")
    engine4_torque = fields.Float(string='Torque', track_visibility="onchange")
    engine4_comp_ids = fields.One2many('ams_fml.component.airframe','eng4_fml_id',string='Engine #4 Component', track_visibility="onchange")

    auxiliary1_hours = fields.Float(string='Hours Added', track_visibility="onchange")
    auxiliary1_cycles = fields.Float(string='Cycles Added', track_visibility="onchange")
    auxiliary1_hours_before_flight = fields.Float(string="Hours Before", readonly=True, store=True, track_visibility="onchange")
    auxiliary1_cycles_before_flight = fields.Float(string="Cycles Before", readonly=True, store=True, track_visibility="onchange")
    auxiliary1_hours_added = fields.Float(string="Hours After", compute='text_comp_fml')
    auxiliary1_cycles_added = fields.Float(string="Cycles After", compute='text_comp_fml')
    auxiliary1_comp_ids = fields.One2many('ams_fml.component.airframe','aux1_fml_id',string='Auxiliary #1 Component', track_visibility="onchange")

    propeller1_hours = fields.Float(string='Hours Added', track_visibility="onchange")
    propeller1_cycles = fields.Float(string='Cycles Added', track_visibility="onchange")
    propeller1_hours_before_flight = fields.Float(string="Hours Before",store=True, track_visibility="onchange")
    propeller1_cycles_before_flight = fields.Float(string="Cycles Before",store=True, track_visibility="onchange")
    propeller1_hours_added = fields.Float(string="Hours After", compute='text_comp_fml')
    propeller1_cycles_added = fields.Float(string="Cycles After", compute='text_comp_fml')
    propeller1_comp_ids = fields.One2many('ams_fml.component.airframe','prop1_fml_id',string='Propeller #1 Component', track_visibility="onchange")

    propeller2_hours = fields.Float(string='Hours Added', track_visibility="onchange")
    propeller2_cycles = fields.Float(string='Cycles Added', track_visibility="onchange")
    propeller2_hours_before_flight = fields.Float(string="Hours Before",store=True, track_visibility="onchange")
    propeller2_cycles_before_flight = fields.Float(string="Cycles Before",store=True, track_visibility="onchange")
    propeller2_hours_added = fields.Float(string="Hours After", compute='text_comp_fml')
    propeller2_cycles_added = fields.Float(string="Cycles After", compute='text_comp_fml')
    propeller2_comp_ids = fields.One2many('ams_fml.component.airframe','prop2_fml_id',string='Propeller #2 Component', track_visibility="onchange")

    propeller3_hours = fields.Float(string='Hours Added', track_visibility="onchange")
    propeller3_cycles = fields.Float(string='Cycles Added', track_visibility="onchange")
    propeller3_hours_before_flight = fields.Float(string="Hours Before",store=True, track_visibility="onchange")
    propeller3_cycles_before_flight = fields.Float(string="Cycles Before",store=True, track_visibility="onchange")
    propeller3_hours_added = fields.Float(string="Hours After", compute='text_comp_fml')
    propeller3_cycles_added = fields.Float(string="Cycles After", compute='text_comp_fml')
    propeller3_comp_ids = fields.One2many('ams_fml.component.airframe','prop3_fml_id',string='Propeller #3 Component', track_visibility="onchange")

    propeller4_hours = fields.Float(string='Hours Added', track_visibility="onchange")
    propeller4_cycles = fields.Float(string='Cycles Added', track_visibility="onchange")
    propeller4_hours_before_flight = fields.Float(string="Hours Before",store=True, track_visibility="onchange")
    propeller4_cycles_before_flight = fields.Float(string="Cycles Before",store=True, track_visibility="onchange")
    propeller4_hours_added = fields.Float(string="Hours After", compute='text_comp_fml')
    propeller4_cycles_added = fields.Float(string="Cycles After", compute='text_comp_fml')
    propeller4_comp_ids = fields.One2many('ams_fml.component.airframe','prop4_fml_id',string='Propeller #4 Component', track_visibility="onchange")

    current_aircraft_hours = fields.Float(string='Aircraft Hours')
    current_aircraft_cycles = fields.Float(string='Aircraft Cycles')
    current_aircraft_rin = fields.Float(string='Aircraft RIN')
    current_engine1_hours = fields.Float(string='Hours')
    current_engine1_cycles = fields.Float(string='Cycles')
    current_engine1_rin = fields.Float(string='RIN')
    current_engine2_hours = fields.Float(string='Hours')
    current_engine2_cycles = fields.Float(string='Cycles')
    current_engine2_rin = fields.Float(string='RIN')
    current_engine3_hours = fields.Float(string='Hours')
    current_engine3_cycles = fields.Float(string='Cycles')
    current_engine3_rin = fields.Float(string='RIN')
    current_engine4_hours = fields.Float(string='Hours')
    current_engine4_cycles = fields.Float(string='Cycles')
    current_engine4_rin = fields.Float(string='RIN')
    current_auxiliary1_hours = fields.Float(string='Hours')
    current_auxiliary1_cycles = fields.Float(string='Cycles')
    current_auxiliary1_rin = fields.Float(string='RIN')
    current_propeller1_hours = fields.Float(string='Hours')
    current_propeller1_cycles = fields.Float(string='Cycles')
    current_propeller1_rin = fields.Float(string='RIN')
    current_propeller2_hours = fields.Float(string='Hours')
    current_propeller2_cycles = fields.Float(string='Cycles')
    current_propeller2_rin = fields.Float(string='RIN')
    current_propeller3_hours = fields.Float(string='Hours')
    current_propeller3_cycles = fields.Float(string='Cycles')
    current_propeller3_rin = fields.Float(string='RIN')
    current_propeller4_hours = fields.Float(string='Hours')
    current_propeller4_cycles = fields.Float(string='Cycles')
    current_propeller4_rin = fields.Float(string='RIN')
    total_hours = fields.Float(track_visibility="onchange")
    total_cycles = fields.Float(track_visibility="onchange")
    total_after_hours = fields.Float(compute='text_comp_fml')
    total_after_cycles = fields.Float(compute='text_comp_fml')

    discard_btn = fields.Boolean('Discard')

    @api.one
    def text_comp_fml(self):
        engine = ""
        if self.engine1_id:
            engine += "1. "+str(self.engine1_id_text)+" = "+str(self.engine1_hours)+"/"+str(self.engine1_cycles)+"<br/>"
        if self.engine2_id:
            engine += "2. "+str(self.engine2_id_text)+" = "+str(self.engine2_hours)+"/"+str(self.engine2_cycles)+"<br/>"
        if self.engine3_id:
            engine += "3. "+str(self.engine3_id_text)+" = "+str(self.engine3_hours)+"/"+str(self.engine3_cycles)+"<br/>"
        if self.engine4_id:
            engine += "4. "+str(self.engine4_id_text)+" = "+str(self.engine4_hours)+"/"+str(self.engine4_cycles)+"<br/>"

        auxiliary = ""
        if self.auxiliary1_id:
            auxiliary += str(self.auxiliary1_id_text)+" = "+str(self.auxiliary1_hours)+"/"+str(self.auxiliary1_cycles)+"<br/>"
            
        propeller = ""
        if self.propeller1_id:
            propeller += str(self.propeller1_id_text)+" = "+str(self.propeller1_id.total_hours)+"/"+str(self.propeller1_id.total_cycles)+"<br/>"
        if self.propeller2_id:
            propeller += str(self.propeller2_id_text)+" = "+str(self.propeller2_id.total_hours)+"/"+str(self.propeller2_id.total_cycles)+"<br/>"
        if self.propeller3_id:
            propeller += str(self.propeller3_id_text)+" = "+str(self.propeller3_id.total_hours)+"/"+str(self.propeller3_id.total_cycles)+"<br/>"
        if self.propeller4_id:
            propeller += str(self.propeller4_id_text)+" = "+str(self.propeller4_id.total_hours)+"/"+str(self.propeller4_id.total_cycles)+"<br/>"

        self.total_after_hours = self.total_hours + self.aircraft_hours
        self.total_after_cycles = self.total_cycles + self.aircraft_cycles

        self.engine1_hours_added = self.engine1_hours_before_flight + self.engine1_hours
        self.engine1_cycles_added = self.engine1_cycles_before_flight + self.engine1_cycles
        self.engine2_hours_added = self.engine2_hours_before_flight + self.engine2_hours
        self.engine2_cycles_added = self.engine2_cycles_before_flight + self.engine2_cycles
        self.engine3_hours_added = self.engine3_hours_before_flight + self.engine3_hours
        self.engine3_cycles_added = self.engine3_cycles_before_flight + self.engine3_cycles
        self.engine4_hours_added = self.engine4_hours_before_flight + self.engine4_hours
        self.engine4_cycles_added = self.engine4_cycles_before_flight + self.engine4_cycles
        self.auxiliary1_hours_added = self.auxiliary1_hours_before_flight + self.auxiliary1_hours
        self.auxiliary1_cycles_added = self.auxiliary1_cycles_before_flight + self.auxiliary1_cycles
        self.propeller1_hours_added = self.propeller1_hours_before_flight + self.propeller1_hours
        self.propeller1_cycles_added = self.propeller1_cycles_before_flight + self.propeller1_cycles
        self.propeller2_hours_added = self.propeller2_hours_before_flight + self.propeller2_hours
        self.propeller2_cycles_added = self.propeller2_cycles_before_flight + self.propeller2_cycles
        self.propeller3_hours_added = self.propeller3_hours_before_flight + self.propeller3_hours
        self.propeller3_cycles_added = self.propeller3_cycles_before_flight + self.propeller3_cycles
        self.propeller4_hours_added = self.propeller4_hours_before_flight + self.propeller4_hours
        self.propeller4_cycles_added = self.propeller4_cycles_before_flight + self.propeller4_cycles

        self.engine_comp_text = engine
        self.auxiliary_comp_text = auxiliary
        self.propeller_comp_text = propeller


    @api.model
    def get_menuId(self, name=''):
        menu_id = False

        if name not in [False,'',""]:
            menu_id = self.env['ir.ui.menu'].search([('name','ilike',name)], limit=1)
            if menu_id:
                return {'menu_id':menu_id.id, 'actions': menu_id.action.id}
            else:
                return {'menu_id':False, 'actions': False}
                # return None
        else:
            return {'menu_id':False, 'actions': False}
            # return None

    @api.multi
    @api.constrains('name')
    def _check_fml_number(self):
        for record in self:
            obj = self.search([('name','=', record.name),('id', '!=', record.id)])
            if obj:
                raise exceptions.except_orm(_("Fml Number: %s already exist" % record.name))


    @api.multi
    def change_status(self):
        if self.issued_by.id != self.env.user.id:
            self.status = 'verified'
        else:
            raise exceptions.except_orm(_('Attention!'), _("You can't verify your own fml. Please let other verify for you"))

    @api.onchange('engine1_id')
    def _engine1_change(self):
        # if self.id:
        #     current_id  = self.env['ams_fml.log'].search([('id', '=', self._origin.id)])
        #     if self.engine1_id.id != current_id.engine1_id.id:
        #         self.engine1_reason_change = True
        #     else:
        #         self.engine1_reason_change = False
        if not self.id:
            if self.engine1_id:
                self.engine1_hours_before_flight = self.engine1_id.engine_tsn
                self.engine1_cycles_before_flight = self.engine1_id.engine_csn

    @api.onchange('engine2_id')
    def _engine2_change(self):
        # if self.id:
        #     current_id  = self.env['ams_fml.log'].search([('id', '=', self._origin.id)])
        #     if self.engine2_id.id != current_id.engine2_id.id:
        #         self.engine2_reason_change = True
        #     else:
        #         self.engine2_reason_change = False
        if not self.id:
            if self.engine2_id:
                self.engine2_hours_before_flight = self.engine2_id.engine_tsn
                self.engine2_cycles_before_flight = self.engine2_id.engine_csn

    @api.onchange('engine3_id')
    def _engine3_change(self):
        # if self.id:
        #     current_id  = self.env['ams_fml.log'].search([('id', '=', self._origin.id)])
        #     if self.engine3_id.id != current_id.engine3_id.id:
        #         self.engine3_reason_change = True
        #     else:
        #         self.engine3_reason_change = False
        if not self.id:
            if self.engine3_id:
                self.engine3_hours_before_flight = self.engine3_id.engine_tsn
                self.engine3_cycles_before_flight = self.engine3_id.engine_csn

    @api.onchange('engine4_id')
    def _engine4_change(self):
        # if self.id:
        #     current_id  = self.env['ams_fml.log'].search([('id', '=', self._origin.id)])
        #     if self.engine4_id.id != current_id.engine4_id.id:
        #         self.engine4_reason_change = True
        #     else:
        #         self.engine4_reason_change = False
        if not self.id:
            if self.engine4_id:
                self.engine4_hours_before_flight = self.engine4_id.engine_tsn
                self.engine4_cycles_before_flight = self.engine4_id.engine_csn

    @api.onchange('propeller1_id')
    def _propeller1_change(self):
        if self.propeller1_id:
            self.propeller1_hours_before_flight = self.propeller1_id.propeller_tsn
            self.propeller1_cycles_before_flight = self.propeller1_id.propeller_csn

    @api.onchange('propeller2_id')
    def _propeller2_change(self):
        if self.propeller2_id:
            self.propeller2_hours_before_flight = self.propeller2_id.propeller_tsn
            self.propeller2_cycles_before_flight = self.propeller2_id.propeller_csn

    @api.onchange('propeller3_id')
    def _propeller3_change(self):
        if self.propeller3_id:
            self.propeller3_hours_before_flight = self.propeller3_id.propeller_tsn
            self.propeller3_cycles_before_flight = self.propeller3_id.propeller_csn

    @api.onchange('propeller4_id')
    def _propeller4_change(self):
        if self.propeller4_id:
            self.propeller4_hours_before_flight = self.propeller4_id.propeller_tsn
            self.propeller4_cycles_before_flight = self.propeller4_id.propeller_csn

    @api.onchange('auxiliary1_id')
    def _auxiliary1_change(self):
        if not self.id:
            if self.auxiliary1_id:
                self.auxiliary1_hours_before_flight = self.auxiliary1_id.auxiliary_tsn
                self.auxiliary1_cycles_before_flight = self.auxiliary1_id.auxiliary_csn

    @api.one
    def copy(self, default=None):
        default = dict(default or {})
        default.update({
         'name': '0000',
        })
        return super(ams_fml, self).copy(default)

    @api.model
    def _gi_count_component(self,comp,hours,cycles,rin):
        findcomp = self.env['ams.component.part'].search([('id','=',comp)])
        wdict = {
            'tsn' : findcomp.tsn + hours,
            'csn' : findcomp.csn + cycles,
            'rsn' : findcomp.rsn + rin,
            'tso' : findcomp.tso + hours,
            'cso' : findcomp.cso + cycles,
            'rso' : findcomp.rso + rin,
            }
        if(findcomp.serial_number != False):
            findser = self.env['stock.production.lot'].search([('id','=',findcomp.serial_number.id)])
            findser.write({
                'tsn' : findcomp.tsn + hours,
                'csn' : findcomp.csn + cycles,
                'rsn' : findcomp.rsn + rin,
                'tso' : findcomp.tso + hours,
                'cso' : findcomp.cso + cycles,
                'rso' : findcomp.rso + rin,
            })
        findcomp.write(wdict)
        # component service life Hours
        slife = self.env['ams.component.servicelife'].search([('part_id','=',comp)])
        for g in slife:
            i = self.env['ams.component.servicelife'].search([('id','=',g.id)])
            if(g.unit == 'hours'):
                i.write({
                    'current' : i.current + hours,
                    'remaining' : i.remaining - hours,
                })
            elif(g.unit == 'cycles'):
                i.write({
                    'current' : i.current + cycles,
                    'remaining' : i.remaining - cycles,
                })
            elif(g.unit == 'rin'):
                i.write({
                    'current' : i.current + rin,
                    'remaining' : i.remaining - rin,
                })



    @api.onchange('name')
    def _onchange_name(self):
        idlog = self.env['flight.maintenance.log'].search([('name', '=', self.name )])
        if(idlog):
            self.log_id = idlog
            self.aircraft_id = self.log_id.fl_acquisition_id.id
            self.date = self.log_id.schedule_date
            # count otomatis hours & cycles
            hour = 0
            cycle = 0
            if(self.aircraft_type == 'fixedwing'):
                for g in self.maintenance_fixed_ids:
                    hour = hour + g.flight_hour_matrix
                    cycle = cycle + 2

            else:
                for g in self.maintenance_rotary_ids:
                    hour = hour + g.block_matrix
                    cycle = cycle + g.cycle_start1
                    cycle = cycle + g.cycle_start2

            self.aircraft_hours = hour
            self.aircraft_cycles = cycle

        else:
            self.log_id = False
            # self.aircraft_id = False
            
    @api.onchange('aircraft_hours')
    def _onchange_aircraft_hours(self):
        # Set Hours After
        self.total_after_hours = float(self.total_hours) + float(self.aircraft_hours)
        # SET ENGINE HOURS
        if(self.engine1_id):
            self.engine1_hours = self.aircraft_hours
        else:
            self.engine1_hours = 0

        if(self.engine2_id):
            self.engine2_hours = self.aircraft_hours
        else:
            self.engine2_hours = 0

        if(self.engine3_id):
            self.engine3_hours = self.aircraft_hours
        else:
            self.engine3_hours = 0

        if(self.engine4_id):
            self.engine4_hours = self.aircraft_hours
        else:
            self.engine4_hours = 0

        # SET PROPELLER HOURS
        if(self.propeller1_id):
            self.propeller1_hours = self.aircraft_hours
        else:
            self.propeller1_hours = 0

        if(self.propeller2_id):
            self.propeller2_hours = self.aircraft_hours
        else:
            self.propeller2_hours = 0

        if(self.propeller3_id):
            self.propeller3_hours = self.aircraft_hours
        else:
            self.propeller3_hours = 0

        if(self.propeller4_id):
            self.propeller4_hours = self.aircraft_hours
        else:
            self.propeller4_hours = 0

        # SET AUXILIARY HOURS
        if(self.auxiliary1_id):
            self.auxiliary1_hours = self.aircraft_hours
        else:
            self.auxiliary1_hours = 0

        # AIRFRAME COMPONENT
        for comp in self.aircraft_comp_ids:
            comp.hours = self.aircraft_hours

    @api.onchange('aircraft_cycles')
    def _onchange_aircraft_cycles(self):
        # Set Cycles After
        self.total_after_cycles = float(self.total_cycles) + float(self.aircraft_cycles)
        # SET ENGINE cycles
        if(self.engine1_id):
            self.engine1_cycles = self.aircraft_cycles
        else:
            self.engine1_cycles = 0

        if(self.engine2_id):
            self.engine2_cycles = self.aircraft_cycles
        else:
            self.engine2_cycles = 0

        if(self.engine3_id):
            self.engine3_cycles = self.aircraft_cycles
        else:
            self.engine3_cycles = 0

        if(self.engine4_id):
            self.engine4_cycles = self.aircraft_cycles
        else:
            self.engine4_cycles = 0

        # SET PROPELLER cycles
        if(self.propeller1_id):
            self.propeller1_cycles = self.aircraft_cycles
        else:
            self.propeller1_cycles = 0

        if(self.propeller2_id):
            self.propeller2_cycles = self.aircraft_cycles
        else:
            self.propeller2_cycles = 0

        if(self.propeller3_id):
            self.propeller3_cycles = self.aircraft_cycles
        else:
            self.propeller3_cycles = 0

        if(self.propeller4_id):
            self.propeller4_cycles = self.aircraft_cycles
        else:
            self.propeller4_cycles = 0

        # SET AUXILIARY cycles
        if(self.auxiliary1_id):
            self.auxiliary1_cycles = self.aircraft_cycles
        else:
            self.auxiliary1_cycles = 0

        # AIRFRAME COMPONENT
        for comp in self.aircraft_comp_ids:
            comp.cycles = self.aircraft_cycles
            comp.cycles_before = comp.component_id.csn

    @api.onchange('aircraft_id')
    def _onchange_aircraft_id(self):
        if self.aircraft_id:
            _logger.warning(self.ac_type)
            if(not self.id):
                self.total_hours = self.aircraft_id.total_hours
                self.total_cycles = self.aircraft_id.total_landings

            fml = self.env['ams_fml.log'].search([('aircraft_id','=', self.aircraft_id.id)], limit=1, order="create_date DESC")
            self.aircraft_hours = fml.aircraft_hours
            self.aircraft_cycles = fml.aircraft_cycles

        
        if not (self.id):
            idlog = self.env['flight.maintenance.log'].search([('name', '=', self.name )])
            self.engine1_id = self.aircraft_id.engine_type_id
            self.engine2_id = self.aircraft_id.engine2_type_id
            self.engine3_id = self.aircraft_id.engine3_type_id
            self.engine4_id = self.aircraft_id.engine4_type_id

            self.auxiliary1_id = self.aircraft_id.auxiliary_type_id
            # self.auxiliary2_id = self.aircraft_id.auxiliary2_type_id
            # self.auxiliary3_id = self.aircraft_id.auxiliary3_type_id
            # self.auxiliary4_id = self.aircraft_id.auxiliary4_type_id

            self.propeller1_id = self.aircraft_id.propeller_type_id
            self.propeller2_id = self.aircraft_id.propeller2_type_id
            self.propeller3_id = self.aircraft_id.propeller3_type_id
            self.propeller4_id = self.aircraft_id.propeller4_type_id

            if(not idlog):
                self.aircraft_hours = 0
                self.aircraft_cycles = 0
            # GET AIRCRAFT COMPONENT

            self._onchange_aircraft_hours()
            self._onchange_aircraft_cycles()
            self._onchange_engine1_hours()
            self._onchange_engine1_cycles()
            self._onchange_engine2_hours()
            self._onchange_engine2_cycles()
            self._onchange_engine3_hours()
            self._onchange_engine3_cycles()
            self._onchange_engine4_hours()
            self._onchange_engine4_cycles()
            self._onchange_propeller1_hours()
            self._onchange_propeller1_cycles()
            self._onchange_propeller2_hours()
            self._onchange_propeller2_cycles()
            self._onchange_propeller3_hours()
            self._onchange_propeller3_cycles()
            self._onchange_propeller4_hours()
            self._onchange_propeller4_cycles()
            self._onchange_auxiliary1_hours()
            self._onchange_auxiliary1_cycles()

            specomp = []
            for comp in self.aircraft_id.component_ids:
                if(comp.not_follow_parent):
                    specomp.append((0, 0,{
                        # 'fml_id': self.id,
                        'component_id': comp.id,
                        'hours': self.aircraft_hours,
                        'cycles': self.aircraft_cycles,
                    }))
                for scomp in comp.sub_part_ids:
                    if(scomp.not_follow_parent):
                        specomp.append((0, 0,{
                            # 'fml_id': self.id,
                            'component_id': scomp.id,
                            'hours': self.aircraft_hours,
                            'cycles': self.aircraft_cycles,
                        }))
            self.aircraft_comp_ids = specomp
            # GET ENGINE COMPONENT
            for eng_loop in xrange(1,4):
                if(eng_loop == 1):
                    comp_ids = self.engine1_id.component_ids
                elif(eng_loop == 2):
                    comp_ids = self.engine2_id.component_ids
                elif(eng_loop == 3):
                    comp_ids = self.engine3_id.component_ids
                elif(eng_loop == 4):
                    comp_ids = self.engine4_id.component_ids
                specomp = []
                for comp in comp_ids:
                    if(comp.not_follow_parent):
                        specomp.append((0, 0,{
                            # 'fml_id': self.id,
                            'component_id': comp.id,
                            'hours': self.aircraft_hours,
                            'cycles': self.aircraft_cycles,
                        }))
                    for scomp in comp.sub_part_ids:
                        if(scomp.not_follow_parent):
                            specomp.append((0, 0,{
                                # 'fml_id': self.id,
                                'component_id': scomp.id,
                                'hours': self.aircraft_hours,
                                'cycles': self.aircraft_cycles,
                            }))
                if(eng_loop == 1):
                    self.engine1_comp_ids = specomp
                elif(eng_loop == 2):
                    self.engine2_comp_ids = specomp
                elif(eng_loop == 3):
                    self.engine3_comp_ids = specomp
                elif(eng_loop == 4):
                    self.engine4_comp_ids = specomp
            # GET PROPELLER COMPONENT
            for prop_loop in xrange(1,4):
                if(prop_loop == 1):
                    comp_ids = self.propeller1_id.component_ids
                elif(prop_loop == 2):
                    comp_ids = self.propeller2_id.component_ids
                elif(prop_loop == 3):
                    comp_ids = self.propeller3_id.component_ids
                elif(prop_loop == 4):
                    comp_ids = self.propeller4_id.component_ids
                specomp = []
                for comp in comp_ids:
                    if(comp.not_follow_parent):
                        specomp.append((0, 0,{
                            # 'fml_id': self.id,
                            'component_id': comp.id,
                            'hours': self.aircraft_hours,
                            'cycles': self.aircraft_cycles,
                        }))
                    for scomp in comp.sub_part_ids:
                        if(scomp.not_follow_parent):
                            specomp.append((0, 0,{
                                # 'fml_id': self.id,
                                'component_id': scomp.id,
                                'hours': self.aircraft_hours,
                                'cycles': self.aircraft_cycles,
                            }))
                if(prop_loop == 1):
                    self.propeller1_comp_ids = specomp
                elif(prop_loop == 2):
                    self.propeller2_comp_ids = specomp
                elif(prop_loop == 3):
                    self.propeller3_comp_ids = specomp
                elif(prop_loop == 4):
                    self.propeller4_comp_ids = specomp
            # GET AUXILIARY 1 COMPONENT
            specomp = []
            for comp in self.auxiliary1_id.component_ids:
                if(comp.not_follow_parent):
                    specomp.append((0, 0,{
                        # 'fml_id': self.id,
                        'component_id': comp.id,
                        'hours': self.aircraft_hours,
                        'cycles': self.aircraft_cycles,
                    }))
                for scomp in comp.sub_part_ids:
                    if(scomp.not_follow_parent):
                        specomp.append((0, 0,{
                            # 'fml_id': self.id,
                            'component_id': scomp.id,
                            'hours': self.aircraft_hours,
                            'cycles': self.aircraft_cycles,
                        }))
            self.auxiliary1_comp_ids = specomp

    @api.onchange('engine1_hours')
    def _onchange_engine1_hours(self):
        # 
        self.engine1_hours_added = float(self.engine1_hours_before_flight) + float(self.engine1_hours)
        for comp in self.engine1_comp_ids:
            comp.hours = self.engine1_hours

    @api.onchange('engine1_cycles')
    def _onchange_engine1_cycles(self):
        # 
        self.engine1_cycles_added = float(self.engine1_cycles_before_flight) + float(self.engine1_cycles)
        for comp in self.engine1_comp_ids:
            comp.cycles = self.engine1_cycles
            comp.cycles_before = comp.component_id.csn

    @api.onchange('engine2_hours')
    def _onchange_engine2_hours(self):
        # 
        self.engine2_hours_added = float(self.engine2_hours_before_flight) + float(self.engine2_hours)
        for comp in self.engine2_comp_ids:
            comp.hours = self.engine2_hours

    @api.onchange('engine2_cycles')
    def _onchange_engine2_cycles(self):
        # 
        self.engine2_cycles_added = float(self.engine2_cycles_before_flight) + float(self.engine2_cycles)
        for comp in self.engine2_comp_ids:
            comp.cycles = self.engine2_cycles
            comp.cycles_before = comp.component_id.csn

    @api.onchange('engine3_hours')
    def _onchange_engine3_hours(self):
        # 
        self.engine3_hours_added = float(self.engine3_hours_before_flight) + float(self.engine3_hours)
        for comp in self.engine3_comp_ids:
            comp.hours = self.engine3_hours

    @api.onchange('engine3_cycles')
    def _onchange_engine3_cycles(self):
        # 
        self.engine3_cycles_added = float(self.engine3_cycles_before_flight) + float(self.engine3_cycles)
        for comp in self.engine3_comp_ids:
            comp.cycles = self.engine3_cycles
            comp.cycles_before = comp.component_id.csn

    @api.onchange('engine4_hours')
    def _onchange_engine4_hours(self):
        # 
        self.engine4_hours_added = float(self.engine4_hours_before_flight) + float(self.engine4_hours)
        for comp in self.engine4_comp_ids:
            comp.hours = self.engine4_hours

    @api.onchange('engine4_cycles')
    def _onchange_engine4_cycles(self):
        # 
        self.engine4_cycles_added = float(self.engine4_cycles_before_flight) + float(self.engine4_cycles)
        for comp in self.engine4_comp_ids:
            comp.cycles = self.engine4_cycles
            comp.cycles_before = comp.component_id.csn

    @api.onchange('propeller1_hours')
    def _onchange_propeller1_hours(self):
        # 
        self.propeller1_hours_added = float(self.propeller1_hours_before_flight) + float(self.propeller1_hours)
        for comp in self.propeller1_comp_ids:
            comp.hours = self.propeller1_hours

    @api.onchange('propeller1_cycles')
    def _onchange_propeller1_cycles(self):
        # 
        self.propeller1_cycles_added = float(self.propeller1_cycles_before_flight) + float(self.propeller1_cycles)
        for comp in self.propeller1_comp_ids:
            comp.cycles = self.propeller1_cycles
            self.cycles_before = comp.component_id.csn

    @api.onchange('propeller2_hours')
    def _onchange_propeller2_hours(self):
        # 
        self.propeller2_hours_added = float(self.propeller2_hours_before_flight) + float(self.propeller2_hours)
        for comp in self.propeller2_comp_ids:
            comp.hours = self.propeller2_hours

    @api.onchange('propeller2_cycles')
    def _onchange_propeller2_cycles(self):
        # 
        self.propeller2_cycles_added = float(self.propeller2_cycles_before_flight) + float(self.propeller2_cycles)
        for comp in self.propeller2_comp_ids:
            comp.cycles = self.propeller2_cycles
            self.cycles_before = comp.component_id.csn

    @api.onchange('propeller3_hours')
    def _onchange_propeller3_hours(self):
        # 
        self.propeller3_hours_added = float(self.propeller3_hours_before_flight) + float(self.propeller3_hours)
        for comp in self.propeller3_comp_ids:
            comp.hours = self.propeller3_hours

    @api.onchange('propeller3_cycles')
    def _onchange_propeller3_cycles(self):
        # 
        self.propeller3_cycles_added = float(self.propeller3_cycles_before_flight) + float(self.propeller3_cycles)
        for comp in self.propeller3_comp_ids:
            comp.cycles = self.propeller3_cycles
            self.cycles_before = comp.component_id.csn

    @api.onchange('propeller4_hours')
    def _onchange_propeller4_hours(self):
        # 
        self.propeller4_hours_added = float(self.propeller4_hours_before_flight) + float(self.propeller4_hours)
        for comp in self.propeller4_comp_ids:
            comp.hours = self.propeller4_hours

    @api.onchange('propeller4_cycles')
    def _onchange_propeller4_cycles(self):
        # 
        self.propeller4_cycles_added = float(self.propeller4_cycles_before_flight) + float(self.propeller4_cycles)
        for comp in self.propeller4_comp_ids:
            comp.cycles = self.propeller4_cycles
            self.cycles_before = comp.component_id.csn

    @api.onchange('auxiliary1_hours')
    def _onchange_auxiliary1_hours(self):
        # 
        self.auxiliary1_hours_added = float(self.auxiliary1_hours_before_flight) + float(self.auxiliary1_hours)
        for comp in self.auxiliary1_comp_ids:
            comp.hours = self.auxiliary1_hours

    @api.onchange('auxiliary1_cycles')
    def _onchange_auxiliary1_cycles(self):
        # 
        self.auxiliary1_cycles_added = float(self.auxiliary1_cycles_before_flight) + float(self.auxiliary1_cycles)
        for comp in self.auxiliary1_comp_ids:
            comp.cycles = self.auxiliary1_cycles
            self.cycles_before = comp.component_id.csn
    

    # PADA SAAT SAVE
    @api.multi
    def write(self, vals):
        user = self.env['res.users'].browse(self.env.uid)
        authorization_update_name_date = user.has_group('ams_security.group_edit_fml_log_log_name_date_approved')
        if ('name' in vals):    
            if authorization_update_name_date == False:
                raise UserError(('Butuh Autorisasi untuk mengedit field FML Number.\nMohon menghubungi System Administrator.'))
        elif ('date' in vals):    
            if authorization_update_name_date == False:
                raise UserError(('Butuh Autorisasi untuk mengedit field Date.\nMohon menghubungi System Administrator.'))

        # KURANG SPECIAL COMPONENT
        gin = {}
        rec = self.env['ams_fml.log'].search([('id','=',self.id)])
        vals['aircraft_id'] = rec.aircraft_id.id
        vals['engine1_id'] = rec.engine1_id.id
        vals['engine2_id'] = rec.engine2_id.id
        vals['engine3_id'] = rec.engine3_id.id
        vals['engine4_id'] = rec.engine4_id.id
        vals['auxiliary1_id'] = rec.auxiliary1_id.id
        vals['propeller1_id'] = rec.propeller1_id.id
        vals['propeller2_id'] = rec.propeller2_id.id
        vals['propeller3_id'] = rec.propeller3_id.id
        vals['propeller4_id'] = rec.propeller4_id.id

        vals['propeller1_cycles'] = vals['aircraft_cycles']
        vals['propeller2_cycles'] = vals['aircraft_cycles']
        vals['propeller3_cycles'] = vals['aircraft_cycles']
        vals['propeller4_cycles'] = vals['aircraft_cycles']

        gin['aircraft_id'] = rec.aircraft_id.id
        gin['engine1_id'] = rec.engine1_id.id
        gin['engine2_id'] = rec.engine2_id.id
        gin['engine3_id'] = rec.engine3_id.id
        gin['engine4_id'] = rec.engine4_id.id
        gin['auxiliary1_id'] = rec.auxiliary1_id.id
        gin['propeller1_id'] = rec.propeller1_id.id
        gin['propeller2_id'] = rec.propeller2_id.id
        gin['propeller3_id'] = rec.propeller3_id.id
        gin['propeller4_id'] = rec.propeller4_id.id
        gin['aircraft_comp_ids'] = []
        gin['engine1_comp_ids'] = []
        gin['engine2_comp_ids'] = []
        gin['engine3_comp_ids'] = []
        gin['engine4_comp_ids'] = []
        gin['auxiliary1_comp_ids'] = []
        gin['propeller1_comp_ids'] = []
        gin['propeller2_comp_ids'] = []
        gin['propeller3_comp_ids'] = []
        gin['propeller4_comp_ids'] = []


        acraft = self.env['aircraft.acquisition'].search([('id','=',gin['aircraft_id'])])

        if 'aircraft_hours' in vals:
            gin['aircraft_hours'] = vals['aircraft_hours'] - rec.aircraft_hours
        else:
            gin['aircraft_hours'] = False
        if 'aircraft_cycles' in vals:
            gin['aircraft_cycles'] = vals['aircraft_cycles'] - rec.aircraft_cycles
        else:
            gin['aircraft_cycles'] = False
        if 'aircraft_rin' in vals:
            gin['aircraft_rin'] = vals['aircraft_rin'] - rec.aircraft_rin
        else:
            gin['aircraft_rin'] = False

        if 'engine1_hours' in vals:
            gin['engine1_hours'] = vals['engine1_hours'] - rec.engine1_hours
        else:
            gin['engine1_hours'] = False
        if 'engine1_cycles' in vals:
            gin['engine1_cycles'] = vals['engine1_cycles'] - rec.engine1_cycles
        else:
            gin['engine1_cycles'] = False
        if 'engine2_hours' in vals:
            gin['engine2_hours'] = vals['engine2_hours'] - rec.engine2_hours
        else:
            gin['engine2_hours'] = False
        if 'engine2_cycles' in vals:
            gin['engine2_cycles'] = vals['engine2_cycles'] - rec.engine2_cycles
        else:
            gin['engine2_cycles'] = False
        if 'engine3_hours' in vals:
            gin['engine3_hours'] = vals['engine3_hours'] - rec.engine3_hours
        else:
            gin['engine3_hours'] = False
        if 'engine3_cycles' in vals:
            gin['engine3_cycles'] = vals['engine3_cycles'] - rec.engine3_cycles
        else:
            gin['engine3_cycles'] = False
        if 'engine4_hours' in vals:
            gin['engine4_hours'] = vals['engine4_hours'] - rec.engine4_hours
        else:
            gin['engine4_hours'] = False
        if 'engine4_cycles' in vals:
            gin['engine4_cycles'] = vals['engine4_cycles'] - rec.engine4_cycles
        else:
            gin['engine4_cycles'] = False

        if 'propeller1_hours' in vals:
            gin['propeller1_hours'] = vals['propeller1_hours'] - rec.propeller1_hours
        else:
            gin['propeller1_hours'] = False
        if 'propeller1_cycles' in vals:
            gin['propeller1_cycles'] = vals['propeller1_cycles'] - rec.propeller1_cycles
        else:
            gin['propeller1_cycles'] = False
        if 'propeller2_hours' in vals:
            gin['propeller2_hours'] = vals['propeller2_hours'] - rec.propeller2_hours
        else:
            gin['propeller2_hours'] = False
        if 'propeller2_cycles' in vals:
            gin['propeller2_cycles'] = vals['propeller2_cycles'] - rec.propeller2_cycles
        else:
            gin['propeller2_cycles'] = False
        if 'propeller3_hours' in vals:
            gin['propeller3_hours'] = vals['propeller3_hours'] - rec.propeller3_hours
        else:
            gin['propeller3_hours'] = False
        if 'propeller3_cycles' in vals:
            gin['propeller3_cycles'] = vals['propeller3_cycles'] - rec.propeller3_cycles
        else:
            gin['propeller3_cycles'] = False
        if 'propeller4_hours' in vals:
            gin['propeller4_hours'] = vals['propeller4_hours'] - rec.propeller4_hours
        else:
            gin['propeller4_hours'] = False
        if 'propeller4_cycles' in vals:
            gin['propeller4_cycles'] = vals['propeller4_cycles'] - rec.propeller4_cycles
        else:
            gin['propeller4_cycles'] = False

        if 'auxiliary1_hours' in vals:
            gin['auxiliary1_hours'] = vals['auxiliary1_hours'] - rec.auxiliary1_hours
        else:
            gin['auxiliary1_hours'] = False
        if 'auxiliary1_cycles' in vals:
            gin['auxiliary1_cycles'] = vals['auxiliary1_cycles'] - rec.auxiliary1_cycles
        else:
            gin['auxiliary1_cycles'] = False
        
        vals['total_hours'] = acraft.total_hours + gin['aircraft_hours']
        vals['total_cycles'] = acraft.total_landings + gin['aircraft_cycles']
        
        # vals['engine1_hours_before_flight'] = rec.aircraft_hours + gin['engine1_hours']
        # vals['engine1_cycles_before_flight'] = rec.aircraft_cycles + gin['engine1_cycles']
        # vals['engine2_hours_before_flight'] = rec.aircraft_hours + gin['engine2_hours']
        # vals['engine2_cycles_before_flight'] = rec.aircraft_cycles + gin['engine2_cycles']
        # vals['engine3_hours_before_flight'] = rec.aircraft_hours + gin['engine3_hours']
        # vals['engine3_cycles_before_flight'] = rec.aircraft_cycles + gin['engine3_cycles']
        # vals['engine4_hours_before_flight'] = rec.aircraft_hours + gin['engine4_hours']
        # vals['engine4_cycles_before_flight'] = rec.aircraft_cycles + gin['engine4_cycles']

        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        # HOURS CYCLES AIRFRAME
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        gin['engine1_id'] = acraft.engine_type_id.id
        gin['engine2_id'] = acraft.engine2_type_id.id
        gin['engine3_id'] = acraft.engine3_type_id.id
        gin['engine4_id'] = acraft.engine4_type_id.id
        gin['auxiliary1_id'] = acraft.auxiliary_type_id.id
        gin['propeller1_id'] = acraft.propeller_type_id.id
        gin['propeller2_id'] = acraft.propeller2_type_id.id
        gin['propeller3_id'] = acraft.propeller3_type_id.id
        gin['propeller4_id'] = acraft.propeller4_type_id.id

        rin = gin['aircraft_rin']
        gin['current_aircraft_hours'] = acraft.total_hours
        gin['current_aircraft_cycles'] = acraft.total_landings
        gin['current_aircraft_rin'] = acraft.total_rins
       
        acraft.write({
            'total_hours' : acraft.total_hours + gin['aircraft_hours'],
            'total_landings' : acraft.total_landings + gin['aircraft_cycles']
            })
        # HOURS CYCLES INSPECTION
        hours  = gin['aircraft_hours']
        cycles = gin['aircraft_cycles']
        for g in acraft.inspection_ids:
            for i in g.serfice_life:
                if(i.unit == 'hours'):
                    i.write({
                        'current' : i.current + gin['aircraft_hours'],
                        'remaining' : i.remaining - gin['aircraft_hours'],
                    })
                elif(i.unit == 'cycles'):
                    i.write({
                        'current' : i.current + gin['aircraft_cycles'],
                        'remaining' : i.remaining - gin['aircraft_cycles'],
                    })
                elif(i.unit == 'rin'):
                    i.write({
                        'current' : i.current + rin,
                        'remaining' : i.remaining - rin,
                    })
        # HOURS CYCLES BULLETIN
        bulletin = self.env['bulletin.aircraft.affected'].search([('fleet_id','=',gin['aircraft_id'])])
        for x in bulletin:
            if(x.bulletin_id.repetitive == True):
                if(x.unit == 'hours'):
                    x.write({
                        'current' : x.current + gin['aircraft_hours'],
                        'remaining' : x.remaining - gin['aircraft_hours'],
                    })
                elif(x.unit == 'cycles'):
                    x.write({
                        'current' : x.current + gin['aircraft_cycles'],
                        'remaining' : x.remaining - gin['aircraft_cycles'],
                    })
                elif(x.unit == 'rin'):
                    x.write({
                        'current' : x.current + rin,
                        'remaining' : x.remaining - rin,
                    })
        # HOURS CYCLES COMPONENT
        specomp = []
        for x in gin['aircraft_comp_ids']:
            specomp.append(x[2]['component_id'])
        for accomp in acraft.component_ids:
            # HOURS CYCLES KHUSUS
            hours  = gin['aircraft_hours']
            cycles = gin['aircraft_cycles']
            if(accomp.id in specomp):
                for x in gin['aircraft_comp_ids']:
                    if(x[2]['component_id'] == accomp.id):
                        # hours = x[2]['hours']
                        cycles = x[2]['cycles']
            self._gi_count_component(accomp.id,hours,cycles,rin)
            # HOURS CYCLES SUB COMPONENT
            for subaccomp in accomp.sub_part_ids:
                # HOURS CYCLES KHUSUS
                hours  = gin['aircraft_hours']
                cycles = gin['aircraft_cycles']
                if(subaccomp.id in specomp):
                    for x in gin['aircraft_comp_ids']:
                        if(x[2]['component_id'] == subaccomp.id or x[2]['component_id'] == subaccomp.part_id.id):
                            # hours = x[2]['hours']
                            cycles = x[2]['cycles']
                self._gi_count_component(subaccomp.id,hours,cycles,rin)
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        # HOURS CYCLES ENGINE
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        for num in xrange(1,4):
            engnum = str(num)
            eng = self.env['engine.type'].search([('id','=',gin['engine'+engnum+'_id'])])
            gin['current_engine'+engnum+'_hours'] = eng.total_hours
            gin['current_engine'+engnum+'_cycles'] = eng.total_cycles
            gin['current_engine'+engnum+'_rin'] = eng.total_rins

            vals['engine'+engnum+'_hours_before_flight'] = eng.engine_tsn + gin['engine1_hours']
            vals['engine'+engnum+'_cycles_before_flight'] = eng.engine_csn + gin['engine1_cycles']

            eng.write({
                'engine_tsn' : eng.engine_tsn + gin['engine'+engnum+'_hours'],
                'engine_csn' : eng.engine_csn + gin['engine'+engnum+'_cycles'],
                'total_hours' : eng.engine_tsn + gin['engine'+engnum+'_hours'],
                'total_cycles' : eng.engine_csn + gin['engine'+engnum+'_cycles']
                })
            # HOURS CYCLES INSPECTION
            for g in eng.inspection_ids:
                for i in g.serfice_life:
                    if(i.unit == 'hours'):
                        i.write({
                            'current' : i.current + gin['engine'+engnum+'_hours'],
                            'remaining' : i.remaining - gin['engine'+engnum+'_hours'],
                        })
                    elif(i.unit == 'cycles'):
                        i.write({
                            'current' : i.current + gin['engine'+engnum+'_cycles'],
                            'remaining' : i.remaining - gin['engine'+engnum+'_cycles'],
                        })
                    elif(i.unit == 'rin'):
                        i.write({
                            'current' : i.current + rin,
                            'remaining' : i.remaining - rin,
                        })
            eng = self.env['engine.spare'].search([('name','=',gin['engine'+engnum+'_id'])])
            eng.write({
                'engine_tsn' : eng.engine_tsn + gin['engine'+engnum+'_hours'],
                'engine_csn' : eng.engine_csn + gin['engine'+engnum+'_cycles'],
                'tsn' : eng.engine_tsn + gin['engine'+engnum+'_hours'],
                'csn' : eng.engine_csn + gin['engine'+engnum+'_cycles']
                })
            # HOURS CYCLES COMPONENT
            specomp = []
            for x in gin['engine'+engnum+'_comp_ids']:
                specomp.append(x[2]['component_id'])
            eng = self.env['engine.type'].search([('id','=',gin['engine'+engnum+'_id'])])
            for accomp in eng.component_ids:
                # HOURS CYCLES KHUSUS
                hours  = gin['engine'+engnum+'_hours']
                cycles = gin['engine'+engnum+'_cycles']
                if(accomp.id in specomp):
                    for x in gin['engine'+engnum+'_comp_ids']:
                        if(x[2]['component_id'] == accomp.id):
                            # hours = x[2]['hours']
                            cycles = x[2]['cycles']
                self._gi_count_component(accomp.id,hours,cycles,rin)
                # HOURS CYCLES SUB COMPONENT
                for subaccomp in accomp.sub_part_ids:
                    # HOURS CYCLES KHUSUS
                    hours  = gin['engine'+engnum+'_hours']
                    cycles = gin['engine'+engnum+'_cycles']
                    if(subaccomp.id in specomp):
                        for x in gin['engine'+engnum+'_comp_ids']:
                            if(x[2]['component_id'] == subaccomp.id or x[2]['component_id'] == subaccomp.part_id.id):
                                # hours = x[2]['hours']
                                cycles = x[2]['cycles']
                    self._gi_count_component(subaccomp.id,hours,cycles,rin)
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        # END OF HOURS CYCLES ENGINE
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        # HOURS CYCLES PROPELLER
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        for num in xrange(1,4):
            engnum = str(num)
            eng = self.env['propeller.type'].search([('id','=',gin['propeller'+engnum+'_id'])])
            gin['current_propeller'+engnum+'_hours'] = eng.total_hours
            gin['current_propeller'+engnum+'_cycles'] = eng.total_cycles
            gin['current_propeller'+engnum+'_rin'] = eng.total_rins

            vals['propeller'+engnum+'_hours_before_flight'] = eng.propeller_tsn
            vals['propeller'+engnum+'_cycles_before_flight'] = eng.propeller_csn

            eng.write({
                'propeller_tsn' : eng.propeller_tsn + gin['propeller'+engnum+'_hours'],
                'propeller_csn' : eng.propeller_csn + gin['propeller'+engnum+'_cycles'],
                'total_hours' : eng.propeller_tsn + gin['propeller'+engnum+'_hours'],
                'total_cycles' : eng.propeller_csn + gin['propeller'+engnum+'_cycles']
                })
            # HOURS CYCLES INSPECTION
            for g in eng.inspection_ids:
                for i in g.serfice_life:
                    if(i.unit == 'hours'):
                        i.write({
                            'current' : i.current + gin['propeller'+engnum+'_hours'],
                            'remaining' : i.remaining - gin['propeller'+engnum+'_hours'],
                        })
                    elif(i.unit == 'cycles'):
                        i.write({
                            'current' : i.current + gin['propeller'+engnum+'_cycles'],
                            'remaining' : i.remaining - gin['propeller'+engnum+'_cycles'],
                        })
                    elif(i.unit == 'rin'):
                        i.write({
                            'current' : i.current + rin,
                            'remaining' : i.remaining - rin,
                        })
            eng = self.env['propeller.spare'].search([('name','=',gin['propeller'+engnum+'_id'])])
            eng.write({
                'propeller_tsn' : eng.propeller_tsn + gin['propeller'+engnum+'_hours'],
                'propeller_csn' : eng.propeller_csn + gin['propeller'+engnum+'_cycles'],
                'total_hours' : eng.propeller_tsn + gin['propeller'+engnum+'_hours'],
                'total_cycles' : eng.propeller_csn + gin['propeller'+engnum+'_cycles']
                })
            # HOURS CYCLES COMPONENT
            specomp = []
            for x in gin['propeller'+engnum+'_comp_ids']:
                specomp.append(x[2]['component_id'])
            eng = self.env['propeller.type'].search([('id','=',gin['propeller'+engnum+'_id'])])
            for accomp in eng.component_ids:
                # HOURS CYCLES KHUSUS
                hours  = gin['propeller'+engnum+'_hours']
                cycles = gin['propeller'+engnum+'_cycles']
                if(accomp.id in specomp):
                    for x in gin['propeller'+engnum+'_comp_ids']:
                        if(x[2]['component_id'] == accomp.id):
                            # hours = x[2]['hours']
                            cycles = x[2]['cycles']
                self._gi_count_component(accomp.id,hours,cycles,rin)
                # HOURS CYCLES SUB COMPONENT
                for subaccomp in accomp.sub_part_ids:
                    # HOURS CYCLES KHUSUS
                    hours  = gin['propeller'+engnum+'_hours']
                    cycles = gin['propeller'+engnum+'_cycles']
                    if(subaccomp.id in specomp):
                        for x in gin['propeller'+engnum+'_comp_ids']:
                            if(x[2]['component_id'] == subaccomp.id or x[2]['component_id'] == subaccomp.part_id.id):
                                # hours = x[2]['hours']
                                cycles = x[2]['cycles']
                    self._gi_count_component(subaccomp.id,hours,cycles,rin)
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        # END OF HOURS CYCLES PROPELLER
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        # HOURS CYCLES AUXILIARY
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        for num in xrange(1,1):
            engnum = str(num)
            eng = self.env['auxiliary.type'].search([('id','=',gin['auxiliary'+engnum+'_id'])])
            gin['current_auxiliary'+engnum+'_hours'] = eng.total_hours
            gin['current_auxiliary'+engnum+'_cycles'] = eng.total_cycles
            gin['current_auxiliary'+engnum+'_rin'] = eng.total_rins

            vals['auxiliary'+engnum+'_hours_before_flight'] = eng.auxiliary_tsn
            vals['auxiliary'+engnum+'_cycles_before_flight'] = eng.auxiliary_csn

            eng.write({
                'auxiliary_tsn' : eng.auxiliary_tsn + gin['auxiliary'+engnum+'_hours'],
                'auxiliary_csn' : eng.auxiliary_csn + gin['auxiliary'+engnum+'_cycles'],
                'total_hours' : eng.auxiliary_tsn + gin['engine'+engnum+'_hours'],
                'total_cycles' : eng.auxiliary_csn + gin['engine'+engnum+'_cycles']
                })
            # HOURS CYCLES INSPECTION
            for g in eng.inspection_ids:
                for i in g.serfice_life:
                    if(i.unit == 'hours'):
                        i.write({
                            'current' : i.current + gin['auxiliary'+engnum+'_hours'],
                            'remaining' : i.remaining - gin['auxiliary'+engnum+'_hours'],
                        })
                    elif(i.unit == 'cycles'):
                        i.write({
                            'current' : i.current + gin['auxiliary'+engnum+'_cycles'],
                            'remaining' : i.remaining - gin['auxiliary'+engnum+'_cycles'],
                        })
                    elif(i.unit == 'rin'):
                        i.write({
                            'current' : i.current + rin,
                            'remaining' : i.remaining - rin,
                        })
            eng = self.env['auxiliary.spare'].search([('name','=',gin['auxiliary'+engnum+'_id'])])
            eng.write({
                'auxiliary_tsn' : eng.auxiliary_tsn + gin['auxiliary'+engnum+'_hours'],
                'auxiliary_csn' : eng.auxiliary_csn + gin['auxiliary'+engnum+'_cycles'],
                'total_hours' : eng.auxiliary_tsn + gin['engine'+engnum+'_hours'],
                'total_cycles' : eng.auxiliary_csn + gin['engine'+engnum+'_cycles']

                })
            # HOURS CYCLES COMPONENT
            specomp = []
            for x in gin['auxiliary'+engnum+'_comp_ids']:
                specomp.append(x[2]['component_id'])
            eng = self.env['auxiliary.type'].search([('id','=',gin['auxiliary'+engnum+'_id'])])
            for accomp in eng.component_ids:
                # HOURS CYCLES KHUSUS
                hours  = gin['auxiliary'+engnum+'_hours']
                cycles = gin['auxiliary'+engnum+'_cycles']
                if(accomp.id in specomp):
                    for x in gin['auxiliary'+engnum+'_comp_ids']:
                        if(x[2]['component_id'] == accomp.id):
                            # hours = x[2]['hours']
                            cycles = x[2]['cycles']
                self._gi_count_component(accomp.id,hours,cycles,rin)
                # HOURS CYCLES SUB COMPONENT
                for subaccomp in accomp.sub_part_ids:
                    # HOURS CYCLES KHUSUS
                    hours  = gin['auxiliary'+engnum+'_hours']
                    cycles = gin['auxiliary'+engnum+'_cycles']
                    if(subaccomp.id in specomp):
                        for x in gin['auxiliary'+engnum+'_comp_ids']:
                            if(x[2]['component_id'] == subaccomp.id or x[2]['component_id'] == subaccomp.part_id.id):
                                # hours = x[2]['hours']
                                cycles = x[2]['cycles']
                    self._gi_count_component(subaccomp.id,hours,cycles,rin)
                    findcomp.write(wdict)
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        # END OF HOURS CYCLES AUXILIARY
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        write = super(ams_fml, self).write(vals)
        return write

    @api.model
    def create(self, vals):
        """ CREATE TOTAL HOUR"""
        if(self._context.get('aircraft_id',False) != False):
            vals['aircraft_id'] = self._context.get('aircraft_id',False)
        acraft = self.env['aircraft.acquisition'].search([('id','=',vals['aircraft_id'])])
        if acraft.id != False:
            vals['total_hours'] = float(acraft.total_hours)
            vals['total_cycles'] = float(acraft.total_landings)

        if acraft.engine_type_id.id != False:
            vals['engine1_hours_before_flight'] = float(acraft.engine_type_id.engine_tsn)
            vals['engine1_cycles_before_flight'] = float(acraft.engine_type_id.engine_csn)

        if acraft.engine2_type_id.id != False:
            vals['engine2_hours_before_flight'] = float(acraft.engine2_type_id.engine_tsn)
            vals['engine2_cycles_before_flight'] = float(acraft.engine2_type_id.engine_csn)

        if acraft.engine3_type_id.id != False:
            vals['engine3_hours_before_flight'] = float(acraft.engine3_type_id.engine_tsn)
            vals['engine3_cycles_before_flight'] = float(acraft.engine3_type_id.engine_csn)


        if acraft.engine4_type_id.id != False:
            vals['engine4_hours_before_flight'] = float(acraft.engine4_type_id.engine_tsn)
            vals['engine4_cycles_before_flight'] = float(acraft.engine4_type_id.engine_csn)

        # KURANG PROPELLER & AUXILIARY
        if acraft.propeller_type_id.id != False:
            vals['propeller1_hours_before_flight'] = float(acraft.propeller_type_id.propeller_tsn)
            vals['propeller1_cycles_before_flight'] = float(acraft.propeller_type_id.propeller_csn)

        if acraft.propeller2_type_id.id != False:
            vals['propeller2_hours_before_flight'] = float(acraft.propeller2_type_id.propeller_tsn)
            vals['propeller2_cycles_before_flight'] = float(acraft.propeller2_type_id.propeller_csn)

        if acraft.propeller3_type_id.id != False:
            vals['propeller3_hours_before_flight'] = float(acraft.propeller3_type_id.propeller_tsn)
            vals['propeller3_cycles_before_flight'] = float(acraft.propeller3_type_id.propeller_csn)

        if acraft.propeller4_type_id.id != False:
            vals['propeller4_hours_before_flight'] = float(acraft.propeller4_type_id.propeller_tsn)
            vals['propeller4_cycles_before_flight'] = float(acraft.propeller4_type_id.propeller_csn)

        if acraft.auxiliary_type_id.id != False:
            vals['auxiliary1_hours_before_flight'] = float(acraft.auxiliary1_type_id.auxiliary_tsn)
            vals['auxiliary1_cycles_before_flight'] = float(acraft.auxiliary1_type_id.auxiliary_csn)

        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        # HOURS CYCLES AIRFRAME
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        vals['engine1_id'] = acraft.engine_type_id.id
        vals['engine2_id'] = acraft.engine2_type_id.id
        vals['engine3_id'] = acraft.engine3_type_id.id
        vals['engine4_id'] = acraft.engine4_type_id.id
        vals['auxiliary1_id'] = acraft.auxiliary_type_id.id
        vals['propeller1_id'] = acraft.propeller_type_id.id
        vals['propeller2_id'] = acraft.propeller2_type_id.id
        vals['propeller3_id'] = acraft.propeller3_type_id.id
        vals['propeller4_id'] = acraft.propeller4_type_id.id

        vals['propeller1_cycles'] = vals['aircraft_cycles']
        vals['propeller2_cycles'] = vals['aircraft_cycles']
        vals['propeller3_cycles'] = vals['aircraft_cycles']
        vals['propeller4_cycles'] = vals['aircraft_cycles']
        

        idlog = self.env['flight.maintenance.log'].search([('name', '=', vals['name'] )])
        if(idlog):
            vals['aircraft_id'] = idlog.fl_acquisition_id.id
            vals['date'] = idlog.schedule_date
        rin = vals['aircraft_rin']
        vals['current_aircraft_hours'] = acraft.total_hours
        vals['current_aircraft_cycles'] = acraft.total_landings
        vals['current_aircraft_rin'] = acraft.total_rins
        acraft.write({
            'total_hours' : acraft.total_hours + vals['aircraft_hours'],
            'total_landings' : acraft.total_landings + vals['aircraft_cycles']
            })
        # HOURS CYCLES INSPECTION
        hours  = vals['aircraft_hours']
        cycles = vals['aircraft_cycles']
        for g in acraft.inspection_ids:
            for i in g.serfice_life:
                if(i.unit == 'hours'):
                    i.write({
                        'current' : i.current + vals['aircraft_hours'],
                        'remaining' : i.remaining - vals['aircraft_hours'],
                    })
                elif(i.unit == 'cycles'):
                    i.write({
                        'current' : i.current + vals['aircraft_cycles'],
                        'remaining' : i.remaining - vals['aircraft_cycles'],
                    })
                elif(i.unit == 'rin'):
                    i.write({
                        'current' : i.current + rin,
                        'remaining' : i.remaining - rin,
                    })
        # HOURS CYCLES BULLETIN
        bulletin = self.env['bulletin.aircraft.affected'].search([('fleet_id','=',vals['aircraft_id'])])
        for x in bulletin:
            if(x.bulletin_id.repetitive == True):
                if(x.unit == 'hours'):
                    x.write({
                        'current' : x.current + vals['aircraft_hours'],
                        'remaining' : x.remaining - vals['aircraft_hours'],
                    })
                elif(x.unit == 'cycles'):
                    x.write({
                        'current' : x.current + vals['aircraft_cycles'],
                        'remaining' : x.remaining - vals['aircraft_cycles'],
                    })
                elif(x.unit == 'rin'):
                    x.write({
                        'current' : x.current + rin,
                        'remaining' : x.remaining - rin,
                    })
        # HOURS CYCLES COMPONENT
        specomp = []
        for x in vals['aircraft_comp_ids']:
            specomp.append(x[2]['component_id'])
        acraft = self.env['aircraft.acquisition'].search([('id','=',vals['aircraft_id'])])
        for accomp in acraft.component_ids:
            # HOURS CYCLES KHUSUS
            hours  = vals['aircraft_hours']
            cycles = vals['aircraft_cycles']
            if(accomp.id in specomp):
                for x in vals['aircraft_comp_ids']:
                    if(x[2]['component_id'] == accomp.id):
                        # hours = x[2]['hours']
                        cycles = x[2]['cycles']
            self._gi_count_component(accomp.id,hours,cycles,rin)
            # HOURS CYCLES SUB COMPONENT
            for subaccomp in accomp.sub_part_ids:
                # HOURS CYCLES KHUSUS
                hours  = vals['aircraft_hours']
                cycles = vals['aircraft_cycles']
                if(subaccomp.id in specomp):
                    for x in vals['aircraft_comp_ids']:
                        if(x[2]['component_id'] == subaccomp.id or x[2]['component_id'] == subaccomp.part_id.id):
                            # hours = x[2]['hours']
                            cycles = x[2]['cycles']
                self._gi_count_component(subaccomp.id,hours,cycles,rin)
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        # HOURS CYCLES ENGINE
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        for num in xrange(1,4):
            engnum = str(num)
            eng = self.env['engine.type'].search([('id','=',vals['engine'+engnum+'_id'])])
            vals['current_engine'+engnum+'_hours'] = eng.total_hours
            vals['current_engine'+engnum+'_cycles'] = eng.total_cycles
            vals['current_engine'+engnum+'_rin'] = eng.total_rins
            eng.write({
                'engine_tsn' : eng.engine_tsn + vals['engine'+engnum+'_hours'],
                'engine_csn' : eng.engine_csn + vals['engine'+engnum+'_cycles'],
                'total_hours' : eng.engine_tsn + vals['engine'+engnum+'_hours'],
                'total_cycles' : eng.engine_csn + vals['engine'+engnum+'_cycles']
                })
            # HOURS CYCLES INSPECTION
            for g in eng.inspection_ids:
                for i in g.serfice_life:
                    if(i.unit == 'hours'):
                        i.write({
                            'current' : i.current + vals['engine'+engnum+'_hours'],
                            'remaining' : i.remaining - vals['engine'+engnum+'_hours'],
                        })
                    elif(i.unit == 'cycles'):
                        i.write({
                            'current' : i.current + vals['engine'+engnum+'_cycles'],
                            'remaining' : i.remaining - vals['engine'+engnum+'_cycles'],
                        })
                    elif(i.unit == 'rin'):
                        i.write({
                            'current' : i.current + rin,
                            'remaining' : i.remaining - rin,
                        })
            eng = self.env['engine.spare'].search([('name','=',vals['engine'+engnum+'_id'])])
            eng.write({
                'engine_tsn' : eng.engine_tsn + vals['engine'+engnum+'_hours'],
                'engine_csn' : eng.engine_csn + vals['engine'+engnum+'_cycles'],
                'total_hours' : eng.engine_tsn + vals['engine'+engnum+'_hours'],
                'total_cycles' : eng.engine_csn + vals['engine'+engnum+'_cycles']
                })
            # HOURS CYCLES COMPONENT
            specomp = []
            for x in vals['engine'+engnum+'_comp_ids']:
                specomp.append(x[2]['component_id'])
            eng = self.env['engine.type'].search([('id','=',vals['engine'+engnum+'_id'])])
            for accomp in eng.component_ids:
                # HOURS CYCLES KHUSUS
                hours  = vals['engine'+engnum+'_hours']
                cycles = vals['engine'+engnum+'_cycles']
                if(accomp.id in specomp):
                    for x in vals['engine'+engnum+'_comp_ids']:
                        if(x[2]['component_id'] == accomp.id):
                            # hours = x[2]['hours']
                            cycles = x[2]['cycles']
                self._gi_count_component(accomp.id,hours,cycles,rin)
                # HOURS CYCLES SUB COMPONENT
                for subaccomp in accomp.sub_part_ids:
                    # HOURS CYCLES KHUSUS
                    hours  = vals['engine'+engnum+'_hours']
                    cycles = vals['engine'+engnum+'_cycles']
                    if(subaccomp.id in specomp):
                        for x in vals['engine'+engnum+'_comp_ids']:
                            if(x[2]['component_id'] == subaccomp.id or x[2]['component_id'] == subaccomp.part_id.id):
                                # hours = x[2]['hours']
                                cycles = x[2]['cycles']
                    self._gi_count_component(subaccomp.id,hours,cycles,rin)
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        # END OF HOURS CYCLES ENGINE
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        # HOURS CYCLES PROPELLER
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        for num in xrange(1,4):
            engnum = str(num)
            eng = self.env['propeller.type'].search([('id','=',vals['propeller'+engnum+'_id'])])
            vals['current_propeller'+engnum+'_hours'] = eng.total_hours
            vals['current_propeller'+engnum+'_cycles'] = eng.total_cycles
            vals['current_propeller'+engnum+'_rin'] = eng.total_rins

            eng.write({
                'propeller_tsn' : eng.propeller_tsn + vals['propeller'+engnum+'_hours'],
                'propeller_csn' : eng.propeller_csn + vals['propeller'+engnum+'_cycles'],
                'total_hours' : eng.propeller_tsn + vals['propeller'+engnum+'_hours'],
                'total_cycles' : eng.propeller_csn + vals['propeller'+engnum+'_cycles']
                })
            # HOURS CYCLES INSPECTION
            for g in eng.inspection_ids:
                for i in g.serfice_life:
                    if(i.unit == 'hours'):
                        i.write({
                            'current' : i.current + vals['propeller'+engnum+'_hours'],
                            'remaining' : i.remaining - vals['propeller'+engnum+'_hours'],
                        })
                    elif(i.unit == 'cycles'):
                        i.write({
                            'current' : i.current + vals['propeller'+engnum+'_cycles'],
                            'remaining' : i.remaining - vals['propeller'+engnum+'_cycles'],
                        })
                    elif(i.unit == 'rin'):
                        i.write({
                            'current' : i.current + rin,
                            'remaining' : i.remaining - rin,
                        })
            eng = self.env['propeller.spare'].search([('name','=',vals['propeller'+engnum+'_id'])])
            eng.write({
                'propeller_tsn' : eng.propeller_tsn + vals['propeller'+engnum+'_hours'],
                'propeller_csn' : eng.propeller_csn + vals['propeller'+engnum+'_cycles'],
                'total_hours' : eng.propeller_tsn + vals['propeller'+engnum+'_hours'],
                'total_cycles' : eng.propeller_csn + vals['propeller'+engnum+'_cycles']
                })
            # HOURS CYCLES COMPONENT
            specomp = []
            for x in vals['propeller'+engnum+'_comp_ids']:
                specomp.append(x[2]['component_id'])
            eng = self.env['propeller.type'].search([('id','=',vals['propeller'+engnum+'_id'])])
            for accomp in eng.component_ids:
                # HOURS CYCLES KHUSUS
                hours  = vals['propeller'+engnum+'_hours']
                cycles = vals['propeller'+engnum+'_cycles']
                if(accomp.id in specomp):
                    for x in vals['propeller'+engnum+'_comp_ids']:
                        if(x[2]['component_id'] == accomp.id):
                            # hours = x[2]['hours']
                            cycles = x[2]['cycles']
                self._gi_count_component(accomp.id,hours,cycles,rin)
                # HOURS CYCLES SUB COMPONENT
                for subaccomp in accomp.sub_part_ids:
                    # HOURS CYCLES KHUSUS
                    hours  = vals['propeller'+engnum+'_hours']
                    cycles = vals['propeller'+engnum+'_cycles']
                    if(subaccomp.id in specomp):
                        for x in vals['propeller'+engnum+'_comp_ids']:
                            if(x[2]['component_id'] == subaccomp.id or x[2]['component_id'] == subaccomp.part_id.id):
                                # hours = x[2]['hours']
                                cycles = x[2]['cycles']
                    self._gi_count_component(subaccomp.id,hours,cycles,rin)
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        # END OF HOURS CYCLES PROPELLER
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        # HOURS CYCLES AUXILIARY
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        for num in xrange(1,1):
            engnum = str(num)
            eng = self.env['auxiliary.type'].search([('id','=',vals['auxiliary'+engnum+'_id'])])
            vals['current_auxiliary'+engnum+'_hours'] = eng.total_hours
            vals['current_auxiliary'+engnum+'_cycles'] = eng.total_cycles
            vals['current_auxiliary'+engnum+'_rin'] = eng.total_rins

            eng.write({
                'auxiliary_tsn' : eng.auxiliary_tsn + vals['auxiliary'+engnum+'_hours'],
                'auxiliary_csn' : eng.auxiliary_csn + vals['auxiliary'+engnum+'_cycles'],
                'total_hours' : eng.auxiliary_tsn + vals['engine'+engnum+'_hours'],
                'total_cycles' : eng.auxiliary_csn + vals['engine'+engnum+'_cycles']
                })
            # HOURS CYCLES INSPECTION
            for g in eng.inspection_ids:
                for i in g.serfice_life:
                    if(i.unit == 'hours'):
                        i.write({
                            'current' : i.current + vals['auxiliary'+engnum+'_hours'],
                            'remaining' : i.remaining - vals['auxiliary'+engnum+'_hours'],
                        })
                    elif(i.unit == 'cycles'):
                        i.write({
                            'current' : i.current + vals['auxiliary'+engnum+'_cycles'],
                            'remaining' : i.remaining - vals['auxiliary'+engnum+'_cycles'],
                        })
                    elif(i.unit == 'rin'):
                        i.write({
                            'current' : i.current + rin,
                            'remaining' : i.remaining - rin,
                        })
            eng = self.env['auxiliary.spare'].search([('name','=',vals['auxiliary'+engnum+'_id'])])
            eng.write({
                'auxiliary_tsn' : eng.auxiliary_tsn + vals['auxiliary'+engnum+'_hours'],
                'auxiliary_csn' : eng.auxiliary_csn + vals['auxiliary'+engnum+'_cycles'],
                'total_hours' : eng.auxiliary_tsn + vals['engine'+engnum+'_hours'],
                'total_cycles' : eng.auxiliary_csn + vals['engine'+engnum+'_cycles']

                })
            # HOURS CYCLES COMPONENT
            specomp = []
            for x in vals['auxiliary'+engnum+'_comp_ids']:
                specomp.append(x[2]['component_id'])
            eng = self.env['auxiliary.type'].search([('id','=',vals['auxiliary'+engnum+'_id'])])
            for accomp in eng.component_ids:
                # HOURS CYCLES KHUSUS
                hours  = vals['auxiliary'+engnum+'_hours']
                cycles = vals['auxiliary'+engnum+'_cycles']
                if(accomp.id in specomp):
                    for x in vals['auxiliary'+engnum+'_comp_ids']:
                        if(x[2]['component_id'] == accomp.id):
                            # hours = x[2]['hours']
                            cycles = x[2]['cycles']
                self._gi_count_component(accomp.id,hours,cycles,rin)
                # HOURS CYCLES SUB COMPONENT
                for subaccomp in accomp.sub_part_ids:
                    # HOURS CYCLES KHUSUS
                    hours  = vals['auxiliary'+engnum+'_hours']
                    cycles = vals['auxiliary'+engnum+'_cycles']
                    if(subaccomp.id in specomp):
                        for x in vals['auxiliary'+engnum+'_comp_ids']:
                            if(x[2]['component_id'] == subaccomp.id or x[2]['component_id'] == subaccomp.part_id.id):
                                # hours = x[2]['hours']
                                cycles = x[2]['cycles']
                    self._gi_count_component(subaccomp.id,hours,cycles,rin)
                    findcomp.write(wdict)
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        # END OF HOURS CYCLES AUXILIARY
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        
        # total_all_time = int(vals['engine1_hours'])+int(vals['engine2_hours'])+int(vals['engine3_hours'])+int(vals['engine4_hours'])+int(vals['aircraft_hours'])
        # vals['total_hours'] = total_all_time
        # rec = super(ams_fml, self).create(vals)
        create = super(ams_fml, self).create(vals)
        for specomp in create.aircraft_comp_ids:
            specomp.cycles_before = specomp.component_id.csn

        for specomp in create.engine1_comp_ids:
            specomp.cycles_before = specomp.component_id.csn
        for specomp in create.engine2_comp_ids:
            specomp.cycles_before = specomp.component_id.csn
        for specomp in create.engine3_comp_ids:
            specomp.cycles_before = specomp.component_id.csn
        for specomp in create.engine4_comp_ids:
            specomp.cycles_before = specomp.component_id.csn
        for specomp in create.propeller1_comp_ids:
            specomp.cycles_before = specomp.component_id.csn
        for specomp in create.propeller2_comp_ids:
            specomp.cycles_before = specomp.component_id.csn
        for specomp in create.propeller3_comp_ids:
            specomp.cycles_before = specomp.component_id.csn
        for specomp in create.propeller4_comp_ids:
            specomp.cycles_before = specomp.component_id.csn
        for specomp in create.auxiliary1_comp_ids:
            specomp.cycles_before = specomp.component_id.csn
        return create

    
    @api.onchange('discard_btn')
    def act_discard_fml(self):
        self.fml_wizard()   

    @api.multi
    def fml_wizard(self):
        return {
            'name': 'Flight Maintenance Log',
            'type': 'ir.actions.act_window_close',
            'res_model': 'wizard.fml',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref('ams_fml.wizard_fml_filter').id,
            'res_id': False,
            'views': [(False, 'form')],
            'target': 'new',
        }

# UNTUK KEBUTUHAN COMPONENT KHUSUS
class AircraftFmlComp(models.Model):
    _name = 'ams_fml.component.airframe'
    _description = 'Component Log'

    ac_fml_id = fields.Many2one('ams_fml.log', string='FML', readonly=True)
    eng1_fml_id = fields.Many2one('ams_fml.log', string='FML', readonly=True)
    eng2_fml_id = fields.Many2one('ams_fml.log', string='FML', readonly=True)
    eng3_fml_id = fields.Many2one('ams_fml.log', string='FML', readonly=True)
    eng4_fml_id = fields.Many2one('ams_fml.log', string='FML', readonly=True)
    aux1_fml_id = fields.Many2one('ams_fml.log', string='FML', readonly=True)
    prop1_fml_id = fields.Many2one('ams_fml.log', string='FML', readonly=True)
    prop2_fml_id = fields.Many2one('ams_fml.log', string='FML', readonly=True)
    prop3_fml_id = fields.Many2one('ams_fml.log', string='FML', readonly=True)
    prop4_fml_id = fields.Many2one('ams_fml.log', string='FML', readonly=True)

    component_id = fields.Many2one('ams.component.part', string='Component', readonly=True)
    hours = fields.Float(string='Component Hours')
    cycles = fields.Float(string='Cycles Added')
    cycles_before = fields.Float(string="Cycles Before", store=True)
    cycles_after = fields.Float(string="Cycles After", compute='_get_cycles_after')

    @api.onchange('component_id')
    def _onchange_component_id(self):
        self.cycles_before = self.component_id.csn

    @api.onchange('cycles')
    def _get_cycles_after(self):
        self.cycles_after = float(self.cycles_before) + float(self.cycles)

    @api.model
    def create(self, values):
        values['cycles_before'] = self.component_id.csn    
        return super(AircraftFmlComp, self).create(values)


# NANTI DITAMBAH ACTION KALAO SAVE DI PAIIS MASUKIN KE FML SINI
# oncreate FOREACH ams_fml.log if name sama ubah ref fml

class PaiisFmlCorrection(models.Model):
    _inherit = "flight.maintenance.log"

    @api.model
    def create(self, vals):
        if vals.get('is_instructor', False) and (not vals.get('brief_time') or vals.get('brief_time') <= 0.0):
            crew_name = self.env['hr.employee'].browse(vals.get('crew_id')).name if vals.get('crew_id', False) else _("")
            raise UserError(_('Brief/De Brief should not be empty, please check again...\n"%s" ') % crew_name)

        ret = super(PaiisFmlCorrection, self).create(vals)
        self.env['ams_fml.log'].search([('name','=',vals['name'])]).write({
            'log_id':ret.id,
            'log_id_text':vals['name'],
            })
        return ret

# 
# # FILTER FML
class WizardFml(models.Model):
    _name = 'wizard.fml'

    aircraft_id = fields.Many2one('aircraft.acquisition', 'Aircraft Registration')
    sum_hours   = fields.Float('Hours', related="aircraft_id.total_hours", readonly=True)
    sum_cycles  = fields.Float('Hours', related="aircraft_id.total_landings", readonly=True)

    engine_1st  = fields.Char('Engine#1', related="aircraft_id.engine_type_id.name", readonly=True)
    eng_tsn_1st = fields.Float(string="TSN", related="aircraft_id.engine1_tsn", readonly=True)
    eng_csn_1st = fields.Float(string="CSN", related="aircraft_id.engine1_csn", readonly=True)

    engine_2nd  = fields.Char('Engine#2', related="aircraft_id.engine2_type_id.name", readonly=True)
    eng_tsn_2nd = fields.Float(string="TSN", related="aircraft_id.engine2_tsn", readonly=True)
    eng_csn_2nd = fields.Float(string="CSN", related="aircraft_id.engine2_csn", readonly=True)

    engine_3rd  = fields.Char('Engine#3', related="aircraft_id.engine3_type_id.name", readonly=True)
    eng_tsn_3rd = fields.Float(string="TSN", related="aircraft_id.engine3_tsn", readonly=True)
    eng_csn_3rd = fields.Float(string="CSN", related="aircraft_id.engine3_csn", readonly=True)

    engine_4th  = fields.Char('Engine#4', related="aircraft_id.engine4_type_id.name", readonly=True)
    eng_tsn_4th = fields.Float(string="TSN", related="aircraft_id.engine4_tsn", readonly=True)
    eng_csn_4th = fields.Float(string="CSN", related="aircraft_id.engine4_csn", readonly=True)
    
    auxiliary_id = fields.Char('Auxiliary', related="aircraft_id.auxiliary_type_id.name", readonly=True)
    auxiliary_tsn = fields.Float(string="TSN", related="aircraft_id.auxiliary_tsn", readonly=True)
    auxiliary_csn = fields.Float(string="CSN", related="aircraft_id.auxiliary_csn", readonly=True)

    @api.multi
    def view_fml(self):

        domain = []
        if self.aircraft_id.id:
            domain.append(('aircraft_id','=',self.aircraft_id.id))

        return {
            'name': 'Flight Maintenance Log',
            'type': 'ir.actions.act_window',
            'res_model': 'ams_fml.log',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'view_search_id': 'fml_list_filter',
            'res_id': False,
            'domain': domain,
            'target': 'main',
        }

    @api.multi
    def create_fml(self):
        return {
            'name': 'Flight Maintenance Log',
            'type': 'ir.actions.act_window',
            'res_model': 'ams_fml.log',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': False,
            'views': [(False, 'form')],
            'target': 'main',
            'context': {
                'aircraft_id':self.aircraft_id.id,
            }
        }