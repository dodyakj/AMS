# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api

class EmsBulletinVendor(models.Model):
    _name = 'bulletin.regulator'
    _description = 'Regulator'

    name = fields.Char(string='Regulator', required=True)
    inter = fields.Boolean(string="International")

class EmsBulletinCompliance(models.Model):
    _name = 'bulletin.comply'
    _description = 'Comply Bulletin'
    _rec_name = 'bulletin_id'

    unserviceable = fields.Boolean(string='Aircraft is unserviceable during this compliance', default=True)
    service_life_id = fields.Many2one('ams.component.servicelife', string='Service Life', default=lambda self:self.env.context.get('service_life_id',False))
    compliance_id = fields.Many2one('bulletin.aircraft.affected', string='Compliance', related='service_life_id.bulletin_affected_id')
    bulletin_id = fields.Many2one('ams.bulletin', string='Bulletin', related='compliance_id.bulletin_id')
    date = fields.Date(string='Compliance Start Date',required=True,default=fields.Date.today())
    date_finish = fields.Date(string='Compliance Finish Date',required=True,default=fields.Date.today())

    Compliance_cycle = fields.Float(string='Compliance Cycle')
    Compliance_hour = fields.Float(string='Compliance Hour')

    comply_status = fields.Selection([('ncw','Not Comply'),('cw','Comply With'),('pcw','Previously Comply With'),('na','N/A')], string='Comply', default='ncw',required=True)
    comply_with = fields.Selection([('ti','TI - Technical Information'),('mi','MI - Maintenance Instruction'),('oti','OTI - One Time Inspection'),('eo','EO - Enginering Order')], string='Comply With')
    not_comply_reason = fields.Text('Not Comply Reason')
    
    ti_id = fields.Many2one('document.ti', string='Technical Information')
    oti_id = fields.Many2one('document.oti', string='One Time Inspection')
    mi_id = fields.Many2one('document.mi', string='Maintenance Instruction')
    eo_id = fields.Many2one('document.eo', string='Enginering Order')

    type = fields.Selection([('AD','AD - Airwothiness Directive'),('SB','SB / ASB - Service Bulletin / Alert Service Bulletin'),('STC','STC - Supplemental Type Certificate'),('SERVICE','Service')], string='Type', related="bulletin_id.type")
    affected = fields.Selection([('fleet','Aircraft'),('engine','Engine'),('auxiliary','Auxiliary'),('propeller','Propeller'),('component','Component')], string='Affected', related="bulletin_id.bulletin_of")
    fleet = fields.Many2one('aircraft.acquisition', 'Aircraft',related="compliance_id.fleet_id")
    engine = fields.Many2one('engine.type', 'Engine')
    auxiliary = fields.Many2one('auxiliary.type', 'Auxiliary')
    propeller = fields.Many2one('propeller.type', 'Propeller')
    # number = fields.Many2one('ams.bulletin', ' Numbers')

    @api.model
    def create(self, vals):
        vals['service_life_id'] = self.env.context.get('service_life_id',False)
        # vals['compliance_id'] = self.env.context.get('compliance_id',False)

        slive = self.env['ams.component.servicelife'].search([('id','=',vals['service_life_id'])])
        compliance = slive.bulletin_affected_id
        fleet = compliance.fleet_id
        bulletin = compliance.bulletin_id
        
        create = super(EmsBulletinCompliance, self).create(vals)
        compliance.write({
            'bulletin_compliance_id' : create.id
            })

        date_format = "%Y-%m-%d"
        a = datetime.strptime(vals['date'], date_format)
        b = datetime.strptime(vals['date_finish'], date_format)
        delta = b - a

        self.env['maintenance.request'].create({
            'name' : str(fleet.name) + ' ' + str(bulletin.name) + ' Compliance',
            'bulletin_comply_id' : create.id,
            'fl_acquisition_id' : fleet.id,
            'maintenance_team_id' : self.env['maintenance.team'].search([], limit=1).id,
            'reason_maintenance' : str(bulletin.name),
            'schedule_date' : vals['date'],
            'duration' : (24 * delta.days) - 1,
            'aircraft_state' : 'unserviceable' if vals['unserviceable'] == True else 'serviceable',
            })
        # RESET
        if slive.unit == 'year':
            dateDue = datetime.strptime(vals['date'], '%Y-%m-%d') + relativedelta(years=int(math.floor(slive.value)))
        if slive.unit == 'month':
            dateDue = datetime.strptime(vals['date'], '%Y-%m-%d') + relativedelta(months=int(math.floor(slive.value)))
        if slive.unit == 'days':
            dateDue = datetime.strptime(vals['date'], '%Y-%m-%d') + relativedelta(days=int(math.floor(slive.value)))
        slive.update({
                'unit' : slive.unit,
                'value' : slive.value,
                'current' : 0,
                'remaining' : slive.value,
                'current_date' : slive.current_date,
                'next_date' : slive.next_date,
                'current_text' : vals['date'] if slive.unit in ['year','month','days'] else str(0) + " " + slive.unit,
                'next_text' : dateDue.strftime("%Y-%m-%d") if slive.unit in ['year','month','days'] else str(slive.value) + " " + slive.unit,
                })
        return create

