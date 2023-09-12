from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class ConfigWarningTime(models.Model):
    _name = 'ams.config'

    name = fields.Char(required=True)
    int_value = fields.Integer(string="Value")

class SettingWarningTime(models.Model):
    _name = 'ams.setting'

    warning_hours = fields.Float(string="Default Hours",default=lambda self:self._get_hours())
    warning_cycles = fields.Float(string="Default Cycles",default=lambda self:self._get_cycles())
    warning_rins = fields.Float(string="Default Rin",default=lambda self:self._get_rins())
    warning_calendars = fields.Integer(string="Default Calendars",default=lambda self:self._get_calendars())

    warning_hours_limit = fields.Float(string="Warning Hours",default=lambda self:self._get_hours_limit())
    warning_cycles_limit = fields.Float(string="Warning Cycles",default=lambda self:self._get_cycles_limit())
    warning_rins_limit = fields.Float(string="Warning Rin",default=lambda self:self._get_rins_limit())
    warning_calendars_limit = fields.Integer(string="Warning Calendars",default=lambda self:self._get_calendars_limit())

    def _get_hours(self):
        return self.env['ams.config'].search([('name','=','warning_hours')],limit=1).int_value

    def _get_cycles(self):
        return self.env['ams.config'].search([('name','=','warning_cycles')],limit=1).int_value

    def _get_rins(self):
        return self.env['ams.config'].search([('name','=','warning_rins')],limit=1).int_value

    def _get_calendars(self):
        return self.env['ams.config'].search([('name','=','warning_calendars')],limit=1).int_value

    def _get_hours_limit(self):
        return self.env['ams.config'].search([('name','=','warning_hours_limit')],limit=1).int_value

    def _get_cycles_limit(self):
        return self.env['ams.config'].search([('name','=','warning_cycles_limit')],limit=1).int_value

    def _get_rins_limit(self):
        return self.env['ams.config'].search([('name','=','warning_rins_limit')],limit=1).int_value

    def _get_calendars_limit(self):
        return self.env['ams.config'].search([('name','=','warning_calendars_limit')],limit=1).int_value

    @api.multi
    @api.constrains('warning_hours', 'warning_hours_limit')
    def date_constrains(self):
        for rec in self:
            if rec.warning_hours_limit > rec.warning_hours:
                raise ValidationError(_('Sorry, Default Hours Limit Must be greater Than Warning Hours Limit'))

    @api.multi
    @api.constrains('warning_cycles', 'warning_cycles_limit')
    def date_constrains(self):
        for rec in self:
            if rec.warning_hours_limit > rec.warning_hours:
                raise ValidationError(_('Sorry, Default Cycles Limit Must be greater Than Warning Cycles Limit'))

    @api.multi
    @api.constrains('warning_rins', 'warning_rins_limit')
    def date_constrains(self):
        for rec in self:
            if rec.warning_hours_limit > rec.warning_hours:
                raise ValidationError(_('Sorry, Default Rins Limit Must be greater Than Warning Rins Limit'))

    @api.multi
    @api.constrains('warning_calendars', 'warning_calendars_limit')
    def date_constrains(self):
        for rec in self:
            if rec.warning_hours_limit > rec.warning_hours:
                raise ValidationError(_('Sorry, Default Calendars Limit Must be greater Than Warning Calendars Limit'))


    @api.multi 
    def action_save(self):
        #your code
        self.ensure_one()
        #close popup
        return {'type': 'ir.actions.act_window_close'}

    @api.model
    def create(self, vals):
        self.env['ams.config'].search([('name','=','warning_hours')]).write({'int_value' : vals['warning_hours']})
        self.env['ams.config'].search([('name','=','warning_cycles')]).write({'int_value' : vals['warning_cycles']})
        self.env['ams.config'].search([('name','=','warning_rins')]).write({'int_value' : vals['warning_rins']})
        self.env['ams.config'].search([('name','=','warning_calendars')]).write({'int_value' : vals['warning_calendars']})
        self.env['ams.config'].search([('name','=','warning_hours_limit')]).write({'int_value' : vals['warning_hours_limit']})
        self.env['ams.config'].search([('name','=','warning_cycles_limit')]).write({'int_value' : vals['warning_cycles_limit']})
        self.env['ams.config'].search([('name','=','warning_rins_limit')]).write({'int_value' : vals['warning_rins_limit']})
        self.env['ams.config'].search([('name','=','warning_calendars_limit')]).write({'int_value' : vals['warning_calendars_limit']})
        return super(SettingWarningTime, self).create(vals)

class BaseOperation(models.Model):
    _name = "config.vendor"
    # _inherit = ["mail.thread", "ir.needaction_mixin"]
    # _order = "code asc, name asc"
    
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
    # # route_id = fields.Many2one('flight.requisition')


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
