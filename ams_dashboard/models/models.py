from odoo import fields, models, api
from datetime import datetime, timedelta, date


class AircraftDashboard(models.Model):
    _inherit= 'aircraft.acquisition'

    @api.model
    def for_aircraft_dashboard(self):
        aircraft_list = []
        aircrafts = self.env['aircraft.acquisition'].search([('is_deleted','=',False)])

        for aircraft in aircrafts:

            # state = 'serviceable'

            maintenance_request_list = []
            maintenances = self.env['maintenance.request'].search([
                ('fl_acquisition_id', '=', aircraft.id), 
                ('schedule_date', '<=', datetime.now().strftime('%Y-%m-%d')),
                ('date_finished', '>', datetime.now().strftime('%Y-%m-%d')),
                ])

            for maintenance in maintenances:
                maintenance_temp = {
                    "id": maintenance.id,
                    "aircraft_state": maintenance.aircraft_state,
                    "schedule_date": maintenance.schedule_date,
                    "duration": maintenance.duration,
                    "name": maintenance.name,
                    "aircraft_state": maintenance.aircraft_state
                }
                maintenance_request_list.append(maintenance_temp)

            document_certificate_list = []
            certificates = self.env['document.certificate'].search([
                ('acquisition_id', '=', aircraft.id),
            ])
            for certificate in certificates:
                certificate_tmp = {
                    "id": certificate.id,
                    "document_name": certificate.document_id.name,
                    "file_date": certificate.file_data,
                    "date_expired": certificate.date_expired,
                }
                document_certificate_list.append(certificate_tmp)


            components_list = []
            # components = self.env['ams.component.part'].search([
            #     ('fleet_id', '=', aircraft.id), 
            #     ])

            # for component in components:

            #     service_life_list = []
            #     for service_life_id in component.serfice_life:
            #         service_lifes = self.env['ams.component.servicelife'].search([('id', '=', service_life_id.id), ])

            #         for service_life in service_lifes:
            #             next_date = service_life.next_date
            #             date_range = 32
            #             if next_date:
            #                 nextdate = datetime.strptime(next_date, '%Y-%m-%d')
            #                 if nextdate <= datetime.now():
            #                     delta = datetime.now() - nextdate
            #                     date_range = delta.days + 1
            #                 else:
            #                     delta = nextdate - datetime.now()
            #                     date_range = delta.days + 1

            #             service_life_temp = {
            #                 "id": service_life.id,
            #                 "next_date": service_life.next_date,
            #                 "unit": service_life.unit,
            #                 "display_name": service_life.display_name,
            #                 "value": service_life.value,
            #                 "range": date_range,
            #             }
            #             service_life_list.append(service_life_temp)

            #     component_temp = {
            #         "id": component.id,
            #         "display_name": component.display_name,
            #         "service_life": service_life_list,
            #     }
            #     components_list.append(component_temp)

            # if len(maintenance_request_list) > 0:
            #     state = maintenance_request_list[len(maintenance_request_list) - 1]['aircraft_state']

            aircraft_temp = {
                "id": aircraft.id,
                "display_name": aircraft.display_name,
                "image": aircraft.image,
                "category": aircraft.category,
                "ownership": aircraft.ownership,
                "rin_active": aircraft.rin_active,
                "total_hours": aircraft.total_hours,
                "total_landings": aircraft.total_landings,
                "total_rins": aircraft.total_rins,
                "inspection": {
                    "last": aircraft.last_inspection,
                    "last_at": aircraft.last_inspection_hours,
                    "last_date": aircraft.last_inspection_date,
                    "next": aircraft.next_inspection,
                    "next_at": aircraft.next_inspection_at,
                },
                "maintenances": maintenance_request_list,
                "components": components_list,
                "certificates": document_certificate_list,
                "state": 'serviceable' if aircraft.aircraft_status == True else 'unserviceable',
            }
            aircraft_list.append(aircraft_temp)

        return {
            "result_arr": aircraft_list
            }

