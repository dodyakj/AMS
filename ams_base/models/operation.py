from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class BaseOperation(models.Model):
    _inherit = "base.operation"
    
    # name = fields.Char(string = 'Name',required=True, track_visibility='onchange')
    # code = fields.Char(string='Code', track_visibility='onchange')
    # description = fields.Text('Description')
    # latitude = fields.Char(string='Latitude', track_visibility='onchange')
    # longitude = fields.Char(string='Longitude', track_visibility='onchange')
    # coordinate =  fields.Char('Coordinate')
    # coordinate_map = fields.Char('MAP', compute='_get_coordinate')
    # status = fields.Selection([('active','Active'),('nonactive','Non Active')], string='Status')
    # active = fields.Boolean(string='Status', default=True, 
    #                         help="Set active to false to hide the tax without removing it.")
    # google_map_base_ops = fields.Char(string="Map", track_visibility='onchange')
    # active = fields.Boolean(string='Status', default=True,
    #                         help="Set active to false to hide the tax without removing it.")
    # route_id = fields.Many2one('flight.requisition')
    message_last_post = fields.Date(readonly=True)
    warehouse_id = fields.Many2one('stock.location', 'Werehouse')

    # @api.onchange('google_map_base_ops')
    # def onchange_google_map_base_ops(self):
    #     if self.google_map_base_ops:
    #         dict_map = ast.literal_eval(self.google_map_base_ops)
    #         if dict_map and dict_map['position']:
    #             self.latitude = dict_map['position']['lat']
    #             self.longitude = dict_map['position']['lng']

    # @api.depends('latitude','longitude')
    # def _get_coordinate(self):
    #     for record in self:
    #         if record.latitude is False or record.longitude is False:
    #             record.latitude = record.longitude = 0.0
    #         record.coordinate_map = '{"position":{"lat":%s,"lng":%s},"zoom":18}'%(
    #             record.latitude,record.longitude)
