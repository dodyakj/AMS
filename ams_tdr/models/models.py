# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
import math
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
import math
import xlwt
from xlsxwriter import *
from cStringIO import StringIO
import base64
from reportlab.pdfgen import canvas
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
import time

class AmsMainTracking(models.Model):
    _name = 'ams.mtr'
    _description = 'Maintenance Tracking Report'

    name = fields.Date(string="Date",default=fields.Date.today())
    fleet_id = fields.Many2one('aircraft.acquisition',string='Aircraft', required=True)
    show_pp = fields.Boolean(string='Show Project Date', default=False)

    states = fields.Selection([('create_by','Create By'),('checked_by','Checked By'),('approved_by','Approved By'),('qc_by','Quality Control')])
    create_by = fields.Many2one('res.partner', readonly=True)
    checked_by = fields.Many2one('res.partner', readonly=True)
    approved_by = fields.Many2one('res.partner', readonly=True)
    qc_by = fields.Many2one('res.partner', string="Quality Control", readonly=True)

    data_status = fields.Boolean(string='Data Status', default=False)

    mtr_seq = fields.Char(string="Number", compute="_get_squence", store=True)

    ac_hours = fields.Float(string='Aircraft Hours')
    ac_cycles = fields.Float(string='Aircraft Cycles')

    eng1_hours = fields.Float(string='Engine #1 Hours')
    eng1_cycles = fields.Float(string='Engine #1 Cycles')

    eng2_hours = fields.Float(string='Engine #2 Hours')
    eng2_cycles = fields.Float(string='Engine #2 Cycles')

    eng3_hours = fields.Float(string='Engine #3 Hours')
    eng3_cycles = fields.Float(string='Engine #3 Cycles')

    eng4_hours = fields.Float(string='Engine #4 Hours')
    eng4_cycles = fields.Float(string='Engine #4 Cycles')

    aux_hours = fields.Float(string='APU Hours')
    aux_cycles = fields.Float(string='APU Cycles')
    
    engine1_id = fields.Many2one('engine.type',string='Engine #1')
    engine2_id = fields.Many2one('engine.type',string='Engine #2')
    engine3_id = fields.Many2one('engine.type',string='Engine #3')
    engine4_id = fields.Many2one('engine.type',string='Engine #4')
    
    auxiliary_id = fields.Many2one('auxiliary.type',string='Auxiliary Power Unit')

    last_flight = fields.Date(string='Last Flight')
    daily_hours = fields.Float(string='Daily A/C Hours')

    component_ids = fields.One2many('ams_tdr.component','ref_id',string='Components')
    componenteng1_ids = fields.One2many('ams_tdr.componenteng1','ref_id',string='Components')
    componenteng2_ids = fields.One2many('ams_tdr.componenteng2','ref_id',string='Components')
    componenteng3_ids = fields.One2many('ams_tdr.componenteng3','ref_id',string='Components')
    componenteng4_ids = fields.One2many('ams_tdr.componenteng4','ref_id',string='Components')
    componentaux_ids = fields.One2many('ams_tdr.componentaux','ref_id',string='Components')
    
    inspection_ids = fields.One2many('ams_tdr.inspection','ref_id',string='Inspection')
    inspectioneng1_ids = fields.One2many('ams_tdr.inspectioneng1','ref_id',string='Inspection')
    inspectioneng2_ids = fields.One2many('ams_tdr.inspectioneng2','ref_id',string='Inspection')
    inspectioneng3_ids = fields.One2many('ams_tdr.inspectioneng3','ref_id',string='Inspection')
    inspectioneng4_ids = fields.One2many('ams_tdr.inspectioneng4','ref_id',string='Inspection')
    inspectionaux_ids = fields.One2many('ams_tdr.inspectionaux','ref_id',string='Inspection')


    def __datetime(self, date_str):
        return datetime.strptime(str(date_str), "%d/%m/%Y")


    def get_at_ins(self, compdate, install_at):
        if install_at and compdate:
            get = str(self.__datetime(datetime.strptime(compdate, '%Y-%m-%d').strftime('%d/%m/%Y')) - self.__datetime(datetime.strptime(install_at, '%d/%m/%Y').strftime('%d/%m/%Y'))).split(' ')
            if get[0] != '0:00:00':
                get = str(abs(int(get[0])))+' '+str(get[1])[:-1]
            else:
                get = '0 days'
            return get 
        else:
            get = '0 days'
            return get 
            


    def get_re_inp(self, remaining, since_last):
        if isinstance(since_last, float) == False:
            get = int(remaining) - int(since_last.split('days')[0])
            return str(get)+ " days"
        else:
            return remaining



    def get_remaining(self, due_at, remaining):
        if len(str(due_at).split('/')) == 1:
            get = remaining
        else:
            get = str(self.__datetime(due_at) - self.__datetime(str(datetime.today().strftime('%d/%m/%Y')))).split(' ')
            get = str(get[0])+' '+str(get[1])[:-1]
        return get




    def get_tso(self, installed_at, due_at, service_life, at_installation, eng):
        installed_at = self.get_ins_at(installed_at, due_at, service_life, at_installation)
        # print installed_at, service_life, at_installation, service_life in 'MO'
        get = '' 
        if isinstance(installed_at, float) == False:
            at =  len(installed_at.split('/'))
        else:
            at = 0
        if service_life != 'OC':
            ser = service_life.split(' ')[1]
        else:
            ser = service_life

        if (ser == 'MO:IN' or ser == 'MO:OH' or ser == 'MO:RT' or ser == 'DY:OH' or ser == 'DY:IN' or ser == 'DY:RT' or ser == 'YR:OH' or ser == 'YR:IN' or ser == 'YR:RT') and at != 1:
            serv = int(service_life.split(' ')[0])
            if ser == 'DY:OH' or ser == 'DY:IN' or ser == 'DY:RT':
                get = (datetime.now() + relativedelta(days=serv)).strftime('%d/%m/%Y')
            elif ser == 'MO:IN' or ser == 'MO:OH' or ser == 'MO:RT':
                get = (datetime.now() + relativedelta(months=serv)).strftime('%d/%m/%Y')
            else:
                get = (datetime.now() + relativedelta(years=serv)).strftime('%d/%m/%Y')
            get = str(self.__datetime(str(datetime.now().strftime('%d/%m/%Y'))) - self.__datetime(datetime.strptime(get, '%d/%m/%Y').strftime('%d/%m/%Y'))).split(' ')
            get = str(str(abs(int(get[0]))))+' '+str(get[1])[:-1]
            return get 
        elif ser == 'HR:RT' or ser == 'CY:RT' or ser == 'DY:RT' or ser == 'MO:RT' or ser == 'YR:RT' :
            get = 'N/A'
            return str(get)
         
        else:
            if ser == 'HR:OH' or ser == 'HR:IN 'or ser == 'HR:RT':
                if eng == 0:
                    total_jam = self.fleet_id.total_hours
                elif eng == 1:
                    total_jam = self.fleet_id.engine_type_id.engine_tsn
                elif eng == 2:
                    total_jam = self.fleet_id.engine2_type_id.engine_tsn
                elif eng == 3:
                    total_jam = self.fleet_id.engine3_type_id.engine_tsn
                else:
                    total_jam = self.fleet_id.engine4_type_id.engine_tsn

            elif ser == 'RIN:OH' and self.fleet_id.rin_active:
                total_jam = self.fleet_id.total_rins
            else:
                if eng == 0:
                    total_jam = self.fleet_id.total_landings
                elif eng == 1:
                    total_jam = self.fleet_id.engine_type_id.engine_csn
                elif eng == 2:
                    total_jam = self.fleet_id.engine2_type_id.engine_csn
                elif eng == 3:
                    total_jam = self.fleet_id.engine3_type_id.engine_csn
                else:
                    total_jam = self.fleet_id.engine4_type_id.engine_csn
                
            get = float((float(total_jam) - float(installed_at))+float(at_installation))
            get = round(get,2)
            # get = self.get_float(str(get))
            # print service_life, due_at, '(', total_jam, ' - ', installed_at, ') + ', at_installation,  'FLEEt', get
            return self.get_float(str(get))

    def get_tsn_real():
        return 'XTSN'

    def get_tsn(self, compdate):
        get = str(self.__datetime(str(datetime.now().strftime('%d/%m/%Y'))) - self.__datetime(datetime.strptime(compdate, '%Y-%m-%d').strftime('%d/%m/%Y'))).split(' ')
        get = str(get[0])+' '+str(get[1])[:-1]
        return get 

    def get_cal_tso(self, date):
        get = str(self.__datetime(str(datetime.now().strftime('%d/%m/%Y'))) + self.__datetime(datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y'))).split(' ')
        get = str(get[0])+' '+str(get[1])[:-1]
        return get 


    def get_last_insp(self, last_inspection):
        get = str(self.__datetime(str(datetime.now().strftime('%d/%m/%Y'))) - self.__datetime(datetime.strptime(last_inspection, '%Y-%m-%d').strftime('%d/%m/%Y'))).split(' ')
        get = str(str(abs(int(get[0]))))+' '+str(get[1])[:-1]
        return get 


    def get_due_at(self, remaining, inpectiondate, service_life, baseon, status):
        # print remaining, baseon, inpectiondate, service_life, status, 'due at'
        if baseon == "hours":
            if status == 'FLEET':
                get = float(self.fleet_id.total_hours) + float(remaining) 
            elif status == 'ENG1':
                get = float(self.fleet_id.engine_type_id.engine_tsn) + float(remaining)
            elif status == 'ENG2':
                get = float(self.fleet_id.engine2_type_id.engine_tsn) + float(remaining)
            elif status == 'ENG3':
                get = float(self.fleet_id.engine3_type_id.engine_tsn) + float(remaining)
            elif status == 'ENG4':
                get = float(self.fleet_id.engine4_type_id.engine_tsn) + float(remaining)
            else:
                get = float(self.fleet_id.auxiliary_type_id.auxiliary_tsn) + float(remaining)
        elif baseon == "cycles":
            if status == 'FLEET':
                get = float(self.fleet_id.total_landings) + float(remaining) 
            elif status == 'ENG1':
                get = float(self.fleet_id.engine_type_id.engine_csn) + float(remaining)
            elif status == 'ENG2':
                get = float(self.fleet_id.engine2_type_id.engine_csn) + float(remaining)
            elif status == 'ENG3':
                get = float(self.fleet_id.engine3_type_id.engine_csn) + float(remaining)
            elif status == 'ENG4':
                get = float(self.fleet_id.engine4_type_id.engine_csn) + float(remaining)
            else:
                get = float(self.fleet_id.auxiliary_type_id.auxiliary_csn) + float(remaining)
        elif baseon == "days":
            get = (datetime.strptime(str(inpectiondate), '%Y-%m-%d') + relativedelta(days=int(service_life))).strftime('%d/%m/%Y')
        elif baseon == "month":
            get = (datetime.strptime(str(inpectiondate), '%Y-%m-%d') + relativedelta(months=int(service_life))).strftime('%d/%m/%Y')
        elif baseon == "year":
            get = (datetime.strptime(str(inpectiondate), '%Y-%m-%d') + relativedelta(years=int(service_life))).strftime('%d/%m/%Y')
        else:
            get = ''
            
        return get

    def get_since_last(self, current, last_inspection, baseon, status):
        if baseon == "hours":
            if status == 'FLEET':
                get = current 
            elif status == 'ENG1':
                get = current
            elif status == 'ENG2':
                get = current
            elif status == 'ENG3':
                get = current
            elif status == 'ENG4':
                get = current
            else:
                get = current
        elif baseon == "cycles":
            if status == 'FLEET':
                get = current 
            elif status == 'ENG1':
                get = current
            elif status == 'ENG2':
                get = current
            elif status == 'ENG3':
                get = current
            elif status == 'ENG4':
                get = current
            else:
                get = current
        elif baseon == 'month' or baseon == 'days' or baseon == 'year':
            get = str(self.__datetime(str(datetime.now().strftime('%d/%m/%Y'))) - self.__datetime(datetime.strptime(last_inspection, '%Y-%m-%d').strftime('%d/%m/%Y'))).split(' ')
            get = str(str(abs(int(get[0]))))+' '+str(get[1])[:-1]
        else:
            get = 'N/A'
        return get

    def get_ins_at(self, installed_at, due_at, service_life, at_installation):
        # print installed_at, due_at, service_life, at_installation
        if len(str(due_at).split('/')) == 1 and service_life != 'OC':
            return float((float(due_at)-float(str(service_life).split(' ')[0]))+float(at_installation))
        else:
            return str(installed_at)


    def get_string(self, string):
        get_str = str(string).title()
        return get_str

    def get_float_h(self, number):
        get = str(str(number).split('.')[0])
        get2 = str(str(number).split('.')[1])
        numbers = ''
        for x in get:
            if x.isdigit():
                numbers += str(x)
        hasil = numbers +'.'+ get2
        return self.get_float(hasil)

    def get_float(self, number):
        get = str(number.split('.')[1])
        numbers = str(number)
        if len(get) != 1:
            numbers = str(number)
        else:
            numbers = str(number)+'0'
        return numbers

    def get_date(self, date):
        if date == 0:
            get = datetime.now().strftime('%d/%m/%Y')
        elif date == '':
            get = ''
        else:
            get = datetime.strptime(date, '%Y-%m-%d').strftime("%d/%m/%Y")
        return get

    def get_time(self, time):
        if time == 0:
            get = datetime.now().strftime('%H:%M:%S')
        else:
            get = datetime.strptime(time, '%Y-%m-%d').strftime("%H:%M:%S")
        return get

    def get_lasflight(self, fleet):
        fml = self.env['ams_fml.log'].search([('aircraft_id','=',fleet)], order="create_date ASC", limit=1)
        if fml:
            return fml.date
        else:
            return 'None'

    """ ENGINE COMPONENT"""

    def get_due_at_hour(self, due_at, at_installation):
        get = float(due_at) - float(at_installation)
        return get

    def get_tsn_engine_hour(self, hours, installed_at, at_installation):
        get = (float(hours) - float(installed_at))+ float(at_installation)
        return get

    def get_tso_hour(self, tso, at_installation):
        get = float(tso) + float(at_installation)
        return get

    def get_remaining_hour(self, remaining, at_installation):
        get = float(remaining) - float(at_installation)
        return get

    @api.model
    def process_data_part(self, r_id):
        ro = self.env['ams.mtr'].search([('id','=',r_id)])
        # SEEK FOR CMOMPONENT
        final_specomp = []
        specomp = []
        subspecomp = []
        for g in ro.mapped('fleet_id').mapped('component_ids').mapped('serfice_life'):
            if(g.unit in ['year','month','days']):
                date_format = "%Y-%m-%d"
                d0 = datetime.strptime(g.current_date, date_format)
                d1 = datetime.strptime(g.next_date, date_format)
                delta = d1 - d0
            specomp.append((0, 0,{
                'is_subcomp':False,
                'parents_id':'X' + str(g.part_id.id).zfill(6) + '.000000',
                'ref_id' : ro.id,
                'installed_at':g.installed_at,
                'ata':g.part_id.ata_code.name,
                'tsn':self.getTsinceNew(g.id),
                'tso':self.getTsinceOverhaul(g.id),
                'at_installation': g.at_install if g.unit not in ['year','month','days'] else '',
                'component_id': g.part_id.id,
                'expired': self.countDate(self.fleet_id,g.id) if g.unit not in ['year','month','days'] else g.next_date,
                'remaining': g.remaining if g.unit not in ['year','month','days'] else str(delta.days) + ' days',
                'remaining_text': g.remaining_text,
                'service_life':self.getSliveText(g.id),
                'due_at':self.getDueatText(g.id),
                'comment':g.comments,
                'gi_part_name':g.part_id.product_id.name,
                'gi_part_number':g.part_id.product_id.default_code,
                'gi_serial_number':g.part_id.serial_number.name,
                'remaining_number': g.remaining if g.unit not in ['year','month','days'] else str(delta.days),
                }))
        # PROPELLER COMPONENT
        for propnum in xrange(1,5):
            if(propnum == 1):
                propeller = ro.fleet_id.propeller_type_id
            elif(propnum == 2):
                propeller = ro.fleet_id.propeller2_type_id
            elif(propnum == 3):
                propeller = ro.fleet_id.propeller3_type_id
            elif(propnum == 4):
                propeller = ro.fleet_id.propeller4_type_id
            if(propeller):
                for g in propeller.mapped('component_ids').mapped('serfice_life'):
                    if(g.unit in ['year','month','days']):
                        date_format = "%Y-%m-%d"
                        d0 = datetime.strptime(g.current_date, date_format)
                        d1 = datetime.strptime(g.next_date, date_format)
                        delta = d1 - d0
                    specomp.append((0, 0,{
                        'is_subcomp':False,
                        'parents_id':'X' + str(g.part_id.id).zfill(6) + '.000000',
                        'ref_id' : ro.id,
                        'installed_at':g.installed_at,
                        'ata':g.part_id.ata_code.name,
                        'tsn':self.getTsinceNew(g.id),
                        'tso':self.getTsinceOverhaul(g.id),
                        'at_installation': g.at_install if g.unit not in ['year','month','days'] else '',
                        'component_id': g.part_id.id,
                        'expired': self.countDate(self.fleet_id,g.id) if g.unit not in ['year','month','days'] else g.next_date,
                        'remaining': g.remaining if g.unit not in ['year','month','days'] else str(delta.days) + ' days',
                        'remaining_text': g.remaining_text,
                        'service_life':self.getSliveText(g.id),
                        'due_at':self.getDueatText(g.id),
                        'comment':g.comments,
                        'gi_part_name':g.part_id.product_id.name,
                        'gi_part_number':g.part_id.product_id.default_code,
                        'gi_serial_number':g.part_id.serial_number.name,
                        'remaining_number': g.remaining if g.unit not in ['year','month','days'] else str(delta.days),
                        }))
        specomp = sorted(specomp, key=lambda k: (k[2]['ata'] , k[2]['parents_id']))
        index = 1
        for i in range(len(specomp)):
            specomp[i][2]['parents_id'] = str(index).zfill(6) + '.000000'
            index = index + 1
            # SEEK FOR SUBCOMPONENT
        for g in ro.mapped('fleet_id').mapped('component_ids').mapped('sub_part_ids').mapped('serfice_life'):
            # GET PARENT
            parents_id = False
            for i in range(len(specomp)):
                if (specomp[i][2]['component_id'] == g.part_id.part_id.id):
                    parents_id = specomp[i][2]['parents_id']
            if(g.unit in ['year','month','days']):
                date_format = "%Y-%m-%d"
                d0 = datetime.strptime(g.current_date, date_format)
                d1 = datetime.strptime(g.next_date, date_format)
                delta = d1 - d0
            subspecomp.append((0, 0,{
                'is_subcomp':True,
                'parents_id': (str(parents_id)[:6] + '.' + str(g.part_id.id).zfill(6)),
                'ref_id' : ro.id,
                'installed_at':g.installed_at,
                'ata':g.part_id.ata_code.name,
                'tsn':self.getTsinceNew(g.id),
                'tso':self.getTsinceOverhaul(g.id),
                'at_installation': g.at_install if g.unit not in ['year','month','days'] else '',
                'component_id': g.part_id.id,
                'expired': self.countDate(self.fleet_id,g.id) if g.unit not in ['year','month','days'] else g.next_date,
                'remaining': g.remaining if g.unit not in ['year','month','days'] else str(delta.days) + ' days',
                'remaining_text': g.remaining_text,
                'service_life':self.getSliveText(g.id),
                'due_at':self.getDueatText(g.id),
                'comment':g.comments,
                'gi_part_name':g.part_id.product_id.name,
                'gi_part_number':g.part_id.product_id.default_code,
                'gi_serial_number':g.part_id.serial_number.name,
                'remaining_number': g.remaining if g.unit not in ['year','month','days'] else str(delta.days),
                }))
        # PROPELLER SUB-COMPONENT
        for propnum in xrange(1,5):
            if(propnum == 1):
                propeller = ro.fleet_id.propeller_type_id
            elif(propnum == 2):
                propeller = ro.fleet_id.propeller2_type_id
            elif(propnum == 3):
                propeller = ro.fleet_id.propeller3_type_id
            elif(propnum == 4):
                propeller = ro.fleet_id.propeller4_type_id
            if(propeller):
                for g in propeller.mapped('component_ids').mapped('sub_part_ids').mapped('serfice_life'):
                    # GET PARENT
                    parents_id = False
                    for i in range(len(specomp)):
                        if (specomp[i][2]['component_id'] == g.part_id.part_id.id):
                            parents_id = specomp[i][2]['parents_id']
                    if(g.unit in ['year','month','days']):
                        date_format = "%Y-%m-%d"
                        d0 = datetime.strptime(g.current_date, date_format)
                        d1 = datetime.strptime(g.next_date, date_format)
                        delta = d1 - d0
                    subspecomp.append((0, 0,{
                        'is_subcomp':True,
                        'parents_id': (str(parents_id)[:6] + '.' + str(g.part_id.id).zfill(6)),
                        'ref_id' : ro.id,
                        'installed_at':g.installed_at,
                        'ata':g.part_id.ata_code.name,
                        'tsn':self.getTsinceNew(g.id),
                        'tso':self.getTsinceOverhaul(g.id),
                        'at_installation': g.at_install if g.unit not in ['year','month','days'] else '',
                        'component_id': g.part_id.id,
                        'expired': self.countDate(self.fleet_id,g.id) if g.unit not in ['year','month','days'] else g.next_date,
                        'remaining': g.remaining if g.unit not in ['year','month','days'] else str(delta.days) + ' days',
                        'remaining_text': g.remaining_text,
                        'service_life':self.getSliveText(g.id),
                        'due_at':self.getDueatText(g.id),
                        'comment':g.comments,
                        'gi_part_name':g.part_id.product_id.name,
                        'gi_part_number':g.part_id.product_id.default_code,
                        'gi_serial_number':g.part_id.serial_number.name,
                        'remaining_number': g.remaining if g.unit not in ['year','month','days'] else str(delta.days),
                        }))
        subspecomp = sorted(subspecomp, key=lambda k: (k[2]['parents_id'], k[2]['ata']))
        # SORTING DATA
        specomp = sorted(specomp, key=lambda k: (k[2]['ata'] , k[2]['parents_id']))
        final_specomp = specomp + subspecomp
        final_specomp = sorted(final_specomp, key=lambda k: (k[2]['parents_id'] , k[2]['ata']))
        # # CHECK FOR DUPLICATION
        # curr_clear = ''
        # for i in range(len(final_specomp)):
        #     if (final_specomp[i][2]['component_id'] == curr_clear):
        #         final_specomp[i][2]['component_id'] = ''
        #         final_specomp[i][2]['ata'] = ''
        #         final_specomp[i][2]['name'] = ''
        #     else:
        #         curr_clear = final_specomp[i][2]['component_id'] #BELUM FIX

        ro.component_ids = final_specomp
        # ENGINE :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        for engnum in xrange(1,5):
            if(engnum == 1):
                engine = ro.fleet_id.engine_type_id
            elif(engnum == 2):
                engine = ro.fleet_id.engine2_type_id
            elif(engnum == 3):
                engine = ro.fleet_id.engine3_type_id
            elif(engnum == 4):
                engine = ro.fleet_id.engine4_type_id
            if(engine):
                # SEEK FOR CMOMPONENT
                final_specomp = []
                specomp = []
                subspecomp = []
                for g in engine.mapped('component_ids').mapped('serfice_life'):
                    if(g.unit in ['year','month','days']):
                        date_format = "%Y-%m-%d"
                        d0 = datetime.strptime(g.current_date, date_format)
                        d1 = datetime.strptime(g.next_date, date_format)
                        delta = d1 - d0
                    specomp.append((0, 0,{
                        'is_subcomp':False,
                        'parents_id':'X' + str(g.part_id.id).zfill(6) + '.000000',
                        'ref_id' : ro.id,
                        'installed_at':g.installed_at,
                        'ata':g.part_id.ata_code.name,
                        'tsn':self.getTsinceNew(g.id),
                        'tso':self.getTsinceOverhaul(g.id),
                        'at_installation': g.at_install if g.unit not in ['year','month','days'] else '',
                        'component_id': g.part_id.id,
                        'expired': self.countDate(self.fleet_id,g.id) if g.unit not in ['year','month','days'] else g.next_date,
                        'remaining': g.remaining if g.unit not in ['year','month','days'] else str(delta.days) + ' days',
                        'remaining_text': g.remaining_text,
                        'service_life':self.getSliveText(g.id),
                        'due_at':self.getDueatText(g.id),
                        'comment':g.comments,
                        'gi_part_name':g.part_id.product_id.name,
                        'gi_part_number':g.part_id.product_id.default_code,
                        'gi_serial_number':g.part_id.serial_number.name,
                        'remaining_number': g.remaining if g.unit not in ['year','month','days'] else str(delta.days),
                        }))
                specomp = sorted(specomp, key=lambda k: (k[2]['ata'] , k[2]['parents_id']))
                index = 1
                for i in range(len(specomp)):
                    specomp[i][2]['parents_id'] = str(index).zfill(6) + '.000000'
                    index = index + 1
                    # SEEK FOR SUBCOMPONENT
                for g in engine.mapped('component_ids').mapped('sub_part_ids').mapped('serfice_life'):
                    # GET PARENT
                    parents_id = False
                    for i in range(len(specomp)):
                        if (specomp[i][2]['component_id'] == g.part_id.part_id.id):
                            parents_id = specomp[i][2]['parents_id']
                    if(g.unit in ['year','month','days']):
                        date_format = "%Y-%m-%d"
                        d0 = datetime.strptime(g.current_date, date_format)
                        d1 = datetime.strptime(g.next_date, date_format)
                        delta = d1 - d0
                    subspecomp.append((0, 0,{
                        'is_subcomp':True,
                        'parents_id': (str(parents_id)[:6] + '.' + str(g.part_id.id).zfill(6)),
                        'ref_id' : ro.id,
                        'installed_at':g.installed_at,
                        'ata':g.part_id.ata_code.name,
                        'tsn':self.getTsinceNew(g.id),
                        'tso':self.getTsinceOverhaul(g.id),
                        'at_installation': g.at_install if g.unit not in ['year','month','days'] else '',
                        'component_id': g.part_id.id,
                        'expired': self.countDate(self.fleet_id,g.id) if g.unit not in ['year','month','days'] else g.next_date,
                        'remaining': g.remaining if g.unit not in ['year','month','days'] else str(delta.days) + ' days',
                        'remaining_text': g.remaining_text,
                        'service_life':self.getSliveText(g.id),
                        'due_at':self.getDueatText(g.id),
                        'comment':g.comments,
                        'gi_part_name':g.part_id.product_id.name,
                        'gi_part_number':g.part_id.product_id.default_code,
                        'gi_serial_number':g.part_id.serial_number.name,
                        'remaining_number': g.remaining if g.unit not in ['year','month','days'] else str(delta.days),
                        }))
                subspecomp = sorted(subspecomp, key=lambda k: (k[2]['parents_id'], k[2]['ata']))
                # SORTING DATA
                specomp = sorted(specomp, key=lambda k: (k[2]['ata'] , k[2]['parents_id']))
                final_specomp = specomp + subspecomp
                final_specomp = sorted(final_specomp, key=lambda k: (k[2]['parents_id'] , k[2]['ata']))
                # # CHECK FOR DUPLICATION
                # curr_clear = ''
                # for i in range(len(final_specomp)):
                #     if (final_specomp[i][2]['component_id'] == curr_clear):
                #         final_specomp[i][2]['component_id'] = ''
                #         final_specomp[i][2]['ata'] = ''
                #         final_specomp[i][2]['name'] = ''
                #     else:
                #         curr_clear = final_specomp[i][2]['component_id'] #BELUM FIX

                if(engnum == 1):
                    ro.componenteng1_ids = final_specomp
                elif(engnum == 2):
                    ro.componenteng2_ids = final_specomp
                elif(engnum == 3):
                    ro.componenteng3_ids = final_specomp
                elif(engnum == 4):
                    ro.componenteng4_ids = final_specomp
        # AUXILIARY :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        auxiliary = ro.fleet_id.auxiliary_type_id
        # SEEK FOR CMOMPONENT
        final_specomp = []
        specomp = []
        subspecomp = []
        for g in auxiliary.mapped('component_ids').mapped('serfice_life'):
            if(g.unit in ['year','month','days']):
                date_format = "%Y-%m-%d"
                d0 = datetime.strptime(g.current_date, date_format)
                d1 = datetime.strptime(g.next_date, date_format)
                delta = d1 - d0
            specomp.append((0, 0,{
                'is_subcomp':False,
                'parents_id':'X' + str(g.part_id.id).zfill(6) + '.000000',
                'ref_id' : ro.id,
                'installed_at':g.installed_at,
                'ata':g.part_id.ata_code.name,
                'tsn':self.getTsinceNew(g.id),
                'tso':self.getTsinceOverhaul(g.id),
                'at_installation': g.at_install if g.unit not in ['year','month','days'] else '',
                'component_id': g.part_id.id,
                'expired': self.countDate(self.fleet_id,g.id) if g.unit not in ['year','month','days'] else g.next_date,
                'remaining': g.remaining if g.unit not in ['year','month','days'] else str(delta.days) + ' days',
                'remaining_text': g.remaining_text,
                'service_life':self.getSliveText(g.id),
                'due_at':self.getDueatText(g.id),
                'comment':g.comments,
                'gi_part_name':g.part_id.product_id.name,
                'gi_part_number':g.part_id.product_id.default_code,
                'gi_serial_number':g.part_id.serial_number.name,
                'remaining_number': g.remaining if g.unit not in ['year','month','days'] else str(delta.days),
                }))
        specomp = sorted(specomp, key=lambda k: (k[2]['ata'] , k[2]['parents_id']))
        index = 1
        for i in range(len(specomp)):
            specomp[i][2]['parents_id'] = str(index).zfill(6) + '.000000'
            index = index + 1
            # SEEK FOR SUBCOMPONENT
        for g in auxiliary.mapped('component_ids').mapped('sub_part_ids').mapped('serfice_life'):
            # GET PARENT
            parents_id = False
            for i in range(len(specomp)):
                if (specomp[i][2]['component_id'] == g.part_id.part_id.id):
                    parents_id = specomp[i][2]['parents_id']
            if(g.unit in ['year','month','days']):
                date_format = "%Y-%m-%d"
                d0 = datetime.strptime(g.current_date, date_format)
                d1 = datetime.strptime(g.next_date, date_format)
                delta = d1 - d0
            subspecomp.append((0, 0,{
                'is_subcomp':True,
                'parents_id': (str(parents_id)[:6] + '.' + str(g.part_id.id).zfill(6)),
                'ref_id' : ro.id,
                'installed_at':g.installed_at,
                'ata':g.part_id.ata_code.name,
                'tsn':self.getTsinceNew(g.id),
                'tso':self.getTsinceOverhaul(g.id),
                'at_installation': g.at_install if g.unit not in ['year','month','days'] else '',
                'component_id': g.part_id.id,
                'expired': self.countDate(self.fleet_id,g.id) if g.unit not in ['year','month','days'] else g.next_date,
                'remaining': g.remaining if g.unit not in ['year','month','days'] else str(delta.days) + ' days',
                'remaining_text': g.remaining_text,
                'service_life':self.getSliveText(g.id),
                'due_at':self.getDueatText(g.id),
                'comment':g.comments,
                'gi_part_name':g.part_id.product_id.name,
                'gi_part_number':g.part_id.product_id.default_code,
                'gi_serial_number':g.part_id.serial_number.name,
                'remaining_number': g.remaining if g.unit not in ['year','month','days'] else str(delta.days),
                }))
        subspecomp = sorted(subspecomp, key=lambda k: (k[2]['parents_id'], k[2]['ata']))
        # SORTING DATA
        specomp = sorted(specomp, key=lambda k: (k[2]['ata'] , k[2]['parents_id']))
        final_specomp = specomp + subspecomp
        final_specomp = sorted(final_specomp, key=lambda k: (k[2]['parents_id'] , k[2]['ata']))
        # # CHECK FOR DUPLICATION
        # curr_clear = ''
        # for i in range(len(final_specomp)):
        #     if (final_specomp[i][2]['component_id'] == curr_clear):
        #         final_specomp[i][2]['component_id'] = ''
        #         final_specomp[i][2]['ata'] = ''
        #         final_specomp[i][2]['name'] = ''
        #     else:
        #         curr_clear = final_specomp[i][2]['component_id'] #BELUM FIX

        ro.componentaux_ids = final_specomp
        # INSPECTION
        speinsp = []
        for insp in ro.fleet_id.mapped('inspection_ids'):
            for slive in insp.serfice_life:
                if(slive.unit in ['year','month','days']):
                    date_format = "%Y-%m-%d"
                    d0 = datetime.strptime(slive.current_date, date_format)
                    d1 = datetime.strptime(slive.next_date, date_format)
                    delta = d1 - d0
                speinsp.append((0, 0,{
                    'ata_id' : insp.ata_code,
                    'ata' : insp.ata_code.name,
                    'inspection_id' : insp,
                    'item' : insp.item,
                    'based_on' : slive.unit,
                    'service_life' : slive.value,
                    'last_inspection' : slive.current_date,
                    'inspected_at' : '',
                    'since_last' : '',
                    'remaining' : slive.remaining if slive.unit not in ['year','month','days'] else delta.days,
                    'current' : slive.value - slive.remaining,
                    'expired' : self.countDate(self.fleet_id,slive.id) if slive.unit not in ['year','month','days'] else slive.next_date,
                }))
        # for i in range(len(speinsp)):
        #     if (speinsp[i][2]['inspection_id'] == curr_clear):
        #         speinsp[i][2]['item'] = ''
        #         speinsp[i][2]['ata_id'] = ''
        #         speinsp[i][2]['item'] = ''
        #     else:
        #         curr_clear = speinsp[i][2]['inspection_id'] #BELUM FIX
        ro.inspection_ids = speinsp
        # INSPECTION ENGINE
        speinspeng = []
        for engnum in xrange(1,5):
            if(engnum == 1):
                engine = ro.fleet_id.engine_type_id
            elif(engnum == 2):
                engine = ro.fleet_id.engine2_type_id
            elif(engnum == 3):
                engine = ro.fleet_id.engine3_type_id
            elif(engnum == 4):
                engine = ro.fleet_id.engine4_type_id
            if(engine):
                for insp in engine.mapped('inspection_ids'):
                    for slive in insp.serfice_life:
                        if(slive.unit in ['year','month','days']):
                            date_format = "%Y-%m-%d"
                            d0 = datetime.strptime(slive.current_date, date_format)
                            d1 = datetime.strptime(slive.next_date, date_format)
                            delta = d1 - d0
                        speinspeng.append((0, 0,{
                            'ata_id' : insp.ata_code,
                            'ata' : insp.ata_code.name,
                            'inspection_id' : insp,
                            'item' : insp.item,
                            'based_on' : slive.unit,
                            'service_life' : slive.value,
                            'last_inspection' : slive.current_date,
                            'inspected_at' : '',
                            'since_last' : '',
                            'remaining' : slive.remaining if slive.unit not in ['year','month','days'] else delta.days,
                            'current' : slive.value - slive.remaining,
                            'expired' : self.countDate(self.fleet_id,slive.id) if slive.unit not in ['year','month','days'] else slive.next_date,
                        }))
                # for i in range(len(speinspeng)):
                #     if (speinspeng[i][2]['inspection_id'] == curr_clear):
                #         speinspeng[i][2]['item'] = ''
                #         speinspeng[i][2]['ata_id'] = ''
                #         speinspeng[i][2]['item'] = ''
                #     else:
                #         curr_clear = speinspeng[i][2]['inspection_id']


                if(engnum == 1):
                    ro.inspectioneng1_ids = speinspeng
                elif(engnum == 2):
                    ro.inspectioneng2_ids = speinspeng
                elif(engnum == 3):
                    ro.inspectioneng3_ids = speinspeng
                elif(engnum == 4):
                    ro.inspectioneng4_ids = speinspeng

        # INSPECTION AUX
        speinspaux = []
        for insp in ro.fleet_id.auxiliary_type_id.mapped('inspection_ids'):
            for slive in insp.serfice_life:
                if(slive.unit in ['year','month','days']):
                    date_format = "%Y-%m-%d"
                    d0 = datetime.strptime(slive.current_date, date_format)
                    d1 = datetime.strptime(slive.next_date, date_format)
                    delta = d1 - d0
                speinspaux.append((0, 0,{
                    'ata_id' : insp.ata_code,
                    'ata' : insp.ata_code.name,
                    'inspection_id' : insp,
                    'item' : insp.item,
                    'based_on' : slive.unit,
                    'service_life' : slive.value,
                    'last_inspection' : slive.current_date,
                    'inspected_at' : '',
                    'since_last' : '',
                    'remaining' : slive.remaining if slive.unit not in ['year','month','days'] else delta.days,
                    'current' : slive.value - slive.remaining,
                    'expired' : self.countDate(self.fleet_id,slive.id) if slive.unit not in ['year','month','days'] else slive.next_date,
                }))
        # for i in range(len(speinspaux)):
        #     if (speinspaux[i][2]['inspection_id'] == curr_clear):
        #         speinspaux[i][2]['item'] = ''
        #         speinspaux[i][2]['ata_id'] = ''
        #         speinspaux[i][2]['item'] = ''
        #     else:
        #         curr_clear = speinspaux[i][2]['inspection_id']
        ro.inspectionaux_ids = speinspaux

        ro.data_status = True

    @api.model
    def create(self,value):
        partner = self.env.user.partner_id.id
        fleet = self.env['aircraft.acquisition'].search([('id','=',value['fleet_id'])])

        # create Sequence 
        default_seq     = self.env['ir.sequence'].next_by_code('mtr_seq')
        if default_seq: 
            fleet_type = None
            if self.fleet_id.category == "fixedwing":
                fleet_type = "FW"
            else:
                fleet_type = "RW"

            seq     = str(str(default_seq) + "/" + str(fleet.name) +"/"+ fleet_type +"/"+ str(datetime.strftime(datetime.today(), "%y")))

            value['mtr_seq'] = seq

        value['last_flight'] = fleet.last_flight
        value['states'] = 'checked_by'
        value['engine1_id'] = fleet.engine_type_id.id  
        value['engine2_id'] = fleet.engine2_type_id.id
        value['engine3_id'] = fleet.engine3_type_id.id
        value['engine4_id'] = fleet.engine4_type_id.id
        value['create_by'] = partner
        value['daily_hours'] = self.env['ams.daily'].search([('fleet_id','=',value['fleet_id'])], order="start_date desc", limit=1).aircraft_hours
        value['last_flight'] = self.env['ams_fml.log'].search(['&',('date','!=',False),('aircraft_id','=',value['fleet_id'])], order="date desc", limit=1).date
        res = super(AmsMainTracking, self).create(value)
        self.env['ir.cron'].create({
                'name': 'Maintenance Tracking',
                'user_id': self._uid,
                'model': 'ams.mtr',
                'function': 'process_data_part',
                'args': repr([res.id]),
                'doall': True,
               })
        return res

    def getTsinceNew(self,slive_id):
        slive = self.env['ams.component.servicelife'].search([('id','=',slive_id)])
        return slive.since_new_text

    def getTsinceOverhaul(self,slive_id):
        slive = self.env['ams.component.servicelife'].search([('id','=',slive_id)])
        return slive.since_overhaul_text
            

    def getSliveText(self,slive_id):
        slive_name = ''
        slive = self.env['ams.component.servicelife'].search([('id','=',slive_id)])
        slive_name = str(slive.value) 
        slive_name = slive_name.rstrip('0').rstrip('.') if '.' in slive_name else slive_name
        if(slive.unit == 'hours'):
            slive_name = slive_name + ' HR:'
        elif(slive.unit == 'cycles'):
            slive_name = slive_name + ' CY:'
        elif(slive.unit == 'rin'):
            slive_name = slive_name + ' RIN:'
        elif(slive.unit == 'year'):
            slive_name = slive_name + ' YR:'
        elif(slive.unit == 'month'):
            slive_name = slive_name + ' MO:'
        elif(slive.unit == 'days'):
            slive_name = slive_name + ' DY:'

        if(slive.action_type == 'inspection'):
            slive_name = slive_name + 'IN'
        elif(slive.action_type == 'overhaul'):
            slive_name = slive_name + 'OH'
        elif(slive.action_type == 'retirement'):
            slive_name = slive_name + 'RT'
        elif(slive.action_type == 'oncondition'):
            slive_name = 'OC'
        elif(slive.action_type == 'conditionmonitoring'):
            slive_name = slive_name + 'CM'

        return str(slive_name)

    def getDueatText(self,slive_id):
        slive = self.env['ams.component.servicelife'].search([('id','=',slive_id)])
        return slive.next_text


    def countDate(self,fleet_id,slive_id):
        service_life = self.env['ams.component.servicelife'].search([('id','=',slive_id)])
        today = datetime.now()
        Remaining = service_life.remaining
        Target = 0

        part_of = False
        fleet_id = fleet_id
        engine_id = False
        auxiliary_id = False
        propeller_id = False
        comp = service_life.part_id

        if(comp.is_subcomp == True):
            if (comp.part_id.fleet_id != False):
                fleet_id = comp.part_id.fleet_id
                part_of = 'F'
            elif (comp.part_id.engine_id != False):
                engine_id = comp.part_id.engine_id
                part_of = 'E'
            elif (comp.part_id.auxiliary_id != False):
                auxiliary_id = comp.part_id.auxiliary_id
                part_of = 'A'
            elif (comp.part_id.propeller_id != False):
                propeller_id = comp.part_id.propeller_id
                part_of = 'P'
        else:
            if (comp.fleet_id != False):
                fleet_id = comp.fleet_id
                part_of = 'F'
            elif (comp.engine_id != False):
                engine_id = comp.engine_id
                part_of = 'E'
            elif (comp.auxiliary_id != False):
                auxiliary_id = comp.auxiliary_id
                part_of = 'A'
            elif (comp.propeller_id != False):
                propeller_id = comp.propeller_id
                part_of = 'P'


        daily_utilz = self.env['ams.daily'].search([('fleet_id','=',fleet_id.id)], order="create_date asc", limit=1)
        hours = daily_utilz.aircraft_hours
        cycles = daily_utilz.aircraft_cycles

        if(part_of == 'E'):
            if(engine_id == daily_utilz.engine1_id):
                hours = engine1_hours
                cycles = engine1_cycles
            elif(engine_id == daily_utilz.engine2_id):
                hours = engine2_hours
                cycles = engine2_cycles
            elif(engine_id == daily_utilz.engine3_id):
                hours = engine3_hours
                cycles = engine3_cycles
            elif(engine_id == daily_utilz.engine4_id):
                hours = engine4_hours
                cycles = engine4_cycles
        elif(part_of == 'A'):
            if(auxiliary_id == daily_utilz.auxiliary1_id):
                hours = auxiliary1_hours
                cycles = auxiliary1_cycles
            elif(auxiliary_id == daily_utilz.auxiliary2_id):
                hours = auxiliary2_hours
                cycles = auxiliary2_cycles
            elif(auxiliary_id == daily_utilz.auxiliary3_id):
                hours = auxiliary3_hours
                cycles = auxiliary3_cycles
            elif(auxiliary_id == daily_utilz.auxiliary4_id):
                hours = auxiliary4_hours
                cycles = auxiliary4_cycles
        elif(part_of == 'P'):
            if(propeller_id == daily_utilz.propeller1_id):
                hours = propeller1_hours
                cycles = propeller1_cycles
            elif(propeller_id == daily_utilz.propeller2_id):
                hours = propeller2_hours
                cycles = propeller2_cycles
            elif(propeller_id == daily_utilz.propeller3_id):
                hours = propeller3_hours
                cycles = propeller3_cycles
            elif(propeller_id == daily_utilz.propeller4_id):
                hours = propeller4_hours
                cycles = propeller4_cycles

        if service_life.unit not in ['oncondition','conditionmonitoring']:
            if(hours != 0):
                if(Remaining > 0):
                    daysRemaining = math.ceil( (0-Remaining) / hours)
                    dateDue = datetime.strptime(today.strftime("%Y-%m-%d"), '%Y-%m-%d') - timedelta(days=daysRemaining)
                else:
                    daysRemaining = math.ceil(Remaining / hours)
                    dateDue = datetime.strptime(today.strftime("%Y-%m-%d"), '%Y-%m-%d') + timedelta(days=daysRemaining)
                    # dihiting ngikut FML
                if (int(str(dateDue)[:4]) < 1900):
                    dateDue = str(dateDue)[:10]
                else:
                    dateDue = dateDue.strftime("%Y-%m-%d")
                return dateDue
            else:
                return today.strftime("%Y-%m-%d")
        else:
            return today.strftime("%Y-%m-%d")
        

        # for g in self.env['ams.daily'].search([('end_date','>',today.strftime("%Y-%m-%d"))], order="end_date asc"):
        #     if g.start_date > today.strftime("%Y-%m-%d"):
        #         ProjectDays = datetime.strptime(g.end_date, '%Y-%m-%d') - datetime.strptime(g.start_date, '%Y-%m-%d')
        #     else:
        #         ProjectDays = datetime.strptime(g.end_date, '%Y-%m-%d') - datetime.strptime(today.strftime("%Y-%m-%d"), '%Y-%m-%d')
        #     ProjectDays = ProjectDays.days
        #     projectHours = g.aircraft_hours * ProjectDays

        #     if (Remaining - projectHours) <= Target:
        #         daysRemaining = math.ceil(Remaining / g.aircraft_hours)
        #         dateDue = datetime.strptime(today.strftime("%Y-%m-%d"), '%Y-%m-%d') + timedelta(days=daysRemaining)
        #         dateDue = dateDue.strftime("%Y-%m-%d")
        #         return dateDue
        #     else : 
        #         Remaining = Remaining - projectHours
        return False

    @api.multi
    def create_by_(self):
        partner = self.env.user.partner_id.id
        self.create_by = partner
        self.states = 'checked_by'

    @api.multi
    def checked_by_(self):
        partner = self.env.user.partner_id.id
        self.checked_by = partner
        self.states = 'approved_by'

    @api.multi
    def approved_by_(self):
        partner = self.env.user.partner_id.id
        self.approved_by = partner
        # self.date_approved = datetime.now().strftime('%Y-%m-%d')
        self.states = 'qc_by'

    @api.multi
    def qc_by_(self):
        partner = self.env.user.partner_id.id
        self.qc_by = partner
        # self.date_approved = datetime.now().strftime('%Y-%m-%d')
        self.states = ''

class TdrComponent(models.Model):
    _name = 'ams_tdr.component'

    ref_id = fields.Many2one('ams.mtr',string='TDR')
    component_id = fields.Many2one('ams.component.part',string='Component')

    ata_id = fields.Many2one('ams.ata',string='Ata',related='component_id.ata_code')
    ata = fields.Char(string='Ata Text',related='ata_id.name')
    item_pos = fields.Char(string='Item/Pos',related='component_id.item')
    component_name = fields.Char(string='Component Name',related='component_id.product_id.name')
    part = fields.Char(string='Part#',related='component_id.product_id.default_code')
    serial = fields.Many2one('stock.production.lot',string='Serial#',related='component_id.serial_number')

    installed_at = fields.Char(string='Installed/Complied/Completed at')
    tsn = fields.Char(string='Since New')
    tso = fields.Char(string='Since Overhaul')
    
    service_life = fields.Char(string='Service Life')
    at_installation = fields.Char(string='At Installation')
    # service_life = fields.Selection([('IN','IN'),('OV','OV'),('RT','RT'),('OC','OC'),('CM','CM'),('B','B'),('MO','MO'),('DY','DY'),('YR','YR')], string='Service Life', default="OC")
    due_at = fields.Char(string='Due at')
    remaining = fields.Char(string='Remaining')
    remaining_text = fields.Char(string='Remaining')
    expired = fields.Date(string="Expired Date")

    is_subcomp = fields.Boolean(string='Is Sub Component')
    parents_id = fields.Char(string='Parent Id')
    comment = fields.Char(string='Comment')
    gi_part_name = fields.Char(string='gi_part_name')
    gi_part_number = fields.Char(string='gi_part_number')
    gi_serial_number = fields.Char(string='gi_serial_number')
    remaining_number = fields.Float(string='remaining_number')

class TdrComponenteng1(models.Model):
    _name = 'ams_tdr.componenteng1'

    ref_id = fields.Many2one('ams.mtr',string='TDR')
    component_id = fields.Many2one('ams.component.part',string='Component')

    ata_id = fields.Many2one('ams.ata',string='Ata',related='component_id.ata_code')
    ata = fields.Char(string='Ata Text',related='ata_id.name')
    item_pos = fields.Char(string='Item/Pos',related='component_id.item')
    component_name = fields.Char(string='Component Name',related='component_id.product_id.name')
    part = fields.Char(string='Part#',related='component_id.product_id.default_code')
    serial = fields.Many2one('stock.production.lot',string='Serial#',related='component_id.serial_number')

    installed_at = fields.Char(string='Installed/Complied/Completed at')
    tsn = fields.Char(string='Since New')
    tso = fields.Char(string='Since Overhaul')
    
    service_life = fields.Char(string='Service Life')
    at_installation = fields.Char(string='At Installation')
    # service_life = fields.Selection([('IN','IN'),('OV','OV'),('RT','RT'),('OC','OC'),('CM','CM'),('B','B'),('MO','MO'),('DY','DY'),('YR','YR')], string='Service Life', default="OC")
    due_at = fields.Char(string='Due at')
    remaining = fields.Char(string='Remaining')
    remaining_text = fields.Char(string='Remaining')
    expired = fields.Date(string="Expired Date")

    is_subcomp = fields.Boolean(string='Is Sub Component')
    parents_id = fields.Char(string='Parent Id')
    comment = fields.Char(string='Comment')
    gi_part_name = fields.Char(string='gi_part_name')
    gi_part_number = fields.Char(string='gi_part_number')
    gi_serial_number = fields.Char(string='gi_serial_number')
    remaining_number = fields.Float(string='remaining_number')

class TdrComponenteng2(models.Model):
    _name = 'ams_tdr.componenteng2'

    ref_id = fields.Many2one('ams.mtr',string='TDR')
    component_id = fields.Many2one('ams.component.part',string='Component')

    ata_id = fields.Many2one('ams.ata',string='Ata',related='component_id.ata_code')
    ata = fields.Char(string='Ata Text',related='ata_id.name')
    item_pos = fields.Char(string='Item/Pos',related='component_id.item')
    component_name = fields.Char(string='Component Name',related='component_id.product_id.name')
    part = fields.Char(string='Part#',related='component_id.product_id.default_code')
    serial = fields.Many2one('stock.production.lot',string='Serial#',related='component_id.serial_number')

    installed_at = fields.Char(string='Installed/Complied/Completed at')
    tsn = fields.Char(string='Since New')
    tso = fields.Char(string='Since Overhaul')
    
    service_life = fields.Char(string='Service Life')
    at_installation = fields.Char(string='At Installation')
    # service_life = fields.Selection([('IN','IN'),('OV','OV'),('RT','RT'),('OC','OC'),('CM','CM'),('B','B'),('MO','MO'),('DY','DY'),('YR','YR')], string='Service Life', default="OC")
    due_at = fields.Char(string='Due at')
    remaining = fields.Char(string='Remaining')
    remaining_text = fields.Char(string='Remaining')
    expired = fields.Date(string="Expired Date")

    is_subcomp = fields.Boolean(string='Is Sub Component')
    parents_id = fields.Char(string='Parent Id')
    comment = fields.Char(string='Comment')
    gi_part_name = fields.Char(string='gi_part_name')
    gi_part_number = fields.Char(string='gi_part_number')
    gi_serial_number = fields.Char(string='gi_serial_number')
    remaining_number = fields.Float(string='remaining_number')

class TdrComponenteng3(models.Model):
    _name = 'ams_tdr.componenteng3'

    ref_id = fields.Many2one('ams.mtr',string='TDR')
    component_id = fields.Many2one('ams.component.part',string='Component')

    ata_id = fields.Many2one('ams.ata',string='Ata',related='component_id.ata_code')
    ata = fields.Char(string='Ata Text',related='ata_id.name')
    item_pos = fields.Char(string='Item/Pos',related='component_id.item')
    component_name = fields.Char(string='Component Name',related='component_id.product_id.name')
    part = fields.Char(string='Part#',related='component_id.product_id.default_code')
    serial = fields.Many2one('stock.production.lot',string='Serial#',related='component_id.serial_number')

    installed_at = fields.Char(string='Installed/Complied/Completed at')
    tsn = fields.Char(string='Since New')
    tso = fields.Char(string='Since Overhaul')
    
    service_life = fields.Char(string='Service Life')
    at_installation = fields.Char(string='At Installation')
    # service_life = fields.Selection([('IN','IN'),('OV','OV'),('RT','RT'),('OC','OC'),('CM','CM'),('B','B'),('MO','MO'),('DY','DY'),('YR','YR')], string='Service Life', default="OC")
    due_at = fields.Char(string='Due at')
    remaining = fields.Char(string='Remaining')
    remaining_text = fields.Char(string='Remaining')
    expired = fields.Date(string="Expired Date")

    is_subcomp = fields.Boolean(string='Is Sub Component')
    parents_id = fields.Char(string='Parent Id')
    comment = fields.Char(string='Comment')
    gi_part_name = fields.Char(string='gi_part_name')
    gi_part_number = fields.Char(string='gi_part_number')
    gi_serial_number = fields.Char(string='gi_serial_number')
    remaining_number = fields.Float(string='remaining_number')

class TdrComponenteng4(models.Model):
    _name = 'ams_tdr.componenteng4'

    ref_id = fields.Many2one('ams.mtr',string='TDR')
    component_id = fields.Many2one('ams.component.part',string='Component')

    ata_id = fields.Many2one('ams.ata',string='Ata',related='component_id.ata_code')
    ata = fields.Char(string='Ata Text',related='ata_id.name')
    item_pos = fields.Char(string='Item/Pos',related='component_id.item')
    component_name = fields.Char(string='Component Name',related='component_id.product_id.name')
    part = fields.Char(string='Part#',related='component_id.product_id.default_code')
    serial = fields.Many2one('stock.production.lot',string='Serial#',related='component_id.serial_number')

    installed_at = fields.Char(string='Installed/Complied/Completed at')
    tsn = fields.Char(string='Since New')
    tso = fields.Char(string='Since Overhaul')
    
    service_life = fields.Char(string='Service Life')
    at_installation = fields.Char(string='At Installation')
    # service_life = fields.Selection([('IN','IN'),('OV','OV'),('RT','RT'),('OC','OC'),('CM','CM'),('B','B'),('MO','MO'),('DY','DY'),('YR','YR')], string='Service Life', default="OC")
    due_at = fields.Char(string='Due at')
    remaining = fields.Char(string='Remaining')
    remaining_text = fields.Char(string='Remaining')
    expired = fields.Date(string="Expired Date")

    is_subcomp = fields.Boolean(string='Is Sub Component')
    parents_id = fields.Char(string='Parent Id')
    comment = fields.Char(string='Comment')
    gi_part_name = fields.Char(string='gi_part_name')
    gi_part_number = fields.Char(string='gi_part_number')
    gi_serial_number = fields.Char(string='gi_serial_number')
    remaining_number = fields.Float(string='remaining_number')

class TdrComponentaux(models.Model):
    _name = 'ams_tdr.componentaux'

    ref_id = fields.Many2one('ams.mtr',string='TDR')
    component_id = fields.Many2one('ams.component.part',string='Component')

    ata_id = fields.Many2one('ams.ata',string='Ata',related='component_id.ata_code')
    ata = fields.Char(string='Ata Text',related='ata_id.name')
    item_pos = fields.Char(string='Item/Pos',related='component_id.item')
    component_name = fields.Char(string='Component Name',related='component_id.product_id.name')
    part = fields.Char(string='Part#',related='component_id.product_id.default_code')
    serial = fields.Many2one('stock.production.lot',string='Serial#',related='component_id.serial_number')

    installed_at = fields.Char(string='Installed/Complied/Completed at')
    tsn = fields.Char(string='Since New')
    tso = fields.Char(string='Since Overhaul')
    
    service_life = fields.Char(string='Service Life')
    at_installation = fields.Char(string='At Installation')
    # service_life = fields.Selection([('IN','IN'),('OV','OV'),('RT','RT'),('OC','OC'),('CM','CM'),('B','B'),('MO','MO'),('DY','DY'),('YR','YR')], string='Service Life', default="OC")
    due_at = fields.Char(string='Due at')
    remaining = fields.Char(string='Remaining')
    remaining_text = fields.Char(string='Remaining')
    expired = fields.Date(string="Expired Date")

    is_subcomp = fields.Boolean(string='Is Sub Component')
    parents_id = fields.Char(string='Parent Id')
    comment = fields.Char(string='Comment')
    gi_part_name = fields.Char(string='gi_part_name')
    gi_part_number = fields.Char(string='gi_part_number')
    gi_serial_number = fields.Char(string='gi_serial_number')
    remaining_number = fields.Float(string='remaining_number')


class TdrInspection(models.Model):
    _name = 'ams_tdr.inspection'
    
    ref_id = fields.Many2one('ams.mtr',string='TDR')
    ata_id = fields.Many2one('ams.ata',string='Ata')
    ata = fields.Char(string='Ata Text',related='ata_id.name')
    inspection_id = fields.Many2one('ams.inspection',string='Inspection')
    item = fields.Char(string='Item')
    based_on = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Based On', default="hours")
    service_life = fields.Float(string='Serfice Life')
    last_inspection = fields.Date(string='Last inspection Date')
    inspected_at = fields.Float(string='Last Inspection Hours')
    since_last = fields.Float(string='Since Last Inspection')
    remaining = fields.Char(string='Remaining')
    remaining_text = fields.Char(string='Remaining')
    current = fields.Float(string='Period to Next Insp')
    expired = fields.Date(string='Projected Date')
    gi_part_name = fields.Char(string='gi_part_name')
    gi_part_number = fields.Char(string='gi_part_number')
    gi_serial_number = fields.Char(string='gi_serial_number')
    remaining_number = fields.Float(string='remaining_number')

class TdrInspectionEng1(models.Model):
    _name = 'ams_tdr.inspectioneng1'
    
    ref_id = fields.Many2one('ams.mtr',string='TDR')
    ata_id = fields.Many2one('ams.ata',string='Ata')
    ata = fields.Char(string='Ata Text',related='ata_id.name')
    inspection_id = fields.Many2one('ams.inspection',string='Inspection')
    item = fields.Char(string='Item')
    based_on = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Based On', default="hours")
    service_life = fields.Float(string='Serfice Life')
    last_inspection = fields.Date(string='Last inspection Date')
    inspected_at = fields.Float(string='Last Inspection Hours')
    since_last = fields.Float(string='Since Last Inspection')
    remaining = fields.Char(string='Remaining')
    remaining_text = fields.Char(string='Remaining')
    current = fields.Float(string='Period to Next Insp')
    expired = fields.Date(string='Projected Date')
    gi_part_name = fields.Char(string='gi_part_name')
    gi_part_number = fields.Char(string='gi_part_number')
    gi_serial_number = fields.Char(string='gi_serial_number')
    remaining_number = fields.Float(string='remaining_number')

class TdrInspectionEng2(models.Model):
    _name = 'ams_tdr.inspectioneng2'
    
    ref_id = fields.Many2one('ams.mtr',string='TDR')
    ata_id = fields.Many2one('ams.ata',string='Ata')
    ata = fields.Char(string='Ata Text',related='ata_id.name')
    inspection_id = fields.Many2one('ams.inspection',string='Inspection')
    item = fields.Char(string='Item')
    based_on = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Based On', default="hours")
    service_life = fields.Float(string='Serfice Life')
    last_inspection = fields.Date(string='Last inspection Date')
    inspected_at = fields.Float(string='Last Inspection Hours')
    since_last = fields.Float(string='Since Last Inspection')
    remaining = fields.Char(string='Remaining')
    remaining_text = fields.Char(string='Remaining')
    current = fields.Float(string='Period to Next Insp')
    expired = fields.Date(string='Projected Date')
    gi_part_name = fields.Char(string='gi_part_name')
    gi_part_number = fields.Char(string='gi_part_number')
    gi_serial_number = fields.Char(string='gi_serial_number')
    remaining_number = fields.Float(string='remaining_number')

class TdrInspectionEng3(models.Model):
    _name = 'ams_tdr.inspectioneng3'
    
    ref_id = fields.Many2one('ams.mtr',string='TDR')
    ata_id = fields.Many2one('ams.ata',string='Ata')
    ata = fields.Char(string='Ata Text',related='ata_id.name')
    inspection_id = fields.Many2one('ams.inspection',string='Inspection')
    item = fields.Char(string='Item')
    based_on = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Based On', default="hours")
    service_life = fields.Float(string='Serfice Life')
    last_inspection = fields.Date(string='Last inspection Date')
    inspected_at = fields.Float(string='Last Inspection Hours')
    since_last = fields.Float(string='Since Last Inspection')
    remaining = fields.Char(string='Remaining')
    remaining_text = fields.Char(string='Remaining')
    current = fields.Float(string='Period to Next Insp')
    expired = fields.Date(string='Projected Date')
    gi_part_name = fields.Char(string='gi_part_name')
    gi_part_number = fields.Char(string='gi_part_number')
    gi_serial_number = fields.Char(string='gi_serial_number')
    remaining_number = fields.Float(string='remaining_number')

class TdrInspectionEng4(models.Model):
    _name = 'ams_tdr.inspectioneng4'
    
    ref_id = fields.Many2one('ams.mtr',string='TDR')
    ata_id = fields.Many2one('ams.ata',string='Ata')
    ata = fields.Char(string='Ata Text',related='ata_id.name')
    inspection_id = fields.Many2one('ams.inspection',string='Inspection')
    item = fields.Char(string='Item')
    based_on = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Based On', default="hours")
    service_life = fields.Float(string='Serfice Life')
    last_inspection = fields.Date(string='Last inspection Date')
    inspected_at = fields.Float(string='Last Inspection Hours')
    since_last = fields.Float(string='Since Last Inspection')
    remaining = fields.Char(string='Remaining')
    remaining_text = fields.Char(string='Remaining')
    current = fields.Float(string='Period to Next Insp')
    expired = fields.Date(string='Projected Date')
    gi_part_name = fields.Char(string='gi_part_name')
    gi_part_number = fields.Char(string='gi_part_number')
    gi_serial_number = fields.Char(string='gi_serial_number')
    remaining_number = fields.Float(string='remaining_number')

class TdrInspectionAux(models.Model):
    _name = 'ams_tdr.inspectionaux'
    
    ref_id = fields.Many2one('ams.mtr',string='TDR')
    ata_id = fields.Many2one('ams.ata',string='Ata')
    ata = fields.Char(string='Ata Text',related='ata_id.name')
    inspection_id = fields.Many2one('ams.inspection',string='Inspection')
    item = fields.Char(string='Item')
    based_on = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Based On', default="hours")
    service_life = fields.Float(string='Serfice Life')
    last_inspection = fields.Date(string='Last inspection Date')
    inspected_at = fields.Float(string='Last Inspection Hours')
    since_last = fields.Float(string='Since Last Inspection')
    remaining = fields.Char(string='Remaining')
    remaining_text = fields.Char(string='Remaining')
    current = fields.Float(string='Period to Next Insp')
    expired = fields.Date(string='Projected Date')
    gi_part_name = fields.Char(string='gi_part_name')
    gi_part_number = fields.Char(string='gi_part_number')
    gi_serial_number = fields.Char(string='gi_serial_number')
    remaining_number = fields.Float(string='remaining_number')


class MTRXlsx(ReportXlsx):
    def get_mtr(self, data):
        if data['form']['id']:
            mtr = self.env['ams_tdr.mtr'].search([('id','=',data['form']['id'])])
            return mtr

    def generate_xlsx_report(self, workbook, data, lines):
        mtr = self.get_mtr(data)
        format1 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'vcenter', 'bold': True})
        format11 = workbook.add_format({'font_size': 12, 'align': 'center', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True})
        format21 = workbook.add_format({'font_size': 10, 'align': 'center', 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': True})
        format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 12})
        format2 = workbook.add_format({'bottom': True, 'top': False, 'font_size': 12})
        font_size_8 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8})
        red_mark = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8,
                                        'bg_color': 'red'})
        justify = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 12})
        format3.set_align('center')
        format2.set_align('center')
        font_size_8.set_align('center')
        justify.set_align('justify')
        format1.set_align('center')
        red_mark.set_align('center')
        col = 0
        col1 = 5
        sheet = workbook.add_worksheet('Maintenance Tracking Report')

        sheet.merge_range('A1:M1', 'Maintenance Tracking Report', format1)
        sheet.merge_range('A2:C2', 'Aircraft Tail Number :', format21)
        if mtr.fleet_id.name:
            sheet.write(1, 3, mtr.fleet_id.name, format21)
        sheet.merge_range('J2:L2', 'Description :', format21)
        if mtr.fleet_id.aircraft_type_id.name:
            sheet.write(1, 12, mtr.fleet_id.aircraft_type_id.name, format21)
        sheet.merge_range('A3:C3', 'Manufacture Date :', format21)
        sheet.write(2, 3, mtr.fleet_id.date_manufacture, format21)
        sheet.write(2, 4, 'Model No. :', format21)
        if mtr.fleet_id.aircraft_name.name:
            sheet.write(2, 5, mtr.fleet_id.aircraft_name.name, format21)
        sheet.write(2, 6, 'Serial No. :', format21)
        sheet.write(2, 7, mtr.fleet_id.vin_sn, format21)
        sheet.write(2, 8, 'Last Flight :', format21)
        sheet.write(2, 9, mtr.last_flight, format21)

        sheet.write(3, 0, 'Hours :', format21)
        sheet.write(3, 1, mtr.ac_hours, format21)
        sheet.write(3, 2, 'Cycles :', format21)
        sheet.write(3, 3, mtr.ac_cycles, format21)
        
        sheet.merge_range('A5:M5', 'Projected Date Based on Average Daily Utilization: ' + str(mtr.daily_hours) + ' A/C Hrs', format21)
        sheet.merge_range('A6:E6', 'This Report is Ordered By : ATA Code', format21)

        sheet.write(6, 0, 'ATA/Item', font_size_8)
        sheet.write(6, 1, 'Item/POS', font_size_8)
        sheet.write(6, 2, 'Component Name', font_size_8)
        sheet.write(6, 3, 'Part#', font_size_8)
        sheet.write(6, 4, 'Serial#', font_size_8)
        sheet.write(6, 5, 'Service Life', font_size_8)
        sheet.write(6, 6, 'Installed/Complied/Completed At', font_size_8)
        sheet.write(6, 7, 'Due At', font_size_8)
        sheet.write(6, 8, 'Since New', font_size_8)
        sheet.write(6, 9, 'Since Overhoul', font_size_8)
        sheet.write(6, 10, 'At Installation', font_size_8)
        sheet.write(6, 11, 'Remaining', font_size_8)
        sheet.write(6, 12, 'Project Date', font_size_8)

        no = 7
        for x in mtr.component_ids:
            if x.ata_id.name:
                sheet.write(no, 0, x.ata_id.name, font_size_8)
            sheet.write(no, 1, x.item_pos, font_size_8)
            sheet.write(no, 2, x.component_name, font_size_8)
            sheet.write(no, 3, x.part, font_size_8)
            if x.serial.name:
                sheet.write(no, 4, x.serial.name, font_size_8)
            sheet.write(no, 5, x.service_life, font_size_8)
            sheet.write(no, 6, x.installed_at, font_size_8)
            sheet.write(no, 7, x.due_at, font_size_8)
            sheet.write(no, 8, x.tsn, font_size_8)
            sheet.write(no, 9, x.tso, font_size_8)
            sheet.write(no, 10, x.at_installation, font_size_8)
            sheet.write(no, 11, x.remaining, font_size_8)
            sheet.write(no, 12, x.expired, font_size_8)
            if x.comment:
                no += 1
                sheet.write(no, 0, 'Comments : '+ str(x.comment), font_size_8)
            no += 1

            
        if mtr.componenteng1_ids:
            sheet1 = workbook.add_worksheet('Engine1')

            sheet1.merge_range('A1:M1', 'Maintenance Tracking Report', format1)
            sheet1.merge_range('A2:C2', 'Aircraft Tail Number :', format21)
            if mtr.fleet_id.name:
                sheet1.write(1, 3, mtr.fleet_id.name, format21)
            sheet1.merge_range('J2:L2', 'Description :', format21)
            if mtr.fleet_id.aircraft_type_id.name:
                sheet1.write(1, 12, mtr.fleet_id.aircraft_type_id.name, format21)
            sheet1.merge_range('A3:C3', 'Manufacture Date :', format21)
            sheet1.write(2, 3, mtr.fleet_id.date_manufacture, format21)
            sheet1.write(2, 4, 'Model No. :', format21)
            if mtr.fleet_id.aircraft_name.name:
                sheet1.write(2, 5, mtr.fleet_id.aircraft_name.name, format21)
            sheet1.write(2, 6, 'Serial No. :', format21)
            sheet1.write(2, 7, mtr.fleet_id.vin_sn, format21)
            sheet1.write(2, 8, 'Last Flight :', format21)
            sheet1.write(2, 9, mtr.last_flight, format21)

            sheet1.write(3, 0, 'Hours :', format21)
            sheet1.write(3, 1, mtr.ac_hours, format21)
            sheet1.write(3, 2, 'Cycles :', format21)
            sheet1.write(3, 3, mtr.ac_cycles, format21)
            
            sheet1.merge_range('A5:M5', 'Projected Date Based on Average Daily Utilization: ' + str(mtr.daily_hours) + ' A/C Hrs', format21)
            sheet1.merge_range('A6:E6', 'This Report is Ordered By : ATA Code', format21)

            sheet1.write(6, 0, 'ATA/Item', font_size_8)
            sheet1.write(6, 1, 'Item/POS', font_size_8)
            sheet1.write(6, 2, 'Component Name', font_size_8)
            sheet1.write(6, 3, 'Part#', font_size_8)
            sheet1.write(6, 4, 'Serial#', font_size_8)
            sheet1.write(6, 5, 'Service Life', font_size_8)
            sheet1.write(6, 6, 'Installed/Complied/Completed At', font_size_8)
            sheet1.write(6, 7, 'Due At', font_size_8)
            sheet1.write(6, 8, 'Since New', font_size_8)
            sheet1.write(6, 9, 'Since Overhoul', font_size_8)
            sheet1.write(6, 10, 'At Installation', font_size_8)
            sheet1.write(6, 11, 'Remaining', font_size_8)
            sheet1.write(6, 12, 'Project Date', font_size_8)

            no1 = 7
            for x in mtr.componenteng1_ids:
                if x.ata_id.name:
                    sheet1.write(no1, 0, x.ata_id.name, font_size_8)
                sheet1.write(no1, 1, x.item_pos, font_size_8)
                sheet1.write(no1, 2, x.component_name, font_size_8)
                sheet1.write(no1, 3, x.part, font_size_8)
                if x.serial.name:
                    sheet1.write(no1, 4, x.serial.name, font_size_8)
                sheet1.write(no1, 5, x.service_life, font_size_8)
                sheet1.write(no1, 6, x.installed_at, font_size_8)
                sheet1.write(no1, 7, x.due_at, font_size_8)
                sheet1.write(no1, 8, x.tsn, font_size_8)
                sheet1.write(no1, 9, x.tso, font_size_8)
                sheet1.write(no1, 10, x.at_installation, font_size_8)
                sheet1.write(no1, 11, x.remaining, font_size_8)
                sheet1.write(no1, 12, x.expired, font_size_8)  
                if x.comment:
                    no1 += 1
                    sheet1.write(no1, 0, 'Comments : '+ str(x.comment), font_size_8)
                no1 += 1

        if mtr.componenteng2_ids:
            sheet2 = workbook.add_worksheet('Engine2')

            sheet2.merge_range('A1:M1', 'Maintenance Tracking Report', format1)
            sheet2.merge_range('A2:C2', 'Aircraft Tail Number :', format21)
            if mtr.fleet_id.name:
                sheet2.write(1, 3, mtr.fleet_id.name, format21)
            sheet2.merge_range('J2:L2', 'Description :', format21)
            if mtr.fleet_id.aircraft_type_id.name:
                sheet2.write(1, 12, mtr.fleet_id.aircraft_type_id.name, format21)
            sheet2.merge_range('A3:C3', 'Manufacture Date :', format21)
            sheet2.write(2, 3, mtr.fleet_id.date_manufacture, format21)
            sheet2.write(2, 4, 'Model No. :', format21)
            if mtr.fleet_id.aircraft_name.name:
                sheet2.write(2, 5, mtr.fleet_id.aircraft_name.name, format21)
            sheet2.write(2, 6, 'Serial No. :', format21)
            sheet2.write(2, 7, mtr.fleet_id.vin_sn, format21)
            sheet2.write(2, 8, 'Last Flight :', format21)
            sheet2.write(2, 9, mtr.last_flight, format21)

            sheet2.write(3, 0, 'Hours :', format21)
            sheet2.write(3, 1, mtr.ac_hours, format21)
            sheet2.write(3, 2, 'Cycles :', format21)
            sheet2.write(3, 3, mtr.ac_cycles, format21)
            
            sheet2.merge_range('A5:M5', 'Projected Date Based on Average Daily Utilization: ' + str(mtr.daily_hours) + ' A/C Hrs', format21)
            sheet2.merge_range('A6:E6', 'This Report is Ordered By : ATA Code', format21)

            sheet2.write(6, 0, 'ATA/Item', font_size_8)
            sheet2.write(6, 1, 'Item/POS', font_size_8)
            sheet2.write(6, 2, 'Component Name', font_size_8)
            sheet2.write(6, 3, 'Part#', font_size_8)
            sheet2.write(6, 4, 'Serial#', font_size_8)
            sheet2.write(6, 5, 'Service Life', font_size_8)
            sheet2.write(6, 6, 'Installed/Complied/Completed At', font_size_8)
            sheet2.write(6, 7, 'Due At', font_size_8)
            sheet2.write(6, 8, 'Since New', font_size_8)
            sheet2.write(6, 9, 'Since Overhoul', font_size_8)
            sheet2.write(6, 10, 'At Installation', font_size_8)
            sheet2.write(6, 11, 'Remaining', font_size_8)
            sheet2.write(6, 12, 'Project Date', font_size_8)

            no2 = 7
            for x in mtr.componenteng2_ids:
                if x.ata_id.name:
                    sheet2.write(no2, 0, x.ata_id.name, font_size_8)
                sheet2.write(no2, 1, x.item_pos, font_size_8)
                sheet2.write(no2, 2, x.component_name, font_size_8)
                sheet2.write(no2, 3, x.part, font_size_8)
                if x.serial.name:
                    sheet2.write(no2, 4, x.serial.name, font_size_8)
                sheet2.write(no2, 5, x.service_life, font_size_8)
                sheet2.write(no2, 6, x.installed_at, font_size_8)
                sheet2.write(no2, 7, x.due_at, font_size_8)
                sheet2.write(no2, 8, x.tsn, font_size_8)
                sheet2.write(no2, 9, x.tso, font_size_8)
                sheet2.write(no2, 10, x.at_installation, font_size_8)
                sheet2.write(no2, 11, x.remaining, font_size_8)
                sheet2.write(no2, 12, x.expired, font_size_8)
                if x.comment:
                    no2 += 1
                    sheet2.write(no2, 0, 'Comments : '+ str(x.comment), font_size_8)
                no2 += 1

        if mtr.componenteng3_ids:
            sheet3 = workbook.add_worksheet('Engine3')

            sheet3.merge_range('A1:M1', 'Maintenance Tracking Report', format1)
            sheet3.merge_range('A2:C2', 'Aircraft Tail Number :', format21)
            if mtr.fleet_id.name:
                sheet3.write(1, 3, mtr.fleet_id.name, format21)
            sheet3.merge_range('J2:L2', 'Description :', format21)
            if mtr.fleet_id.aircraft_type_id.name:
                sheet3.write(1, 12, mtr.fleet_id.aircraft_type_id.name, format21)
            sheet3.merge_range('A3:C3', 'Manufacture Date :', format21)
            sheet3.write(2, 3, mtr.fleet_id.date_manufacture, format21)
            sheet3.write(2, 4, 'Model No. :', format21)
            if mtr.fleet_id.aircraft_name.name:
                sheet3.write(2, 5, mtr.fleet_id.aircraft_name.name, format21)
            sheet3.write(2, 6, 'Serial No. :', format21)
            sheet3.write(2, 7, mtr.fleet_id.vin_sn, format21)
            sheet3.write(2, 8, 'Last Flight :', format21)
            sheet3.write(2, 9, mtr.last_flight, format21)

            sheet3.write(3, 0, 'Hours :', format21)
            sheet3.write(3, 1, mtr.ac_hours, format21)
            sheet3.write(3, 2, 'Cycles :', format21)
            sheet3.write(3, 3, mtr.ac_cycles, format21)
            
            sheet3.merge_range('A5:M5', 'Projected Date Based on Average Daily Utilization: ' + str(mtr.daily_hours) + ' A/C Hrs', format21)
            sheet3.merge_range('A6:E6', 'This Report is Ordered By : ATA Code', format21)

            sheet3.write(6, 0, 'ATA/Item', font_size_8)
            sheet3.write(6, 1, 'Item/POS', font_size_8)
            sheet3.write(6, 2, 'Component Name', font_size_8)
            sheet3.write(6, 3, 'Part#', font_size_8)
            sheet3.write(6, 4, 'Serial#', font_size_8)
            sheet3.write(6, 5, 'Service Life', font_size_8)
            sheet3.write(6, 6, 'Installed/Complied/Completed At', font_size_8)
            sheet3.write(6, 7, 'Due At', font_size_8)
            sheet3.write(6, 8, 'Since New', font_size_8)
            sheet3.write(6, 9, 'Since Overhoul', font_size_8)
            sheet3.write(6, 10, 'At Installation', font_size_8)
            sheet3.write(6, 11, 'Remaining', font_size_8)
            sheet3.write(6, 12, 'Project Date', font_size_8)

            no3 = 7
            for x in mtr.componenteng3_ids:
                if x.ata_id.name:
                    sheet3.write(no3, 0, x.ata_id.name, font_size_8)
                sheet3.write(no3, 1, x.item_pos, font_size_8)
                sheet3.write(no3, 2, x.component_name, font_size_8)
                sheet3.write(no3, 3, x.part, font_size_8)
                if x.serial.name:
                    sheet3.write(no3, 4, x.serial.name, font_size_8)
                sheet3.write(no3, 5, x.service_life, font_size_8)
                sheet3.write(no3, 6, x.installed_at, font_size_8)
                sheet3.write(no3, 7, x.due_at, font_size_8)
                sheet3.write(no3, 8, x.tsn, font_size_8)
                sheet3.write(no3, 9, x.tso, font_size_8)
                sheet3.write(no3, 10, x.at_installation, font_size_8)
                sheet3.write(no3, 11, x.remaining, font_size_8)
                sheet3.write(no3, 12, x.expired, font_size_8)
                if x.comment:
                    no3 += 1
                    sheet3.write(no3, 0, 'Comments : '+ str(x.comment), font_size_8)   
                no3 += 1


        if mtr.componenteng4_ids:
            sheet4 = workbook.add_worksheet('Engine4')

            sheet4.merge_range('A1:M1', 'Maintenance Tracking Report', format1)
            sheet4.merge_range('A2:C2', 'Aircraft Tail Number :', format21)
            if mtr.fleet_id.name:
                sheet4.write(1, 3, mtr.fleet_id.name, format21)
            sheet4.merge_range('J2:L2', 'Description :', format21)
            if mtr.fleet_id.aircraft_type_id.name:
                sheet4.write(1, 12, mtr.fleet_id.aircraft_type_id.name, format21)
            sheet4.merge_range('A3:C3', 'Manufacture Date :', format21)
            sheet4.write(2, 3, mtr.fleet_id.date_manufacture, format21)
            sheet4.write(2, 4, 'Model No. :', format21)
            if mtr.fleet_id.aircraft_name.name:
                sheet4.write(2, 5, mtr.fleet_id.aircraft_name.name, format21)
            sheet4.write(2, 6, 'Serial No. :', format21)
            sheet4.write(2, 7, mtr.fleet_id.vin_sn, format21)
            sheet4.write(2, 8, 'Last Flight :', format21)
            sheet4.write(2, 9, mtr.last_flight, format21)

            sheet4.write(3, 0, 'Hours :', format21)
            sheet4.write(3, 1, mtr.ac_hours, format21)
            sheet4.write(3, 2, 'Cycles :', format21)
            sheet4.write(3, 3, mtr.ac_cycles, format21)
            
            sheet4.merge_range('A5:M5', 'Projected Date Based on Average Daily Utilization: ' + str(mtr.daily_hours) + ' A/C Hrs', format21)
            sheet4.merge_range('A6:E6', 'This Report is Ordered By : ATA Code', format21)

            sheet4.write(6, 0, 'ATA/Item', font_size_8)
            sheet4.write(6, 1, 'Item/POS', font_size_8)
            sheet4.write(6, 2, 'Component Name', font_size_8)
            sheet4.write(6, 3, 'Part#', font_size_8)
            sheet4.write(6, 4, 'Serial#', font_size_8)
            sheet4.write(6, 5, 'Service Life', font_size_8)
            sheet4.write(6, 6, 'Installed/Complied/Completed At', font_size_8)
            sheet4.write(6, 7, 'Due At', font_size_8)
            sheet4.write(6, 8, 'Since New', font_size_8)
            sheet4.write(6, 9, 'Since Overhoul', font_size_8)
            sheet4.write(6, 10, 'At Installation', font_size_8)
            sheet4.write(6, 11, 'Remaining', font_size_8)
            sheet4.write(6, 12, 'Project Date', font_size_8)

            no4 = 7
            for x in mtr.componenteng4_ids:
                if x.ata_id.name:
                    sheet4.write(no4, 0, x.ata_id.name, font_size_8)
                sheet4.write(no4, 1, x.item_pos, font_size_8)
                sheet4.write(no4, 2, x.component_name, font_size_8)
                sheet4.write(no4, 3, x.part, font_size_8)
                if x.serial.name:
                    sheet4.write(no4, 4, x.serial.name, font_size_8)
                sheet4.write(no4, 5, x.service_life, font_size_8)
                sheet4.write(no4, 6, x.installed_at, font_size_8)
                sheet4.write(no4, 7, x.due_at, font_size_8)
                sheet4.write(no4, 8, x.tsn, font_size_8)
                sheet4.write(no4, 9, x.tso, font_size_8)
                sheet4.write(no4, 10, x.at_installation, font_size_8)
                sheet4.write(no4, 11, x.remaining, font_size_8)
                sheet4.write(no4, 12, x.expired, font_size_8)
                if x.comment:
                    no4 += 1
                    sheet4.write(no4, 0, 'Comments : '+ str(x.comment), font_size_8) 
                no4 += 1


        if mtr.componentaux_ids:
            sheet5 = workbook.add_worksheet('Auxiliary')

            sheet5.merge_range('A1:M1', 'Maintenance Tracking Report', format1)
            sheet5.merge_range('A2:C2', 'Aircraft Tail Number :', format21)
            if mtr.fleet_id.name:
                sheet5.write(1, 3, mtr.fleet_id.name, format21)
            sheet5.merge_range('J2:L2', 'Description :', format21)
            if mtr.fleet_id.aircraft_type_id.name:
                sheet5.write(1, 12, mtr.fleet_id.aircraft_type_id.name, format21)
            sheet5.merge_range('A3:C3', 'Manufacture Date :', format21)
            sheet5.write(2, 3, mtr.fleet_id.date_manufacture, format21)
            sheet5.write(2, 4, 'Model No. :', format21)
            if mtr.fleet_id.aircraft_name.name:
                sheet5.write(2, 5, mtr.fleet_id.aircraft_name.name, format21)
            sheet5.write(2, 6, 'Serial No. :', format21)
            sheet5.write(2, 7, mtr.fleet_id.vin_sn, format21)
            sheet5.write(2, 8, 'Last Flight :', format21)
            sheet5.write(2, 9, mtr.last_flight, format21)

            sheet5.write(3, 0, 'Hours :', format21)
            sheet5.write(3, 1, mtr.ac_hours, format21)
            sheet5.write(3, 2, 'Cycles :', format21)
            sheet5.write(3, 3, mtr.ac_cycles, format21)
            
            sheet5.merge_range('A5:M5', 'Projected Date Based on Average Daily Utilization: ' + str(mtr.daily_hours) + ' A/C Hrs', format21)
            sheet5.merge_range('A6:E6', 'This Report is Ordered By : ATA Code', format21)

            sheet5.write(6, 0, 'ATA/Item', font_size_8)
            sheet5.write(6, 1, 'Item/POS', font_size_8)
            sheet5.write(6, 2, 'Component Name', font_size_8)
            sheet5.write(6, 3, 'Part#', font_size_8)
            sheet5.write(6, 4, 'Serial#', font_size_8)
            sheet5.write(6, 5, 'Service Life', font_size_8)
            sheet5.write(6, 6, 'Installed/Complied/Completed At', font_size_8)
            sheet5.write(6, 7, 'Due At', font_size_8)
            sheet5.write(6, 8, 'Since New', font_size_8)
            sheet5.write(6, 9, 'Since Overhoul', font_size_8)
            sheet5.write(6, 10, 'At Installation', font_size_8)
            sheet5.write(6, 11, 'Remaining', font_size_8)
            sheet5.write(6, 12, 'Project Date', font_size_8)

            no5 = 7
            for x in mtr.componentaux_ids:
                if x.ata_id.name:
                    sheet5.write(no5, 0, x.ata_id.name, font_size_8)
                sheet5.write(no5, 1, x.item_pos, font_size_8)
                sheet5.write(no5, 2, x.component_name, font_size_8)
                sheet5.write(no5, 3, x.part, font_size_8)
                if x.serial.name:
                    sheet5.write(no5, 4, x.serial.name, font_size_8)
                sheet5.write(no5, 5, x.service_life, font_size_8)
                sheet5.write(no5, 6, x.installed_at, font_size_8)
                sheet5.write(no5, 7, x.due_at, font_size_8)
                sheet5.write(no5, 8, x.tsn, font_size_8)
                sheet5.write(no5, 9, x.tso, font_size_8)
                sheet5.write(no5, 10, x.at_installation, font_size_8)
                sheet5.write(no5, 11, x.remaining, font_size_8)
                sheet5.write(no5, 12, x.expired, font_size_8)
                if x.comment:
                    no5 += 1
                    sheet5.write(no5, 0, 'Comments : '+ str(x.comment), font_size_8) 
                no5 += 1


        if mtr.inspection_ids:
            sheet6 = workbook.add_worksheet('Inspection')

            sheet6.merge_range('A1:M1', 'Airframe Inspection Report', format1)
            sheet6.merge_range('A2:C2', 'Aircraft Tail Number :', format21)
            if mtr.fleet_id.name:
                sheet6.write(1, 3, mtr.fleet_id.name, format21)
            sheet6.merge_range('J2:L2', 'Description :', format21)
            if mtr.fleet_id.aircraft_type_id.name:
                sheet6.write(1, 12, mtr.fleet_id.aircraft_type_id.name, format21)
            sheet6.merge_range('A3:C3', 'Manufacture Date :', format21)
            sheet6.write(2, 3, mtr.fleet_id.date_manufacture, format21)
            sheet6.write(2, 4, 'Model No. :', format21)
            if mtr.fleet_id.aircraft_name.name:
                sheet6.write(2, 5, mtr.fleet_id.aircraft_name.name, format21)
            sheet6.write(2, 6, 'Serial No. :', format21)
            sheet6.write(2, 7, mtr.fleet_id.vin_sn, format21)
            sheet6.write(2, 8, 'Last Flight :', format21)
            sheet6.write(2, 9, mtr.last_flight, format21)

            sheet6.write(3, 0, 'Hours :', format21)
            sheet6.write(3, 1, mtr.ac_hours, format21)
            sheet6.write(3, 2, 'Cycles :', format21)
            sheet6.write(3, 3, mtr.ac_cycles, format21)
            
            sheet6.merge_range('A5:M5', 'Projected Date Based on Average Daily Utilization: ' + str(mtr.daily_hours) + ' A/C Hrs', format21)
            sheet6.merge_range('A6:E6', 'This Report is Ordered By : ATA Code', format21)

            sheet6.write(6, 0, 'ATA code Inspection', font_size_8)
            sheet6.write(6, 1, 'Item', font_size_8)
            sheet6.write(6, 2, 'W/O#', font_size_8)
            sheet6.write(6, 3, 'Based On', font_size_8)
            sheet6.write(6, 4, 'Service Life', font_size_8)
            sheet6.write(6, 5, 'Last - Inspection - Date', font_size_8)
            sheet6.write(6, 6, 'Last - Inspection - Time', font_size_8)
            sheet6.write(6, 7, 'Since - Last - Time', font_size_8)
            sheet6.write(6, 8, 'Due At', font_size_8)
            sheet6.write(6, 9, 'Period To - Next Insp', font_size_8)
            sheet6.write(6, 10, 'Projected - Date', font_size_8)

            no6 = 7
            for x in mtr.inspection_ids:
                if x.ata_id.name:
                    sheet6.write(no6, 0, x.ata_id.name, font_size_8)
                sheet6.write(no6, 1, x.item, font_size_8)
                # sheet6.write(no6, 2, x.component_name, font_size_8)
                sheet6.write(no6, 3, x.based_on, font_size_8)
                sheet6.write(no6, 4, x.service_life, font_size_8)
                sheet6.write(no6, 5, x.last_inspection, font_size_8)
                sheet6.write(no6, 6, x.inspected_at, font_size_8)
                sheet6.write(no6, 7, x.since_last, font_size_8)
                sheet6.write(no6, 8, x.remaining, font_size_8)
                sheet6.write(no6, 9, x.current, font_size_8)
                sheet6.write(no6, 10, x.expired, font_size_8)
                no6 += 1




MTRXlsx('report.ams_tdr.maintenance_tracking_report.xlsx','ams_tdr.mtr')
