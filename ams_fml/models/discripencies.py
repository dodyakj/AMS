from odoo import models, fields, api

class Discripencies(models.Model):
    _name = 'ams.discripencies'
    _description = 'Discripencies'

    fleet_id = fields.Many2one('aircraft.acquisition', 'A/C Reg', related='fml_id.aircraft_id')
    name = fields.Char('Discrepencies')
    root_cause = fields.Char('Root Cause')
    action_take = fields.Text('Action Taken')
    status = fields.Selection([('waiting','Waiting'),('working','Working on it'),('done','Done')], string='Status', default='waiting')
    component = fields.Many2one('ams.component.part', 'Component Affeted')
    # allowed_component = fields.Many2many('ams.component.part', string='Allowed Component')
    fml_id = fields.Many2one('ams_fml.log', default=lambda self:self.env.context.get('default_config_id',False))

    @api.multi 
    def action_save(self):
        #your code
        self.ensure_one()
        #close popup
        return {'type': 'ir.actions.act_window_close'}

    @api.onchange('fleet_id')
    def _onchange_fleet_id(self):
        allowed_comp = []
        for comp in self.fleet_id.component_ids:
            allowed_comp.append(comp.id)
            for subcomp in comp.sub_part_ids:
                allowed_comp.append(subcomp.id)
        for comp in self.fleet_id.engine_type_id.component_ids:
            allowed_comp.append(comp.id)
            for subcomp in comp.sub_part_ids:
                allowed_comp.append(subcomp.id)
        for comp in self.fleet_id.engine2_type_id.component_ids:
            allowed_comp.append(comp.id)
            for subcomp in comp.sub_part_ids:
                allowed_comp.append(subcomp.id)
        for comp in self.fleet_id.engine3_type_id.component_ids:
            allowed_comp.append(comp.id)
            for subcomp in comp.sub_part_ids:
                allowed_comp.append(subcomp.id)
        for comp in self.fleet_id.engine4_type_id.component_ids:
            allowed_comp.append(comp.id)
            for subcomp in comp.sub_part_ids:
                allowed_comp.append(subcomp.id)
        for comp in self.fleet_id.propeller_type_id.component_ids:
            allowed_comp.append(comp.id)
            for subcomp in comp.sub_part_ids:
                allowed_comp.append(subcomp.id)
        for comp in self.fleet_id.propeller2_type_id.component_ids:
            allowed_comp.append(comp.id)
            for subcomp in comp.sub_part_ids:
                allowed_comp.append(subcomp.id)
        for comp in self.fleet_id.propeller3_type_id.component_ids:
            allowed_comp.append(comp.id)
            for subcomp in comp.sub_part_ids:
                allowed_comp.append(subcomp.id)
        for comp in self.fleet_id.propeller4_type_id.component_ids:
            allowed_comp.append(comp.id)
            for subcomp in comp.sub_part_ids:
                allowed_comp.append(subcomp.id)
        for comp in self.fleet_id.auxiliary_type_id.component_ids:
            allowed_comp.append(comp.id)
            for subcomp in comp.sub_part_ids:
                allowed_comp.append(subcomp.id)
        # self.allowed_component = [(6,0,allowed_comp)]
        return {'domain':{'component': [('id', 'in', allowed_comp)]}}

    @api.multi
    def do_corrective(self):
        return {
            'name': 'Corrective Action',
            'type': 'ir.actions.act_window',
            'res_model': 'ams.corrective_action',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': False,
            'views': [(False, 'form')],
            'target': 'new',
            'context': "{'discripencies':" + str(self.id) + "}",
        }

class InheritDiscrepecies(models.Model):
    _inherit = "ams_fml.log"

    discripencies = fields.One2many('ams.discripencies', 'fml_id', string="Descrepancies", track_visibility="onchange")

class CorrectiveAction(models.Model):
    _name = "ams.corrective_action"
    _rec_name = "action"

    discripencies = fields.Many2one('ams.discripencies', string='Descrepancies', readonly=True, default=lambda self:self.env.context.get('discripencies',False))
    action = fields.Text(string='Action Taken', required=True)
    wo_id = fields.Many2one('ams.work.order', string='Work Order To Comply')
    mwo_id = fields.Many2one('ams.mwo', string='Maintenance Work Order To Comply')
    instruction_type = fields.Selection([('wo','WO'),('mwo','MWO')], string="Instruction Type", default="wo", required=True)

    @api.model
    def create(self, vals):
        if('discripencies' not in vals):
            vals['discripencies']=self.env.context.get('discripencies',False)
        desc = self.env['ams.discripencies'].search([('id','=',vals['discripencies'])])
        if(vals['wo_id'] != False):
            desc.write({
                'status' : 'working',
                'action_take' : vals['action'],
                })
        else:
            desc.write({
                'status' : 'done',
                'action_take' : vals['action'],
                })
        create = super(CorrectiveAction, self).create(vals)
        return create


