from odoo import fields, models, api, _
from websocket import create_connection
import json


class StatusService(models.Model):
    _name = 'status.service'
    _description = 'Status Service'

    fleet_id = fields.Many2one('aircraft.acquisition')
    remark = fields.Text('Remark')
    status_s = fields.Selection([('inservice','In Service'),('available','Available'),('useassubtitution','Use As Subtitution')], default='inservice')
    status_us = fields.Selection([('inmaintenance','In Maintenance'),('grounded','Grounded')], default='inmaintenance')
    type = fields.Selection([('S','Serviceable'),('US','Unserviceable')], default='S')



    @api.multi 
    def action_save(self):
        #your code
        self.ensure_one()
        #close popup
        return {'type': 'ir.actions.act_window_close'}

    @api.model
    def create(self, values):

        status = super(StatusService, self).create(values)
        if values['type'] == 'S':
            self.env['aircraft.acquisition'].search([('id','=',status.fleet_id.id)]).write({
                'status' : status.status_us,
                'remark' : status.remark,
                'aircraft_status' : False,
                })
        else:
            self.env['aircraft.acquisition'].search([('id','=',status.fleet_id.id)]).write({
                'status' : status.status_s,
                'remark' : status.remark,
                'aircraft_status' : True,
                })
        ws = create_connection("ws://paiis.pelita-air.com:8000/dashboard")
        ws.send(json.dumps({"platform": "dashboard", "method": "refresh","message":"Refresh"}))
        result =  ws.recv()
        ws.close()
        return status