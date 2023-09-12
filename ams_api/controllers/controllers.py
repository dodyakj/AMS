# -*- coding: utf-8 -*-
import logging
import pprint
import werkzeug
from werkzeug.wrappers import Response
import json

from odoo import http
from odoo.http import request
from datetime import date, datetime


_logger = logging.getLogger(__name__)

class AmsAuth(http.Controller):
    @http.route('/auth', type='http', auth='public', csrf=False, sitemap=False)
    def authenticate(self):
        user_id = request.env['res.users'].sudo().search([('id','=',request.uid)])
        if user_id:
            data = {
                "jsonrpc": "2.0",
                "params": {
                    "login": user_id.login,
                    "password": user_id.password,
                }
            }
            return Response(json.dumps(data),content_type='text',status=200)
        else:
            raise werkzeug.exceptions.BadRequest("Please Log in Fist")


class AmsApi(http.Controller):
    @http.route(['/unserviceable/1.0/',], type='http', auth="public", website=True, csrf=False)
    def get_aircraft_remark(self):
        res = request.env['aircraft.acquisition'].sudo().search([('aircraft_status','=', False)])
        result = []
        for record in res:
            result.append({
                'status_aircraft_id': record.name,
                'status_remark': record.remark,
            })
        return Response(json.dumps(result),content_type='text',status=200)

    @http.route(['/maintenance_planning/1.0/',], type='http', auth="public", website=True, csrf=False)
    def get_aircraft_planning(self):
        res = request.env['maintenance.request'].sudo().search([])
        result = []
        for record in res:
            result.append({
                'status_aircraft_id': record.fl_acquisition_id.name,
                'status_reason_maintenance': record.reason_maintenance,
                'status_request_date': record.request_date,
                'status_schedule_date': record.schedule_date,
                'status_maintenance_team': record.maintenance_team_id.name,
            })
        return Response(json.dumps(result),content_type='text',status=200)

    @http.route(['/aircraft_status/1.0/',], type='http', auth="public", website=True, csrf=False)
    def get_aircraft_status(self):
        res = request.env['aircraft.acquisition'].sudo().search([])
        
        result = []
        for record in res:

            # s/n, c of a, r dll
            certificates = []
            for certificate in record.document_ids:
                certificates.append({
                    'name':certificate.document_id.name,
                    'date_expired':certificate.date_expired
                })

            # maintenance planning
            planning = []
            for plan in request.env['maintenance.request'].sudo().search([('fl_acquisition_id','=',record.id)]):
                planning.append({
                    'name':plan.name,
                    'schedule_date':plan.schedule_date,
                    'request_date':plan.request_date,
                    'date_finished':plan.date_finished,
                    'close_date':plan.close_date,
                })

            remaining_date = []
            remaining_hours = []
            remaining_cycle = []
            remaining_rin = []
            due_date = []
            due_hours = []
            due_cycle = []
            due_rin = []
            for component in record.component_ids:
                for servicelife in component.serfice_life:
                    # field treatment yang bukan on condition atau condition monitoring
                    if servicelife.action_type not in ['oncondition','conditionmonitoring']:
                        if servicelife.unit == 'hours':
                            # print 'hours '+str(servicelife.remaining)
                            remaining_hours.append(servicelife.remaining)
                            due_hours.append(servicelife.current)
                        elif servicelife.unit == 'cycles':
                            # print 'cycle '+str(servicelife.remaining)
                            remaining_cycle.append(servicelife.remaining)
                            due_cycle.append(servicelife.current)
                        elif servicelife.unit == 'rin':
                            # print 'rin '+str(servicelife.remaining)
                            remaining_rin.append(servicelife.remaining)
                            due_rin.append(servicelife.current)
                        elif servicelife.unit in ['days','month','year']:
                            # print servicelife.next_date
                            remaining_date.append(servicelife.remaining)
                            due_date.append(servicelife.current)

            result.append({
                'aircraft_id':{
                    'id':record.aircraft_name.id,
                    'reg':record.name,
                    'type':record.aircraft_type_id.name,
                    'category':record.category,
                    'status':record.status,
                    's_n':record.vin_sn,
                    'state': 'serviceable' if record.aircraft_status == True else 'unserviceable',
                    },
                'certificates':certificates,
                'planning':planning,
                'service_life':{
                    'remaining_date':min(remaining_date) if len(remaining_date) > 0 else False,
                    'remaining_hours':min(remaining_hours) if len(remaining_hours) > 0 else False,
                    'remaining_cycle':min(remaining_cycle) if len(remaining_cycle) > 0 else False,
                    'remaining_rin':min(remaining_rin) if len(remaining_rin) > 0 else False,
                    # 'remaining_description':record.remaining_description,
                    'due_date':min(due_date) if len(due_date) > 0 else False,
                    'due_hours':min(due_hours) if len(due_hours) > 0 else False,
                    'due_cycle':min(due_cycle) if len(due_cycle) > 0 else False,
                    'due_rin':min(due_rin) if len(due_rin) > 0 else False,
                },
                'charterer':record.rent_by,
                'location':{
                    'id':record.location.id,
                    'name':record.location.name
                },
                'last_inspection':record.last_inspection,
                'next_inspection':record.next_inspection,
                'total_hours':record.total_hours,
                'total_cycle':record.total_landings,
                'write_date':record.write_date,
            })
        return Response(json.dumps(result),content_type='text',status=200)

    @http.route(['/aircraft_status/2.0/',], type='http', auth="public", website=True, csrf=False)
    def get_aircraft_status_v2(self):
        res = request.env['aircraft.acquisition'].sudo().search([('is_deleted','=',False)])
        result = []
        serviceable = 0
        unserviceable = 0
        remark = []
        astatlist = []

        for record in res:
            remaining_date = []
            remaining_hours = []
            remaining_cycle = []
            remaining_rin = []
            due_date = []
            due_hours = []
            due_cycle = []
            due_rin = []
            if(record.aircraft_status == False):
                unserviceable += 1
                if(record.remark):
                    remark.append([record.name,record.remark,"OPEN"])
            else:
                serviceable += 1
            
            document = {}
            for doc in record.document_ids:
                document[doc.document_id.name] = doc.date_expired

            all_engine = []
            if(record.engine_type_id.id != False):
                all_engine.append(record.engine_type_id.id)
            if(record.engine2_type_id.id != False):
                all_engine.append(record.engine2_type_id.id)
            if(record.engine3_type_id.id != False):
                all_engine.append(record.engine3_type_id.id)
            if(record.engine4_type_id.id != False):
                all_engine.append(record.engine4_type_id.id)

            all_propeller = []
            if(record.propeller_type_id.id != False):
                all_propeller.append(record.propeller_type_id.id)
            if(record.propeller2_type_id.id != False):
                all_propeller.append(record.propeller2_type_id.id)
            if(record.propeller3_type_id.id != False):
                all_propeller.append(record.propeller3_type_id.id)
            if(record.propeller4_type_id.id != False):
                all_propeller.append(record.propeller4_type_id.id)

            all_auxiliary = []
            if(record.auxiliary_type_id.id != False):
                all_auxiliary.append(record.auxiliary_type_id.id)

            acraft_part = request.env['ams.component.part'].sudo().search(['|',('fleet_id','=',record.id),'|',('part_id.fleet_id','=',record.id),'|',('engine_id','in',all_engine),'|',('part_id.engine_id','in',all_engine),'|',('propeller_id','in',all_propeller),'|',('part_id.propeller_id','in',all_propeller),'|',('auxiliary_id','in',all_auxiliary),('part_id.auxiliary_id','in',all_auxiliary)]).mapped('id')
            acraft_insp = request.env['ams.inspection'].sudo().search(['|',('fleet_id','=',record.id),'|',('engine_id','in',all_engine),'|',('propeller_id','in',all_propeller),('auxiliary_id','in',all_auxiliary)]).mapped('id')
            min_ac_hour = request.env['ams.component.servicelife'].sudo().search(['&',('is_major','=',True),'&',('unit','=','hours'),'|',('inspection_id','in',acraft_insp),('part_id','in',acraft_part)],order='remaining ASC',limit=1).remaining
            min_ac_date = request.env['ams.component.servicelife'].sudo().search(['&',('is_major','=',True),'&',('unit','in',['days','month','year']),'|',('inspection_id','in',acraft_insp),('part_id','in',acraft_part)],order='next_date ASC',limit=1).next_date
            min_cal_date = request.env['document.certificate'].sudo().search([('acquisition_id','=',record.id)],order='date_expired ASC',limit=1).date_expired

            rem_hour = (min_ac_hour if min_ac_hour > 0 else '')
            rem_date = min_ac_date if min_ac_date < min_cal_date and min_ac_date != False else min_cal_date

            rem_date = ('' if (rem_date == False) else str((datetime.strptime(rem_date, "%Y-%m-%d") - datetime.now()).days)*-1)


            result.append({
                'status_aircraft_id':record.name,
                'status_aircraft_status_id': 'Serviceable' if record.aircraft_status == True else 'Unserviceable',
                'status_serviceable_status_id':record.status,
                'status_remaining_hours':rem_hour,
                # 'status_remaining_hours':rem_hour if rem_hour != '' else 0,
                'status_remaining_date':rem_date,
                # 'status_remaining_date':rem_date if rem_date != '' else 0,
                'status_remaining_description':'',
                'status_charterer_id': record.rent_by,
                'status_location_id': record.location.name,
                'status_last_inspection': datetime.strptime(record.last_inspection_date, '%Y-%m-%d').strftime('%Y-%m-%d') if record.last_inspection_date else False,
                'status_next_inspection': record.next_inspection if record.next_inspection != '' else False,
                'status_updated_date': datetime.strptime(record.write_date , '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'),
                'status_total_hours': record.total_hours,
                'status_total_cycle': record.total_landings,
                'status_due_date': min(due_date) if len(due_date) > 0 else False,
                'status_due_hours' : min(due_hours) if len(due_hours) > 0 else False
            })
        return Response(json.dumps(result),content_type='text',status=200)


    @http.route(['/aircraft',], type='http', auth="public", website=True, csrf=False)
    def get_aircrafts(self):
        res = request.env['aircraft.aircraft'].sudo().search([])
        
        result = []
        for record in res:
            result.append({
                'id':record.id,
                'name':record.name,
            })
        
        return Response(json.dumps(result),content_type='application/json;charset=utf-8',status=200)


    @http.route(['/location',], type='http', auth="public", website=True, csrf=False)
    def get_locations(self):
        res = request.env['base.operation'].sudo().search([])
        
        result = []
        for record in res:
            result.append({
                'id':record.id,
                'name':record.name,
            })
        
        return Response(json.dumps(result),content_type='application/json;charset=utf-8',status=200)

    # GINRO ===============================================================================================
    # =====================================================================================================
    @http.route(['/pelita_dashboard/maintenance_dashboard_aircraft_status/data_astat/signage_',], type="http", auth='public',  methods=['POST','GET'], website=True, cors='*', csrf=False)
    def signage_astat(self, **kw):
        num_rows = 0
        serviceable = 0
        unserviceable = 0
        remark = []
        astatlist = []
        ro = request.env['aircraft.acquisition'].sudo().search([('is_deleted','=',False)])

        for g in ro:
            num_rows += 1
            if(g.aircraft_status == False):
                unserviceable += 1
                if(g.remark):
                    remark.append([g.name,g.remark,"OPEN"])
            else:
                serviceable += 1
            
            document = {}
            for doc in g.document_ids:
                document[doc.document_id.name] = doc.date_expired

            all_engine = []
            if(g.engine_type_id.id != False):
                all_engine.append(g.engine_type_id.id)
            if(g.engine2_type_id.id != False):
                all_engine.append(g.engine2_type_id.id)
            if(g.engine3_type_id.id != False):
                all_engine.append(g.engine3_type_id.id)
            if(g.engine4_type_id.id != False):
                all_engine.append(g.engine4_type_id.id)

            all_propeller = []
            if(g.propeller_type_id.id != False):
                all_propeller.append(g.propeller_type_id.id)
            if(g.propeller2_type_id.id != False):
                all_propeller.append(g.propeller2_type_id.id)
            if(g.propeller3_type_id.id != False):
                all_propeller.append(g.propeller3_type_id.id)
            if(g.propeller4_type_id.id != False):
                all_propeller.append(g.propeller4_type_id.id)

            all_auxiliary = []
            if(g.auxiliary_type_id.id != False):
                all_auxiliary.append(g.auxiliary_type_id.id)

            acraft_part = request.env['ams.component.part'].sudo().search(['|',('fleet_id','=',g.id),'|',('part_id.fleet_id','=',g.id),'|',('engine_id','in',all_engine),'|',('part_id.engine_id','in',all_engine),'|',('propeller_id','in',all_propeller),'|',('part_id.propeller_id','in',all_propeller),'|',('auxiliary_id','in',all_auxiliary),('part_id.auxiliary_id','in',all_auxiliary)]).mapped('id')
            acraft_insp = request.env['ams.inspection'].sudo().search(['|',('fleet_id','=',g.id),'|',('engine_id','in',all_engine),'|',('propeller_id','in',all_propeller),('auxiliary_id','in',all_auxiliary)]).mapped('id')
            min_ac_hour = request.env['ams.component.servicelife'].sudo().search(['&',('is_major','=',True),'&',('unit','=','hours'),'|',('inspection_id','in',acraft_insp),('part_id','in',acraft_part)],order='remaining ASC',limit=1).remaining
            min_ac_date = request.env['ams.component.servicelife'].sudo().search(['&',('is_major','=',True),'&',('unit','in',['days','month','year']),'|',('inspection_id','in',acraft_insp),('part_id','in',acraft_part)],order='next_date ASC',limit=1).next_date
            min_cal_date = request.env['document.certificate'].sudo().search([('acquisition_id','=',g.id)],order='date_expired ASC',limit=1).date_expired

            rem_hour = (min_ac_hour if min_ac_hour > 0 else '')
            rem_date = min_ac_date if min_ac_date < min_cal_date and min_ac_date != False else min_cal_date

            rem_date = ('' if (rem_date == False) else str((datetime.strptime(rem_date, "%Y-%m-%d") - datetime.now()).days)*-1)

            astatlist.append([num_rows,
                '<span style="height:40px;display:table;padding-top:6%;padding-left:4%;">'+str(g.aircraft_type_id.name)+'</span>',
                '<a style="height:40px;display:table;padding-top:6%;padding-left:4%;" class="ajaxify" href="javascript:void(0)">'+str(g.name)+'</a>',
                '<span style="height:40px;display:table;padding-top:6%;padding-left:4%;">'+str('Fixed Wing' if g.category == 'fixedwing' else 'Rotary Wing')+'</span>',
                '<span style="width:140px;height:40px;display:table;background-color:'+str('#2ECC71' if g.aircraft_status == True else '#E74C3C')+';color:#E8FAEF;font-weight:bold;padding-top:6%;padding-left:4%;">'+str('S' if g.aircraft_status == True else 'US')+'</span>',
                '<span style="height:40px;display:table;padding-top:6%;padding-left:4%; font-weight: bold;">'+str(g.status)+'</span>',
                '<span style="height:40px;display:table;padding-top:6%;padding-left:4%;">'+str(rem_hour)+'</span>',
                '<span style="height:40px;display:table;padding-top:6%;padding-left:4%;">'+str(rem_date)+'</span>',
                '<span style="height:40px;display:table;padding-top:6%;padding-left:4%;">'+str(g.vin_sn)+'</span>',
                '<span style="height:40px;display:table;padding-top:6%;padding-left:4%;">'+(str(document['MFR'] if 'MFR' in document else ''))+'</span>',
                '<span style="height:40px;display:table;padding-top:6%;padding-left:4%;">'+(str(document['C of A'] if 'C of A' in document else ''))+'</span>',
                '<span style="height:40px;display:table;padding-top:6%;padding-left:4%;">'+(str(document['C of R'] if 'C of R' in document else ''))+'</span>',
                '<span style="height:40px;display:table;padding-top:6%;padding-left:4%;">'+(str(document['W & B'] if 'W & B' in document else ''))+'</span>',
                '<span style="height:40px;display:table;padding-top:6%;padding-left:4%;">'+(str(document['Compass Swing'] if 'Compass Swing' in document else ''))+'</span>',
                '<span style="height:40px;display:table;padding-top:6%;padding-left:4%;">'+(str(document['Radio Permit'] if 'Radio Permit' in document else ''))+'</span>',
                ])
        result = {
            "date_filter":date.today().strftime("%d %B %Y"),
            "status":"1",
            "color": ["#2ECC71","#E74C3C","#f1c40f","#9b59b6","#34495e","#e74c3c","#e67e22","#bdc3c7","#d35400","#c0392b","#7f8c8d"],
            "chart" : {
                    "text" : "Aircraft Status(" + str(serviceable + unserviceable) + ")",
                    "data":[{"name":"S",
                             "y":serviceable,
                             "color":"#2ECC71"},
                            {"name":"US",
                             "y":unserviceable,
                            "color":"#E74C3C"}],
                    },
            "remark" : remark,
            "astatlist" : astatlist,
        }
        return Response(json.dumps(result),content_type='text',status=200)


    # GINRO ===============================================================================================
    # =====================================================================================================
    @http.route(['/pelita_dashboard/maintenance_dashboard_aircraft_status/data_astat_fw',], type="http", auth='public',  methods=['POST','GET'], website=True, cors='*', csrf=False)
    def data_astat_fw(self, **kw):
        serviceable = request.env['aircraft.acquisition'].sudo().search(['&',('category','=','fixedwing'),'&',('is_deleted','=',False),('aircraft_status','=',True)])
        unserviceable = request.env['aircraft.acquisition'].sudo().search(['&',('category','=','fixedwing'),'&',('is_deleted','=',False),('aircraft_status','=',False)])
        result = {
            "date_filter":date.today().strftime("%d %B %Y"),
            "status":"1",
            "color": ["#2ECC71","#E74C3C","#f1c40f","#9b59b6","#34495e","#e74c3c","#e67e22","#bdc3c7","#d35400","#c0392b","#7f8c8d"],
            "chart" : {
                    "text" : "Fixed Wing(" + str(len(serviceable) + len(unserviceable)) + ")",
                    "data":[{"name":"S",
                             "y":len(serviceable),
                             "color":"#2ECC71"},
                            {"name":"US",
                             "y":len(unserviceable),
                            "color":"#E74C3C"}],
                    },
        }
        return Response(json.dumps(result),content_type='text',status=200)


    # GINRO ===============================================================================================
    # =====================================================================================================
    @http.route(['/pelita_dashboard/maintenance_dashboard_aircraft_status/data_astat_rw',], type="http", auth='public',  methods=['POST','GET'], website=True, cors='*', csrf=False)
    def data_astat_rw(self, **kw):
        serviceable = request.env['aircraft.acquisition'].sudo().search(['&',('category','=','rotary'),'&',('is_deleted','=',False),('aircraft_status','=',True)])
        unserviceable = request.env['aircraft.acquisition'].sudo().search(['&',('category','=','rotary'),'&',('is_deleted','=',False),('aircraft_status','=',False)])
        result = {
            "date_filter":date.today().strftime("%d %B %Y"),
            "status":"1",
            "color": ["#2ECC71","#E74C3C","#f1c40f","#9b59b6","#34495e","#e74c3c","#e67e22","#bdc3c7","#d35400","#c0392b","#7f8c8d"],
            "chart" : {
                    "text" : "Rotary Wing(" + str(len(serviceable) + len(unserviceable)) + ")",
                    "data":[{"name":"S",
                             "y":len(serviceable),
                             "color":"#2ECC71"},
                            {"name":"US",
                             "y":len(unserviceable),
                            "color":"#E74C3C"}],
                    },
        }
        return Response(json.dumps(result),content_type='text',status=200)



        