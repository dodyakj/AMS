# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import datetime, timedelta
from odoo import fields, models, api

class Inventory(models.Model):
    _inherit = ["product.product"]
    _name = 'ams.inventory'
    _description = 'Inventory'

class InventoryRequestPart(models.Model):
    _name = 'request.inventory.part'
    _description = 'Inventory Request Part'
    
    request_id  = fields.Many2one('request.inventory', string='Request Number')
    part_name   = fields.Many2one('product.product', string='Part Name', required=True)
    quantity    = fields.Integer(string='Quantity',default=1)

class InventoryRequest(models.Model):
    _name = 'request.inventory'
    _description = 'Inventory Request'

    name                    = fields.Char(string='Request Number')
    ref_type                = fields.Selection([('none','-None-'), ('wo','Work Order'), ('inspection','Inspection Completion'), ('sb','SB Completion'), ('ad','AD Completion'), ('stc','STC Completion'), ('other','Other...')], default='none', string='Reference Type')
    base_id                 = fields.Many2one('base.operation', string='Location')
    request_employee_id     = fields.Many2one('res.partner', string="Requested By", default=False, readonly=True)
    checked_employee_id     = fields.Many2one('res.partner', string="Checked By", default=False, readonly=True)
    approved_employee_id    = fields.Many2one('res.partner', string="Approved By", default=False, readonly=True)
    compliance_employee_id  = fields.Many2one('res.partner', string="Rejected By", default=False, readonly=True)
    part_line               = fields.One2many('request.inventory.part','request_id',string='Part Request')

    states = fields.Selection([('create','Created'), ('check','Checked'), ('validate','Validate'), ('inprogress','In Progress'), ('done','Complete'), ('rejected','Rejected')], default='create', readonly=True)

    @api.model
    def create(self, value):
        value['states'] = 'check'
        rec = super(InventoryRequest, self).create(value)
        return rec

    @api.multi
    def button_req(self):
        partner = self.env.user.partner_id.id
        self.request_employee_id = partner
        self.states = 'validate'

    @api.multi
    def button_check(self):
        partner = self.env.user.partner_id.id
        self.checked_employee_id = partner
        self.states = 'inprogress'

    @api.multi
    def button_appr(self):
        partner = self.env.user.partner_id.id
        self.approved_employee_id = partner
        self.states = 'done'

    @api.multi
    def button_comp(self):
        partner = self.env.user.partner_id.id
        self.compliance_employee_id = partner
        self.states = 'rejected'



class InventoryReceiveTemplate(models.Model):
    _name = 'receiving.template'
    _description = 'Inventory Receive Template'

    name = fields.Text(string='Description',required=True)

class ReceivingInventory(models.Model):
    _name = 'receiving.inventory'
    _description = 'Receiving Inventory'

    name        = fields.Char(readonly=True)
    tipe        = fields.Selection([('fw','Fixed Wing'),('rw','Rotary')],'Type',default='rw')
    part_name   = fields.Many2one('product.product', string='Part Name', required=True)
    part_no     = fields.Char(string='Part No.', related='part_name.default_code')
    serial_no   = fields.Char(string='Serial No.')
    quantity    = fields.Integer(string='Quantity')
    vendor      = fields.Many2one('res.partner', string='Supplier/Vendor', domain=[('is_company','=',True)])
    rcv_date    = fields.Date(string='Received Date',default=fields.Date.today())
    ins_date    = fields.Date(string='Inspection Date',default=fields.Date.today())
    ins_by      = fields.Many2one('hr.employee', string='Receiving By')

    description = fields.One2many('receiving.inventory.description', 'di_id')

    note = fields.Text()
    result = fields.Text()
            

    @api.multi
    def print_ri_pdf(self):
        return self.env['report'].get_action(self, 'ams_inventory.report_ri')

    @api.model
    def create(self, values):
        now = datetime.now()
        mon = now.strftime('%m')
        if int(mon) == 1:
            bulan = 'I'
        elif int(mon) == 2:
            bulan = 'II'
        elif int(mon) == 3:
            bulan = 'III'
        elif int(mon) == 4:
            bulan = 'IV'
        elif int(mon) == 5:
            bulan = 'V'
        elif int(mon) == 6:
            bulan = 'VI'
        elif int(mon) == 7:
            bulan = 'VII'
        elif int(mon) == 8:
            bulan = 'VIII'
        elif int(mon) == 9:
            bulan = 'IX'
        elif int(mon) == 10:
            bulan = 'X'
        elif int(mon) == 11:
            bulan = 'XI'
        else:
            bulan = 'XII'
        if(self.env['ir.sequence'].search([('code','=','ams_inventory.receive' + str(now.year))]).name == False):
            self.env['ir.sequence'].create({
                    'name' : 'Receive Inventory ' + str(now.year),
                    'code' : 'ams_inventory.receive' + str(now.year),
                    'padding' : '3',
                    'prefix' : '',
                    'suffix' : '/GRN/',
                })
        seq = self.env['ir.sequence'].next_by_code('ams_inventory.receive' + str(now.year))
        values['name'] = seq + values['tipe'].upper() + '/' + bulan + '/' + str(now.year)
    
        return super(ReceivingInventory, self).create(values)

    @api.onchange('part_name')
    def _onchange_part_name(self):
        checklist = []
        ro = self.env['receiving.template'].search([])
        for g in ro:
            checklist.append((0,0,{
                'name' : g.name,
                'acceptance' : True,
                }))
        self.description = checklist

class DescriptionInventory(models.Model):
    _name = 'receiving.inventory.description'
    _description = 'Description'

    name = fields.Text('Description')
    acceptance = fields.Boolean(string='Acceptance')
    yes_no = fields.Selection([('yes','Yes'),('no','No')],readonly=True)

    di_id = fields.Many2one('receiving.inventory')

    @api.model
    def create(self, values):
        if(values['acceptance'] == True):
            values['yes_no'] = 'yes'
        else:
            values['yes_no'] = 'no'
        
        return super(DescriptionInventory, self).create(values)