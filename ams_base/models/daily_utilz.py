# -*- coding: utf-8 -*-

from odoo import models, fields, api

class VerifyFlight(models.Model):
    _name = 'ams.daily_utilization'

    aircraft_id = fields.Many2one('aircraft.acquisition', string="Airframes")
    
    starting_date = fields.Datetime(string='Starting Date')
    end_date = fields.Datetime(string='End Date')

    aircraft_hours = fields.Float(string='Aircraft Hours')
    aircraft_cycles = fields.Float(string='Aircraft Cycles')

    aircraft_comp_ids = fields.One2many(comodel_name='ams_utilz.component.airframe',inverse_name='ac_fml_id',string='Aircraft Component')

    engine1_id = fields.Many2one('engine.type', string='Engine #1')
    engine1_id_text = fields.Char(string='Engine #1',related='engine1_id.name')
    engine2_id = fields.Many2one('engine.type', string='Engine #2')
    engine2_id_text = fields.Char(string='Engine #2',related='engine2_id.name')
    engine3_id = fields.Many2one('engine.type', string='Engine #3')
    engine3_id_text = fields.Char(string='Engine #3',related='engine3_id.name')
    engine4_id = fields.Many2one('engine.type', string='Engine #4')
    engine4_id_text = fields.Char(string='Engine #4',related='engine4_id.name')

    auxiliary1_id = fields.Many2one('auxiliary.type', string='Auxiliary #1')
    auxiliary1_id_text = fields.Char(string='Auxiliary #1',related='auxiliary1_id.name')
    auxiliary2_id = fields.Many2one('auxiliary.type', string='Auxiliary #2')
    auxiliary2_id_text = fields.Char(string='Auxiliary #2',related='auxiliary2_id.name')
    auxiliary3_id = fields.Many2one('auxiliary.type', string='Auxiliary #3')
    auxiliary3_id_text = fields.Char(string='Auxiliary #3',related='auxiliary3_id.name')
    auxiliary4_id = fields.Many2one('auxiliary.type', string='Auxiliary #4')
    auxiliary4_id_text = fields.Char(string='Auxiliary #4',related='auxiliary4_id.name')

    engine1_hours = fields.Float(string='Hours')
    engine1_cycles = fields.Float(string='Cycles')
    engine1_power = fields.Float(string='Power')
    engine1_torque = fields.Float(string='Torque')
    engine1_comp_ids = fields.One2many(comodel_name='ams_utilz.component.airframe',inverse_name='eng1_fml_id',string='Engine #1 Component')

    engine2_hours = fields.Float(string='Hours')
    engine2_cycles = fields.Float(string='Cycles')
    engine2_power = fields.Float(string='Power')
    engine2_torque = fields.Float(string='Torque')
    engine2_comp_ids = fields.One2many(comodel_name='ams_utilz.component.airframe',inverse_name='eng2_fml_id',string='Engine #2 Component')

    engine3_hours = fields.Float(string='Hours')
    engine3_cycles = fields.Float(string='Cycles')
    engine3_power = fields.Float(string='Power')
    engine3_torque = fields.Float(string='Torque')
    engine3_comp_ids = fields.One2many(comodel_name='ams_utilz.component.airframe',inverse_name='eng3_fml_id',string='Engine #3 Component')

    engine4_hours = fields.Float(string='Hours')
    engine4_cycles = fields.Float(string='Cycles')
    engine4_power = fields.Float(string='Power')
    engine4_torque = fields.Float(string='Torque')
    engine4_comp_ids = fields.One2many(comodel_name='ams_utilz.component.airframe',inverse_name='eng4_fml_id',string='Engine #4 Component')

    auxiliary1_hours = fields.Float(string='Auxiliary #1 Hours')
    auxiliary1_cycles = fields.Float(string='Auxiliary #1 Cycles')
    auxiliary1_comp_ids = fields.One2many(comodel_name='ams_utilz.component.airframe',inverse_name='aux1_fml_id',string='Auxiliary #1 Component')

    auxiliary2_hours = fields.Float(string='Auxiliary #2 Hours')
    auxiliary2_cycles = fields.Float(string='Auxiliary #2 Cycles')
    auxiliary2_comp_ids = fields.One2many(comodel_name='ams_utilz.component.airframe',inverse_name='aux2_fml_id',string='Auxiliary #2 Component')

    auxiliary3_hours = fields.Float(string='Auxiliary #3 Hours')
    auxiliary3_cycles = fields.Float(string='Auxiliary #3 Cycles')
    auxiliary3_comp_ids = fields.One2many(comodel_name='ams_utilz.component.airframe',inverse_name='aux3_fml_id',string='Auxiliary #3 Component')

    auxiliary4_hours = fields.Float(string='Auxiliary #4 Hours')
    auxiliary4_cycles = fields.Float(string='Auxiliary #4 Cycles')
    auxiliary4_comp_ids = fields.One2many(comodel_name='ams_utilz.component.airframe',inverse_name='aux4_fml_id',string='Auxiliary #4 Component')

    @api.onchange('aircraft_id')
    def _onchange_aircraft_id(self):
        if not (self.id):
            if self.aircraft_id.auxiliary_type_id:
                self.aircraft_hours = 0
                self.aircraft_cycles = 0
                self.engine1_id = self.aircraft_id.engine_type_id
                self.engine2_id = self.aircraft_id.engine2_type_id
                self.engine3_id = self.aircraft_id.engine3_type_id
                self.engine4_id = self.aircraft_id.engine4_type_id

                self.auxiliary1_id = self.aircraft_id.auxiliary_type_id
                self.auxiliary2_id = self.aircraft_id.auxiliary2_type_id
                self.auxiliary3_id = self.aircraft_id.auxiliary3_type_id
                self.auxiliary4_id = self.aircraft_id.auxiliary4_type_id

            # GET AIRCRAFT COMPONENT
            specomp = []
            for comp in self.aircraft_id.component_ids:
                if(comp.not_follow_parent):
                    specomp.append((0, 0,{
                        # 'fml_id': self.id,
                        'component_id': comp.id,
                        'hours': 0,
                        'cycles': 0,
                    }))
                for scomp in comp.sub_part_ids:
                    if(scomp.not_follow_parent):
                        specomp.append((0, 0,{
                            # 'fml_id': self.id,
                            'component_id': scomp.id,
                            'hours': 0,
                            'cycles': 0,
                        }))
            self.aircraft_comp_ids = specomp
            # GET ENGINE 1 COMPONENT
            specomp = []
            for comp in self.engine1_id.component_ids:
                if(comp.not_follow_parent):
                    specomp.append((0, 0,{
                        # 'fml_id': self.id,
                        'component_id': comp.id,
                        'hours': 0,
                        'cycles': 0,
                    }))
                for scomp in comp.sub_part_ids:
                    if(scomp.not_follow_parent):
                        specomp.append((0, 0,{
                            # 'fml_id': self.id,
                            'component_id': scomp.id,
                            'hours': 0,
                            'cycles': 0,
                        }))
            self.engine1_comp_ids = specomp
            # GET ENGINE 2 COMPONENT
            specomp = []
            for comp in self.engine2_id.component_ids:
                if(comp.not_follow_parent):
                    specomp.append((0, 0,{
                        # 'fml_id': self.id,
                        'component_id': comp.id,
                        'hours': 0,
                        'cycles': 0,
                    }))
                for scomp in comp.sub_part_ids:
                    if(scomp.not_follow_parent):
                        specomp.append((0, 0,{
                            # 'fml_id': self.id,
                            'component_id': scomp.id,
                            'hours': 0,
                            'cycles': 0,
                        }))
            self.engine2_comp_ids = specomp
            # GET ENGINE 3 COMPONENT
            specomp = []
            for comp in self.engine3_id.component_ids:
                if(comp.not_follow_parent):
                    specomp.append((0, 0,{
                        # 'fml_id': self.id,
                        'component_id': comp.id,
                        'hours': 0,
                        'cycles': 0,
                    }))
                for scomp in comp.sub_part_ids:
                    if(scomp.not_follow_parent):
                        specomp.append((0, 0,{
                            # 'fml_id': self.id,
                            'component_id': scomp.id,
                            'hours': 0,
                            'cycles': 0,
                        }))
            self.engine3_comp_ids = specomp
            # GET ENGINE 4 COMPONENT
            specomp = []
            for comp in self.engine4_id.component_ids:
                if(comp.not_follow_parent):
                    specomp.append((0, 0,{
                        # 'fml_id': self.id,
                        'component_id': comp.id,
                        'hours': 0,
                        'cycles': 0,
                    }))
                for scomp in comp.sub_part_ids:
                    if(scomp.not_follow_parent):
                        specomp.append((0, 0,{
                            # 'fml_id': self.id,
                            'component_id': scomp.id,
                            'hours': 0,
                            'cycles': 0,
                        }))
            self.engine4_comp_ids = specomp
            # GET AUXILIARY 1 COMPONENT
            specomp = []
            for comp in self.auxiliary1_id.component_ids:
                if(comp.not_follow_parent):
                    specomp.append((0, 0,{
                        # 'fml_id': self.id,
                        'component_id': comp.id,
                        'hours': 0,
                        'cycles': 0,
                    }))
                for scomp in comp.sub_part_ids:
                    if(scomp.not_follow_parent):
                        specomp.append((0, 0,{
                            # 'fml_id': self.id,
                            'component_id': scomp.id,
                            'hours': 0,
                            'cycles': 0,
                        }))
            self.auxiliary1_comp_ids = specomp
            # GET AUXILIARY 2 COMPONENT
            specomp = []
            for comp in self.auxiliary2_id.component_ids:
                if(comp.not_follow_parent):
                    specomp.append((0, 0,{
                        # 'fml_id': self.id,
                        'component_id': comp.id,
                        'hours': 0,
                        'cycles': 0,
                    }))
                for scomp in comp.sub_part_ids:
                    if(scomp.not_follow_parent):
                        specomp.append((0, 0,{
                            # 'fml_id': self.id,
                            'component_id': scomp.id,
                            'hours': 0,
                            'cycles': 0,
                        }))
            self.auxiliary2_comp_ids = specomp
            # GET AUXILIARY 3 COMPONENT
            specomp = []
            for comp in self.auxiliary3_id.component_ids:
                if(comp.not_follow_parent):
                    specomp.append((0, 0,{
                        # 'fml_id': self.id,
                        'component_id': comp.id,
                        'hours': 0,
                        'cycles': 0,
                    }))
                for scomp in comp.sub_part_ids:
                    if(scomp.not_follow_parent):
                        specomp.append((0, 0,{
                            # 'fml_id': self.id,
                            'component_id': scomp.id,
                            'hours': 0,
                            'cycles': 0,
                        }))
            self.auxiliary3_comp_ids = specomp
            # GET AUXILIARY 4 COMPONENT
            specomp = []
            for comp in self.auxiliary4_id.component_ids:
                if(comp.not_follow_parent):
                    specomp.append((0, 0,{
                        # 'fml_id': self.id,
                        'component_id': comp.id,
                        'hours': 0,
                        'cycles': 0,
                    }))
                for scomp in comp.sub_part_ids:
                    if(scomp.not_follow_parent):
                        specomp.append((0, 0,{
                            # 'fml_id': self.id,
                            'component_id': scomp.id,
                            'hours': 0,
                            'cycles': 0,
                        }))
            self.auxiliary4_comp_ids = specomp

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

        # SET AUXILIARY HOURS
        if(self.auxiliary1_id):
            self.auxiliary1_hours = self.aircraft_hours
        else:
            self.auxiliary1_hours = 0

        if(self.auxiliary2_id):
            self.auxiliary2_hours = self.aircraft_hours
        else:
            self.auxiliary2_hours = 0

        if(self.auxiliary3_id):
            self.auxiliary3_hours = self.aircraft_hours
        else:
            self.auxiliary3_hours = 0

        if(self.auxiliary4_id):
            self.auxiliary4_hours = self.aircraft_hours
        else:
            self.auxiliary4_hours = 0

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

        # SET AUXILIARY cycles
        if(self.auxiliary1_id):
            self.auxiliary1_cycles = self.aircraft_cycles
        else:
            self.auxiliary1_cycles = 0

        if(self.auxiliary2_id):
            self.auxiliary2_cycles = self.aircraft_cycles
        else:
            self.auxiliary2_cycles = 0

        if(self.auxiliary3_id):
            self.auxiliary3_cycles = self.aircraft_cycles
        else:
            self.auxiliary3_cycles = 0

        if(self.auxiliary4_id):
            self.auxiliary4_cycles = self.aircraft_cycles
        else:
            self.auxiliary4_cycles = 0

        # AIRFRAME COMPONENT
        for comp in self.aircraft_comp_ids:
            comp.cycles = self.aircraft_cycles


# UNTUK KEBUTUHAN COMPONENT KHUSUS
class AircraftFmlComp(models.Model):
    _name = 'ams_utilz.component.airframe'
    _description = 'Component Log'

    ac_fml_id = fields.Many2one('ams.daily_utilization', string='FML', readonly=True)
    eng1_fml_id = fields.Many2one('ams.daily_utilization', string='FML', readonly=True)
    eng2_fml_id = fields.Many2one('ams.daily_utilization', string='FML', readonly=True)
    eng3_fml_id = fields.Many2one('ams.daily_utilization', string='FML', readonly=True)
    eng4_fml_id = fields.Many2one('ams.daily_utilization', string='FML', readonly=True)
    aux1_fml_id = fields.Many2one('ams.daily_utilization', string='FML', readonly=True)
    aux2_fml_id = fields.Many2one('ams.daily_utilization', string='FML', readonly=True)
    aux3_fml_id = fields.Many2one('ams.daily_utilization', string='FML', readonly=True)
    aux4_fml_id = fields.Many2one('ams.daily_utilization', string='FML', readonly=True)

    component_id = fields.Many2one('ams.component.part', string='Component', readonly=True)
    hours = fields.Float(string='Component Hours')
    cycles = fields.Integer(string='Component Cycles')
