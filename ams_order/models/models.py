# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from odoo import models, fields, api
import math

class InheritProduct(models.Model):
    _inherit = 'res.partner'
    
    company_code = fields.Char(string='Letter Code')

class WorkOrder(models.Model):
    _name = 'ams.work.order'
    _description = 'Work Order'

    name = fields.Char()
    start_date = fields.Date('Planning date Start', help='Tanggal mulai maintenance', default=datetime.today())
    end_date = fields.Date('Planning date End', help='Tanggal selesai maintenance', default=datetime.today())
    is_unserviceable = fields.Boolean(string='Aircraft unserviceable during this maintenance')

    date_issued = fields.Date('Date Issue', help='Isikan Tanggal', default=datetime.today())
    wo_no   = fields.Char('W.O. Number', related='name', help='Referensi Dari SAP')
    ref     = fields.Char('Ref.', required=True)
    status = fields.Selection([('request','Request'),('progress','Progress'),('done','Done')], default='request') 
    states = fields.Selection([('draft','Draft'),('confrimed','Confirmed')], default='draft') 
    """ 
    Inspection = material
    material = inspection
    kebalik
    """
    wo_type = fields.Selection([('material','Material'),('inspection','Inspection')], default='material', string="Work Order Type")

    """aircraft"""
    ac      = fields.Many2one('aircraft.acquisition', string="Registration")
    type    = fields.Char('Type', readonly=True, compute='_onchange_ac') 
    serial_no   = fields.Char('Serial Number', readonly=True, compute='_onchange_ac') 
    hr_cy       = fields.Char('Acft. Hrs./Cycle', readonly=False) 
    ins_type    = fields.Char('Inspection type', readonly=False) 
    """component"""
    part_name   = fields.Many2one('product.product', string="Part Name")
    part_number = fields.Char('Part Number', readonly=True, related="part_name.default_code") 
    serial_number = fields.Many2one('stock.production.lot', 'Serial Number') 
    tsn_tso     = fields.Char('TSN / TSO') 
    work_req    = fields.Char('Work required') 
    """address"""
    to    = fields.Text() 
    cc    = fields.Char() 
    """Description"""
    des_id = fields.One2many('work.order.description', 'des_id', string="Description")
    mr_id = fields.One2many('material.required', 'wo_id')
    """NOTE"""
    note =  fields.Html('Note', default='\
                                        - After finish, return original sign WO to Enineering or followed by email to <u>engineering@pelita-air.com</u> <br/>\
                                        - Fill Material Required for any new material required in this inspection <br/>\
                                        - (*) Refer To Maintenance Program <br/>\
                                        ')
    """Employee"""
    performed_by = fields.Many2one('hr.employee')
    inspector = fields.Many2one('hr.employee')
    # engineer = fields.Many2one('hr.employee')
    # supervisor = fields.Many2one('hr.employee')
    issued_by = fields.Many2one('hr.employee')
    recorded = fields.Many2one('hr.employee', store=True)
    # otr_per =  fields.Char('OTR Number')
    otr_ins =  fields.Char('OTR Number')
    # otr_eng =  fields.Char('OTR Number')
    # otr_sup =  fields.Char('OTR Number')
    otr_iss =  fields.Char('OTR Number')
    insp_no =  fields.Char('Refer To')
    otr_record = fields.Char('OTR Number')

    schedule = fields.Boolean('Schedule', default=False)
    recorded_date = fields.Date('Recorded Date')
    checklist_id = fields.Many2one('ams.checklist', string='Checklist')
    todo_ids = fields.One2many('ams.checklist.todo','checklist_id',string='To Do',readonly=True,related='checklist_id.todo_ids')
    desc = fields.Text(string='Description',readonly=True,related='checklist_id.desc')
    
    file_name = fields.Char('File Name', compute=lambda self: self._upload_name())
    file = fields.Binary(string='Scan File',readonly=True,related='checklist_id.file')

    upload_name = fields.Char('File Name')
    upload = fields.Binary(string='Upload File')

    @api.one
    def _upload_name(self):
        if self.file and self.date_issued:
            self.file_name = str(self.date_issued+".pdf")



    @api.model
    def create(self, values):
        fleet = self.env['aircraft.acquisition'].search([('id','=',values['ac'])])
        if(values['wo_type'] == 'material'):
            now = datetime.now()
            if(self.env['ir.sequence'].search([('code','=','ams_order.wo' + str(now.year))]).name == False):
                self.env['ir.sequence'].create({
                        'name' : 'WO ' + str(now.year),
                        'code' : 'ams_order.wo' + str(now.year),
                        'padding' : '3',
                        'prefix' : '/',
                        'suffix' : '/' + str(now.year),
                    })
            seq = self.env['ir.sequence'].next_by_code('ams_order.wo' + str(now.year))
            pstr = ''
            if(fleet.category == 'rotary'):
                pstr = 'WO/RW'
            else:
                pstr = 'WO/FW'
            values['name'] = pstr + seq
    
        create = super(WorkOrder, self).create(values)
        # CREATE LOG
        if(fleet.id != False):
            for des in create.des_id:
                self.env['ams.log'].create({
                    'aircraft_id' : fleet.id,
                    'hours' : fleet.total_hours,
                    'cycles' : fleet.total_landings,
                    'rins' : fleet.total_rins,
                    'date' : create.date_issued,
                    'description' : des.inspection + ' - ' + des.take_action,
                    'wo_id' : create.id,
                    })

        return create



    @api.onchange('ac')
    def _onchange_ac(self):
        for x in self.ac:
            self.type = x.aircraft_type_id.name
            self.hr_cy = str(x.total_hours) +' / '+ str(x.total_landings)

    @api.onchange('part_name')
    def _onchange_part_name(self):
        ctx = self._context.get('servicelife_id', False)
        if ctx != False:
            servicelife_id = self.env['ams.component.servicelife'].search([('id', '=', ctx)], limit=1)

            # 
            if servicelife_id.id != False:
                self.part_name = servicelife_id.part_id.product_id.id
                self.serial_number = servicelife_id.part_id.serial_number.id 
                self.tsn_tso =  str(servicelife_id.part_id.tsn) +" / "+ str(servicelife_id.part_id.tso)
        # for x in self.part_name:
        #     component = self.env['ams.component.part'].search([('product_id','=',x.id)], limit=1, order="create_date DESC")
        #     self.part_number = x.default_code
        #     self.seri_number = component.serial_number.name        
        #     self.qty = x.qty_available  
        #     self.tsn_tso = str(component.tsn)+' / '+str(component.tso)  

    @api.multi
    def confrim(self):
        # CREATE MAINTENANCE
        if(self.ac.id != False):
            date_format = "%Y-%m-%d"
            a = datetime.strptime(self.start_date, date_format)
            b = datetime.strptime(self.end_date, date_format)
            delta = b - a
            self.env['maintenance.request'].create({
                'name' : self.ac.name + '-' + self.name,
                'fl_acquisition_id' : self.ac.id,
                'maintenance_team_id' : self.env['maintenance.team'].search([], limit=1).id,
                'reason_maintenance' : self.note.replace("\
                                        - After finish, return original sign WO to Enineering or followed by email to <u>engineering@pelita-air.com</u> <br/>\
                                        - Fill Material Required for any new material required in this inspection <br/>\
                                        - (*) Refer To Maintenance Program <br/>",""),
                'schedule_date' : self.start_date,
                'duration' : (24 * delta.days) - 1,
                'aircraft_state' : ('serviceable' if self.is_unserviceable == False else 'unserviceable'),
                'wo_id' : self.id
                })
        self.states = 'confrimed'

    @api.onchange('date_issued')
    def _get_current_user(self):
        curr_user = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

        if curr_user != False:
            self.recorded = curr_user.id

    @api.multi
    def get_last_utils(self):
        utils   = self.env['ams.daily'].search([('fleet_id', '=', self.ac.id)], order='id DESC', limit=1)

        if utils.id != False:
            return utils.project_name.name
            

    @api.multi
    def print_engine_work_order_pdf(self):
        return self.env['report'].get_action(self, 'ams_order.report_work_order')


    @api.multi
    def next_stage(self):
        for rec in self:
            if(rec.status == 'request'):
                rec.status = 'progress'
            elif(rec.status == 'progress'):
                rec.status = 'done'

            



