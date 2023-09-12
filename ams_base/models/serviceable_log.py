from odoo import models, fields, api, _
import json
from websocket import create_connection

class InheritServiceableAircraft(models.Model):
    _inherit = 'aircraft.acquisition'


    @api.multi
    def toggle_active(self):
        if(self.aircraft_status == True):
            self.aircraft_status = False
        else:
            self.aircraft_status = True

        current_id = self.env['aircraft.acquisition'].search([], limit=1,  order="id asc")
        self.env['serviceable.log'].create({
                    'date_start' : current_id.write_date,
                    'date_end' : self.write_date,
                    'servicable' : self.aircraft_status,
                    'fleet' : self.name,
                    'duration_hour' : self.total_hours,
                    'duration_cycle' : self.total_landings,
                    })
        ws = create_connection("ws://paiis.pelita-air.com:8000/dashboard")
        ws.send(json.dumps({"platform": "dashboard", "method": "refresh","message":"Refresh"}))
        result =  ws.recv()
        ws.close()
        
class ServiceableLog(models.Model):
    _name = 'serviceable.log'
    _description = 'ServiceStatus Log'
    _rec_name = 'fleet'

    date_start = fields.Datetime(string="Datetime Start")
    date_end = fields.Datetime(string="Datetime Stop")
    employee = fields.Many2one('res.partner', default=lambda self: self.env.user.partner_id.id)
    fleet = fields.Char(string='Aircraft')
    servicable = fields.Boolean(string='Serviceable')
    duration_hour = fields.Float(string="Duration (Hours)")
    duration_cycle = fields.Float(string="Duration (Cycles)")