class MaintenanceCalendarCorrectiveBulletinCompliance(models.Model):
    _inherit = 'maintenance.request'
    
    bulletin_comply_id = fields.Many2one('bulletin.comply',string='Bulletin Compliance')

class AMSBulletinType(models.Model):
    _name = 'ams.bulletin.type'
    _description = 'Bulletin Document Type'

    name = fields.Char(string='Document Type')
    


class EMSBulletin(models.Model):
    _name = 'ams.bulletin'
    _description = 'Bulletin'

    file = fields.Binary(string='File Scan')
    file_name = fields.Char('File Name')

    repetitive = fields.Boolean(string='Repetitive Bulletin', default=False)
    repetitive_value = fields.Integer(string='Repetitive Every')
    repetitive_every = fields.Selection([('hours','Hours'),('cycles','Cycles'),('days','Days'),('months','Months'),('years','Years')], string=' ')

    is_supersedes = fields.Boolean(string="Supersedes", default=False)
    supersedes_id = fields.Many2one('ams.bulletin', string="Supersedes")
    superseded_id = fields.Many2one('ams.bulletin', string="Superseded")

    type = fields.Selection([('AD','AD - Airwothiness Directive'),('SB','SB / ASB - Service Bulletin / Alert Service Bulletin'),('STC','STC - Supplemental Type Certificate'),('SERVICE','Service')], string='Type', required=True, default=lambda self:self.env.context.get('bulletin_type','SB'))
    status = fields.Selection([('mandatory','Mandatory'),('recommended','Recommended'),('optional','Optional')], string='Compliance Type', required=True, default='mandatory')
    document_type_id = fields.Many2one('ams.bulletin.type',string='Document Type')
    name = fields.Char('Bulletin Number',required=True)
    date = fields.Date(string='Date Issued',required=True)
    comply_before = fields.Date(string='Effective Date')
    
    
    bulletin_of = fields.Selection([('fleet','Aircraft'),('engine','Engine'),('auxiliary','Auxiliary'),('propeller','Propeller'),('component','Component')], string='Bulletin For')

    fleet_id = fields.Many2many('aircraft.aircraft', string='Aircraft')
    engine_id = fields.Many2many('engine.engine', string='Engine')
    auxiliary_id = fields.Many2many('auxiliary.auxiliary', string='Auxiliary')
    propeller_id = fields.Many2one('propeller.propeller', string='Propeller')
    product_id = fields.Many2one('product.product', string='Component')
    
    aff_msn = fields.Char(string='Affected Msn')
    aff_sn = fields.Char(string='Affected SN')

    aff_pn = fields.Char(string='Affected Part Number')
    aff_sn = fields.Char(string='Affected Serial Number')
    remarks = fields.Text(string='Remarks')

    fleet_ids = fields.One2many('bulletin.aircraft.affected','bulletin_id',string='Affected Aircraft')
    engine_ids = fields.One2many('bulletin.engine.affected','bulletin_id',string='Affected Engine')
    auxiliary_ids = fields.One2many('bulletin.auxiliary.affected','bulletin_id',string='Affected Auxiliary')
    propeller_ids = fields.One2many('bulletin.propeller.affected','bulletin_id',string='Affected Propeller')
    component_ids = fields.One2many('bulletin.component.affected','bulletin_id',string='Affected Component')
    
    component_ids = fields.One2many('bulletin.component.affected','bulletin_id',string='Affected Component')
    needed_component_ids = fields.One2many('bulletin.component.needed','bulletin_id',string='Needed Component')
    bulletin_id = fields.Many2one('ams.bulletin',string="Reference Bulletin")
    bulletin_line = fields.One2many('ams.bulletin','bulletin_id',string="Sub Bulletin")
    regulator_id = fields.Many2one('bulletin.regulator',string='Regulator')
    vendor_id = fields.Many2one('res.partner',string='Vendor')
    manufacturer_id = fields.Many2one('res.partner',string='Manufacturer')
    subject = fields.Text('Subject')
    attachment_ids = fields.Many2many('ir.attachment', 'class_ir_attachments_rel', 'class_id', 'attachment_id', 'Attachments')

    limit_ = fields.Selection([(False,'-None-'),(1,'Date'),(2,'Hours'),(3,'Cycles')], string='Compliance Due')
    comply_date = fields.Date(string='Compliance Date')
    Compliance_cycle = fields.Float(string='Compliance Cycle')
    Compliance_hour = fields.Float(string='Compliance Hour')
  

    state = fields.Selection([('create','Created'), ('check','Checked'), ('validate','Validate')], default='create')
    create_by = fields.Many2one('res.partner', readonly=True, compute='_create_by')
    checked_by = fields.Many2one('res.partner', readonly=True)
    validate_by = fields.Many2one('res.partner', readonly=True)

    service_life_id = fields.One2many('ams.component.servicelife' , 'bulletin_inspection_id', string='Service Life')
    merge_mp = fields.Boolean('Major (Show MP)')    

    @api.model
    def create(self, vals):
        create = super(EMSBulletin, self).create(vals)
        # if(vals['repetitive'] == True):
        #     self.env['bulletin.aircraft.affected'].search([('bulletin_id','=',create.id)]).update({
        #         'unit' : vals['repetitive_every'],
        #         'value' : vals['repetitive_value'],
        #         'current' : vals['repetitive_value'],
        #         'remaining' : 0,
        #         'current_date' : vals['date'] if(vals['repetitive_every'] in ["year","month","days"]) else False,
        #         'next_date' : vals['date'] if(vals['repetitive_every'] in ["year","month","days"]) else False,
        #         'current_text' : vals['date'] if(vals['repetitive_every'] in ["year","month","days"]) else str(vals['repetitive_value']) + ' ' + vals['repetitive_every'],
        #         'next_text' : vals['date'] if(vals['repetitive_every'] in ["year","month","days"]) else '0 ' + vals['repetitive_every'],
        #         })
        if(vals['is_supersedes'] == True):
            self.env['ams.bulletin'].search([('id','=', vals['supersedes_id'])]).update({
                'superseded_id' : create.id
            })

        return create

    @api.multi
    def write(self, vals):
        last_val = self.env['ams.bulletin'].search([('id','=',self.id)])
        last_slive = last_val.service_life_id.ids
        iwrite = super(EMSBulletin, self).write(vals)
        saved = self.env['ams.bulletin'].search([('id','=',self.id)])
        for slive in saved.service_life_id:
            if (slive.id not in last_slive):
                for fleet in saved.fleet_ids:
                    self.env['ams.component.servicelife'].create({
                        'ref_id' : slive.id,
                        'bulletin_affected_id' : fleet.id,
                        'action_type' : 'inspection',
                        'current' : 0,
                        'value' : slive.value,
                        'unit' : slive.unit,
                        'comments' : slive.comments,
                    })
        return iwrite

    @api.model
    @api.one
    def _create_by(self):
        partner = self.env.user.partner_id.id
        self.create_by = partner
        self.state = 'check'

    @api.multi
    def get_validate(self):
        partner = self.env.user.partner_id.id
        self.validate_by = partner
        self.state = 'validate'

    @api.multi
    def get_check(self):
        partner = self.env.user.partner_id.id
        self.checked_by = partner
        self.state = 'check'

    @api.onchange('name')
    def _onchange_name(self):
        atc = self.env['ir.attachment'].search([('res_model','=','ams.bulletin'),('res_id','=',self.id)])
        self.attachment_ids = atc

    @api.onchange('type')
    def _onchange_type(self):
        if(self.type == 'AD'):
            self.status = 'mandatory'

    # @api.one
    # def _upload_name(self):
    #     if self.file and self.name:
    #         self.file_name = str(self.name+".pdf")
            

