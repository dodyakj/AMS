
from odoo import models, fields, api

class AircraftBulletinAddition(models.Model):
    _name = 'bulletin.addition'
    _description = 'Add Bulletin'

    fleet_id = fields.Many2one('aircraft.acquisition', string='Aircraft Registration', default=lambda self:self.env.context.get('fleet_id',False), readonly=True)
    engine_id = fields.Many2one('engine.type', string='Engine', default=lambda self:self.env.context.get('engine_id',False), readonly=True)
    propeller_id = fields.Many2one('propeller.type', string='Propeller', default=lambda self:self.env.context.get('propeller_id',False), readonly=True)
    auxiliary_id = fields.Many2one('auxiliary.type', string='Auxiliary', default=lambda self:self.env.context.get('auxiliary_id',False), readonly=True)
    bulletin_id = fields.Many2one('ams.bulletin', string='Bulletin', required=True)
    bulletin_check_text = fields.Char(string=' ',readonly=True)

    comply_status = fields.Selection([('ncw','Not Comply'),('cw','Comply With'),('pcw','Previously Comply With'),('na','N/A')], string='Comply', required=True)
    comply_with = fields.Selection([('ti','TI - Technical Information'),('mi','MI - Maintenance Instruction'),('oti','OTI - One Time Inspection'),('eo','EO - Enginering Order')], string='Comply With')
    not_comply_reason = fields.Text('Not Comply Reason')
    ti_id = fields.Many2one('document.ti', string='Technical Information')
    oti_id = fields.Many2one('document.oti', string='One Time Inspection')
    mi_id = fields.Many2one('document.mi', string='Maintenance Instruction')
    eo_id = fields.Many2one('document.eo', string='Enginering Order')

    last_comply = fields.Date(string='Last Comply Date')
    last_comply_hours = fields.Float(string='Last Comply at')
    last_comply_cycles = fields.Float(string='Last Comply at')
    last_comply_unit = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Last Comply Unit', default="hours")

    repetitive = fields.Boolean(string='Repetitive')
    value = fields.Float(string='Repetitive at')
    unit = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Repetitive Unit', default="hours")

    secondary = fields.Selection([('-',''),('and','AND'),('or','OR')], string='Other', default="-")
    secondary_value = fields.Float(string='Repetitive at')
    secondary_unit = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Repetitive Unit', default="hours")
    remark = fields.Text(string='Remark')

    last_comply_hours_label = fields.Char(string='A/C Hours', readonly=True)
    last_comply_cycles_label = fields.Char(string='A/C Cycles', readonly=True)

    @api.onchange('fleet_id','engine_id','propeller_id','auxiliary_id')
    def _onchange_key_name(self):
        if(self.fleet_id.id != False):
            self.last_comply_hours_label = 'A/C Hours'
            self.last_comply_cycles_label = 'A/C Cycles'
        elif(self.engine_id.id != False):
            self.last_comply_hours_label = 'Engine Hours'
            self.last_comply_cycles_label = 'Engine Cycles'
        elif(self.propeller_id.id != False):
            self.last_comply_hours_label = 'Propeller Hours'
            self.last_comply_cycles_label = 'Propeller Cycles'
        elif(self.auxiliary_id.id != False):
            self.last_comply_hours_label = 'Auxiliary Hours'
            self.last_comply_cycles_label = 'Auxiliary Cycles'
    
    @api.onchange('bulletin_id')
    def _onchange_bulletin_id(self):
        bulletin_ids = self.env['bulletin.aircraft.affected'].search([('fleet_id','=',self.fleet_id.id)]).mapped('bulletin_id').mapped('id')
        if(self.bulletin_id.id in bulletin_ids):
            self.bulletin_check_text = 'Bulletin has been entered'
        else:
            self.bulletin_check_text = ''

    @api.multi
    def action_add(self):
        return {
            "type": "ir.actions.do_nothing",
        }

    
    @api.onchange('fleet_id')
    def _aircraft_bulletin_filter(self):
        if self.fleet_id.id:
            return{
                'domain':{
                    'bulletin_id': [('fleet_id','in', [self.fleet_id.aircraft_name.id])],
                }
            }

    @api.onchange('engine_id')
    def _engine_bulletin_filter(self):
        if self.engine_id.id:
            return{
                'domain':{
                    'bulletin_id':[('engine_id','in',[self.engine_id.engine_model.id])],
                }
            }

    @api.onchange('propeller_id')
    def _propeller_bulletin_filter(self):
        if self.propeller_id.id:
            return{
                'domain':{
                    'bulletin_id':[('propeller_id','in',[self.propeller_id.propeller_model.id])],
                }
            }

    @api.onchange('auxiliary_id')
    def _auxiliary_bulletin_filter(self):
        if self.auxiliary_id.id:
            return{
                'domain':{
                    'bulletin_id':[('auxiliary_id','in',[self.auxiliary_id.auxiliary_model.id])],
                }
            }

