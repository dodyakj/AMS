# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import json, time
from websocket import create_connection

class calm_correction(models.Model):
    _name = 'calm.correction'

    fleet_id = fields.Many2one('aircraft.acquisition', string='Fleet Id')
    logs = fields.Text(string='Log')

    @api.model
    def create(self, values):
        log = ''
        acraft = ro = self.env['aircraft.acquisition'].search([('id','=',values['fleet_id'])])
        arrays = ['fleet','engine1','engine2','engine3','engine4','propeller1','propeller2','propeller3','propeller4','auxiliary1']

        # SET TSN TSO PROPELLER
        if(acraft.propeller_type_id.id != False):
            acraft.propeller_type_id.propeller_tsn = acraft.propeller_type_id.total_hours
        if(acraft.propeller2_type_id.id != False):
            acraft.propeller2_type_id.propeller_tsn = acraft.propeller2_type_id.total_hours 
        if(acraft.propeller3_type_id.id != False):
            acraft.propeller3_type_id.propeller_tsn = acraft.propeller3_type_id.total_hours 
        if(acraft.propeller4_type_id.id != False):
            acraft.propeller4_type_id.propeller_tsn = acraft.propeller4_type_id.total_hours 
            
        for eng in arrays:
            if(eng == 'fleet'):
                ro = acraft.component_ids
            elif(eng == 'engine1'):
                ro = acraft.engine_type_id.component_ids
            elif(eng == 'engine2'):
                ro = acraft.engine2_type_id.component_ids
            elif(eng == 'engine3'):
                ro = acraft.engine3_type_id.component_ids
            elif(eng == 'engine4'):
                ro = acraft.engine4_type_id.component_ids
            elif(eng == 'propeller1'):
                ro = acraft.propeller_type_id.component_ids
            elif(eng == 'propeller2'):
                ro = acraft.propeller2_type_id.component_ids
            elif(eng == 'propeller3'):
                ro = acraft.propeller3_type_id.component_ids
            elif(eng == 'propeller4'):
                ro = acraft.propeller4_type_id.component_ids
            elif(eng == 'auxiliary1'):
                ro = acraft.auxiliary_type_id.component_ids
            for g in ro:
                for slive in g.serfice_life:
                    if(slive.action_type == 'retirement' or slive.action_type == 'oncondition'):
                        # set component TSN
                        if(slive.unit == 'hours'):
                            if(g.tsn != slive.at_install + (slive.value - slive.remaining)):
                                log + '#'
                            log += 'tsn :: ' + (str(g.product_id.name) + '-' + str(g.serial_number.name) + ':' + str(g.tsn) + '/' + str(slive.at_install + (slive.value - slive.remaining)) + '\n')
                            g.tsn = slive.at_install + (slive.value - slive.remaining)
                        elif(slive.unit == 'cycles'):
                            if(g.csn != slive.at_install + (slive.value - slive.remaining)):
                                log + '#'
                            log += 'csn :: ' + (str(g.product_id.name) + '-' + str(g.serial_number.name) + ':' + str(g.csn) + '/' + str(slive.at_install + (slive.value - slive.remaining)) + '\n')
                            g.csn = slive.at_install + (slive.value - slive.remaining)
                    elif(slive.action_type == 'overhaul'):
                        # set component TSO
                        if(slive.unit == 'hours'):
                            if(g.tso != slive.at_install + (slive.value - slive.remaining)):
                                log + '#'
                            log += 'tso :: ' + (str(g.product_id.name) + '-' + str(g.serial_number.name) + ':' + str(g.tso) + '/' + str(slive.at_install + (slive.value - slive.remaining)) + '\n')
                            g.tso = slive.at_install + (slive.value - slive.remaining)
                        elif(slive.unit == 'cycles'):
                            if(g.cso != slive.at_install + (slive.value - slive.remaining)):
                                log + '#'
                            log += 'cso :: ' + (str(g.product_id.name) + '-' + str(g.serial_number.name) + ':' + str(g.cso) + '/' + str(slive.at_install + (slive.value - slive.remaining)) + '\n')
                            g.cso = slive.at_install + (slive.value - slive.remaining)
                    print g.product_id.name
                for sg in g.sub_part_ids:
                    for slive in sg.serfice_life:
                        if(slive.action_type == 'retirement' or slive.action_type == 'oncondition'):
                            # set component TSN
                            if(slive.unit == 'hours'):
                                if(sg.tsn != slive.at_install + (slive.value - slive.remaining)):
                                    log + '#'
                                log += 'tsn :: ' + (str(sg.product_id.name) + '-' + str(sg.serial_number.name) + ':' + str(sg.tsn) + '/' + str(slive.at_install + (slive.value - slive.remaining)) + '\n')
                                sg.tsn = slive.at_install + (slive.value - slive.remaining)
                            elif(slive.unit == 'cycles'):
                                if(sg.csn != slive.at_install + (slive.value - slive.remaining)):
                                    log + '#'
                                log += 'csn :: ' + (str(sg.product_id.name) + '-' + str(sg.serial_number.name) + ':' + str(sg.csn) + '/' + str(slive.at_install + (slive.value - slive.remaining)) + '\n')
                                sg.csn = slive.at_install + (slive.value - slive.remaining)
                        elif(slive.action_type == 'overhaul'):
                            # set component TSO
                            if(slive.unit == 'hours'):
                                if(sg.tso != slive.at_install + (slive.value - slive.remaining)):
                                    log + '#'
                                log += 'tso :: ' + (str(sg.product_id.name) + '-' + str(sg.serial_number.name) + ':' + str(sg.tso) + '/' + str(slive.at_install + (slive.value - slive.remaining)) + '\n')
                                sg.tso = slive.at_install + (slive.value - slive.remaining)
                            elif(slive.unit == 'cycles'):
                                if(sg.cso != slive.at_install + (slive.value - slive.remaining)):
                                    log + '#'
                                log += 'cso :: ' + (str(sg.product_id.name) + '-' + str(sg.serial_number.name) + ':' + str(sg.cso) + '/' + str(slive.at_install + (slive.value - slive.remaining)) + '\n')
                                sg.cso = slive.at_install + (slive.value - slive.remaining)
                    print sg.product_id.name
                print g.product_id.name
        values['logs'] = log
        # ws = create_connection("ws://paiis.pelita-air.com:8000/dashboard")
        # ws.send(json.dumps({"platform": "ams", "method": "calm_correction","message":'All import'}))
        # result =  ws.recv()
        # ws.close()
        # time.sleep(3)
        return super(calm_correction, self).create(values)