class BulletinComponentPartAffected(models.Model):
    _name = 'bulletin.component.affected'
    _description = 'Affected Component'


    bulletin_id = fields.Many2one('ams.bulletin', string='Bulletin')
    product_id = fields.Many2one('product.product', string='Component Name', required=True)
    part_number = fields.Char(related='product_id.default_code',string="Part Number",readonly=True)
    
    serial_number = fields.Many2one('stock.production.lot', string='Serial Number')

class BulletinAircraftAffected(models.Model):
    _name = 'bulletin.aircraft.affected'
    _description = 'Affected Aircraft'


    bulletin_id = fields.Many2one('ams.bulletin', string='Bulletin')
    fleet_id = fields.Many2one('aircraft.acquisition', string='Aircraft')
    engine_id = fields.Many2one('engine.type', string='Engine')
    auxiliary_id = fields.Many2one('auxiliary.type', string='Auxiliary')
    propeller_id = fields.Many2one('propeller.type', string='Propeller')
    component_id = fields.Many2one('product.product', string='Component')

    bulletin_of = fields.Selection([('fleet','Aircraft'),('engine','Engine'),('auxiliary','Auxiliary'),('propeller','Propeller'),('component','Component')], string='Bulletin For')

    bulletin_compliance_id = fields.Many2one('bulletin.comply', string='Compliance')
    
    comply_status = fields.Selection([('ncw','Not Comply'),('cw','Comply With'),('pcw','Previously Comply With'),('na','N/A')], string='Comply',readonly=True, related="bulletin_compliance_id.comply_status")
    comply_with = fields.Selection([('ti','TI - Technical Information'),('mi','MI - Maintenance Instruction'),('oti','OTI - One Time Inspection'),('eo','EO - Enginering Order')], string='Comply With',readonly=True, related="bulletin_compliance_id.comply_with")
    not_comply_reason = fields.Text('Not Comply Reason',readonly=True, related="bulletin_compliance_id.not_comply_reason")
    ti_id = fields.Many2one('document.ti', string='Technical Information',readonly=True, related="bulletin_compliance_id.ti_id")
    oti_id = fields.Many2one('document.oti', string='One Time Inspection',readonly=True, related="bulletin_compliance_id.oti_id")
    mi_id = fields.Many2one('document.mi', string='Maintenance Instruction',readonly=True, related="bulletin_compliance_id.mi_id")
    eo_id = fields.Many2one('document.eo', string='Enginering Order',readonly=True, related="bulletin_compliance_id.eo_id")

    

    last_comply = fields.Date(string='Last Comply at')

    service_life_id = fields.One2many('ams.component.servicelife' , 'bulletin_affected_id', string='Service Life')

    value = fields.Float(string='Value')
    current = fields.Float(string='Current')
    remaining = fields.Float(string='Next Due')
    current_date = fields.Date(string='Installed At', default=fields.Date.today)
    next_date = fields.Date(string='Date Due')
    unit = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Unit', default="hours",required=True)
    current_text = fields.Char(string='Current')
    next_text = fields.Char(string='Next Due')
    remark = fields.Text(string="Remark")
    last_comply_hour = fields.Float(string="Last Comply Hours")
    last_comply_cycle = fields.Float(string="Last Comply Cycles")
    last_comply_date = fields.Date(string="Last Comply Date")

    # ONCREATE COCOKIN DENGAN SERVICE LIVE BULLETIN
    @api.onchange('bulletin_id')
    def _onchange_bulletin_id(self):
        ro = self.bulletin_id.service_life_id
        app = []
        for g in ro:
            app.append((0, 0,{
                    'ref_id' : g.id,
                    'action_type' : 'inspection',
                    'current' : 0,
                    'value' : g.value,
                    'unit' : g.unit,
                    'comments' : g.comments,
                    }))
        self.service_life_id = app

    @api.multi
    def comply(self):
        return {
            'name': 'Comply',
            'type': 'ir.actions.act_window',
            'res_model': 'bulletin.comply',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': False,
            'views': [(False, 'form')],
            'target': 'new',
            'context': "{'compliance_id':" + str(self.id) + "}",
        }
    

