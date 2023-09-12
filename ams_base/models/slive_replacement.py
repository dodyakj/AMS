from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import math
from odoo import fields, models, api

class ComponentPart(models.Model):
    _inherit = "ams.component.replace"

    use_comp_hour = fields.Boolean(string='Use Component TSN / CSN for parameter', default=True)

    slive_1 = fields.Many2one('ams.component.servicelife', string='Service Live', readonly=True)
    slive_1_action_type = fields.Selection([('inspection','Inspection'),('overhaul','Overhaul'),('retirement','Retirement'),('oncondition','On Condition'),('conditionmonitoring','Condition Monitoring'),('service','Service')], string='Treatment',related='slive_1.action_type')
    slive_1_unit = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Unit', related='slive_1.unit')
    ac_string_1 = fields.Char(string='AC String 1', readonly=True)
    ac_int_1 = fields.Float(string='AC Int 1')
    comp_string_1 = fields.Char(string='COMP String 1', readonly=True)
    comp_int_1 = fields.Float(string='COMP Int 1')
    since_new_string_1 = fields.Char(string='Since New String 1', readonly=True)
    since_new_int_1 = fields.Float(string='Since New Int 1')
    date_string_1 = fields.Char(string='Date String 1', readonly=True)
    comp_date_1 = fields.Date(string='COMP Date 1', default=fields.Date.today())

    slive_2 = fields.Many2one('ams.component.servicelife', string='Service Live', readonly=True)
    slive_2_action_type = fields.Selection([('inspection','Inspection'),('overhaul','Overhaul'),('retirement','Retirement'),('oncondition','On Condition'),('conditionmonitoring','Condition Monitoring'),('service','Service')], string='Treatment',related='slive_2.action_type')
    slive_2_unit = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Unit', related='slive_2.unit')
    ac_string_2 = fields.Char(string='AC String 2', readonly=True)
    ac_int_2 = fields.Float(string='AC Int 2')
    comp_string_2 = fields.Char(string='COMP String 2', readonly=True)
    comp_int_2 = fields.Float(string='COMP Int 2')
    since_new_string_2 = fields.Char(string='Since New String 2', readonly=True)
    since_new_int_2 = fields.Float(string='Since New Int 2')
    date_string_2 = fields.Char(string='Date String 2', readonly=True)
    comp_date_2 = fields.Date(string='COMP Date 2', default=fields.Date.today())

    slive_3 = fields.Many2one('ams.component.servicelife', string='Service Live', readonly=True)
    slive_3_action_type = fields.Selection([('inspection','Inspection'),('overhaul','Overhaul'),('retirement','Retirement'),('oncondition','On Condition'),('conditionmonitoring','Condition Monitoring'),('service','Service')], string='Treatment',related='slive_3.action_type')
    slive_3_unit = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Unit', related='slive_3.unit')
    ac_string_3 = fields.Char(string='AC String 3', readonly=True)
    ac_int_3 = fields.Float(string='AC Int 3')
    comp_string_3 = fields.Char(string='COMP String 3', readonly=True)
    comp_int_3 = fields.Float(string='COMP Int 3')
    since_new_string_3 = fields.Char(string='Since New String 3', readonly=True)
    since_new_int_3 = fields.Float(string='Since New Int 3')
    date_string_3 = fields.Char(string='Date String 3', readonly=True)
    comp_date_3 = fields.Date(string='COMP Date 3', default=fields.Date.today())

    slive_4 = fields.Many2one('ams.component.servicelife', string='Service Live', readonly=True)
    slive_4_action_type = fields.Selection([('inspection','Inspection'),('overhaul','Overhaul'),('retirement','Retirement'),('oncondition','On Condition'),('conditionmonitoring','Condition Monitoring'),('service','Service')], string='Treatment',related='slive_4.action_type')
    slive_4_unit = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Unit', related='slive_4.unit')
    ac_string_4 = fields.Char(string='AC String 4', readonly=True)
    ac_int_4 = fields.Float(string='AC Int 4')
    comp_string_4 = fields.Char(string='COMP String 4', readonly=True)
    comp_int_4 = fields.Float(string='COMP Int 4')
    since_new_string_4 = fields.Char(string='Since New String 4', readonly=True)
    since_new_int_4 = fields.Float(string='Since New Int 4')
    date_string_4 = fields.Char(string='Date String 4', readonly=True)
    comp_date_4 = fields.Date(string='COMP Date 4', default=fields.Date.today())

    slive_2 = fields.Many2one('ams.component.servicelife', string='Service Live', readonly=True)
    slive_2_action_type = fields.Selection([('inspection','Inspection'),('overhaul','Overhaul'),('retirement','Retirement'),('oncondition','On Condition'),('conditionmonitoring','Condition Monitoring'),('service','Service')], string='Treatment',related='slive_2.action_type')
    slive_2_unit = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Unit', related='slive_2.unit')
    ac_string_2 = fields.Char(string='AC String 2', readonly=True)
    ac_int_2 = fields.Float(string='AC Int 2')
    comp_string_2 = fields.Char(string='COMP String 2', readonly=True)
    comp_int_2 = fields.Float(string='COMP Int 2')
    since_new_string_2 = fields.Char(string='Since New String 2', readonly=True)
    since_new_int_2 = fields.Float(string='Since New Int 2')
    date_string_2 = fields.Char(string='Date String 2', readonly=True)
    comp_date_2 = fields.Date(string='COMP Date 2', default=fields.Date.today())

    slive_3 = fields.Many2one('ams.component.servicelife', string='Service Live', readonly=True)
    slive_3_action_type = fields.Selection([('inspection','Inspection'),('overhaul','Overhaul'),('retirement','Retirement'),('oncondition','On Condition'),('conditionmonitoring','Condition Monitoring'),('service','Service')], string='Treatment',related='slive_3.action_type')
    slive_3_unit = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Unit', related='slive_3.unit')
    ac_string_3 = fields.Char(string='AC String 3', readonly=True)
    ac_int_3 = fields.Float(string='AC Int 3')
    comp_string_3 = fields.Char(string='COMP String 3', readonly=True)
    comp_int_3 = fields.Float(string='COMP Int 3')
    since_new_string_3 = fields.Char(string='Since New String 3', readonly=True)
    since_new_int_3 = fields.Float(string='Since New Int 3')
    date_string_3 = fields.Char(string='Date String 3', readonly=True)
    comp_date_3 = fields.Date(string='COMP Date 3', default=fields.Date.today())

    slive_4 = fields.Many2one('ams.component.servicelife', string='Service Live', readonly=True)
    slive_4_action_type = fields.Selection([('inspection','Inspection'),('overhaul','Overhaul'),('retirement','Retirement'),('oncondition','On Condition'),('conditionmonitoring','Condition Monitoring'),('service','Service')], string='Treatment',related='slive_4.action_type')
    slive_4_unit = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Unit', related='slive_4.unit')
    ac_string_4 = fields.Char(string='AC String 4', readonly=True)
    ac_int_4 = fields.Float(string='AC Int 4')
    comp_string_4 = fields.Char(string='COMP String 4', readonly=True)
    comp_int_4 = fields.Float(string='COMP Int 4')
    since_new_string_4 = fields.Char(string='Since New String 4', readonly=True)
    since_new_int_4 = fields.Float(string='Since New Int 4')
    date_string_4 = fields.Char(string='Date String 4', readonly=True)
    comp_date_4 = fields.Date(string='COMP Date 4', default=fields.Date.today())

    slive_5 = fields.Many2one('ams.component.servicelife', string='Service Live', readonly=True)
    slive_5_action_type = fields.Selection([('inspection','Inspection'),('overhaul','Overhaul'),('retirement','Retirement'),('oncondition','On Condition'),('conditionmonitoring','Condition Monitoring'),('service','Service')], string='Treatment',related='slive_5.action_type')
    slive_5_unit = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Unit', related='slive_5.unit')
    ac_string_5 = fields.Char(string='AC String 5', readonly=True)
    ac_int_5 = fields.Float(string='AC Int 5')
    comp_string_5 = fields.Char(string='COMP String 5', readonly=True)
    comp_int_5 = fields.Float(string='COMP Int 5')
    since_new_string_5 = fields.Char(string='Since New String 5', readonly=True)
    since_new_int_5 = fields.Float(string='Since New Int 5')
    date_string_5 = fields.Char(string='Date String 5', readonly=True)
    comp_date_5 = fields.Date(string='COMP Date 5', default=fields.Date.today())

    slive_6 = fields.Many2one('ams.component.servicelife', string='Service Live', readonly=True)
    slive_6_action_type = fields.Selection([('inspection','Inspection'),('overhaul','Overhaul'),('retirement','Retirement'),('oncondition','On Condition'),('conditionmonitoring','Condition Monitoring'),('service','Service')], string='Treatment',related='slive_6.action_type')
    slive_6_unit = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Unit', related='slive_6.unit')
    ac_string_6 = fields.Char(string='AC String 6', readonly=True)
    ac_int_6 = fields.Float(string='AC Int 6')
    comp_string_6 = fields.Char(string='COMP String 6', readonly=True)
    comp_int_6 = fields.Float(string='COMP Int 6')
    since_new_string_6 = fields.Char(string='Since New String 6', readonly=True)
    since_new_int_6 = fields.Float(string='Since New Int 6')
    date_string_6 = fields.Char(string='Date String 6', readonly=True)
    comp_date_6 = fields.Date(string='COMP Date 6', default=fields.Date.today())

    slive_7 = fields.Many2one('ams.component.servicelife', string='Service Live', readonly=True)
    slive_7_action_type = fields.Selection([('inspection','Inspection'),('overhaul','Overhaul'),('retirement','Retirement'),('oncondition','On Condition'),('conditionmonitoring','Condition Monitoring'),('service','Service')], string='Treatment',related='slive_7.action_type')
    slive_7_unit = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Unit', related='slive_7.unit')
    ac_string_7 = fields.Char(string='AC String 7', readonly=True)
    ac_int_7 = fields.Float(string='AC Int 7')
    comp_string_7 = fields.Char(string='COMP String 7', readonly=True)
    comp_int_7 = fields.Float(string='COMP Int 7')
    since_new_string_7 = fields.Char(string='Since New String 7', readonly=True)
    since_new_int_7 = fields.Float(string='Since New Int 7')
    date_string_7 = fields.Char(string='Date String 7', readonly=True)
    comp_date_7 = fields.Date(string='COMP Date 7', default=fields.Date.today())

    slive_8 = fields.Many2one('ams.component.servicelife', string='Service Live', readonly=True)
    slive_8_action_type = fields.Selection([('inspection','Inspection'),('overhaul','Overhaul'),('retirement','Retirement'),('oncondition','On Condition'),('conditionmonitoring','Condition Monitoring'),('service','Service')], string='Treatment',related='slive_8.action_type')
    slive_8_unit = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Unit', related='slive_8.unit')
    ac_string_8 = fields.Char(string='AC String 8', readonly=True)
    ac_int_8 = fields.Float(string='AC Int 8')
    comp_string_8 = fields.Char(string='COMP String 8', readonly=True)
    comp_int_8 = fields.Float(string='COMP Int 8')
    since_new_string_8 = fields.Char(string='Since New String 8', readonly=True)
    since_new_int_8 = fields.Float(string='Since New Int 8')
    date_string_8 = fields.Char(string='Date String 8', readonly=True)
    comp_date_8 = fields.Date(string='COMP Date 8', default=fields.Date.today())

    slive_9 = fields.Many2one('ams.component.servicelife', string='Service Live', readonly=True)
    slive_9_action_type = fields.Selection([('inspection','Inspection'),('overhaul','Overhaul'),('retirement','Retirement'),('oncondition','On Condition'),('conditionmonitoring','Condition Monitoring'),('service','Service')], string='Treatment',related='slive_9.action_type')
    slive_9_unit = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Unit', related='slive_9.unit')
    ac_string_9 = fields.Char(string='AC String 9', readonly=True)
    ac_int_9 = fields.Float(string='AC Int 9')
    comp_string_9 = fields.Char(string='COMP String 9', readonly=True)
    comp_int_9 = fields.Float(string='COMP Int 9')
    since_new_string_9 = fields.Char(string='Since New String 9', readonly=True)
    since_new_int_9 = fields.Float(string='Since New Int 9')
    date_string_9 = fields.Char(string='Date String 9', readonly=True)
    comp_date_9 = fields.Date(string='COMP Date 9', default=fields.Date.today())

    slive_10 = fields.Many2one('ams.component.servicelife', string='Service Live', readonly=True)
    slive_10_action_type = fields.Selection([('inspection','Inspection'),('overhaul','Overhaul'),('retirement','Retirement'),('oncondition','On Condition'),('conditionmonitoring','Condition Monitoring'),('service','Service')], string='Treatment',related='slive_10.action_type')
    slive_10_unit = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Unit', related='slive_10.unit')
    ac_string_10 = fields.Char(string='AC String 10', readonly=True)
    ac_int_10 = fields.Float(string='AC Int 10')
    comp_string_10 = fields.Char(string='COMP String 10', readonly=True)
    comp_int_10 = fields.Float(string='COMP Int 10')
    since_new_string_10 = fields.Char(string='Since New String 10', readonly=True)
    since_new_int_10 = fields.Float(string='Since New Int 10')
    date_string_10 = fields.Char(string='Date String 10', readonly=True)
    comp_date_10 = fields.Date(string='COMP Date 10', default=fields.Date.today())

    slive_11 = fields.Many2one('ams.component.servicelife', string='Service Live', readonly=True)
    slive_11_action_type = fields.Selection([('inspection','Inspection'),('overhaul','Overhaul'),('retirement','Retirement'),('oncondition','On Condition'),('conditionmonitoring','Condition Monitoring'),('service','Service')], string='Treatment',related='slive_11.action_type')
    slive_11_unit = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Unit', related='slive_11.unit')
    ac_string_11 = fields.Char(string='AC String 11', readonly=True)
    ac_int_11 = fields.Float(string='AC Int 11')
    comp_string_11 = fields.Char(string='COMP String 11', readonly=True)
    comp_int_11 = fields.Float(string='COMP Int 11')
    since_new_string_11 = fields.Char(string='Since New String 11', readonly=True)
    since_new_int_11 = fields.Float(string='Since New Int 11')
    date_string_11 = fields.Char(string='Date String 11', readonly=True)
    comp_date_11 = fields.Date(string='COMP Date 11', default=fields.Date.today())

    slive_12 = fields.Many2one('ams.component.servicelife', string='Service Live', readonly=True)
    slive_12_action_type = fields.Selection([('inspection','Inspection'),('overhaul','Overhaul'),('retirement','Retirement'),('oncondition','On Condition'),('conditionmonitoring','Condition Monitoring'),('service','Service')], string='Treatment',related='slive_12.action_type')
    slive_12_unit = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Unit', related='slive_12.unit')
    ac_string_12 = fields.Char(string='AC String 12', readonly=True)
    ac_int_12 = fields.Float(string='AC Int 12')
    comp_string_12 = fields.Char(string='COMP String 12', readonly=True)
    comp_int_12 = fields.Float(string='COMP Int 12')
    since_new_string_12 = fields.Char(string='Since New String 12', readonly=True)
    since_new_int_12 = fields.Float(string='Since New Int 12')
    date_string_12 = fields.Char(string='Date String 12', readonly=True)
    comp_date_12 = fields.Date(string='COMP Date 12', default=fields.Date.today())

    slive_13 = fields.Many2one('ams.component.servicelife', string='Service Live', readonly=True)
    slive_13_action_type = fields.Selection([('inspection','Inspection'),('overhaul','Overhaul'),('retirement','Retirement'),('oncondition','On Condition'),('conditionmonitoring','Condition Monitoring'),('service','Service')], string='Treatment',related='slive_13.action_type')
    slive_13_unit = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Unit', related='slive_13.unit')
    ac_string_13 = fields.Char(string='AC String 13', readonly=True)
    ac_int_13 = fields.Float(string='AC Int 13')
    comp_string_13 = fields.Char(string='COMP String 13', readonly=True)
    comp_int_13 = fields.Float(string='COMP Int 13')
    since_new_string_13 = fields.Char(string='Since New String 13', readonly=True)
    since_new_int_13 = fields.Float(string='Since New Int 13')
    date_string_13 = fields.Char(string='Date String 13', readonly=True)
    comp_date_13 = fields.Date(string='COMP Date 13', default=fields.Date.today())

    slive_14 = fields.Many2one('ams.component.servicelife', string='Service Live', readonly=True)
    slive_14_action_type = fields.Selection([('inspection','Inspection'),('overhaul','Overhaul'),('retirement','Retirement'),('oncondition','On Condition'),('conditionmonitoring','Condition Monitoring'),('service','Service')], string='Treatment',related='slive_14.action_type')
    slive_14_unit = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Unit', related='slive_14.unit')
    ac_string_14 = fields.Char(string='AC String 14', readonly=True)
    ac_int_14 = fields.Float(string='AC Int 14')
    comp_string_14 = fields.Char(string='COMP String 14', readonly=True)
    comp_int_14 = fields.Float(string='COMP Int 14')
    since_new_string_14 = fields.Char(string='Since New String 14', readonly=True)
    since_new_int_14 = fields.Float(string='Since New Int 14')
    date_string_14 = fields.Char(string='Date String 14', readonly=True)
    comp_date_14 = fields.Date(string='COMP Date 14', default=fields.Date.today())

    slive_15 = fields.Many2one('ams.component.servicelife', string='Service Live', readonly=True)
    slive_15_action_type = fields.Selection([('inspection','Inspection'),('overhaul','Overhaul'),('retirement','Retirement'),('oncondition','On Condition'),('conditionmonitoring','Condition Monitoring'),('service','Service')], string='Treatment',related='slive_15.action_type')
    slive_15_unit = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Unit', related='slive_15.unit')
    ac_string_15 = fields.Char(string='AC String 15', readonly=True)
    ac_int_15 = fields.Float(string='AC Int 15')
    comp_string_15 = fields.Char(string='COMP String 15', readonly=True)
    comp_int_15 = fields.Float(string='COMP Int 15')
    since_new_string_15 = fields.Char(string='Since New String 15', readonly=True)
    since_new_int_15 = fields.Float(string='Since New Int 15')
    date_string_15 = fields.Char(string='Date String 15', readonly=True)
    comp_date_15 = fields.Date(string='COMP Date 15', default=fields.Date.today())

    @api.onchange('component')
    def _onchange_component(self):
        if(self.component.is_subcomp == True):
            fleet = self.component.part_id.fleet_id
        else:
            fleet = self.component.fleet_id
        self.product_id = self.component.product_id.id
        self.ac_timeinstallation = self._get_vals()['total_hours']
        self.ac_cyclesinstallation = self._get_vals()['total_landings']
        self.ac_rininstallation = self._get_vals()['total_rins']
        self.rin_enable = False
        for g in self.component.serfice_life:
            if(g.unit == 'rin'):
                self.rin_enable = True

        comp_of = self._get_component_of()
        if(comp_of == 'airframe'):
            comp_of_string = 'A/C'
        elif(comp_of == 'propeller'):
            comp_of_string = 'A/C'
        elif(comp_of == 'engine'):
            comp_of_string = 'Engine'
        elif(comp_of == 'auxiliary'):
            comp_of_string = 'Auxiliary'

        if len(self.component.serfice_life) > 0:
            slive1 = self.component.serfice_life[0]
            self.ac_int_1 = self.ac_timeinstallation
            self.slive_1 = slive1.id
            self.ac_string_1 = comp_of_string + ' ' + str(slive1.unit) + ' since last ' + (str(slive1.value).rstrip('0').rstrip('.') if '.' in str(slive1.value) else str(slive1.value)) + str(slive1.unit) + ' ' + str(slive1.action_type)
            self.comp_string_1 = 'Comp ' + str(slive1.unit) + ' since last ' + (str(slive1.value).rstrip('0').rstrip('.') if '.' in str(slive1.value) else str(slive1.value)) + str(slive1.unit) + ' ' + str(slive1.action_type)
            self.date_string_1 = 'Last ' + (str(slive1.value).rstrip('0').rstrip('.') if '.' in str(slive1.value) else str(slive1.value)) + str(slive1.unit) + ' at'
            self.since_new_string_1 = 'Last ' + str(slive1.value) + ' ' + str(slive1.unit) + ' ' + str(slive1.action_type) + ' at Component ' + ('TSN' if slive1.unit == 'hours' else 'CSN' if slive1.unit == 'cycles' else 'RSN')

        if len(self.component.serfice_life) > 1:
            slive2 = self.component.serfice_life[1]
            self.ac_int_2 = self.ac_timeinstallation
            self.slive_2 = slive2.id
            self.ac_string_2 = comp_of_string + ' ' + str(slive2.unit) + ' since last ' + (str(slive2.value).rstrip('0').rstrip('.') if '.' in str(slive2.value) else str(slive2.value)) + str(slive2.unit) + ' ' + str(slive2.action_type)
            self.comp_string_2 = 'Comp ' + str(slive2.unit) + ' since last ' + (str(slive2.value).rstrip('0').rstrip('.') if '.' in str(slive2.value) else str(slive2.value)) + str(slive2.unit) + ' ' + str(slive2.action_type)
            self.date_string_2 = 'Last ' + (str(slive2.value).rstrip('0').rstrip('.') if '.' in str(slive2.value) else str(slive2.value)) + str(slive2.unit) + ' at'
            self.since_new_string_2 = 'Last ' + str(slive2.value) + ' ' + str(slive2.unit) + ' ' + str(slive2.action_type) + ' at Component ' + ('TSN' if slive2.unit == 'hours' else 'CSN' if slive2.unit == 'cycles' else 'RSN')

        if len(self.component.serfice_life) > 2:
            slive3 = self.component.serfice_life[2]
            self.ac_int_3 = self.ac_timeinstallation
            self.slive_3 = slive3.id
            self.ac_string_3 = comp_of_string + ' ' + str(slive3.unit) + ' since last ' + (str(slive3.value).rstrip('0').rstrip('.') if '.' in str(slive3.value) else str(slive3.value)) + str(slive3.unit) + ' ' + str(slive3.action_type)
            self.comp_string_3 = 'Comp ' + str(slive3.unit) + ' since last ' + (str(slive3.value).rstrip('0').rstrip('.') if '.' in str(slive3.value) else str(slive3.value)) + str(slive3.unit) + ' ' + str(slive3.action_type)
            self.date_string_3 = 'Last ' + (str(slive3.value).rstrip('0').rstrip('.') if '.' in str(slive3.value) else str(slive3.value)) + str(slive3.unit) + ' at'
            self.since_new_string_3 = 'Last ' + str(slive3.value) + ' ' + str(slive3.unit) + ' ' + str(slive3.action_type) + ' at Component ' + ('TSN' if slive3.unit == 'hours' else 'CSN' if slive3.unit == 'cycles' else 'RSN')

        if len(self.component.serfice_life) > 3:
            slive4 = self.component.serfice_life[3]
            self.ac_int_4 = self.ac_timeinstallation
            self.slive_4 = slive4.id
            self.ac_string_4 = comp_of_string + ' ' + str(slive4.unit) + ' since last ' + (str(slive4.value).rstrip('0').rstrip('.') if '.' in str(slive4.value) else str(slive4.value)) + str(slive4.unit) + ' ' + str(slive4.action_type)
            self.comp_string_4 = 'Comp ' + str(slive4.unit) + ' since last ' + (str(slive4.value).rstrip('0').rstrip('.') if '.' in str(slive4.value) else str(slive4.value)) + str(slive4.unit) + ' ' + str(slive4.action_type)
            self.date_string_4 = 'Last ' + (str(slive4.value).rstrip('0').rstrip('.') if '.' in str(slive4.value) else str(slive4.value)) + str(slive4.unit) + ' at'
            self.since_new_string_4 = 'Last ' + str(slive4.value) + ' ' + str(slive4.unit) + ' ' + str(slive4.action_type) + ' at Component ' + ('TSN' if slive4.unit == 'hours' else 'CSN' if slive4.unit == 'cycles' else 'RSN')

        if len(self.component.serfice_life) > 4:
            slive5 = self.component.serfice_life[4]
            self.ac_int_5 = self.ac_timeinstallation
            self.slive_5 = slive5.id
            self.ac_string_5 = comp_of_string + ' ' + str(slive5.unit) + ' since last ' + (str(slive5.value).rstrip('0').rstrip('.') if '.' in str(slive5.value) else str(slive5.value)) + str(slive5.unit) + ' ' + str(slive5.action_type)
            self.comp_string_5 = 'Comp ' + str(slive5.unit) + ' since last ' + (str(slive5.value).rstrip('0').rstrip('.') if '.' in str(slive5.value) else str(slive5.value)) + str(slive5.unit) + ' ' + str(slive5.action_type)
            self.date_string_5 = 'Last ' + (str(slive5.value).rstrip('0').rstrip('.') if '.' in str(slive5.value) else str(slive5.value)) + str(slive5.unit) + ' at'
            self.since_new_string_5 = 'Last ' + str(slive5.value) + ' ' + str(slive5.unit) + ' ' + str(slive5.action_type) + ' at Component ' + ('TSN' if slive5.unit == 'hours' else 'CSN' if slive5.unit == 'cycles' else 'RSN')

        if len(self.component.serfice_life) > 5:
            slive6 = self.component.serfice_life[5]
            self.ac_int_6 = self.ac_timeinstallation
            self.slive_6 = slive6.id
            self.ac_string_6 = comp_of_string + ' ' + str(slive6.unit) + ' since last ' + (str(slive6.value).rstrip('0').rstrip('.') if '.' in str(slive6.value) else str(slive6.value)) + str(slive6.unit) + ' ' + str(slive6.action_type)
            self.comp_string_6 = 'Comp ' + str(slive6.unit) + ' since last ' + (str(slive6.value).rstrip('0').rstrip('.') if '.' in str(slive6.value) else str(slive6.value)) + str(slive6.unit) + ' ' + str(slive6.action_type)
            self.date_string_6 = 'Last ' + (str(slive6.value).rstrip('0').rstrip('.') if '.' in str(slive6.value) else str(slive6.value)) + str(slive6.unit) + ' at'
            self.since_new_string_6 = 'Last ' + str(slive6.value) + ' ' + str(slive6.unit) + ' ' + str(slive6.action_type) + ' at Component ' + ('TSN' if slive6.unit == 'hours' else 'CSN' if slive6.unit == 'cycles' else 'RSN')

        if len(self.component.serfice_life) > 6:
            slive7 = self.component.serfice_life[6]
            self.ac_int_7 = self.ac_timeinstallation
            self.slive_7 = slive7.id
            self.ac_string_7 = comp_of_string + ' ' + str(slive7.unit) + ' since last ' + (str(slive7.value).rstrip('0').rstrip('.') if '.' in str(slive7.value) else str(slive7.value)) + str(slive7.unit) + ' ' + str(slive7.action_type)
            self.comp_string_7 = 'Comp ' + str(slive7.unit) + ' since last ' + (str(slive7.value).rstrip('0').rstrip('.') if '.' in str(slive7.value) else str(slive7.value)) + str(slive7.unit) + ' ' + str(slive7.action_type)
            self.date_string_7 = 'Last ' + (str(slive7.value).rstrip('0').rstrip('.') if '.' in str(slive7.value) else str(slive7.value)) + str(slive7.unit) + ' at'
            self.since_new_string_7 = 'Last ' + str(slive7.value) + ' ' + str(slive7.unit) + ' ' + str(slive7.action_type) + ' at Component ' + ('TSN' if slive7.unit == 'hours' else 'CSN' if slive7.unit == 'cycles' else 'RSN')

        if len(self.component.serfice_life) > 7:
            slive8 = self.component.serfice_life[7]
            self.ac_int_8 = self.ac_timeinstallation
            self.slive_8 = slive8.id
            self.ac_string_8 = comp_of_string + ' ' + str(slive8.unit) + ' since last ' + (str(slive8.value).rstrip('0').rstrip('.') if '.' in str(slive8.value) else str(slive8.value)) + str(slive8.unit) + ' ' + str(slive8.action_type)
            self.comp_string_8 = 'Comp ' + str(slive8.unit) + ' since last ' + (str(slive8.value).rstrip('0').rstrip('.') if '.' in str(slive8.value) else str(slive8.value)) + str(slive8.unit) + ' ' + str(slive8.action_type)
            self.date_string_8 = 'Last ' + (str(slive8.value).rstrip('0').rstrip('.') if '.' in str(slive8.value) else str(slive8.value)) + str(slive8.unit) + ' at'
            self.since_new_string_8 = 'Last ' + str(slive8.value) + ' ' + str(slive8.unit) + ' ' + str(slive8.action_type) + ' at Component ' + ('TSN' if slive8.unit == 'hours' else 'CSN' if slive8.unit == 'cycles' else 'RSN')

        if len(self.component.serfice_life) > 8:
            slive9 = self.component.serfice_life[8]
            self.ac_int_9 = self.ac_timeinstallation
            self.slive_9 = slive9.id
            self.ac_string_9 = comp_of_string + ' ' + str(slive9.unit) + ' since last ' + (str(slive9.value).rstrip('0').rstrip('.') if '.' in str(slive9.value) else str(slive9.value)) + str(slive9.unit) + ' ' + str(slive9.action_type)
            self.comp_string_9 = 'Comp ' + str(slive9.unit) + ' since last ' + (str(slive9.value).rstrip('0').rstrip('.') if '.' in str(slive9.value) else str(slive9.value)) + str(slive9.unit) + ' ' + str(slive9.action_type)
            self.date_string_9 = 'Last ' + (str(slive9.value).rstrip('0').rstrip('.') if '.' in str(slive9.value) else str(slive9.value)) + str(slive9.unit) + ' at'
            self.since_new_string_9 = 'Last ' + str(slive9.value) + ' ' + str(slive9.unit) + ' ' + str(slive9.action_type) + ' at Component ' + ('TSN' if slive9.unit == 'hours' else 'CSN' if slive9.unit == 'cycles' else 'RSN')

        if len(self.component.serfice_life) > 9:
            slive10 = self.component.serfice_life[9]
            self.ac_sint10 = self.ac_timeinstallation
            self.slive_10 = slive10.id
            self.ac_string_10 = comp_of_string + ' ' + str(slive10.unit) + ' since last ' + (str(slive10.value).rstrip('0').rstrip('.') if '.' in str(slive10.value) else str(slive10.value)) + str(slive10.unit) + ' ' + str(slive10.action_type)
            self.comp_string_10 = 'Comp ' + str(slive10.unit) + ' since last ' + (str(slive10.value).rstrip('0').rstrip('.') if '.' in str(slive10.value) else str(slive10.value)) + str(slive10.unit) + ' ' + str(slive10.action_type)
            self.date_string_10 = 'Last ' + (str(slive10.value).rstrip('0').rstrip('.') if '.' in str(slive10.value) else str(slive10.value)) + str(slive10.unit) + ' at'
            self.since_new_string_10 = 'Last ' + str(slive10.value) + ' ' + str(slive10.unit) + ' ' + str(slive10.action_type) + ' at Component ' + ('TSN' if slive10.unit == 'hours' else 'CSN' if slive10.unit == 'cycles' else 'RSN')

        if len(self.component.serfice_life) > 10:
            slive11 = self.component.serfice_life[10]
            self.ac_sint11 = self.ac_timeinstallation
            self.slive_11 = slive11.id
            self.ac_string_11 = comp_of_string + ' ' + str(slive11.unit) + ' since last ' + (str(slive11.value).rstrip('0').rstrip('.') if '.' in str(slive11.value) else str(slive11.value)) + str(slive11.unit) + ' ' + str(slive11.action_type)
            self.comp_string_11 = 'Comp ' + str(slive11.unit) + ' since last ' + (str(slive11.value).rstrip('0').rstrip('.') if '.' in str(slive11.value) else str(slive11.value)) + str(slive11.unit) + ' ' + str(slive11.action_type)
            self.date_string_11 = 'Last ' + (str(slive11.value).rstrip('0').rstrip('.') if '.' in str(slive11.value) else str(slive11.value)) + str(slive11.unit) + ' at'
            self.since_new_string_11 = 'Last ' + str(slive11.value) + ' ' + str(slive11.unit) + ' ' + str(slive11.action_type) + ' at Component ' + ('TSN' if slive11.unit == 'hours' else 'CSN' if slive11.unit == 'cycles' else 'RSN')

        if len(self.component.serfice_life) > 11:
            slive12 = self.component.serfice_life[11]
            self.ac_sint12 = self.ac_timeinstallation
            self.slive_12 = slive12.id
            self.ac_string_12 = comp_of_string + ' ' + str(slive12.unit) + ' since last ' + (str(slive12.value).rstrip('0').rstrip('.') if '.' in str(slive12.value) else str(slive12.value)) + str(slive12.unit) + ' ' + str(slive12.action_type)
            self.comp_string_12 = 'Comp ' + str(slive12.unit) + ' since last ' + (str(slive12.value).rstrip('0').rstrip('.') if '.' in str(slive12.value) else str(slive12.value)) + str(slive12.unit) + ' ' + str(slive12.action_type)
            self.date_string_12 = 'Last ' + (str(slive12.value).rstrip('0').rstrip('.') if '.' in str(slive12.value) else str(slive12.value)) + str(slive12.unit) + ' at'
            self.since_new_string_12 = 'Last ' + str(slive12.value) + ' ' + str(slive12.unit) + ' ' + str(slive12.action_type) + ' at Component ' + ('TSN' if slive12.unit == 'hours' else 'CSN' if slive12.unit == 'cycles' else 'RSN')

        if len(self.component.serfice_life) > 12:
            slive13 = self.component.serfice_life[12]
            self.ac_sint13 = self.ac_timeinstallation
            self.slive_13 = slive13.id
            self.ac_string_13 = comp_of_string + ' ' + str(slive13.unit) + ' since last ' + (str(slive13.value).rstrip('0').rstrip('.') if '.' in str(slive13.value) else str(slive13.value)) + str(slive13.unit) + ' ' + str(slive13.action_type)
            self.comp_string_13 = 'Comp ' + str(slive13.unit) + ' since last ' + (str(slive13.value).rstrip('0').rstrip('.') if '.' in str(slive13.value) else str(slive13.value)) + str(slive13.unit) + ' ' + str(slive13.action_type)
            self.date_string_13 = 'Last ' + (str(slive13.value).rstrip('0').rstrip('.') if '.' in str(slive13.value) else str(slive13.value)) + str(slive13.unit) + ' at'
            self.since_new_string_13 = 'Last ' + str(slive13.value) + ' ' + str(slive13.unit) + ' ' + str(slive13.action_type) + ' at Component ' + ('TSN' if slive13.unit == 'hours' else 'CSN' if slive13.unit == 'cycles' else 'RSN')

        if len(self.component.serfice_life) > 13:
            slive14 = self.component.serfice_life[13]
            self.ac_sint14 = self.ac_timeinstallation
            self.slive_14 = slive14.id
            self.ac_string_14 = comp_of_string + ' ' + str(slive14.unit) + ' since last ' + (str(slive14.value).rstrip('0').rstrip('.') if '.' in str(slive14.value) else str(slive14.value)) + str(slive14.unit) + ' ' + str(slive14.action_type)
            self.comp_string_14 = 'Comp ' + str(slive14.unit) + ' since last ' + (str(slive14.value).rstrip('0').rstrip('.') if '.' in str(slive14.value) else str(slive14.value)) + str(slive14.unit) + ' ' + str(slive14.action_type)
            self.date_string_14 = 'Last ' + (str(slive14.value).rstrip('0').rstrip('.') if '.' in str(slive14.value) else str(slive14.value)) + str(slive14.unit) + ' at'
            self.since_new_string_14 = 'Last ' + str(slive14.value) + ' ' + str(slive14.unit) + ' ' + str(slive14.action_type) + ' at Component ' + ('TSN' if slive14.unit == 'hours' else 'CSN' if slive14.unit == 'cycles' else 'RSN')

        if len(self.component.serfice_life) > 14:
            slive15 = self.component.serfice_life[14]
            self.ac_sint15 = self.ac_timeinstallation
            self.slive_15 = slive15.id
            self.ac_string_15 = comp_of_string + ' ' + str(slive15.unit) + ' since last ' + (str(slive15.value).rstrip('0').rstrip('.') if '.' in str(slive15.value) else str(slive15.value)) + str(slive15.unit) + ' ' + str(slive15.action_type)
            self.comp_string_15 = 'Comp ' + str(slive15.unit) + ' since last ' + (str(slive15.value).rstrip('0').rstrip('.') if '.' in str(slive15.value) else str(slive15.value)) + str(slive15.unit) + ' ' + str(slive15.action_type)
            self.date_string_15 = 'Last ' + (str(slive15.value).rstrip('0').rstrip('.') if '.' in str(slive15.value) else str(slive15.value)) + str(slive15.unit) + ' at'
            self.since_new_string_15 = 'Last ' + str(slive15.value) + ' ' + str(slive15.unit) + ' ' + str(slive15.action_type) + ' at Component ' + ('TSN' if slive15.unit == 'hours' else 'CSN' if slive15.unit == 'cycles' else 'RSN')

    def replace(self):
        # PENGURANGAN COMPONENT
        if(self.no_component == True):
            transfer = self.env['stock.picking'].sudo().create({
                'name':'From Plane '+(datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
                'move_type':'direct',
                'picking_type_id':self.env.ref('stock.picking_type_internal').id,
                'location_id':self.env.ref('ams_base.loc_ams_aircraft').id,
                'location_dest_id':self.env.ref('stock.stock_location_stock').id,
                'ctsrf':self.id,
                'move_lines':[(0,0,{
                    'name': self.product_id.name,
                    'product_id': self.product_id.id,
                    'product_uom': self.product_id.uom_id.id,
                    'product_uom_qty': 1, 
                    })],
                })
            transfer.do_transfer()
        if(self.no_component == False):
            # BUG GANTI RUMUS STOCK
            # stock_by_ref = self.env['ams.stock'].search([('product_id','=',self.product_id.id),('bin_id','=',self.warehouse_id.id)])
            transfer = self.env['stock.picking'].sudo().create({
                'name':'From Plane '+(datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
                'move_type':'direct',
                'picking_type_id':self.env.ref('stock.picking_type_internal').id,
                'location_id':self.env.ref('ams_base.loc_ams_aircraft').id,
                'location_dest_id':self.env.ref('stock.stock_location_stock').id,
                'ctsrf':self.id,
                'move_lines':[(0,0,{
                    'name': self.product_id.name,
                    'product_id': self.product_id.id,
                    'product_uom': self.product_id.uom_id.id,
                    'product_uom_qty': 1, 
                    })],
                })
            transfer.do_transfer()
            transfer = self.env['stock.picking'].sudo().create({
                'name':'To Plane '+(datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
                'move_type':'direct',
                'picking_type_id':self.env.ref('stock.picking_type_internal').id,
                'location_id':self.env.ref('stock.stock_location_stock').id,
                'location_dest_id':self.env.ref('ams_base.loc_ams_aircraft').id,
                'ctsrf':self.id,
                'move_lines':[(0,0,{
                    'name': self.product_id.name,
                    'product_id': self.product_id.id,
                    'product_uom': self.product_id.uom_id.id,
                    'product_uom_qty': 1, 
                    })],
                })
            transfer.do_transfer()
            # stock_by_ref = self.env['ams.stock'].search([('product_id','=',self.product_id.id)])
            # stock_by_ref.write({
            #     'stock_on_hand' : stock_by_ref.stock_on_hand - 1,
            #     'stock_scrap' : stock_by_ref.stock_scrap + 1,
            #     })
        self.component.no_component = self.no_component

        if(self.component.is_subcomp == True):
            fleet = self.component.part_id.fleet_id
            engine = self.component.part_id.engine_id
            auxiliary = self.component.part_id.auxiliary_id
            propeller = self.component.part_id.propeller_id
        else:
            fleet = self.component.fleet_id
            engine = self.component.engine_id
            auxiliary = self.component.auxiliary_id
            propeller = self.component.propeller_id

        if (fleet.id == False):
            if (engine):
                fleet = self.env['aircraft.acquisition'].search(['|','|','|',('engine_type_id.id','=',engine.id),('engine2_type_id.id','=',engine.id),('engine3_type_id.id','=',engine.id),('engine4_type_id.id','=',engine.id)], limit=1)
            elif (auxiliary):
                fleet = self.env['aircraft.acquisition'].search([('auxiliary_type_id.id','=',auxiliary.id)], limit=1)
            elif (propeller):
                fleet = self.env['aircraft.acquisition'].search(['|','|','|',('propeller_type_id.id','=',propeller.id),('propeller2_type_id.id','=',propeller.id),('propeller3_type_id.id','=',propeller.id),('propeller4_type_id.id','=',propeller.id)], limit=1)

        recomp_min_hours = self._get_vals()['total_hours'] - self.ac_timeinstallation
        recomp_min_cycles = self._get_vals()['total_landings'] - self.ac_cyclesinstallation
        recomp_min_rins = self._get_vals()['total_rins'] - self.ac_rininstallation

        newcomp_plus_hours = self._get_vals()['total_hours'] - self.ac_timeinstallation
        newcomp_plus_cycles = self._get_vals()['total_landings'] - self.ac_cyclesinstallation
        newcomp_plus_rins = self._get_vals()['total_rins'] - self.ac_rininstallation

        # cek recent component by serial
        if(self.current_serial):
            self.env['stock.production.lot'].search([('id','=',self.current_serial.id)]).write({
                'csn' : self.component.csn - recomp_min_cycles,
                'tsn' : self.component.tsn - recomp_min_hours,
                'tso' : self.component.tso - recomp_min_hours,
                'cso' : self.component.cso - recomp_min_cycles,
                'unserviceable' : self.sn_us,
            })

        # cek new component by serial
        if(self.serial_number):
            self.env['stock.production.lot'].search([('id','=',self.serial_number.id)]).write({
                'csn' : self.component.csn + newcomp_plus_cycles,
                'tsn' : self.component.tsn + newcomp_plus_hours,
                'tso' : self.component.tso + newcomp_plus_hours,
                'cso' : self.component.cso + newcomp_plus_cycles,
            })
        # pengurangan dan penambahan hours cycles component sesuai dengan pemasangan
        comp = self.env['ams.component.part'].search([('id','=',self.component.id)])
        comp.write({
            'product_id' : self.product_id.id,
            'serial_number' : self.serial_number.id,
            'date_installed' : self.date_installed,
            'csn' : self.csn + newcomp_plus_cycles,
            'cso' : self.comp_cyclesinstallation + newcomp_plus_cycles,
            'tsn' : self.tsn + newcomp_plus_hours,
            'tso' : self.comp_timeinstallation + newcomp_plus_hours,
            'ac_timeinstallation' : self.ac_timeinstallation,
            'ac_cyclesinstallation' : self.ac_cyclesinstallation,
            'ac_rininstallation' : self.ac_rininstallation,
            'comp_timeinstallation' : self.comp_timeinstallation + newcomp_plus_hours,
            'comp_cyclesinstallation' : self.comp_cyclesinstallation + newcomp_plus_cycles,
            'comp_rininstallation' : self.comp_rininstallation + newcomp_plus_rins,
            'is_overhaul' : self.is_overhaul,
            'unknown_new' : self.unknown_new,
            })
        if(self.no_component):
            # add history
            hist = self.env['ams.component_history'].create({
                'fleet_id' : fleet.id,
                'engine_id' : engine.id,
                'auxiliary_id' : auxiliary.id,
                'propeller_id' : propeller.id,
                'part_id' : self.component.id,
                'component_id' : self.product_id.id,
                'component_replacement_id' : False,
                'serial_id' : self.current_serial.id,
                'serial_replacement_id' : False,
                'ac_hours' : self.ac_timeinstallation,
                'ac_cycles' : self.ac_cyclesinstallation,
                'hours' : self.comp_timeinstallation + newcomp_plus_hours,
                'cycles' : self.comp_cyclesinstallation + newcomp_plus_cycles,
                'type' : 'detach',
                'reason' : self.reason,
                'premature_removal' : self.premature,
                'date' : False,
                })
        else:
            # add history
            hist = self.env['ams.component_history'].create({
                'fleet_id' : fleet.id,
                'engine_id' : engine.id,
                'auxiliary_id' : auxiliary.id,
                'propeller_id' : propeller.id,
                'part_id' : self.component.id,
                'component_id' : self.product_id.id,
                'component_replacement_id' : self.component.product_id.id,
                'serial_id' : self.current_serial.id,
                'serial_replacement_id' : self.serial_number.id,
                'ac_hours' : self.ac_timeinstallation,
                'ac_cycles' : self.ac_cyclesinstallation,
                'hours' : self.comp_timeinstallation + newcomp_plus_hours,
                'cycles' : self.comp_cyclesinstallation + newcomp_plus_cycles,
                'type' : 'replace',
                'reason' : self.reason,
                'premature_removal' : self.premature,
                'date' : self.date_installed,
                })
        # reset perlakuan servicelife
        normal_treat = ['hours','cycles','rin']
        
        if len(self.component.serfice_life) > 0:
            slive1 = self.component.serfice_life[0]
            if slive1.id != False:
                if(slive1.unit in normal_treat):
                    # HOURS / CYCLES / RIN
                    if(slive1.unit == 'hours'):
                        if(slive1.action_type == 'overhaul'):
                            current = self.comp_timeinstallation
                            at_install = self.comp_timeinstallation
                        elif(slive1.action_type == 'retirement'):
                            current = self.tsn
                            at_install = self.tsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_1
                            at_install = self.tsn - self.since_new_int_1
                        else:
                            current = (self.ac_timeinstallation - self.ac_int_1) + self.comp_int_1
                            at_install = self.comp_int_1
                    elif(slive1.unit == 'cycles'):
                        if(slive1.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive1.action_type == 'retirement'):
                            current = self.csn
                            at_install = self.csn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_1
                            at_install = self.tsn - self.since_new_int_1
                        else:
                            current = (self.ac_cyclesinstallation - self.ac_int_1) + self.comp_int_1
                            at_install = self.comp_int_1
                    elif(slive1.unit == 'rin'):
                        if(slive1.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive1.action_type == 'retirement'):
                            current = self.rsn
                            at_install = self.rsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_1
                            at_install = self.tsn - self.since_new_int_1
                        else:
                            current = (self.ac_rininstallation - self.ac_int_1) + self.comp_int_1
                            at_install = self.comp_int_1
                    slive1.write({
                        'current' : current,
                        'at_install' : at_install,
                        'remaining' : slive1.value - current,
                        # 'at_install' : self.comp_int_1,
                        'value' : slive1.value,
                        'current_date' : False,
                        'next_date' : False,
                        'current_text' : slive1.value,
                        'next_text' : slive1.value,
                        'extension' : 0,
                    })
                else:
                    # CALENDAR
                    if slive1.unit == 'year':
                        dateDue = datetime.strptime(self.comp_date_1, '%Y-%m-%d') + relativedelta(years=int(math.floor(slive1.value)))
                    if slive1.unit == 'month':
                        dateDue = datetime.strptime(self.comp_date_1, '%Y-%m-%d') + relativedelta(months=int(math.floor(slive1.value)))
                    if slive1.unit == 'days':
                        dateDue = datetime.strptime(self.comp_date_1, '%Y-%m-%d') + relativedelta(days=int(math.floor(slive1.value)))
                    dateDue = dateDue.strftime("%Y-%m-%d")
                
                    slive1.write({
                        'current' : 0,
                        'remaining' : slive1.value - 0,
                        'value' : slive1.value,
                        'current_date' : self.comp_date_1,
                        'next_date' : dateDue,
                        'current_text' : self.comp_date_1,
                        'next_text' : dateDue,
                        'extension' : 0,
                    })

        if len(self.component.serfice_life) > 1:
            slive2 = self.component.serfice_life[1]
            if slive2.id != False:
                if(slive2.unit in normal_treat):
                    # HOURS / CYCLES / RIN
                    if(slive2.unit == 'hours'):
                        if(slive2.action_type == 'overhaul'):
                            current = self.comp_timeinstallation
                            at_install = self.comp_timeinstallation
                        elif(slive2.action_type == 'retirement'):
                            current = self.tsn
                            at_install = self.tsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_2
                            at_install = self.tsn - self.since_new_int_2
                        else:
                            current = (self.ac_timeinstallation - self.ac_int_2) + self.comp_int_2
                            at_install = self.comp_int_2
                    elif(slive2.unit == 'cycles'):
                        if(slive2.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive2.action_type == 'retirement'):
                            current = self.csn
                            at_install = self.csn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_2
                            at_install = self.tsn - self.since_new_int_2
                        else:
                            current = (self.ac_cyclesinstallation - self.ac_int_2) + self.comp_int_2
                            at_install = self.comp_int_2
                    elif(slive2.unit == 'rin'):
                        if(slive2.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive2.action_type == 'retirement'):
                            current = self.rsn
                            at_install = self.rsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_2
                            at_install = self.tsn - self.since_new_int_2
                        else:
                            current = (self.ac_rininstallation - self.ac_int_2) + self.comp_int_2
                            at_install = self.comp_int_2
                    slive2.write({
                        'current' : current,
                        'at_install' : at_install,
                        'remaining' : slive2.value - current,
                        'value' : slive2.value,
                        'current_date' : False,
                        'next_date' : False,
                        'current_text' : slive2.value,
                        'next_text' : slive2.value,
                        'extension' : 0,
                    })
                else:
                    # CALENDAR
                    if slive2.unit == 'year':
                        dateDue = datetime.strptime(self.comp_date_2, '%Y-%m-%d') + relativedelta(years=int(math.floor(slive2.value)))
                    if slive2.unit == 'month':
                        dateDue = datetime.strptime(self.comp_date_2, '%Y-%m-%d') + relativedelta(months=int(math.floor(slive2.value)))
                    if slive2.unit == 'days':
                        dateDue = datetime.strptime(self.comp_date_2, '%Y-%m-%d') + relativedelta(days=int(math.floor(slive2.value)))
                    dateDue = dateDue.strftime("%Y-%m-%d")
                
                    slive2.write({
                        'current' : 0,
                        'remaining' : slive2.value - 0,
                        'value' : slive2.value,
                        'current_date' : self.comp_date_2,
                        'next_date' : dateDue,
                        'current_text' : self.comp_date_2,
                        'next_text' : dateDue,
                        'extension' : 0,
                    })

        if len(self.component.serfice_life) > 2:
            slive3 = self.component.serfice_life[2]
            if slive3.id != False:
                if(slive3.unit in normal_treat):
                    # HOURS / CYCLES / RIN
                    if(slive3.unit == 'hours'):
                        if(slive3.action_type == 'overhaul'):
                            current = self.comp_timeinstallation
                            at_install = self.comp_timeinstallation
                        elif(slive3.action_type == 'retirement'):
                            current = self.tsn
                            at_install = self.tsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_3
                            at_install = self.tsn - self.since_new_int_3
                        else:
                            current = (self.ac_timeinstallation - self.ac_int_3) + self.comp_int_3
                            at_install = self.comp_int_3
                    elif(slive3.unit == 'cycles'):
                        if(slive3.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive3.action_type == 'retirement'):
                            current = self.csn
                            at_install = self.csn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_3
                            at_install = self.tsn - self.since_new_int_3
                        else:
                            current = (self.ac_cyclesinstallation - self.ac_int_3) + self.comp_int_3
                            at_install = self.comp_int_3
                    elif(slive3.unit == 'rin'):
                        if(slive3.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive3.action_type == 'retirement'):
                            current = self.rsn
                            at_install = self.rsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_3
                            at_install = self.tsn - self.since_new_int_3
                        else:
                            current = (self.ac_rininstallation - self.ac_int_3) + self.comp_int_3
                            at_install = self.comp_int_3
                    slive3.write({
                        'current' : current,
                        'at_install' : at_install,
                        'remaining' : slive3.value - current,
                        'value' : slive3.value,
                        'current_date' : False,
                        'next_date' : False,
                        'current_text' : slive3.value,
                        'next_text' : slive3.value,
                        'extension' : 0,
                    })
                else:
                    # CALENDAR
                    if slive3.unit == 'year':
                        dateDue = datetime.strptime(self.comp_date_3, '%Y-%m-%d') + relativedelta(years=int(math.floor(slive3.value)))
                    if slive3.unit == 'month':
                        dateDue = datetime.strptime(self.comp_date_3, '%Y-%m-%d') + relativedelta(months=int(math.floor(slive3.value)))
                    if slive3.unit == 'days':
                        dateDue = datetime.strptime(self.comp_date_3, '%Y-%m-%d') + relativedelta(days=int(math.floor(slive3.value)))
                    dateDue = dateDue.strftime("%Y-%m-%d")
                
                    slive3.write({
                        'current' : 0,
                        'remaining' : slive3.value - 0,
                        'value' : slive3.value,
                        'current_date' : self.comp_date_3,
                        'next_date' : dateDue,
                        'current_text' : self.comp_date_3,
                        'next_text' : dateDue,
                        'extension' : 0,
                    })

        if len(self.component.serfice_life) > 3:
            slive4 = self.component.serfice_life[3]
            if slive4.id != False:
                if(slive4.unit in normal_treat):
                    # HOURS / CYCLES / RIN
                    if(slive4.unit == 'hours'):
                        if(slive4.action_type == 'overhaul'):
                            current = self.comp_timeinstallation
                            at_install = self.comp_timeinstallation
                        elif(slive4.action_type == 'retirement'):
                            current = self.tsn
                            at_install = self.tsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_4
                            at_install = self.tsn - self.since_new_int_4
                        else:
                            current = (self.ac_timeinstallation - self.ac_int_4) + self.comp_int_4
                            at_install = self.comp_int_4
                    elif(slive4.unit == 'cycles'):
                        if(slive4.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive4.action_type == 'retirement'):
                            current = self.csn
                            at_install = self.csn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_4
                            at_install = self.tsn - self.since_new_int_4
                        else:
                            current = (self.ac_cyclesinstallation - self.ac_int_4) + self.comp_int_4
                            at_install = self.comp_int_4
                    elif(slive4.unit == 'rin'):
                        if(slive4.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive4.action_type == 'retirement'):
                            current = self.rsn
                            at_install = self.rsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_4
                            at_install = self.tsn - self.since_new_int_4
                        else:
                            current = (self.ac_rininstallation - self.ac_int_4) + self.comp_int_4
                            at_install = self.comp_int_4
                    slive4.write({
                        'current' : current,
                        'at_install' : at_install,
                        'remaining' : slive4.value - current,
                        'value' : slive4.value,
                        'current_date' : False,
                        'next_date' : False,
                        'current_text' : slive4.value,
                        'next_text' : slive4.value,
                        'extension' : 0,
                    })
                else:
                    # CALENDAR
                    if slive4.unit == 'year':
                        dateDue = datetime.strptime(self.comp_date_4, '%Y-%m-%d') + relativedelta(years=int(math.floor(slive4.value)))
                    if slive4.unit == 'month':
                        dateDue = datetime.strptime(self.comp_date_4, '%Y-%m-%d') + relativedelta(months=int(math.floor(slive4.value)))
                    if slive4.unit == 'days':
                        dateDue = datetime.strptime(self.comp_date_4, '%Y-%m-%d') + relativedelta(days=int(math.floor(slive4.value)))
                    dateDue = dateDue.strftime("%Y-%m-%d")
                
                    slive4.write({
                        'current' : 0,
                        'remaining' : slive4.value - 0,
                        'value' : slive4.value,
                        'current_date' : self.comp_date_4,
                        'next_date' : dateDue,
                        'current_text' : self.comp_date_4,
                        'next_text' : dateDue,
                        'extension' : 0,
                    })

        if len(self.component.serfice_life) > 4:
            slive5 = self.component.serfice_life[4]
            if slive5.id != False:
                if(slive5.unit in normal_treat):
                    # HOURS / CYCLES / RIN
                    if(slive5.unit == 'hours'):
                        if(slive5.action_type == 'overhaul'):
                            current = self.comp_timeinstallation
                            at_install = self.comp_timeinstallation
                        elif(slive5.action_type == 'retirement'):
                            current = self.tsn
                            at_install = self.tsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_5
                            at_install = self.tsn - self.since_new_int_5
                        else:
                            current = (self.ac_timeinstallation - self.ac_int_5) + self.comp_int_5
                            at_install = self.comp_int_5
                    elif(slive5.unit == 'cycles'):
                        if(slive5.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive5.action_type == 'retirement'):
                            current = self.csn
                            at_install = self.csn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_5
                            at_install = self.tsn - self.since_new_int_5
                        else:
                            current = (self.ac_cyclesinstallation - self.ac_int_5) + self.comp_int_5
                            at_install = self.comp_int_5
                    elif(slive5.unit == 'rin'):
                        if(slive5.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive5.action_type == 'retirement'):
                            current = self.rsn
                            at_install = self.rsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_5
                            at_install = self.tsn - self.since_new_int_5
                        else:
                            current = (self.ac_rininstallation - self.ac_int_5) + self.comp_int_5
                            at_install = self.comp_int_5
                    slive5.write({
                        'current' : current,
                        'at_install' : at_install,
                        'remaining' : slive5.value - current,
                        'value' : slive5.value,
                        'current_date' : False,
                        'next_date' : False,
                        'current_text' : slive5.value,
                        'next_text' : slive5.value,
                        'extension' : 0,
                    })
                else:
                    # CALENDAR
                    if slive5.unit == 'year':
                        dateDue = datetime.strptime(self.comp_date_5, '%Y-%m-%d') + relativedelta(years=int(math.floor(slive5.value)))
                    if slive5.unit == 'month':
                        dateDue = datetime.strptime(self.comp_date_5, '%Y-%m-%d') + relativedelta(months=int(math.floor(slive5.value)))
                    if slive5.unit == 'days':
                        dateDue = datetime.strptime(self.comp_date_5, '%Y-%m-%d') + relativedelta(days=int(math.floor(slive5.value)))
                    dateDue = dateDue.strftime("%Y-%m-%d")
                
                    slive5.write({
                        'current' : 0,
                        'remaining' : slive5.value - 0,
                        'value' : slive5.value,
                        'current_date' : self.comp_date_5,
                        'next_date' : dateDue,
                        'current_text' : self.comp_date_5,
                        'next_text' : dateDue,
                        'extension' : 0,
                    })

        if len(self.component.serfice_life) > 5:
            slive6 = self.component.serfice_life[5]
            if slive6.id != False:
                if(slive6.unit in normal_treat):
                    # HOURS / CYCLES / RIN
                    if(slive6.unit == 'hours'):
                        if(slive6.action_type == 'overhaul'):
                            current = self.comp_timeinstallation
                            at_install = self.comp_timeinstallation
                        elif(slive6.action_type == 'retirement'):
                            current = self.tsn
                            at_install = self.tsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_6
                            at_install = self.tsn - self.since_new_int_6
                        else:
                            current = (self.ac_timeinstallation - self.ac_int_6) + self.comp_int_6
                            at_install = self.comp_int_6
                    elif(slive6.unit == 'cycles'):
                        if(slive6.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive6.action_type == 'retirement'):
                            current = self.csn
                            at_install = self.csn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_6
                            at_install = self.tsn - self.since_new_int_6
                        else:
                            current = (self.ac_cyclesinstallation - self.ac_int_6) + self.comp_int_6
                            at_install = self.comp_int_6
                    elif(slive6.unit == 'rin'):
                        if(slive6.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive6.action_type == 'retirement'):
                            current = self.rsn
                            at_install = self.rsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_6
                            at_install = self.tsn - self.since_new_int_6
                        else:
                            current = (self.ac_rininstallation - self.ac_int_6) + self.comp_int_6
                            at_install = self.comp_int_6
                    slive6.write({
                        'current' : current,
                        'at_install' : at_install,
                        'remaining' : slive6.value - current,
                        'value' : slive6.value,
                        'current_date' : False,
                        'next_date' : False,
                        'current_text' : slive6.value,
                        'next_text' : slive6.value,
                        'extension' : 0,
                    })
                else:
                    # CALENDAR
                    if slive6.unit == 'year':
                        dateDue = datetime.strptime(self.comp_date_6, '%Y-%m-%d') + relativedelta(years=int(math.floor(slive6.value)))
                    if slive6.unit == 'month':
                        dateDue = datetime.strptime(self.comp_date_6, '%Y-%m-%d') + relativedelta(months=int(math.floor(slive6.value)))
                    if slive6.unit == 'days':
                        dateDue = datetime.strptime(self.comp_date_6, '%Y-%m-%d') + relativedelta(days=int(math.floor(slive6.value)))
                    dateDue = dateDue.strftime("%Y-%m-%d")
                
                    slive6.write({
                        'current' : 0,
                        'remaining' : slive6.value - 0,
                        'value' : slive6.value,
                        'current_date' : self.comp_date_6,
                        'next_date' : dateDue,
                        'current_text' : self.comp_date_6,
                        'next_text' : dateDue,
                        'extension' : 0,
                    })

        if len(self.component.serfice_life) > 6:
            slive7 = self.component.serfice_life[6]
            if slive7.id != False:
                if(slive7.unit in normal_treat):
                    # HOURS / CYCLES / RIN
                    if(slive7.unit == 'hours'):
                        if(slive7.action_type == 'overhaul'):
                            current = self.comp_timeinstallation
                            at_install = self.comp_timeinstallation
                        elif(slive7.action_type == 'retirement'):
                            current = self.tsn
                            at_install = self.tsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_7
                            at_install = self.tsn - self.since_new_int_7
                        else:
                            current = (self.ac_timeinstallation - self.ac_int_7) + self.comp_int_7
                            at_install = self.comp_int_7
                    elif(slive7.unit == 'cycles'):
                        if(slive7.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive7.action_type == 'retirement'):
                            current = self.csn
                            at_install = self.csn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_7
                            at_install = self.tsn - self.since_new_int_7
                        else:
                            current = (self.ac_cyclesinstallation - self.ac_int_7) + self.comp_int_7
                            at_install = self.comp_int_7
                    elif(slive7.unit == 'rin'):
                        if(slive7.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive7.action_type == 'retirement'):
                            current = self.rsn
                            at_install = self.rsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_7
                            at_install = self.tsn - self.since_new_int_7
                        else:
                            current = (self.ac_rininstallation - self.ac_int_7) + self.comp_int_7
                            at_install = self.comp_int_7
                    slive7.write({
                        'current' : current,
                        'at_install' : at_install,
                        'remaining' : slive7.value - current,
                        'value' : slive7.value,
                        'current_date' : False,
                        'next_date' : False,
                        'current_text' : slive7.value,
                        'next_text' : slive7.value,
                        'extension' : 0,
                    })
                else:
                    # CALENDAR
                    if slive7.unit == 'year':
                        dateDue = datetime.strptime(self.comp_date_7, '%Y-%m-%d') + relativedelta(years=int(math.floor(slive7.value)))
                    if slive7.unit == 'month':
                        dateDue = datetime.strptime(self.comp_date_7, '%Y-%m-%d') + relativedelta(months=int(math.floor(slive7.value)))
                    if slive7.unit == 'days':
                        dateDue = datetime.strptime(self.comp_date_7, '%Y-%m-%d') + relativedelta(days=int(math.floor(slive7.value)))
                    dateDue = dateDue.strftime("%Y-%m-%d")
                
                    slive7.write({
                        'current' : 0,
                        'remaining' : slive7.value - 0,
                        'value' : slive7.value,
                        'current_date' : self.comp_date_7,
                        'next_date' : dateDue,
                        'current_text' : self.comp_date_7,
                        'next_text' : dateDue,
                        'extension' : 0,
                    })

        if len(self.component.serfice_life) > 7:
            slive8 = self.component.serfice_life[7]
            if slive8.id != False:
                if(slive8.unit in normal_treat):
                    # HOURS / CYCLES / RIN
                    if(slive8.unit == 'hours'):
                        if(slive8.action_type == 'overhaul'):
                            current = self.comp_timeinstallation
                            at_install = self.comp_timeinstallation
                        elif(slive8.action_type == 'retirement'):
                            current = self.tsn
                            at_install = self.tsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_8
                            at_install = self.tsn - self.since_new_int_8
                        else:
                            current = (self.ac_timeinstallation - self.ac_int_8) + self.comp_int_8
                            at_install = self.comp_int_8
                    elif(slive8.unit == 'cycles'):
                        if(slive8.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive8.action_type == 'retirement'):
                            current = self.csn
                            at_install = self.csn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_8
                            at_install = self.tsn - self.since_new_int_8
                        else:
                            current = (self.ac_cyclesinstallation - self.ac_int_8) + self.comp_int_8
                            at_install = self.comp_int_8
                    elif(slive8.unit == 'rin'):
                        if(slive8.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive8.action_type == 'retirement'):
                            current = self.rsn
                            at_install = self.rsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_8
                            at_install = self.tsn - self.since_new_int_8
                        else:
                            current = (self.ac_rininstallation - self.ac_int_8) + self.comp_int_8
                            at_install = self.comp_int_8
                    slive8.write({
                        'current' : current,
                        'at_install' : at_install,
                        'remaining' : slive8.value - current,
                        'value' : slive8.value,
                        'current_date' : False,
                        'next_date' : False,
                        'current_text' : slive8.value,
                        'next_text' : slive8.value,
                        'extension' : 0,
                    })
                else:
                    # CALENDAR
                    if slive8.unit == 'year':
                        dateDue = datetime.strptime(self.comp_date_8, '%Y-%m-%d') + relativedelta(years=int(math.floor(slive8.value)))
                    if slive8.unit == 'month':
                        dateDue = datetime.strptime(self.comp_date_8, '%Y-%m-%d') + relativedelta(months=int(math.floor(slive8.value)))
                    if slive8.unit == 'days':
                        dateDue = datetime.strptime(self.comp_date_8, '%Y-%m-%d') + relativedelta(days=int(math.floor(slive8.value)))
                    dateDue = dateDue.strftime("%Y-%m-%d")
                
                    slive8.write({
                        'current' : 0,
                        'remaining' : slive8.value - 0,
                        'value' : slive8.value,
                        'current_date' : self.comp_date_8,
                        'next_date' : dateDue,
                        'current_text' : self.comp_date_8,
                        'next_text' : dateDue,
                        'extension' : 0,
                    })

        if len(self.component.serfice_life) > 8:
            slive9 = self.component.serfice_life[8]
            if slive9.id != False:
                if(slive9.unit in normal_treat):
                    # HOURS / CYCLES / RIN
                    if(slive9.unit == 'hours'):
                        if(slive9.action_type == 'overhaul'):
                            current = self.comp_timeinstallation
                            at_install = self.comp_timeinstallation
                        elif(slive9.action_type == 'retirement'):
                            current = self.tsn
                            at_install = self.tsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_9
                            at_install = self.tsn - self.since_new_int_9
                        else:
                            current = (self.ac_timeinstallation - self.ac_int_9) + self.comp_int_9
                            at_install = self.comp_int_9
                    elif(slive9.unit == 'cycles'):
                        if(slive9.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive9.action_type == 'retirement'):
                            current = self.csn
                            at_install = self.csn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_9
                            at_install = self.tsn - self.since_new_int_9
                        else:
                            current = (self.ac_cyclesinstallation - self.ac_int_9) + self.comp_int_9
                            at_install = self.comp_int_9
                    elif(slive9.unit == 'rin'):
                        if(slive9.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive9.action_type == 'retirement'):
                            current = self.rsn
                            at_install = self.rsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_9
                            at_install = self.tsn - self.since_new_int_9
                        else:
                            current = (self.ac_rininstallation - self.ac_int_9) + self.comp_int_9
                            at_install = self.comp_int_9
                    slive9.write({
                        'current' : current,
                        'at_install' : at_install,
                        'remaining' : slive9.value - current,
                        'value' : slive9.value,
                        'current_date' : False,
                        'next_date' : False,
                        'current_text' : slive9.value,
                        'next_text' : slive9.value,
                        'extension' : 0,
                    })
                else:
                    # CALENDAR
                    if slive9.unit == 'year':
                        dateDue = datetime.strptime(self.comp_date_9, '%Y-%m-%d') + relativedelta(years=int(math.floor(slive9.value)))
                    if slive9.unit == 'month':
                        dateDue = datetime.strptime(self.comp_date_9, '%Y-%m-%d') + relativedelta(months=int(math.floor(slive9.value)))
                    if slive9.unit == 'days':
                        dateDue = datetime.strptime(self.comp_date_9, '%Y-%m-%d') + relativedelta(days=int(math.floor(slive9.value)))
                    dateDue = dateDue.strftime("%Y-%m-%d")
                
                    slive9.write({
                        'current' : 0,
                        'remaining' : slive9.value - 0,
                        'value' : slive9.value,
                        'current_date' : self.comp_date_9,
                        'next_date' : dateDue,
                        'current_text' : self.comp_date_9,
                        'next_text' : dateDue,
                        'extension' : 0,
                    })

        if len(self.component.serfice_life) > 9:
            slive10 = self.component.serfice_life[9]
            if slive10.id != False:
                if(slive10.unit in normal_treat):
                    # HOURS / CYCLES / RIN
                    if(slive10.unit == 'hours'):
                        if(slive10.action_type == 'overhaul'):
                            current = self.comp_timeinstallation
                            at_install = self.comp_timeinstallation
                        elif(slive10.action_type == 'retirement'):
                            current = self.tsn
                            at_install = self.tsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_10
                            at_install = self.tsn - self.since_new_int_10
                        else:
                            current = (self.ac_timeinstallation - self.ac_int_10) + self.comp_int_10
                            at_install = self.comp_int_10
                    elif(slive10.unit == 'cycles'):
                        if(slive10.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive10.action_type == 'retirement'):
                            current = self.csn
                            at_install = self.csn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_10
                            at_install = self.tsn - self.since_new_int_10
                        else:
                            current = (self.ac_cyclesinstallation - self.ac_int_10) + self.comp_int_10
                            at_install = self.comp_int_10
                    elif(slive10.unit == 'rin'):
                        if(slive10.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive10.action_type == 'retirement'):
                            current = self.rsn
                            at_install = self.rsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_10
                            at_install = self.tsn - self.since_new_int_10
                        else:
                            current = (self.ac_rininstallation - self.ac_int_10) + self.comp_int_10
                            at_install = self.comp_int_10
                    slive10.write({
                        'current' : current,
                        'at_install' : at_install,
                        'remaining' : slive10.value - current,
                        'value' : slive10.value,
                        'current_date' : False,
                        'next_date' : False,
                        'current_text' : slive10.value,
                        'next_text' : slive10.value,
                        'extension' : 0,
                    })
                else:
                    # CALENDAR
                    if slive10.unit == 'year':
                        dateDue = datetime.strptime(self.comp_date_10, '%Y-%m-%d') + relativedelta(years=int(math.floor(slive10.value)))
                    if slive10.unit == 'month':
                        dateDue = datetime.strptime(self.comp_date_10, '%Y-%m-%d') + relativedelta(months=int(math.floor(slive10.value)))
                    if slive10.unit == 'days':
                        dateDue = datetime.strptime(self.comp_date_10, '%Y-%m-%d') + relativedelta(days=int(math.floor(slive10.value)))
                    dateDue = dateDue.strftime("%Y-%m-%d")
                
                    slive10.write({
                        'current' : 0,
                        'remaining' : slive10.value - 0,
                        'value' : slive10.value,
                        'current_date' : self.comp_date_10,
                        'next_date' : dateDue,
                        'current_text' : self.comp_date_10,
                        'next_text' : dateDue,
                        'extension' : 0,
                    })

        if len(self.component.serfice_life) > 10:
            slive11 = self.component.serfice_life[10]
            if slive11.id != False:
                if(slive11.unit in normal_treat):
                    # HOURS / CYCLES / RIN
                    if(slive11.unit == 'hours'):
                        if(slive11.action_type == 'overhaul'):
                            current = self.comp_timeinstallation
                            at_install = self.comp_timeinstallation
                        elif(slive11.action_type == 'retirement'):
                            current = self.tsn
                            at_install = self.tsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_11
                            at_install = self.tsn - self.since_new_int_11
                        else:
                            current = (self.ac_timeinstallation - self.ac_int_11) + self.comp_int_11
                            at_install = self.comp_int_11
                    elif(slive11.unit == 'cycles'):
                        if(slive11.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive11.action_type == 'retirement'):
                            current = self.csn
                            at_install = self.csn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_11
                            at_install = self.tsn - self.since_new_int_11
                        else:
                            current = (self.ac_cyclesinstallation - self.ac_int_11) + self.comp_int_11
                            at_install = self.comp_int_11
                    elif(slive11.unit == 'rin'):
                        if(slive11.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive11.action_type == 'retirement'):
                            current = self.rsn
                            at_install = self.rsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_11
                            at_install = self.tsn - self.since_new_int_11
                        else:
                            current = (self.ac_rininstallation - self.ac_int_11) + self.comp_int_11
                            at_install = self.comp_int_11
                    slive11.write({
                        'current' : current,
                        'at_install' : at_install,
                        'remaining' : slive11.value - current,
                        'value' : slive11.value,
                        'current_date' : False,
                        'next_date' : False,
                        'current_text' : slive11.value,
                        'next_text' : slive11.value,
                        'extension' : 0,
                    })
                else:
                    # CALENDAR
                    if slive11.unit == 'year':
                        dateDue = datetime.strptime(self.comp_date_11, '%Y-%m-%d') + relativedelta(years=int(math.floor(slive11.value)))
                    if slive11.unit == 'month':
                        dateDue = datetime.strptime(self.comp_date_11, '%Y-%m-%d') + relativedelta(months=int(math.floor(slive11.value)))
                    if slive11.unit == 'days':
                        dateDue = datetime.strptime(self.comp_date_11, '%Y-%m-%d') + relativedelta(days=int(math.floor(slive11.value)))
                    dateDue = dateDue.strftime("%Y-%m-%d")
                
                    slive11.write({
                        'current' : 0,
                        'remaining' : slive11.value - 0,
                        'value' : slive11.value,
                        'current_date' : self.comp_date_11,
                        'next_date' : dateDue,
                        'current_text' : self.comp_date_11,
                        'next_text' : dateDue,
                        'extension' : 0,
                    })

        if len(self.component.serfice_life) > 11:
            slive12 = self.component.serfice_life[11]
            if slive12.id != False:
                if(slive12.unit in normal_treat):
                    # HOURS / CYCLES / RIN
                    if(slive12.unit == 'hours'):
                        if(slive12.action_type == 'overhaul'):
                            current = self.comp_timeinstallation
                            at_install = self.comp_timeinstallation
                        elif(slive12.action_type == 'retirement'):
                            current = self.tsn
                            at_install = self.tsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_12
                            at_install = self.tsn - self.since_new_int_12
                        else:
                            current = (self.ac_timeinstallation - self.ac_int_12) + self.comp_int_12
                            at_install = self.comp_int_12
                    elif(slive12.unit == 'cycles'):
                        if(slive12.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive12.action_type == 'retirement'):
                            current = self.csn
                            at_install = self.csn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_12
                            at_install = self.tsn - self.since_new_int_12
                        else:
                            current = (self.ac_cyclesinstallation - self.ac_int_12) + self.comp_int_12
                            at_install = self.comp_int_12
                    elif(slive12.unit == 'rin'):
                        if(slive12.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive12.action_type == 'retirement'):
                            current = self.rsn
                            at_install = self.rsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_12
                            at_install = self.tsn - self.since_new_int_12
                        else:
                            current = (self.ac_rininstallation - self.ac_int_12) + self.comp_int_12
                            at_install = self.comp_int_12
                    slive12.write({
                        'current' : current,
                        'at_install' : at_install,
                        'remaining' : slive12.value - current,
                        'value' : slive12.value,
                        'current_date' : False,
                        'next_date' : False,
                        'current_text' : slive12.value,
                        'next_text' : slive12.value,
                        'extension' : 0,
                    })
                else:
                    # CALENDAR
                    if slive12.unit == 'year':
                        dateDue = datetime.strptime(self.comp_date_12, '%Y-%m-%d') + relativedelta(years=int(math.floor(slive12.value)))
                    if slive12.unit == 'month':
                        dateDue = datetime.strptime(self.comp_date_12, '%Y-%m-%d') + relativedelta(months=int(math.floor(slive12.value)))
                    if slive12.unit == 'days':
                        dateDue = datetime.strptime(self.comp_date_12, '%Y-%m-%d') + relativedelta(days=int(math.floor(slive12.value)))
                    dateDue = dateDue.strftime("%Y-%m-%d")
                
                    slive12.write({
                        'current' : 0,
                        'remaining' : slive12.value - 0,
                        'value' : slive12.value,
                        'current_date' : self.comp_date_12,
                        'next_date' : dateDue,
                        'current_text' : self.comp_date_12,
                        'next_text' : dateDue,
                        'extension' : 0,
                    })

        if len(self.component.serfice_life) > 12:
            slive13 = self.component.serfice_life[12]
            if slive13.id != False:
                if(slive13.unit in normal_treat):
                    # HOURS / CYCLES / RIN
                    if(slive13.unit == 'hours'):
                        if(slive13.action_type == 'overhaul'):
                            current = self.comp_timeinstallation
                            at_install = self.comp_timeinstallation
                        elif(slive13.action_type == 'retirement'):
                            current = self.tsn
                            at_install = self.tsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_13
                            at_install = self.tsn - self.since_new_int_13
                        else:
                            current = (self.ac_timeinstallation - self.ac_int_13) + self.comp_int_13
                            at_install = self.comp_int_13
                    elif(slive13.unit == 'cycles'):
                        if(slive13.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive13.action_type == 'retirement'):
                            current = self.csn
                            at_install = self.csn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_13
                            at_install = self.tsn - self.since_new_int_13
                        else:
                            current = (self.ac_cyclesinstallation - self.ac_int_13) + self.comp_int_13
                            at_install = self.comp_int_13
                    elif(slive13.unit == 'rin'):
                        if(slive13.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive13.action_type == 'retirement'):
                            current = self.rsn
                            at_install = self.rsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_13
                            at_install = self.tsn - self.since_new_int_13
                        else:
                            current = (self.ac_rininstallation - self.ac_int_13) + self.comp_int_13
                            at_install = self.comp_int_13
                    slive13.write({
                        'current' : current,
                        'at_install' : at_install,
                        'remaining' : slive13.value - current,
                        'value' : slive13.value,
                        'current_date' : False,
                        'next_date' : False,
                        'current_text' : slive13.value,
                        'next_text' : slive13.value,
                        'extension' : 0,
                    })
                else:
                    # CALENDAR
                    if slive13.unit == 'year':
                        dateDue = datetime.strptime(self.comp_date_13, '%Y-%m-%d') + relativedelta(years=int(math.floor(slive13.value)))
                    if slive13.unit == 'month':
                        dateDue = datetime.strptime(self.comp_date_13, '%Y-%m-%d') + relativedelta(months=int(math.floor(slive13.value)))
                    if slive13.unit == 'days':
                        dateDue = datetime.strptime(self.comp_date_13, '%Y-%m-%d') + relativedelta(days=int(math.floor(slive13.value)))
                    dateDue = dateDue.strftime("%Y-%m-%d")
                
                    slive13.write({
                        'current' : 0,
                        'remaining' : slive13.value - 0,
                        'value' : slive13.value,
                        'current_date' : self.comp_date_13,
                        'next_date' : dateDue,
                        'current_text' : self.comp_date_13,
                        'next_text' : dateDue,
                        'extension' : 0,
                    })

        if len(self.component.serfice_life) > 13:
            slive14 = self.component.serfice_life[13]
            if slive14.id != False:
                if(slive14.unit in normal_treat):
                    # HOURS / CYCLES / RIN
                    if(slive14.unit == 'hours'):
                        if(slive14.action_type == 'overhaul'):
                            current = self.comp_timeinstallation
                            at_install = self.comp_timeinstallation
                        elif(slive14.action_type == 'retirement'):
                            current = self.tsn
                            at_install = self.tsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_14
                            at_install = self.tsn - self.since_new_int_14
                        else:
                            current = (self.ac_timeinstallation - self.ac_int_14) + self.comp_int_14
                            at_install = self.comp_int_14
                    elif(slive14.unit == 'cycles'):
                        if(slive14.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive14.action_type == 'retirement'):
                            current = self.csn
                            at_install = self.csn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_14
                            at_install = self.tsn - self.since_new_int_14
                        else:
                            current = (self.ac_cyclesinstallation - self.ac_int_14) + self.comp_int_14
                            at_install = self.comp_int_14
                    elif(slive14.unit == 'rin'):
                        if(slive14.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive14.action_type == 'retirement'):
                            current = self.rsn
                            at_install = self.rsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_14
                            at_install = self.tsn - self.since_new_int_14
                        else:
                            current = (self.ac_rininstallation - self.ac_int_14) + self.comp_int_14
                            at_install = self.comp_int_14
                    slive14.write({
                        'current' : current,
                        'at_install' : at_install,
                        'remaining' : slive14.value - current,
                        'value' : slive14.value,
                        'current_date' : False,
                        'next_date' : False,
                        'current_text' : slive14.value,
                        'next_text' : slive14.value,
                        'extension' : 0,
                    })
                else:
                    # CALENDAR
                    if slive14.unit == 'year':
                        dateDue = datetime.strptime(self.comp_date_14, '%Y-%m-%d') + relativedelta(years=int(math.floor(slive14.value)))
                    if slive14.unit == 'month':
                        dateDue = datetime.strptime(self.comp_date_14, '%Y-%m-%d') + relativedelta(months=int(math.floor(slive14.value)))
                    if slive14.unit == 'days':
                        dateDue = datetime.strptime(self.comp_date_14, '%Y-%m-%d') + relativedelta(days=int(math.floor(slive14.value)))
                    dateDue = dateDue.strftime("%Y-%m-%d")
                
                    slive14.write({
                        'current' : 0,
                        'remaining' : slive14.value - 0,
                        'value' : slive14.value,
                        'current_date' : self.comp_date_14,
                        'next_date' : dateDue,
                        'current_text' : self.comp_date_14,
                        'next_text' : dateDue,
                        'extension' : 0,
                    })

        if len(self.component.serfice_life) > 14:
            slive15 = self.component.serfice_life[14]
            if slive15.id != False:
                if(slive15.unit in normal_treat):
                    # HOURS / CYCLES / RIN
                    if(slive15.unit == 'hours'):
                        if(slive15.action_type == 'overhaul'):
                            current = self.comp_timeinstallation
                            at_install = self.comp_timeinstallation
                        elif(slive15.action_type == 'retirement'):
                            current = self.tsn
                            at_install = self.tsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_15
                            at_install = self.tsn - self.since_new_int_15
                        else:
                            current = (self.ac_timeinstallation - self.ac_int_15) + self.comp_int_15
                            at_install = self.comp_int_15
                    elif(slive15.unit == 'cycles'):
                        if(slive15.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive15.action_type == 'retirement'):
                            current = self.csn
                            at_install = self.csn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_15
                            at_install = self.tsn - self.since_new_int_15
                        else:
                            current = (self.ac_cyclesinstallation - self.ac_int_15) + self.comp_int_15
                            at_install = self.comp_int_15
                    elif(slive15.unit == 'rin'):
                        if(slive15.action_type == 'overhaul'):
                            current = self.comp_cyclesinstallation
                            at_install = self.comp_cyclesinstallation
                        elif(slive15.action_type == 'retirement'):
                            current = self.rsn
                            at_install = self.rsn
                        elif(self.use_comp_hour == True):
                            current = self.tsn - self.since_new_int_15
                            at_install = self.tsn - self.since_new_int_15
                        else:
                            current = (self.ac_rininstallation - self.ac_int_15) + self.comp_int_15
                            at_install = self.comp_int_15
                    slive15.write({
                        'current' : current,
                        'at_install' : at_install,
                        'remaining' : slive15.value - current,
                        'value' : slive15.value,
                        'current_date' : False,
                        'next_date' : False,
                        'current_text' : slive15.value,
                        'next_text' : slive15.value,
                        'extension' : 0,
                    })
                else:
                    # CALENDAR
                    if slive15.unit == 'year':
                        dateDue = datetime.strptime(self.comp_date_15, '%Y-%m-%d') + relativedelta(years=int(math.floor(slive15.value)))
                    if slive15.unit == 'month':
                        dateDue = datetime.strptime(self.comp_date_15, '%Y-%m-%d') + relativedelta(months=int(math.floor(slive15.value)))
                    if slive15.unit == 'days':
                        dateDue = datetime.strptime(self.comp_date_15, '%Y-%m-%d') + relativedelta(days=int(math.floor(slive15.value)))
                    dateDue = dateDue.strftime("%Y-%m-%d")
                
                    slive15.write({
                        'current' : 0,
                        'remaining' : slive15.value - 0,
                        'value' : slive15.value,
                        'current_date' : self.comp_date_15,
                        'next_date' : dateDue,
                        'current_text' : self.comp_date_15,
                        'next_text' : dateDue,
                        'extension' : 0,
                    })


        # for slive in self.component.serfice_life:
        #     cvalue = slive.value
        #     pvalue = 0
        #     if(slive.unit == 'hours'):
        #         cvalue = cvalue + newcomp_plus_hours
        #         plavue = newcomp_plus_hours
        #     elif(slive.unit == 'cycles'):
        #         cvalue = cvalue + newcomp_plus_cycles
        #         plavue = newcomp_plus_cycles
        #     elif(slive.unit == 'rin'):
        #         cvalue = cvalue + newcomp_plus_rins
        #         plavue = newcomp_plus_rins

        #     if(slive.unit in normal_treat):
        #         slive.write({
        #             'extension' : 0,
        #             'current' : plavue,
        #             'remaining' : cvalue,
        #             'current_date' : False,
        #             'next_date' : False,
        #             'current_text' : plavue,
        #             'next_text' : cvalue,
        #         })
        #     else:
        #         if slive.unit == 'year':
        #             dateDue = datetime.strptime(self.date_installed, '%Y-%m-%d') + relativedelta(years=int(math.floor(cvalue)))
        #         if slive.unit == 'month':
        #             dateDue = datetime.strptime(self.date_installed, '%Y-%m-%d') + relativedelta(months=int(math.floor(cvalue)))
        #         if slive.unit == 'days':
        #             dateDue = datetime.strptime(self.date_installed, '%Y-%m-%d') + relativedelta(days=int(math.floor(cvalue)))
        #         dateDue = dateDue.strftime("%Y-%m-%d")

        #         slive.write({
        #             'extension' : 0,
        #             'current' : plavue,
        #             'remaining' : cvalue,
        #             'current_date' : self.date_installed,
        #             'next_date' : dateDue,
        #             'current_text' : self.date_installed,
        #             'next_text' : dateDue,
        #         })

        # change A/C status
        if engine.id != False:
            engine.check_serviceable()
            acraft = self.env['aircraft.acquisition'].search(['|','|','|',('engine_type_id.id','=',engine.id),('engine2_type_id.id','=',engine.id),('engine3_type_id.id','=',engine.id),('engine4_type_id.id','=',engine.id)])
            for g in acraft:
                g.check_serviceable()
        if propeller.id != False:
            propeller.check_serviceable()
            
        if auxiliary.id != False:
            auxiliary.check_serviceable()
            
        fleet.check_serviceable()
        # check apakah ada sub-component yang harus direplace
        if(self.component.is_subcomp == False and len(self.component.sub_part_ids) != 0):
            ro = self.component.sub_part_ids
            for g in ro:
                g.no_component = True
            id_sub = self.env['ams.component.part'].search(['&',('part_id','=',self.component.id),('no_component','=',True)],limit=1)
            return {
                'name': 'Replace Sub-Component',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'ams.component.replace',
                'view_id': False,
                'target': 'new',
                'type': 'ir.actions.act_window',
                'context':"{'search_default_config_id': ["+str(id_sub.id)+"],'default_config_id': "+str(id_sub.id)+"}",
            }
        elif(self.component.is_subcomp == True):
            id_sub = self.env['ams.component.part'].search(['&',('part_id','=',self.component.part_id.id),('no_component','=',True)],limit=1)
            if(id_sub.id != False):
                return {
                    'name': 'Replace Sub-Component',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'ams.component.replace',
                    'view_id': False,
                    'target': 'new',
                    'type': 'ir.actions.act_window',
                    'context':"{'search_default_config_id': ["+str(id_sub.id)+"],'default_config_id': "+str(id_sub.id)+"}",
                }
            else:
                return True

        return True