class AircraftDocumentCheck(models.Model):
    _name = 'aircraft.document'
    _description = 'Aircraft Document'

    fleet_id = fields.Many2one('aircraft.acquisition', string='Aircraft Registration', default=lambda self:self.env.context.get('fleet_id',False), readonly=True)
    engine_id = fields.Many2one('engine.type', string='Engine', default=lambda self:self.env.context.get('engine_id',False), readonly=True)
    propeller_id = fields.Many2one('propeller.type', string='Propeller', default=lambda self:self.env.context.get('propeller_id',False), readonly=True)
    auxiliary_id = fields.Many2one('auxiliary.type', string='Auxiliary', default=lambda self:self.env.context.get('auxiliary_id',False), readonly=True)
    document_line = fields.One2many('aircraft.document_list','aircraft_document_id',string='Document')
    document_ids = fields.One2many('document.certificate','acquisition_id', 'Document Certificates', readonly=True, related='fleet_id.document_ids')
    document_aux_ids = fields.One2many('document.certificate','auxiliary_id', 'Document Certificates', readonly=True, related='auxiliary_id.document_ids')
    document_engine_ids = fields.One2many('document.certificate','engine_id', 'Document Certificates', readonly=True, related='engine_id.document_ids')
    document_propeller_ids = fields.One2many('document.certificate','propeller_id', 'Document Certificates', readonly=True, related='propeller_id.document_ids')

    @api.onchange('fleet_id')
    def _onchange_fleet_id(self):
        affected = []
        doc_aff = self.env['bulletin.aircraft.affected'].search([('fleet_id','=',self.fleet_id.id)])

        for g in doc_aff:
            if g.bulletin_id.id != False:
                affected.append((0, 0,{
                    'bulletin_id' : g.bulletin_id.id,
                    'bulletin_compliance_id' : g.bulletin_compliance_id.id,
                    }))

        self.document_line = affected

    @api.onchange('engine_id')
    def _onchange_engine_id(self):
        affected = []
        doc_aff = self.env['bulletin.aircraft.affected'].search([('engine_id','=',self.engine_id.id)])

        for g in doc_aff:
            if g.bulletin_id.id != False:
                affected.append((0, 0,{
                    'bulletin_id' : g.bulletin_id.id,
                    'bulletin_compliance_id' : g.bulletin_compliance_id.id,
                    }))

        self.document_line = affected            

    @api.onchange('propeller_id')
    def _onchange_propeller_id(self):
        affected = []
        doc_aff = self.env['bulletin.aircraft.affected'].search([('propeller_id','=',self.propeller_id.id)])

        for g in doc_aff:
            if g.bulletin_id.id != False:
                affected.append((0, 0,{
                    'bulletin_id' : g.bulletin_id.id,
                    'bulletin_compliance_id' : g.bulletin_compliance_id.id,
                    }))

        self.document_line = affected 

    @api.multi
    def add_bulletin(self):
        return {
            'name': 'Add Bulletin',
            'type': 'ir.actions.act_window',
            'res_model': 'bulletin.addition',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': False,
            'views': [(False, 'form')],
            'target': 'new',
            'context': "{'fleet_id':" + str(self.fleet_id.id) + ",'engine_id':" + str(self.engine_id.id) + ",'propeller_id':" + str(self.propeller_id.id) + ",'auxiliary_id':" + str(self.auxiliary_id.id) + "}",
        }

class AircraftDocumentList(models.Model):
    _name = 'aircraft.document_list'
    _description = 'Affected AD/SB/STC'

    aircraft_document_id = fields.Many2one('aircraft.document', string='Aircraft')
    
    bulletin_id = fields.Many2one('ams.bulletin', string='Bulletin', readonly=True)
    bulletin_compliance_id = fields.Many2one('bulletin.comply', string='Compliance',readonly=True)
    
    comply_status = fields.Selection([('ncw','Not Comply'),('cw','Comply With'),('pcw','Previously Comply With'),('na','N/A')], string='Comply',readonly=True, related="bulletin_compliance_id.comply_status")
    comply_with = fields.Selection([('ti','TI - Technical Information'),('mi','MI - Maintenance Instruction'),('oti','OTI - One Time Inspection'),('eo','EO - Enginering Order')], string='Comply With',readonly=True, related="bulletin_compliance_id.comply_with")
    not_comply_reason = fields.Text('Not Comply Reason',readonly=True, related="bulletin_compliance_id.not_comply_reason")
    ti_id = fields.Many2one('document.ti', string='Technical Information',readonly=True, related="bulletin_compliance_id.ti_id")
    oti_id = fields.Many2one('document.oti', string='One Time Inspection',readonly=True, related="bulletin_compliance_id.oti_id")
    mi_id = fields.Many2one('document.mi', string='Maintenance Instruction',readonly=True, related="bulletin_compliance_id.mi_id")
    eo_id = fields.Many2one('document.eo', string='Enginering Order',readonly=True, related="bulletin_compliance_id.eo_id")

    compliance_text = fields.Char(string='Compliance',compute='get_text')

    @api.one
    @api.model
    def get_text(self):
        compliance_text = ''
        if(self.comply_status == 'pcw'):
            compliance_text = 'Previously Complied'
        elif(self.comply_status == 'ncw'):
            compliance_text = 'Not Complied ' + str(self.not_comply_reason)
        elif(self.comply_status == 'na'):
            compliance_text = 'N/A ' + str(self.not_comply_reason)
        elif(self.comply_status == 'cw'):
            if(self.bulletin_compliance_id == False):
                compliance_text = 'Waiting For Compliance'
            elif(self.comply_with == 'ti'):
                compliance_text = 'Complied With ' + (str(self.ti_id.no) if self.ti_id.no != False else 'TI')
            elif(self.comply_with == 'oti'):
                compliance_text = 'Complied With ' + (str(self.oti_id.no) if self.oti_id.no != False else 'OTI')
            elif(self.comply_with == 'mi'):
                compliance_text = 'Complied With ' + (str(self.mi_id.no) if self.mi_id.no != False else 'MI')
            elif(self.comply_with == 'eo'):
                compliance_text = 'Complied With ' + (str(self.eo_id.eo_number) if self.eo_id.eo_number != False else 'EO')

        self.compliance_text = compliance_text