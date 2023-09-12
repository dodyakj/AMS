from odoo import fields, models, api, _
from datetime import datetime, timedelta

class ToolType(models.Model):
    _inherit = ["mail.thread", "ir.needaction_mixin", "gse.type"]
    _name = 'tool.type'
    _description = 'Tool'
    _rec_name = 'tool'

    tool = fields.Many2one('master.tools', 'Tools Name', required=True)
    type = fields.Selection([('onboard','On Board'),('onground','On Ground')], required=True)
    fleet_id = fields.Many2one('aircraft.acquisition', string="Location")
    base_id = fields.Many2one('base.operation', string="Location")
    count_calibrate =  fields.Integer(default=1 , readonly=True)
    remark = fields.Text('Remark')
    spesial_tool = fields.Boolean('Is Special Tool')
    tool_type_line = fields.Many2many('aircraft.type',string='Tool For')
    need_calibrate = fields.Boolean('Need Calibration')
    status = fields.Selection([('available','Available'),('qurantine','Qurantine'),('calibrate','On Calibration'),('unserviceable', 'Unserviceable')], string='Status', default='available')
    get_calibrate = fields.Many2one('tool.calibrate',string='Data Calibrate', compute=lambda self: self._onchange_calibrate_line())
    calibrate_last = fields.Date(string='Last Calibrated',related='get_calibrate.calibrate_last')
    calibrate_next = fields.Date(string='Next Calibrate Due',related='get_calibrate.calibrate_next')

    qurantine_line = fields.One2many('tool.qurantine','tool_id', string='Document')
    calibrate_line = fields.One2many('tool.calibrate','tool_id', string='History Calibrate')

    file_name = fields.Char('File Name', compute=lambda self: self._upload_name())
    document_tool = fields.Binary(string='Document Tool',related='get_calibrate.document_calibrate')

    part_num = fields.Char('Part Number')

    @api.one
    def _upload_name(self):
        if self.document_tool and self.tool:
            self.file_name = str(self.tool.name+".pdf")

    # @api.onchange('type')
    # def _associate_account(self):
    #     if (self.id):
    #         data = self.env['tool.calibrated'].search_count([('tool_id.id','=',self.id)])
    #         self.count_calibrate = data
            

    @api.one
    @api.depends('calibrate_line')
    def _onchange_calibrate_line(self):
        for rc in self:
            if rc.id or self.env['tool.calibrate'].search([('tool_id','=',rc.id)]):
                calibrated = self.env['tool.calibrate'].search([('tool_id','=',rc.id)], limit=1, order="create_date desc")
                self.get_calibrate = calibrated.id


    @api.multi
    def do_calibarted(self):
        self.status = 'calibrate'
        return {
            'type': 'ir.actions.act_window',
            'tag': 'reload',
            'res_model': 'tool.calibrate',
            'view_mode': 'form',
            'view_type': 'form',
            'views': [(False, 'form')],
            'target': 'new',
            'context': {
                'tool_id' : self.id
            }
        }

    @api.multi
    def do_calibarted_end(self):
        self.status = 'available'
        return {
            'type': 'ir.actions.act_window',
            'tag': 'reload',
            'res_model': 'tool.calibrate',
            'view_mode': 'form',
            'view_type': 'form',
            'views': [(False, 'form')],
            'target': 'new',
            'context': {
                'tool_id' : self.id
            }
        }

   
    @api.multi
    def do_qurantine_start(self):
        self.status = 'qurantine'
        return {
            'type': 'ir.actions.act_window',
            'tag': 'reload',
            'res_model': 'tool.qurantine',
            'view_mode': 'form',
            'view_type': 'form',
            'views': [(False, 'form')],
            'target': 'new',
            'context': {
                'tool_id' : self.id,
                'status' : False
            }
        }

    @api.multi
    def do_qurantine_end(self):
        self.status = 'available'
        return {
            'type': 'ir.actions.act_window',
            'tag': 'reload',
            'res_model': 'tool.qurantineand',
            'view_mode': 'form',
            'view_type': 'form',
            'views': [(False, 'form')],
            'target': 'new',
            'context': {
                'tool_id' : self.id,
                'status' : True
            }
        }

class ToolsName(models.Model):
    _name = 'master.tools'
    _description = 'Tools Name'

    name = fields.Char('Tools Name', required=True)