class BulletinEngineAffected(models.Model):
    _inherit = 'bulletin.aircraft.affected'
    _name = 'bulletin.engine.affected'
    _description = 'Affected Engine'

class BulletinAuxiliaryAffected(models.Model):
    _inherit = 'bulletin.aircraft.affected'
    _name = 'bulletin.auxiliary.affected'
    _description = 'Affected Auxiliary'


class BulletinPropellerAffected(models.Model):
    _inherit = 'bulletin.aircraft.affected'
    _name = 'bulletin.propeller.affected'
    _description = 'Affected Auxiliary'


class BulletinAComponentAffected(models.Model):
    _inherit = 'bulletin.aircraft.affected'
    _name = 'bulletin.component.affected'
    _description = 'Affected Auxiliary'




class BulletinComponentPartNeeded(models.Model):
    _name = 'bulletin.component.needed'
    _description = 'Affected Needed'


    bulletin_id = fields.Many2one('ams.bulletin', string='Bulletin')
    product_id = fields.Many2one('product.product', string='Component Name', required=True)
    part_number = fields.Char(related='product_id.default_code',string="Part Number",readonly=True)
    amount = fields.Integer(string='Amount')
    in_inventory = fields.Integer(string='In Inventory',default='3',readonly=True)

class AmsAlterationCompReplace(models.Model):
    _name = 'alteration.replace'
    _description = 'Replace Component'


    alteration_id = fields.Many2one('bulletin.alteration', string='Alteration')
    product_id = fields.Many2one('product.product', string='Component Name', required=True)
    part_number = fields.Char(related='product_id.default_code',string="Part Number",readonly=True)

