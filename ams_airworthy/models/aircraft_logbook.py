
from odoo import models, fields, api

class AircraftLogbookCheck(models.Model):
    _name = 'aircraft.logbook'
    _description = 'Aircraft Logbook'

    fleet_id = fields.Many2one('aircraft.acquisition', string='Aircraft Registration', default=lambda self:self.env.context.get('fleet_id',False), readonly=True)
    logbook_line = fields.One2many('aircraft.logbook_list','aircraft_logbook_id',string='Logbook', readonly=True)

    @api.onchange('fleet_id')
    def _onchange_fleet_id(self):
        logbook = []
        ro = self.env['ams.log'].search([('aircraft_id','=',self.fleet_id.id)])
        for g in ro:
            logbook.append((0,0,{
                'logbook_id' : g.id
                }))
        self.logbook_line = logbook            

class AircraftLogbookList(models.Model):
    _name = 'aircraft.logbook_list'
    _description = 'Logbook'

    aircraft_logbook_id = fields.Many2one('aircraft.logbook', string='Aircraft')
    logbook_id = fields.Many2one('ams.log', string='Logbook')

    hours = fields.Float(string='Hours', readonly=True, related='logbook_id.hours')
    cycles = fields.Float(string='Cycles', readonly=True, related='logbook_id.cycles')
    rin = fields.Float(string='RIN', readonly=True, related='logbook_id.rin')
    date = fields.Date(string='Date', readonly=True, related='logbook_id.date')
    ata = fields.Many2one('ams.ata', string="ATA Code", readonly=True, related='logbook_id.ata')
    description = fields.Text('Description', readonly=True, related='logbook_id.description')
    wo_id = fields.Many2one('ams.work.order', string="W/O Reference", readonly=True, related='logbook_id.wo_id')
    mwo_id = fields.Many2one('ams.mwo', string="MWO Reference", readonly=True, related='logbook_id.mwo_id')