class ToolCalibrated(models.Model):
    _name = 'tool.calibrate'
    _description = 'Tool Calibrated'

    tool_type_id = fields.Many2many('tool.type',string='Data Tool')
    calibrate_last = fields.Date(string='Calibrated at')
    calibrate_next = fields.Date(string='Next Calibrate Due')
    tool_id = fields.Many2one('tool.type', default=lambda self:self.env.context.get('tool_id',False))
    file_name = fields.Char('File Name', compute=lambda self: self._upload_name())
    document_calibrate = fields.Binary(string='Document')
    tool_id = fields.Many2one('tool.type', default=lambda self:self.env.context.get('tool_id',False))

    @api.one
    def _upload_name(self):
        if self.calibrate_last:
            for rec in self:
                self.file_name = str(rec.calibrate_last+".pdf")

    @api.multi 
    def action_save(self):
        #your code
        self.ensure_one()
        #close popup
        return {'type': 'ir.actions.act_window_close'}

class ToolQurantine(models.Model):
    _name = 'tool.qurantine'
    _description = "Tool Qurantine"

    tool_type_id = fields.Many2many('tool.type',string='Data Tool')
    qurantine_start = fields.Date(string='Date Start')
    qurantine_end = fields.Date(string='Date End')
    reason = fields.Text(string='Reason')
    file_name = fields.Char('File Name', compute=lambda self: self._upload_name())
    document_qurantine = fields.Binary(string='Document')
    status = fields.Boolean(default=lambda self:self.env.context.get('status'))
    tool_id = fields.Many2one('tool.type', default=lambda self:self.env.context.get('tool_id',False))

    def _upload_name(self):
        self.file_name = str(self.qurantine_start+".pdf")


class ToolQurantineAnd(models.Model):
    _name = 'tool.qurantineand'
    _description = "Tool Qurantine And"

    tool_type_id = fields.Many2many('tool.type',string='Data Tool')
    qurantine_end = fields.Date(string='Date End', default=datetime.now())
    file_name = fields.Char('File Name', compute=lambda self: self._upload_name())
    document_qurantine = fields.Binary(string='Document')
    tool_id = fields.Many2one('tool.type', default=lambda self:self.env.context.get('tool_id',False))

    def _upload_name(self):
        self.file_name = str(self.qurantine_end+".pdf")

    @api.model
    def create(self, vals):
        rec = super(ToolQurantineAnd, self).create(vals)

        tool = self.env['tool.qurantine'].search([('tool_id', '=', rec.tool_id.id)], limit=1, order='id desc')
        tool.write({'qurantine_end': rec.qurantine_end , 'document_qurantine' : rec.document_qurantine})

        return rec    


class ToolMovement(models.Model):
    _name = 'tool.movement'
    _description = 'Tool Movement'
    # _rec_name ='tool'

    name = fields.Char(string='Number')
    employee = fields.Many2one('hr.employee', string="Employee", required=True)
    tool = fields.Many2one('tool.type', string='Tool Name', required=True)
    date = fields.Date('Date', default=lambda *a: datetime.now())
    time = fields.Float()

    refer = fields.Selection([('AD','AD'),('SB','SB'),('STC','STC'),('SERVICE','SERVICE'),('EO','EO'),('MI','MI'),('TI','TI'),('OTI','OTI')], string="Reference", required=True)
   
    
    

    location = fields.Many2one('base.operation')
    status = fields.Selection([('request','Request'),('onhand','On Hand'),('complete','Complete')])

    remark = fields.Text('Remark')

    @api.model
    def create(self, values):
        now = datetime.now()
        if(self.env['ir.sequence'].search([('code','=','ams_base.toolmove' + str(now.year))]).name == False):
            self.env['ir.sequence'].create({
                    'name' : 'Tool Movement ' + str(now.year),
                    'code' : 'ams_base.toolmove' + str(now.year),
                    'padding' : '5',
                    'prefix' : 'PAS/TM/',
                    'suffix' : '/' + str(now.year),
                })
        seq = self.env['ir.sequence'].next_by_code('ams_base.toolmove' + str(now.year))
        values['name'] = seq
        return super(ToolMovement, self).create(values)

    @api.multi
    def get_request(self):
        self.status = 'request'

    @api.multi
    def get_onhand(self):
        self.status = 'onhand'

    @api.multi
    def get_complete(self):
        self.status = 'complete'

    # @api.onchange('refer')
    # def _onchange_refer(self):
    #     self.refer_ad = ''
    #     self.refer_sb = ''
    #     self.refer_stc = ''
    #     self.refer_ser = ''
    #     self.refer_eo = ''
    #     self.refer_mi = ''
    #     self.refer_ti = ''
    #     self.refer_oti = ''
        