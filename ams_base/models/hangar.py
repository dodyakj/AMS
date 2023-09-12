from odoo import fields, models, api

class HangarType(models.Model):
    _inherit = ['mail.thread']
    _name = 'hangar.type'
    _description = 'Hangar Facility'

    base_id = fields.Many2one('base.operation', string="Location")
    count_calibrate =  fields.Integer(default=1 , readonly=True)

    name = fields.Char( string='Hangar Facility Name', required=True)
    category = fields.Selection([('fixedwing','Fixed Wing'),('rotary','Rotary')],'Category')
    ownership = fields.Selection([('leasing','Leasing'),('owner','Owner')],string='Ownership')
    delivery_date = fields.Date('Delivery date')
    date_manufacture = fields.Date('Date of Manufacture')
    propeller_type_id = fields.Many2one('propeller.type','Propeller Type')
    esn = fields.Char(string='S/N')
    rgb = fields.Char(string='RGB S/N')
    propeller = fields.Char(string='Propeller S/N')
    tsn = fields.Char(string='TSN')
    csn = fields.Char(string='CSN')
    tslsv = fields.Char(string='TSLSV')
    cslsv = fields.Char(string='CSLSV')
    lessor = fields.Char(string='Lessor')
    start_lease = fields.Date('Start Lease')
    normal_termination = fields.Date('Normal Termination')
    hangar_lastcb = fields.Date(string='Last Calibrated')
    hangar_nextdue = fields.Date(string='Next Calibrate Due')
    vendors = fields.Many2one('res.partner', string='Vendor')
    hangar_hsi = fields.Date(string='Hangar Facility#1 HSI')
    hangar_tsn = fields.Float(string='TSN')
    hangar_csn = fields.Float(string='GSE CSN')
    hangar_tslsvcb = fields.Float(string='GSE TSLSV Calibrated')
    hangar_tslsv_hsi = fields.Float(string='GSE TSLSV HSI')
    hangar_cslsv = fields.Float(string='GSE CSLSV Calibrated')
    hangar_cslsv_hsi = fields.Float(string='GSE CSLSV HSI')
    propeller_tsn = fields.Float(string='Propeller TSN')
    propeller_tslsv = fields.Float(string='Propeller TSLSV')
    propeller_lastoh =fields.Date(string='Propeller Last Calibrated')
    aircraft_status = fields.Boolean(string='Engine Status',default=True)
    total_hours = fields.Float(string='Total Hours')
    total_cycles = fields.Float(string='Total Cycles')
    special_ratio_counting = fields.Boolean(string='Special ratio Counting')
    component_ids = fields.One2many('ams.component.part','engine_id',string='Component')
    inspection_ids = fields.One2many('ams.inspection','engine_id',string='Inspection')
    history_line = fields.One2many('ams.component_history','engine_id',string='History')
    some_count = fields.Integer(string='Total',default=3)

    # type = fields.Selection([('onboard','On Board'),('onground','On Ground')], required=True)
    fleet_id = fields.Many2one('aircraft.acquisition', string="Location")
    base_id = fields.Many2one('base.operation', string="Location")
    count_calibrate =  fields.Integer(default=1 , readonly=True)


    @api.onchange('type')
    def _associate_account(self):
        if (self.id):
            data = self.env['hangar.calibrated'].search_count([('hangar_id.id','=',self.id)])
            self.count_calibrate = data

    @api.multi
    def return_action_to_open(self):
        return False

    def true(self):
        return True


class HangarCalibrated(models.Model):
    _name = 'hangar.calibrated'
    _description = 'Calibrated'

    calibrate_last = fields.Date(string='Last Calibrated')
    calibrate_next = fields.Date(string='Next Calibrate Due')
    hangar_id = fields.Many2one('hangar.type', default=lambda self:self.env.context.get('default_config_id',False))

    # def replace(self):
    #     comp = self.env['ams.component.part'].search([('id','=',self.component.id)])
    #     comp.write({
    #         'product_id' : self.product_id.id,
    #         'serial_number' : self.serial_number.id,
    #         'date_installed' : self.date_installed,
    #         'csn' : self.csn,
    #         'cso' : self.comp_timeinstallation,
    #         'tsn' : self.tsn,
    #         'tso' : self.comp_cyclesinstallation,
    #         'ac_timeinstallation' : self.ac_timeinstallation,
    #         'ac_cyclesinstallation' : self.ac_cyclesinstallation,
    #         'comp_timeinstallation' : self.comp_timeinstallation,
    #         'comp_cyclesinstallation' : self.comp_cyclesinstallation,
    #         'is_overhaul' : self.is_overhaul,
    #         'unknown_new' : self.unknown_new,
    #         })
    #     return True