class MaterialRequired(models.Model):
    _name = 'material.required'
    _description = 'Material Required'

    name = fields.Many2one('product.product', string='Material Required')
    part_name = fields.Char('Part Number', readonly=True, compute='_partname')
    qty     = fields.Char('Qty', readonly=True, compute='_qty')
    qty_req     = fields.Char('Qty Request')
    spesial_tool = fields.Char('Tool Name')
    spesial_tool_qty = fields.Char('Qty')
    wo_id = fields.Many2one('ams.work.order')
    mwo_id = fields.Many2one('ams.mwo')
    # spesial_tool_id = fields.One2many('special.tool.required', 'mr_id', string="Special Tool Required")

    @api.onchange('name')
    def _onchange_name(self):
        self.part_name = self.name.default_code
        self.qty = self.name.qty_available

    @api.one
    @api.model
    def _partname(self):
        self.part_name = self.name.default_code

    @api.one
    @api.model
    def _qty(self):
        self.qty = self.name.qty_available

            


class DescriptionWO(models.Model):
    _name = 'work.order.description'
    _description = 'Description'

    inspection  = fields.Char() 
    refer_to    = fields.Char() 
    due_at      = fields.Date() 
    take_action = fields.Text()

    date = fields.Date('Date')
    man_power   = fields.Char('Man Power')
    man_hours   = fields.Char('Man Hours')
    start   = fields.Date('Start')
    finish  = fields.Date('Finish')

    text = fields.Html('Description')

    wo_type = fields.Selection([('material','Material'),('inspection','Inspection')], string="Work Order Type", default=lambda self: self._get_default_type())

    des_id = fields.Many2one('ams.work.order', default=lambda self:self.env.context.get('default_config_id',False))
    mwo_id = fields.Many2one('ams.mwo', default=lambda self:self.env.context.get('default_config_id',False))


    @api.onchange('date')
    def _onchange_date(self):
        if self.des_id.wo_type:
            self.wo_type =  self.des_id.wo_type
        else:
            self.wo_type =  self.mwo_id.wo_type

    @api.model
    def _get_default_type(self):
        if self.des_id:
            if self.des_id.wo_type:
                return self.des_id.wo_type
            else:
                return self.mwo_id.wo_type

