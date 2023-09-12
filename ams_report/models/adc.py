from odoo import models, fields, api, _
from datetime import datetime, timedelta
import xlwt
from xlsxwriter import *
from cStringIO import StringIO
import base64
from reportlab.pdfgen import canvas
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx


class ADCReport(models.Model):
    _name = 'ams.adc.report'
    _description = 'ADC Report'

    fleet_id = fields.Many2one('aircraft.acquisition')
    bulletin_line = fields.One2many('ams.adc.data','adc_id',compute='_onchange_plane_id')

    def get_engine(self, no):
        if no == 1:
            eng = self.fleet_id.engine_type_id.id
        if no == 2:
            eng = self.fleet_id.engine2_type_id.id
        if no == 3:
            eng = self.fleet_id.engine3_type_id.id
        if no == 4:
            eng = self.fleet_id.engine4_type_id.id
        bulletin_ids = []
        engine = self.env['bulletin.engine.affected'].search([('engine_id','=',eng),('bulletin_id.type','=',"SB")])
        for g in engine:
            ad_ids = []
            dgac_ids = []
            int_ids = []
            sb_ids = []
            date = ""

            sb_ids.append(g.bulletin_id.id)
            for i in self._check_ref(g.bulletin_id.id):
                ad_ids.append(i)

            for n in self.env['ams.bulletin'].search([('id','in',ad_ids)]):
                if(n.regulator_id.inter == True):
                    int_ids.append(n.id)
                else:
                    dgac_ids.append(n.id)
            if (g.bulletin_id.fleet_ids.comply_status in ['cw','pcw']):
                ress_date = g.bulletin_id.fleet_ids.bulletin_compliance_id.date 
                date = str(ress_date)
            else :
                date = 'N/A'
            bulletin_ids.append({
                'dgac_ids' : self.env['ams.bulletin'].search([('id','in',dgac_ids)]), 
                'inter_ids' : self.env['ams.bulletin'].search([('id','in',int_ids)]),
                'sb_ids' : self.env['ams.bulletin'].search([('id','in',sb_ids)]),
                'subject' :  g.bulletin_id.subject,
                'remarks' : g.bulletin_id.remarks,
                'date_compli' : date,
                'total_hours' : str(g.bulletin_id.fleet_ids.fleet_id.total_landings) + " " + "FC",
                'total_cycle' : str(g.bulletin_id.fleet_ids.fleet_id.total_hours) + " " + "FH",
                'recurring' : str(g.bulletin_id.repetitive_value) + " " + str (g.bulletin_id.repetitive_every)
                })
        return bulletin_ids

    def get_auxiliary(self):
        bulletin_ids = []
        auxiliary = self.env['bulletin.auxiliary.affected'].search([('auxiliary_id','=',self.fleet_id.auxiliary_type_id.id),('bulletin_id.type','=',"SB")])
        for g in auxiliary:
            ad_ids = []
            dgac_ids = []
            int_ids = []
            sb_ids = []
            date = ""

            sb_ids.append(g.bulletin_id.id)
            for i in self._check_ref(g.bulletin_id.id):
                ad_ids.append(i)

            for n in self.env['ams.bulletin'].search([('id','in',ad_ids)]):
                if(n.regulator_id.inter == True):
                    int_ids.append(n.id)
                else:
                    dgac_ids.append(n.id)
            if (g.bulletin_id.fleet_ids.comply_status in ['cw','pcw']):
                ress_date = g.bulletin_id.fleet_ids.bulletin_compliance_id.date 
                date = str(ress_date)
            else :
                date = 'N/A'
            bulletin_ids.append((0,0,{
                'dgac_ids' : self.env['ams.bulletin'].search([('id','in',dgac_ids)]), 
                'inter_ids' : self.env['ams.bulletin'].search([('id','in',int_ids)]),
                'sb_ids' : self.env['ams.bulletin'].search([('id','in',sb_ids)]),
                'subject' :  g.bulletin_id.subject,
                'remarks' : g.bulletin_id.remarks,
                'date_compli' : date,
                'total_hours' : str(g.bulletin_id.fleet_ids.fleet_id.total_landings) + " " + "FC",
                'total_cycle' : str(g.bulletin_id.fleet_ids.fleet_id.total_hours) + " " + "FH",
                'recurring' : str(g.bulletin_id.repetitive_value) + " " + str (g.bulletin_id.repetitive_every)
                }))
        return bulletin_ids


    def get_propeller(self, no):
        if no == 1:
            prop = self.fleet_id.propeller_type_id.id
        elif no == 2:
            prop = self.fleet_id.propeller2_type_id.id
        elif no == 3:
            prop = self.fleet_id.propeller3_type_id.id
        else:
            prop = self.fleet_id.propeller4_type_id.id
            
        
        bulletin_ids = []
        propeller = self.env['bulletin.propeller.affected'].search([('propeller_id','=',prop),('bulletin_id.type','=',"SB")])
        for g in propeller:
            ad_ids = []
            dgac_ids = []
            int_ids = []
            sb_ids = []
            date = ""

            sb_ids.append(g.bulletin_id.id)
            for i in self._check_ref(g.bulletin_id.id):
                ad_ids.append(i)

            for n in self.env['ams.bulletin'].search([('id','in',ad_ids)]):
                if(n.regulator_id.inter == True):
                    int_ids.append(n.id)
                else:
                    dgac_ids.append(n.id)
            if (g.bulletin_id.fleet_ids.comply_status in ['cw','pcw']):
                ress_date = g.bulletin_id.fleet_ids.bulletin_compliance_id.date 
                date = str(ress_date)
            else :
                date = 'N/A'
            bulletin_ids.append((0,0,{
                'dgac_ids' : self.env['ams.bulletin'].search([('id','in',dgac_ids)]), 
                'inter_ids' : self.env['ams.bulletin'].search([('id','in',int_ids)]),
                'sb_ids' : self.env['ams.bulletin'].search([('id','in',sb_ids)]),
                'subject' :  g.bulletin_id.subject,
                'remarks' : g.bulletin_id.remarks,
                'date_compli' : date,
                'total_hours' : str(g.bulletin_id.fleet_ids.fleet_id.total_landings) + " " + "FC",
                'total_cycle' : str(g.bulletin_id.fleet_ids.fleet_id.total_hours) + " " + "FH",
                'recurring' : str(g.bulletin_id.repetitive_value) + " " + str (g.bulletin_id.repetitive_every)
                }))
        return bulletin_ids

    def get_component(self):
        bulletin_ids = []
        component = self.env['bulletin.component.affected'].search([('component_id','in',self.fleet_id.component_ids.ids),('bulletin_id.type','=',"SB")])
        for g in component:
            ad_ids = []
            dgac_ids = []
            int_ids = []
            sb_ids = []
            date = ""

            sb_ids.append(g.bulletin_id.id)
            for i in self._check_ref(g.bulletin_id.id):
                ad_ids.append(i)

            for n in self.env['ams.bulletin'].search([('id','in',ad_ids)]):
                if(n.regulator_id.inter == True):
                    int_ids.append(n.id)
                else:
                    dgac_ids.append(n.id)
            if (g.bulletin_id.fleet_ids.comply_status in ['cw','pcw']):
                ress_date = g.bulletin_id.fleet_ids.bulletin_compliance_id.date 
                date = str(ress_date)
            else :
                date = 'N/A'
            bulletin_ids.append((0,0,{
                'dgac_ids' : self.env['ams.bulletin'].search([('id','in',dgac_ids)]), 
                'inter_ids' : self.env['ams.bulletin'].search([('id','in',int_ids)]),
                'sb_ids' : self.env['ams.bulletin'].search([('id','in',sb_ids)]),
                'subject' :  g.bulletin_id.subject,
                'remarks' : g.bulletin_id.remarks,
                'date_compli' : date,
                'total_hours' : str(g.bulletin_id.fleet_ids.fleet_id.total_landings) + " " + "FC",
                'total_cycle' : str(g.bulletin_id.fleet_ids.fleet_id.total_hours) + " " + "FH",
                'recurring' : str(g.bulletin_id.repetitive_value) + " " + str (g.bulletin_id.repetitive_every)
                }))
        return bulletin_ids

    @api.onchange('fleet_id')
    def _onchange_plane_id(self):
        bulletin_ids = []

        plane = self.fleet_id.id
        fleet = self.env['bulletin.aircraft.affected'].search([('fleet_id','=',plane),('bulletin_id.type','=',"SB")])
        engine = self.env['bulletin.engine.affected'].search([ '|','|','|','&' ,('engine_id','=',self.fleet_id.engine_type_id.id),('engine_id','=',self.fleet_id.engine2_type_id.id),('engine_id','=',self.fleet_id.engine3_type_id.id),('engine_id','=',self.fleet_id.engine4_type_id.id),('bulletin_id.type','=',"SB")])
        auxiliary = self.env['bulletin.auxiliary.affected'].search([('auxiliary_id','=',self.fleet_id.auxiliary_type_id.id),('bulletin_id.type','=',"SB")])
        propeller = self.env['bulletin.propeller.affected'].search([ '|','|','|','&' ,('propeller_id','=',self.fleet_id.propeller_type_id.id),('propeller_id','=',self.fleet_id.propeller2_type_id.id),('propeller_id','=',self.fleet_id.propeller3_type_id.id),('propeller_id','=',self.fleet_id.propeller4_type_id.id),('bulletin_id.type','=',"SB")])
        component = self.env['bulletin.component.affected'].search([('component_id','in',self.fleet_id.component_ids.ids),('bulletin_id.type','=',"SB")])
        for g in fleet:
            ad_ids = []
            dgac_ids = []
            int_ids = []
            sb_ids = []
            date = ""

            sb_ids.append(g.bulletin_id.id)
            for i in self._check_ref(g.bulletin_id.id):
                ad_ids.append(i)

            for n in self.env['ams.bulletin'].search([('id','in',ad_ids)]):
                if(n.regulator_id.inter == True):
                    int_ids.append(n.id)
                else:
                    dgac_ids.append(n.id)
            if (g.bulletin_id.fleet_ids.comply_status in ['cw','pcw']):
                ress_date = g.bulletin_id.fleet_ids.bulletin_compliance_id.date 
                date = str(ress_date)
            else :
                date = 'N/A'
            bulletin_ids.append((0,0,{
                'dgac_ids' : dgac_ids, 
                'inter_ids' : int_ids,
                'sb_ids' : sb_ids,
                'subject' :  g.bulletin_id.subject,
                'remarks' : g.bulletin_id.remarks,
                'date_compli' : date,
                'total_hours' : str(g.bulletin_id.fleet_ids.fleet_id.total_landings) + " " + "FC",
                'total_cycle' : str(g.bulletin_id.fleet_ids.fleet_id.total_hours) + " " + "FH",
                'recurring' : str(g.bulletin_id.repetitive_value) + " " + str (g.bulletin_id.repetitive_every)
                }))

        self.bulletin_line = bulletin_ids

    def _check_ref(self,bulletin_id):
        bulletin_ids = []
        ro = self.env['ams.bulletin'].search([('bulletin_id','=',bulletin_id)])
        for g in ro:
            bulletin_ids.append(g.id)
            if self.env['ams.bulletin'].search([('bulletin_id','=',g.id)]) != []:
                for i in self._check_ref(g.id):
                    bulletin_ids.append(i.id)
        return bulletin_ids
        
    @api.multi
    def print_adc_reports(self):
        return self.env['report'].get_action(self, 'ams_report.report_adc')


class ADCData(models.Model):
    _name = 'ams.adc.data'
    _description = 'ADC Data'

    adc_id = fields.Many2one('ams.adc.report' )
    dgac_ids = fields.Many2many('ams.bulletin')
    inter_ids = fields.Many2many('ams.bulletin')
    sb_ids = fields.Many2many('ams.bulletin')
    subject = fields.Text()
    date_compli = fields.Char()
    total_hours = fields.Char()
    total_cycle = fields.Char()
    recurring = fields.Char()
    remarks =fields.Text()

  