class MdrDashboard(models.Model):
    _inherit= 'maintenance.due.report'


    @api.multi
    def do_mwo(self):
        return {
            'name': 'MWO',
            'type': 'ir.actions.act_window',
            'res_model': 'ams.mwo',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': False,
            'views': [(False, 'form')],
            'target': 'new',
            }

    @api.multi
    def do_wo(self):
        return {
            'name': 'WO',
            'type': 'ir.actions.act_window',
            'res_model': 'ams.work.order',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': False,
            'views': [(False, 'form')],
            'target': 'new',
            }

    def find_index(self, dicts, key, value):
        class Null: pass
        for i, d in enumerate(dicts):
            if d.get(key, Null) == value:
                return i

    @api.model
    def for_mdr_dashboard(self):
        mdr_list = []
        part_list = []
        unique_part_list = []
        unique_part_name_list = []
        mdr = self.env['maintenance.due.report'].search([("states", "in", ["approved_by",'done'])])

        for item in mdr:
            if not item.hour_limit_id:
                item._get_hour()
            if not item.cycle_limit_id:
                item._get_cycle()
            if not item.rin_limit_id:
                item._get_rin()
            if not item.calendar_limit_id:
                item._get_calendar()
                
            component_list = []
            for hour_id in item.hour_limit_id:
                hour = {
                    "id": hour_id.id,
                    "fleet": hour_id.fleet_id,
                    "part": hour_id.part,
                    "name": hour_id.name,
                    "fleet_name": hour_id.hour_id.fleet_id.name,
                    "fleet_id": hour_id.hour_id.fleet_id.id,
                    "due_at": hour_id.due_at_text,
                    "remaining": hour_id.time,
                    "service": hour_id.service,
                    "service_id": hour_id.service_id.id,
                }
                component_list.append(hour)
                part_list.append(hour)

            for cycle_id in item.cycle_limit_id:
                cycle = {
                    "id": cycle_id.id,
                    "fleet": cycle_id.fleet_id,
                    "part": cycle_id.part,
                    "name": cycle_id.name,
                    "fleet_name": cycle_id.cycle_id.fleet_id.name,
                    "fleet_id": cycle_id.cycle_id.fleet_id.id,
                    "due_at": cycle_id.due_at_text,
                    "remaining": cycle_id.time,
                    "service": cycle_id.service,
                    "service_id": hour_id.service_id.id,
                }
                component_list.append(cycle)
                part_list.append(cycle)


            for rin_id in item.rin_limit_id:    
                rin = {
                    "id": rin_id.id,
                    "fleet": rin_id.fleet_id,
                    "part": rin_id.part,
                    "name": rin_id.name,
                    "fleet_name": rin_id.rin_id.fleet_id.name,
                    "fleet_id": rin_id.rin_id.fleet_id.id,
                    "due_at": rin_id.due_at_text,
                    "remaining": rin_id.time,
                    "service": rin_id.service,
                    "service_id": hour_id.service_id.id,
                }
                component_list.append(rin)
                part_list.append(rin)


            for calendar_id in item.calendar_limit_id:
                calendar = {
                    "id": calendar_id.id,
                    "fleet": calendar_id.fleet_id,
                    "part": calendar_id.part,
                    "name": calendar_id.name,
                    "fleet_name": calendar_id.calendar_id.fleet_id.name,
                    "fleet_id": calendar_id.calendar_id.fleet_id.id,
                    "due_at": calendar_id.due_at_text,
                    "remaining": calendar_id.time,
                    "service": calendar_id.service,
                    "service_id": hour_id.service_id.id,
                }
                component_list.append(calendar)
                part_list.append(calendar)

            fleet = item.fleet_id
            fleet_temp = {
                "id": fleet.id,
                "display_name": fleet.display_name,
            }

            new_item = {
                    "id": item.id,
                    "fleet_id": fleet_temp,
                    "components": component_list,
            }
            mdr_list.append(new_item)

        for item_part in part_list: 
            unique_part = {
                "name": item_part["name"],
                "part": item_part["part"],
                "total": 1,
                "fleet_name": item_part["fleet_name"],
                "fleet_id": item_part["fleet_id"],
                "service_id": item_part["service_id"],
                "due_at": item_part["due_at"],
                "remaining": item_part["remaining"],
                "fleet": [item_part["fleet"]],
            }
            if not item_part["part"] in unique_part_name_list:
                unique_part_name_list.append(item_part["part"])
                unique_part_list.append(unique_part)
            else:
                index = self.find_index(unique_part_list, "part", item_part["part"])
                unique_part_list[index]["total"] = unique_part_list[index]["total"] + 1
                if not item_part["fleet"] in unique_part_list[index]["fleet"]:
                    unique_part_list[index]["fleet"].append(item_part["fleet"])
            
        return {
            "result_arr": mdr_list,
            "parts": unique_part_list,
            "parts_list": part_list,
            }