class MWO(models.Model):
    _name = 'ams.mwo'
    _description = 'Maintenance Work Order'

    name = fields.Char(readonly=True)
    start_date = fields.Date('Planning date Start', help='Tanggal mulai maintenance', default=datetime.today())
    end_date = fields.Date('Planning date End', help='Tanggal selesai maintenance', default=datetime.today())
    is_unserviceable = fields.Boolean(string='Aircraft unserviceable during this maintenance')

    date = fields.Date('Date', help='Isikan Tanggal', default=datetime.today())
    mwo_no   = fields.Char('No.', related='name', help='Referensi Dari SAP')
    ref     = fields.Char('Reff. No.') 
    location = fields.Many2one('base.operation', 'Location', help='Lokasi Pekerjaan', )
    mwo_type = fields.Selection([('material','Inspection'),('inspection','Component')], default='material', string="MWO Type")
    status = fields.Selection([('request','Request'),('progress','Progress'),('done','Done')], default='request') 
    states = fields.Selection([('draft','Draft'),('confrimed','Confirmed')], default='draft') 

    recorded = fields.Many2one('hr.employee', store=True)


    """Macam Pekerjaan"""
    macam      = fields.Html('Macam Pekerjaan')
    syarat = fields.Char('Syarat - syarat pekerjaan')
    waktu = fields.Date('Waktu Pelaksanaan')
    harga = fields.Float('Harga Pekerjaan')
    pembayaran = fields.Many2one('cara.pembayaran', string='Cara Pembayaran',  default=lambda self: self.env['cara.pembayaran'].search([('name','=','Transfer setelah Invoice diterima')]))
    sangsi = fields.Html('Sanksi', default="<p>Apabila dalam jangka waktu seperti disebutkan dalam butir 3 (tiga) pada <b>WO</b> ini <b>PIHAK KEDUA</b> tidak dapat memenuhi kewajibannya, maka <b>PIHAK KEDUA</b> dikenakan denda sebesar 0,5% perhari dari perkiraan total harga pekerjaan dan apabila <b>PIHAK PERTAMA</b> tidak dapat memenuhi butir 5, maka <b>PIHAK PERTAMA</b> akan dikenakan denda yang sama.</p>")

    """Pihak Pertama"""
    nama_pihak  = fields.Char(string="Nama")
    jabatan     = fields.Char('Job Title', help='Jabatan')
    perusahaan  = fields.Many2one('res.partner', 'Departement' , help='Perusahaan')
    alamat      = fields.Char('Address', help='Alamat')
    """Pihak Kedua"""
    nama_pihak2  = fields.Char(string="Nama")
    jabatan2     = fields.Char('Job Title', help='Jabatan')
    perusahaan2  = fields.Many2one('res.partner', 'Departement', help='Perusahaan')
    alamat2      = fields.Char('Address', help='Alamat')
    schedule = fields.Boolean('Schedule', default=False)
    ac      = fields.Many2one('aircraft.acquisition', string="Aircraft")

    checklist_id = fields.Many2one('ams.checklist', string='Checklist')
    todo_ids = fields.One2many('ams.checklist.todo','checklist_id',string='To Do',readonly=True,related='checklist_id.todo_ids')
    desc = fields.Text(string='Description',readonly=True,related='checklist_id.desc')

    file_name = fields.Char('File Name', compute=lambda self: self._upload_name())
    file = fields.Binary(string='Scan File',readonly=True,related='checklist_id.file')

    upload_name = fields.Char('File Name')
    upload = fields.Binary(string='Upload File')

    def _upload_name(self):
        self.file_name = str(self.date+".pdf")

    @api.onchange('date')
    def _get_curr_user(self):
        curr_user = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

        if curr_user != False:
            self.recorded = curr_user.id

    @api.model
    def create(self, values):
        now = datetime.now()
        if(self.env['ir.sequence'].search([('code','=','ams_order.mwo' + str(now.year))]).name == False):
            self.env['ir.sequence'].create({
                    'name' : 'MWO ' + str(now.year),
                    'code' : 'ams_order.mwo' + str(now.year),
                    'padding' : '3',
                    'prefix' : 'MWO/',
                    'suffix' : '/AM/',
                })
        seq = self.env['ir.sequence'].next_by_code('ams_order.mwo' + str(now.year))
        pstr = ''

        letter_code = self.env['res.partner'].search([('id','=',values['perusahaan2'])]).company_code 

        if(letter_code == False):
            letter_code = ''

        if(values['mwo_type'] == 'material'):
            pstr = 'WO.'+ str(letter_code) +'/'
        else:
            pstr = 'CRO/WO/'+ str(letter_code) +'/'
        values['name'] = seq + pstr + (str(now.year)[2:])
        create = super(MWO, self).create(values)

        fleet = self.env['aircraft.acquisition'].search([('id','=',values['ac'])])
        if(fleet.id != False):
            self.env['ams.log'].create({
                'aircraft_id' : fleet.id,
                'hours' : fleet.total_hours,
                'cycles' : fleet.total_landings,
                'rins' : fleet.total_rins,
                'date' : create.date,
                'description' : create.macam,
                'mwo_id' : create.id,
                })

        return create

    @api.multi
    def print_mainteenance_work_order_pdf(self):
        return self.env['report'].get_action(self, 'ams_order.report_maintenance_work_order_')
        
    @api.multi
    def confrim(self):
        if(self.ac.id != False):
            # CREATE MAINTENANCE
            date_format = "%Y-%m-%d"
            a = datetime.strptime(self.start_date, date_format)
            b = datetime.strptime(self.end_date, date_format)
            delta = b - a
            self.env['maintenance.request'].create({
                'name' : self.macam,
                'fl_acquisition_id' : self.ac.id,
                'maintenance_team_id' : self.env['maintenance.team'].search([], limit=1).id,
                'reason_maintenance' : self.macam,
                'schedule_date' : self.start_date,
                'duration' : (24 * delta.days) - 1,
                'aircraft_state' : ('serviceable' if self.is_unserviceable == False else 'unserviceable'),
                'mwo_id' : self.id
                })
        self.states = 'confrimed'

    @api.multi
    def next_stage(self):
        for rec in self:
            if(rec.status == 'request'):
                rec.status = 'progress'
            elif(rec.status == 'progress'):
                rec.status = 'done'


class CaraPembayaran(models.Model):
    _name = 'cara.pembayaran'
    _description = 'Cara Pembayaran'

    name = fields.Char('Cara Pembayaran')
    # mwo_id = fields.Many2one('ams.mwo')

class MaintenanceCalendarCorrectiveWO(models.Model):
    _inherit = 'maintenance.request'
    
    wo_id = fields.Many2one('ams.work.order',string='WO')
    mwo_id = fields.Many2one('ams.mwo',string='WO')