class AmsAlterationCompInstall(models.Model):
    _name = 'alteration.install'
    _description = 'Install Component'


    alteration_id = fields.Many2one('bulletin.alteration', string='Alteration')
    product_id = fields.Many2one('product.product', string='Component Name', required=True)
    part_number = fields.Char(related='product_id.default_code',string="Part Number",readonly=True)

class AmsAlteration(models.Model):
    _name = 'bulletin.alteration'
    _description = 'Aircraft Alteration'

    name = fields.Char('Alteration Number', required=True)
    fleet_id = fields.Many2one('aircraft.acquisition', string='Aircraft', required=True)
    file = fields.Binary(string='File Scan')
    file_name = fields.Char('File Name')
    date = fields.Date(string='Date Issued')

    desc = fields.Text('Description')
    subject = fields.Text('Subject')

    status  = fields.Selection([('open', 'Open'),('close', 'Close')], string="Status")

    replace_component_ids = fields.One2many('alteration.replace','alteration_id',string='Replaced Component')
    installed_component_ids = fields.One2many('alteration.install','alteration_id',string='Installed Component')

    state = fields.Selection([('create','Created'), ('check','Checked'), ('validate','Validate')], default='create')
    create_by = fields.Many2one('res.partner', readonly=True, compute='_create_by')
    checked_by = fields.Many2one('res.partner', readonly=True)
    validate_by = fields.Many2one('res.partner', readonly=True)

    comply_date = fields.Date('Comply Date')
    comply_hour = fields.Float('Comply Hours')
    comply_cyc = fields.Float('Comply Cycles')
    comply_rin = fields.Integer('Comply Rin')

    @api.model
    @api.one
    def _create_by(self):
        partner = self.env.user.partner_id.id
        self.create_by = partner
        self.state = 'check'

    @api.multi
    def get_validate(self):
        partner = self.env.user.partner_id.id
        self.validate_by = partner
        self.state = 'validate'

    @api.multi
    def get_check(self):
        partner = self.env.user.partner_id.id
        self.checked_by = partner
        self.state = 'check'

    # def _upload_name(self):
    #     if self.id:
    #         self.file_name = str(self.name+".pdf")


# class CompliedBulletin(models.Model):
#     _name = 'complied.bulletin'
#     _description = 'Complied Bulletin'

#     type = fields.Selection([('all','All'),('sb','SB - Service Bulletin'),('ad','AD - Airworthiness Directive'),('stc','STC - Supplemental Type Certificate')], string='Type')
#     affected = fields.Selection([('all','All'),('aircraft','Aircraft'),('engine','Engine'),('auxiliary','Auxiliary'),('propeller','Propeller')], string='Affected')
#     number = fields.Many2one('ams.bulletin', ' Numbers')
#     date_start  = fields.Date(' ')
#     date_end    = fields.Date(' ')
#     


class BulletinInheritToolMovement(models.Model):
    _inherit = 'tool.movement'

    refer_ad = fields.Many2one('ams.bulletin', string="Ref. Numbers")
    refer_sb = fields.Many2one('ams.bulletin', string="Ref. Numbers")
    refer_stc = fields.Many2one('ams.bulletin', string="Ref. Numbers")
    refer_ser = fields.Many2one('ams.bulletin', string="Ref. Numbers")