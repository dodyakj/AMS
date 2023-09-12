# -*- coding: utf-8 -*-
from datetime import date, datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _

class AmsProject(models.Model):
    _name = 'ams.project'
    _description = 'Project'

    name = fields.Char(string='Project Name')

class paiis_corrective_aircraft_inherit(models.Model):
    _inherit = 'aircraft.acquisition'

    utils_ids = fields.One2many('ams.daily', 'fleet_id', string='Daily Utilization', copy=False, ondelete="cascade")

class AmsDaily(models.Model):
    _name = 'ams.daily'
    _description = 'Daily Utilization'
    _rec_name = 'project_name'

    is_active = fields.Boolean(string='Active', default=True)
    fleet_id = fields.Many2one('aircraft.acquisition',string='Aircraft', required=True)
    start_date = fields.Date(string='Date Start')
    end_date = fields.Date(string='Date End')
    project_name = fields.Many2one('ams.project',string='Project')

    rin_active = fields.Boolean(string='RIN Active',related='fleet_id.rin_active')
    aircraft_hours_real = fields.Float(string='Hours Real', compute='_onchange_dates')
    aircraft_hours = fields.Float(string='Aircraft Hours/Day')
    aircraft_cycles_real = fields.Float(string='Cycles Real', compute='_onchange_dates')
    aircraft_cycles = fields.Float(string='Aircraft Cycles/Day')
    aircraft_rin = fields.Float(string='RIN',default='4')

    aircraft_comp_ids = fields.One2many('ams_daily.component','ac_daily_id',string='Aircraft Component')

    engine1_id = fields.Many2one('engine.type', string='Engine #1')
    engine1_id_text = fields.Char(string='Engine #1',related='engine1_id.name',readonly=True)
    engine2_id = fields.Many2one('engine.type', string='Engine #2')
    engine2_id_text = fields.Char(string='Engine #2',related='engine2_id.name',readonly=True)
    engine3_id = fields.Many2one('engine.type', string='Engine #3')
    engine3_id_text = fields.Char(string='Engine #3',related='engine3_id.name',readonly=True)
    engine4_id = fields.Many2one('engine.type', string='Engine #4')
    engine4_id_text = fields.Char(string='Engine #4',related='engine4_id.name',readonly=True)

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

    engine1_hours = fields.Float(string='Hours/Day')
    engine1_cycles = fields.Float(string='Cycles/Day')
    engine1_comp_ids = fields.One2many('ams_daily.component','eng1_daily_id',string='Engine #1 Component')

    engine2_hours = fields.Float(string='Hours/Day')
    engine2_cycles = fields.Float(string='Cycles/Day')
    engine2_comp_ids = fields.One2many('ams_daily.component','eng2_daily_id',string='Engine #2 Component')

    engine3_hours = fields.Float(string='Hours/Day')
    engine3_cycles = fields.Float(string='Cycles/Day')
    engine3_comp_ids = fields.One2many('ams_daily.component','eng3_daily_id',string='Engine #3 Component')

    engine4_hours = fields.Float(string='Hours/Day')
    engine4_cycles = fields.Float(string='Cycles/Day')
    engine4_comp_ids = fields.One2many('ams_daily.component','eng4_daily_id',string='Engine #4 Component')

    auxiliary1_hours = fields.Float(string='Hours/Day')
    auxiliary1_cycles = fields.Float(string='Cycles/Day')
    auxiliary1_comp_ids = fields.One2many('ams_daily.component','aux1_daily_id',string='Auxiliary #1 Component')

    propeller1_hours = fields.Float(string='Hours/Day')
    propeller1_cycles = fields.Float(string='Cycles/Day')
    propeller1_comp_ids = fields.One2many('ams_daily.component','prop1_daily_id',string='Propeller #1 Component')

    propeller2_hours = fields.Float(string='Hours/Day')
    propeller2_cycles = fields.Float(string='Cycles/Day')
    propeller2_comp_ids = fields.One2many('ams_daily.component','prop2_daily_id',string='Propeller #2 Component')

    propeller3_hours = fields.Float(string='Hours/Day')
    propeller3_cycles = fields.Float(string='Cycles/Day')
    propeller3_comp_ids = fields.One2many('ams_daily.component','prop3_daily_id',string='Propeller #3 Component')

    propeller4_hours = fields.Float(string='Hours/Day')
    propeller4_cycles = fields.Float(string='Cycles/Day')
    propeller4_comp_ids = fields.One2many('ams_daily.component','prop4_daily_id',string='Propeller #4 Component')

    # @api.onchange('start_date','end_date')
    # def _get_real(self):
    #     if self.start_date:
    #         f_date = datetime.strptime(str(self.start_date), '%Y-%m-%d')
    #         l_date = datetime.strptime(str(self.end_date), '%Y-%m-%d')
    #         delta = l_date - f_date
    #         if delta.days != 0:
    #             fml = self.env['ams_fml.log'].search([('date','=',self.start_date)]).ids
    #             print fml
    #             if fml:
    #                 self.aircraft_hours_real = (self.get_fml(fml)['hours']//delta.days)
    #                 self.aircraft_cycles_real = (self.get_fml(fml)['cycles']//delta.days)

    def get_fml(self, idnya):
        a = {}
        fml  = self.env['ams_fml.log'].search([('id','in',idnya)])
        a['hours'] = 0
        a['cycles'] = 0
        for x in fml:
            a['hours'] += x.total_hours
            a['cycles'] += x.total_cycles
        return a

    @api.one
    @api.onchange('start_date','end_date')
    def _onchange_dates(self):
        # print self.start_date
        if(self.start_date and self.end_date):
            f_date = datetime.strptime(self.start_date, '%Y-%m-%d')
            l_date = datetime.strptime(self.end_date, '%Y-%m-%d')
            delta = l_date - f_date
            # print delta.days
            if(delta.days <= 0):
                self.end_date = False
                # raise ValidationError(_("End Date should bigger than Start Date..."))
            else:
                fml = self.env['ams_fml.log'].search([('date','=',self.start_date)]).ids
                self.aircraft_hours_real = (self.get_fml(fml)['hours']//delta.days)
                self.aircraft_cycles_real = (self.get_fml(fml)['cycles']//delta.days)

    @api.onchange('aircraft_hours')
    def _onchange_aircraft_hours(self):
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

    @api.onchange('fleet_id')
    def _onchange_fleet_id(self):
        if not (self.id):
            self.engine1_id = self.fleet_id.engine_type_id
            self.engine2_id = self.fleet_id.engine2_type_id
            self.engine3_id = self.fleet_id.engine3_type_id
            self.engine4_id = self.fleet_id.engine4_type_id

            self.auxiliary1_id = self.fleet_id.auxiliary_type_id
            # self.auxiliary2_id = self.fleet_id.auxiliary2_type_id
            # self.auxiliary3_id = self.fleet_id.auxiliary3_type_id
            # self.auxiliary4_id = self.fleet_id.auxiliary4_type_id

            self.propeller1_id = self.fleet_id.propeller_type_id
            self.propeller2_id = self.fleet_id.propeller2_type_id
            self.propeller3_id = self.fleet_id.propeller3_type_id
            self.propeller4_id = self.fleet_id.propeller4_type_id

            self.aircraft_hours = 0
            self.aircraft_cycles = 0
            # GET AIRCRAFT COMPONENT

            self._onchange_aircraft_hours()
            self._onchange_aircraft_cycles()
            specomp = []
            for comp in self.fleet_id.component_ids:
                if(comp.not_follow_parent):
                    specomp.append((0, 0,{
                        # 'daily_id': self.id,
                        'component_id': comp.id,
                        'hours': self.aircraft_hours,
                        'cycles': self.aircraft_cycles,
                    }))
                for scomp in comp.sub_part_ids:
                    if(scomp.not_follow_parent):
                        specomp.append((0, 0,{
                            # 'daily_id': self.id,
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
                            # 'daily_id': self.id,
                            'component_id': comp.id,
                            'hours': self.aircraft_hours,
                            'cycles': self.aircraft_cycles,
                        }))
                    for scomp in comp.sub_part_ids:
                        if(scomp.not_follow_parent):
                            specomp.append((0, 0,{
                                # 'daily_id': self.id,
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
                            # 'daily_id': self.id,
                            'component_id': comp.id,
                            'hours': self.aircraft_hours,
                            'cycles': self.aircraft_cycles,
                        }))
                    for scomp in comp.sub_part_ids:
                        if(scomp.not_follow_parent):
                            specomp.append((0, 0,{
                                # 'daily_id': self.id,
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
                        # 'daily_id': self.id,
                        'component_id': comp.id,
                        'hours': self.aircraft_hours,
                        'cycles': self.aircraft_cycles,
                    }))
                for scomp in comp.sub_part_ids:
                    if(scomp.not_follow_parent):
                        specomp.append((0, 0,{
                            # 'daily_id': self.id,
                            'component_id': scomp.id,
                            'hours': self.aircraft_hours,
                            'cycles': self.aircraft_cycles,
                        }))
            self.auxiliary1_comp_ids = specomp

    @api.onchange('engine1_hours')
    def _onchange_engine1_hours(self):
        for comp in self.engine1_comp_ids:
            comp.hours = self.engine1_hours

    @api.onchange('engine1_cycles')
    def _onchange_engine1_cycles(self):
        for comp in self.engine1_comp_ids:
            comp.cycles = self.engine1_cycles

    @api.onchange('engine2_hours')
    def _onchange_engine2_hours(self):
        for comp in self.engine2_comp_ids:
            comp.hours = self.engine2_hours

    @api.onchange('engine2_cycles')
    def _onchange_engine2_cycles(self):
        for comp in self.engine2_comp_ids:
            comp.cycles = self.engine2_cycles

    @api.onchange('engine3_hours')
    def _onchange_engine3_hours(self):
        for comp in self.engine3_comp_ids:
            comp.hours = self.engine3_hours

    @api.onchange('engine3_cycles')
    def _onchange_engine3_cycles(self):
        for comp in self.engine3_comp_ids:
            comp.cycles = self.engine3_cycles

    @api.onchange('engine4_hours')
    def _onchange_engine4_hours(self):
        for comp in self.engine4_comp_ids:
            comp.hours = self.engine4_hours

    @api.onchange('engine4_cycles')
    def _onchange_engine4_cycles(self):
        for comp in self.engine4_comp_ids:
            comp.cycles = self.engine4_cycles

    @api.onchange('propeller1_hours')
    def _onchange_propeller1_hours(self):
        for comp in self.propeller1_comp_ids:
            comp.hours = self.propeller1_hours

    @api.onchange('propeller1_cycles')
    def _onchange_propeller1_cycles(self):
        for comp in self.propeller1_comp_ids:
            comp.cycles = self.propeller1_cycles

    @api.onchange('propeller2_hours')
    def _onchange_propeller2_hours(self):
        for comp in self.propeller2_comp_ids:
            comp.hours = self.propeller2_hours

    @api.onchange('propeller2_cycles')
    def _onchange_propeller2_cycles(self):
        for comp in self.propeller2_comp_ids:
            comp.cycles = self.propeller2_cycles

    @api.onchange('propeller3_hours')
    def _onchange_propeller3_hours(self):
        for comp in self.propeller3_comp_ids:
            comp.hours = self.propeller3_hours

    @api.onchange('propeller3_cycles')
    def _onchange_propeller3_cycles(self):
        for comp in self.propeller3_comp_ids:
            comp.cycles = self.propeller3_cycles

    @api.onchange('propeller4_hours')
    def _onchange_propeller4_hours(self):
        for comp in self.propeller4_comp_ids:
            comp.hours = self.propeller4_hours

    @api.onchange('propeller4_cycles')
    def _onchange_propeller4_cycles(self):
        for comp in self.propeller4_comp_ids:
            comp.cycles = self.propeller4_cycles

    @api.onchange('auxiliary1_hours')
    def _onchange_auxiliary1_hours(self):
        for comp in self.auxiliary1_comp_ids:
            comp.hours = self.auxiliary1_hours

    @api.onchange('auxiliary1_cycles')
    def _onchange_auxiliary1_cycles(self):
        for comp in self.auxiliary1_comp_ids:
            comp.cycles = self.auxiliary1_cycles

    @api.model
    def create(self, values):
        values['start_date'] = fields.Date.today()
        self.env['ams.daily'].search(['&',('fleet_id','=',values['fleet_id']),('is_active','=',True)]).write({
            'is_active' : False,
            'end_date' : fields.Date.today(),
            })
    
        return super(AmsDaily, self).create(values)

# UNTUK KEBUTUHAN COMPONENT KHUSUS
class AircraftFmlComp(models.Model):
    _name = 'ams_daily.component'
    _description = 'Component Log'

    ac_daily_id = fields.Many2one('ams.daily', string='Daily Utilization', readonly=True)
    eng1_daily_id = fields.Many2one('ams.daily', string='Daily Utilization', readonly=True)
    eng2_daily_id = fields.Many2one('ams.daily', string='Daily Utilization', readonly=True)
    eng3_daily_id = fields.Many2one('ams.daily', string='Daily Utilization', readonly=True)
    eng4_daily_id = fields.Many2one('ams.daily', string='Daily Utilization', readonly=True)
    aux1_daily_id = fields.Many2one('ams.daily', string='Daily Utilization', readonly=True)
    prop1_daily_id = fields.Many2one('ams.daily', string='Daily Utilization', readonly=True)
    prop2_daily_id = fields.Many2one('ams.daily', string='Daily Utilization', readonly=True)
    prop3_daily_id = fields.Many2one('ams.daily', string='Daily Utilization', readonly=True)
    prop4_daily_id = fields.Many2one('ams.daily', string='Daily Utilization', readonly=True)

    component_id = fields.Many2one('ams.component.part', string='Component', readonly=True)
    hours = fields.Float(string='Component Hours')
    cycles = fields.Integer(string='Component Cycles')