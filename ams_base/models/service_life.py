# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
import math

class ResetOther(models.Model):
    _name = 'ams.component.otherreset'
    _description = 'Reset Service Life'

    service_life_id = fields.Many2one('ams.component.servicelife',string='Self')
    service_life_reset_id = fields.Many2one('ams.component.servicelife', string='Reset', required=True)
    auto = fields.Boolean(string='Auto Create', default=False)

    @api.model
    def create(self, values):
        if 'auto' not in values or ('auto' in values and values['auto'] == False):
            slive = self.env['ams.component.otherreset'].search([('service_life_id','=',values['service_life_reset_id'])])
            if(slive.id == False):
                self.env['ams.component.otherreset'].create({
                    'auto' : True,
                    'service_life_id' : values['service_life_reset_id'],
                    'service_life_reset_id' : values['service_life_id'],
                    })
        slivecheck = self.env['ams.component.otherreset'].search(['&',('service_life_id','=',values['service_life_id']),('service_life_reset_id','=',values['service_life_reset_id'])])
        if (slivecheck.id == False):
            return super(ResetOther, self).create(values)
        else:
            return False

    @api.one
    def unlink(self):
        to_del = self.env['ams.component.otherreset'].search(['&',('service_life_reset_id','=',self.service_life_id.id),('service_life_id','=',self.service_life_reset_id.id)])
        ulink = super(ResetOther, self).unlink()
        if(to_del.id != False):
            to_del.unlink()
        return ulink

class ComponentServiceLife(models.Model):
    _name = 'ams.component.servicelife'
    _description = 'Service Life'

    ref_id = fields.Many2one('ams.component.servicelife', string='Reference Id', default=False)
    is_major = fields.Boolean('Major (Show in Maintenance Planning)')
    
    bulletin_affected_id = fields.Many2one('bulletin.aircraft.affected', string='Bulletin Affected Id')
    bulletin_inspection_id = fields.Many2one('ams.bulletin', string='Bulletin Id')
    part_id = fields.Many2one('ams.component.part', string='Part Id')
    inspection_id = fields.Many2one('ams.inspection', string='Inspection Id')

    action_type = fields.Selection([('inspection','Inspection'),('overhaul','Overhaul'),('retirement','Retirement'),('oncondition','On Condition'),('conditionmonitoring','Condition Monitoring'),('service','Service')], string='Treatment', default="inspection",required=True)
    at_install = fields.Float(string='At Installation')
    value = fields.Float(string='Value')
    current = fields.Float(string='Current')
    overhaul_comp_attach_at = fields.Float(string='Overhoul Current')
    remaining = fields.Float(string='Remaining')
    current_date = fields.Date(string='Installed At', default=fields.Date.today)
    next_date = fields.Date(string='Date Due')
    # current_display = fields.Float(string='Current',readonly=True,related='current')
    # remaining_display = fields.Float(string='Next Due',readonly=True,related='remaining')
    unit = fields.Selection([('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')], string='Unit', default="hours",required=True)
    
    comments = fields.Text(string='Comment')
    comments_text = fields.Text(string='Comment', compute='_get_comment')
    extension = fields.Float(string='extension',default=0)

    current_text = fields.Char(string='Current')
    next_text = fields.Char(string='Next Due',compute='_next_text')
    since_new_text = fields.Char(string='Since New',compute='_next_text')
    installed_at = fields.Char(string='Installed At',compute='_next_text')
    since_overhaul_text = fields.Char(string='Since Overhaul / Inspection',compute='_next_text')

    reset_other = fields.Boolean(string='Reset Other Treatment "(or) condition"')
    other_service_live = fields.One2many('ams.component.otherreset', 'service_life_id', string=' ')

    remaining_text = fields.Char(string='Remaining', compute='_get_remaining')
    last_done = fields.Text(string='Last Done', compute='_get_last_done')
    
    text_value = fields.Text(string='Value', compute='_get_tree_text')
    text_unit = fields.Text(string='Unit', compute='_get_tree_text')
    text_extension = fields.Text(string='Extension', compute='_get_tree_text')
    text_next_due = fields.Text(string='Next Due', compute='_get_tree_text')
    text_remaining = fields.Text(string='Remaining', compute='_get_tree_text')
    replace_at = fields.Date(string='Replacement Date', compute='_get_replacement_date')

    # def _get_actype(self):
    #     if(self.part_id.is_subcomp == True):
    #         fleet_id = self.part_id.part_id.fleet_id
    #     else:
    #         fleet_id = self.part_id.fleet_id
    #     x = []
    #     if(fleet_id.rin_active == True):
    #         x = [('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days'),('rin','RIN')]
    #     else:
    #         x = [('hours','Hours'),('cycles','Cycles'),('year','Year'),('month','Month'),('days','Days')]

    #     return x

    # def _count_next_date(self):
    #     if self.unit == 'year':
    #         d = str(self.current_date).split('/')
    #         if len(d) == 3:
    #             dateDue = datetime.strptime(self.current_date, '%m/%d/%Y') + relativedelta(years=int(math.floor(self.value)))
    #         else:
    #             dateDue = datetime.strptime(self.current_date, '%Y-%m-%d') + relativedelta(years=int(math.floor(self.value)))
    #         dateDue = dateDue.strftime("%d/%m/%Y")
    #         return  dateDue
    #     if self.unit == 'month':
    #         d = str(self.current_date).split('/')
    #         if len(d) == 3:
    #             dateDue = datetime.strptime(self.current_date, '%m/%d/%Y') + relativedelta(months=int(math.floor(self.value)))
    #         else:
    #             dateDue = datetime.strptime(self.current_date, '%Y-%m-%d') + relativedelta(months=int(math.floor(self.value)))
    #         dateDue = dateDue.strftime("%d/%m/%Y")
    #         return  dateDue
    #     if self.unit == 'days':
    #         d = str(self.current_date).split('/')
    #         if len(d) == 3:
    #             dateDue = datetime.strptime(self.current_date, '%m/%d/%Y') + relativedelta(days=int(math.floor(self.value)))
    #         else:
    #             dateDue = datetime.strptime(self.current_date, '%Y-%m-%d') + relativedelta(days=int(math.floor(self.value)))
    #         dateDue = dateDue.strftime("%d/%m/%Y")
    #         return dateDue

    def __datetime(self, date_str):
        return datetime.strptime(str(date_str), "%d/%m/%Y")


    @api.one
    def _get_tree_text(self):
        if self.action_type == 'oncondition':
            self.text_value = '-'
            self.text_unit = '-'
            self.text_extension = '-'
            self.text_next_due = 'N/A'
            self.text_remaining = 'N/A'
        else:
            self.text_value = self.value
            self.text_unit = self.unit
            self.text_extension = self.extension
            self.text_next_due = self.next_text
            self.text_remaining = self.remaining_text

    @api.multi
    def do_ste(self):
        return {
            'name': 'STE',
            'type': 'ir.actions.act_window',
            'res_model': 'airworthy.ste',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': False,
            'views': [(False, 'form')],
            'target': 'new',
            'context': "{'serfice_life_id':" + str(self.id) + "}",
        }

    @api.multi
    def do_mwo(self):
        action = self.action_type
        value = self.value
        unit = self.unit
        macam = "Perlakuan : "+ str(value) + str(unit).upper() +" "+str(action).title() 
        return {
            'name': 'MWO',
            'type': 'ir.actions.act_window',
            'res_model': 'ams.mwo',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': False,
            'views': [(False, 'form')],
            'target': 'new',
            'context': "{'default_macam': '"+macam+"', 'default_ac': "+str(self.part_id.fleet_id.id)+"}"
            }

    @api.multi
    def do_wo(self):
        action = self.action_type
        value = self.value
        unit = self.unit
        note = '\
        - Perlakuan :  '+ str(value) + str(unit).upper() +' '+ str(action).title()+' <br/>\
        - After finish, return original sign WO to Enineering or followed by email to <u>engineering@pelita-air.com</u> <br/>\
        - Fill Material Required for any new material required in this inspection <br/>\
        - (*) Refer To Maintenance Program <br/>\
                                        '
        return {
            'name': 'WO',
            'type': 'ir.actions.act_window',
            'res_model': 'ams.work.order',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': False,
            'views': [(False, 'form')],
            'target': 'new',
            'context': "{'default_note': '"+note+"', 'default_ac': "+str(self.part_id.fleet_id.id)+", 'servicelife_id':"+str(self.id)+"}"
            }


    @api.multi
    def name_get(self):
        return [(record.id, str(record.value)+' '+str(record.unit) + ' ' + str(record.action_type) ) for record in self]

    @api.one
    @api.depends('remaining','value','extension','current')
    def _next_text_back(self):
        if self.unit in ["year","month","days"]:
            self.next_text = str(self.next_date)
        else:
            self.next_text = str(self.value + self.extension - self.current)

    @api.one
    @api.depends('part_id','inspection_id','bulletin_affected_id','bulletin_inspection_id','unit','extension','current','value','at_install')
    def _next_text(self):
        chours = 0
        ccycles = 0
        crins = 0
        if(self.part_id.id != False):
            part_id = self.part_id
            if(part_id.part_id.id != False):
                part_id = part_id.part_id
            if(part_id.fleet_id.id != False):
                chours = float(part_id.fleet_id.total_hours)
                ccycles = float(part_id.fleet_id.total_landings)
                crins = float(part_id.fleet_id.total_rins)
            if(part_id.engine_id.id != False):
                chours = float(part_id.engine_id.engine_tsn)
                ccycles = float(part_id.engine_id.engine_csn)
                crins = float(part_id.engine_id.engine_rsn)
            if(part_id.auxiliary_id.id != False):
                chours = float(part_id.auxiliary_id.auxiliary_tsn)
                ccycles = float(part_id.auxiliary_id.auxiliary_csn)
                crins = float(part_id.auxiliary_id.auxiliary_rsn)
            if(part_id.propeller_id.id != False):
                chours = float(part_id.propeller_id.propeller_tsn)
                ccycles = float(part_id.propeller_id.propeller_csn)
                crins = float(part_id.propeller_id.propeller_rsn)
        elif(self.inspection_id.id != False):
            inspection_id = self.inspection_id
            if(inspection_id.fleet_id.id != False):
                chours = float(inspection_id.fleet_id.total_hours)
                ccycles = float(inspection_id.fleet_id.total_landings)
                crins = float(inspection_id.fleet_id.total_rins)
            if(inspection_id.engine_id.id != False):
                chours = float(inspection_id.engine_id.engine_tsn)
                ccycles = float(inspection_id.engine_id.engine_csn)
                crins = float(inspection_id.engine_id.engine_rsn)
            if(inspection_id.auxiliary_id.id != False):
                chours = float(inspection_id.auxiliary_id.auxiliary_tsn)
                ccycles = float(inspection_id.auxiliary_id.auxiliary_csn)
                crins = float(inspection_id.auxiliary_id.auxiliary_rsn)
            if(inspection_id.propeller_id.id != False):
                chours = float(inspection_id.propeller_id.propeller_tsn)
                ccycles = float(inspection_id.propeller_id.propeller_csn)
                crins = float(inspection_id.propeller_id.propeller_rsn)
        elif(self.bulletin_affected_id.id != False):
            bulletin_affected_id = self.bulletin_affected_id
            if(bulletin_affected_id.fleet_id.id != False):
                chours = float(bulletin_affected_id.fleet_id.total_hours)
                ccycles = float(bulletin_affected_id.fleet_id.total_landings)
                crins = float(bulletin_affected_id.fleet_id.total_rins)
            if(bulletin_affected_id.engine_id.id != False):
                chours = float(bulletin_affected_id.engine_id.engine_tsn)
                ccycles = float(bulletin_affected_id.engine_id.engine_csn)
                crins = float(bulletin_affected_id.engine_id.engine_rsn)
            if(bulletin_affected_id.auxiliary_id.id != False):
                chours = float(bulletin_affected_id.auxiliary_id.auxiliary_tsn)
                ccycles = float(bulletin_affected_id.auxiliary_id.auxiliary_csn)
                crins = float(bulletin_affected_id.auxiliary_id.auxiliary_rsn)
            if(bulletin_affected_id.propeller_id.id != False):
                chours = float(bulletin_affected_id.propeller_id.propeller_tsn)
                ccycles = float(bulletin_affected_id.propeller_id.propeller_csn)
                crins = float(bulletin_affected_id.propeller_id.propeller_rsn)
        elif(self.bulletin_inspection_id.id != False):
            bulletin_inspection_id = self.bulletin_inspection_id
            if(bulletin_inspection_id.fleet_id.id != False):
                chours = float(bulletin_inspection_id.fleet_id.total_hours)
                ccycles = float(bulletin_inspection_id.fleet_id.total_landings)
                crins = float(bulletin_inspection_id.fleet_id.total_rins)
            if(bulletin_inspection_id.engine_id.id != False):
                chours = float(bulletin_inspection_id.engine_id.engine_tsn)
                ccycles = float(bulletin_inspection_id.engine_id.engine_csn)
                crins = float(bulletin_inspection_id.engine_id.engine_rsn)
            if(bulletin_inspection_id.auxiliary_id.id != False):
                chours = float(bulletin_inspection_id.auxiliary_id.auxiliary_tsn)
                ccycles = float(bulletin_inspection_id.auxiliary_id.auxiliary_csn)
                crins = float(bulletin_inspection_id.auxiliary_id.auxiliary_rsn)
            if(bulletin_inspection_id.propeller_id.id != False):
                chours = float(bulletin_inspection_id.propeller_id.propeller_tsn)
                ccycles = float(bulletin_inspection_id.propeller_id.propeller_csn)
                crins = float(bulletin_inspection_id.propeller_id.propeller_rsn)

        if self.action_type == 'oncondition' or self.action_type == 'conditionmonitoring':
            self.next_text = 'N/A'
            self.since_new_text = "%.2f" % self.part_id.tsn
            self.installed_at = self.part_id.ac_timeinstallation
        elif self.unit in ["year","month","days"]:
            if self.next_date:
                self.next_text =  datetime.strptime(self.next_date, '%Y-%m-%d').strftime("%d/%m/%Y")
            else:
                self.next_text =  datetime.now()

            # self.since_new_text =  datetime.strptime(self.next_date, '%Y-%m-%d').strftime("%d/%m/%Y") #BELUM FIX
            if self.current_date:
                get = str(self.__datetime(str(datetime.now().strftime('%d/%m/%Y'))) - self.__datetime(datetime.strptime(self.current_date, '%Y-%m-%d').strftime('%d/%m/%Y'))).split(' ')
                if get[0] == '0:00:00':
                    self.since_new_text = '0 days'
                else:
                    get = str(get[0])+' '+str(get[1])[:-1]
                    self.since_new_text = get
            else:
                self.since_new_text = datetime.now()


            if self.part_id:
                if self.part_id.date_installed != False:
                    get = str(self.__datetime(str(datetime.now().strftime('%d/%m/%Y'))) - self.__datetime(datetime.strptime(self.part_id.date_installed, '%Y-%m-%d').strftime('%d/%m/%Y'))).split(' ')
                    if get[0] == '0:00:00':
                        self.since_overhaul_text = '0 days'
                    else:                
                        get = str(get[0])+' '+str(get[1])[:-1]
                        self.since_overhaul_text = get
            else:
                self.since_overhaul_text = datetime.now()
            self.installed_at = datetime.strptime(self.current_date, '%Y-%m-%d').strftime("%d/%m/%Y")

        else:
            # AC HOURS SEKARANG - CURRENT
            if(self.unit == 'hours'):
                due_at = chours + self.remaining
                installed_at = (due_at - self.value) + self.at_install
                if(self.action_type != 'inspection'):
                    self.since_new_text = "%.2f" % (((chours - installed_at) + self.at_install)+self.overhaul_comp_attach_at)
                    self.since_overhaul_text = "%.2f" % self.current
                else:
                    self.since_new_text = "%.2f" % self.part_id.tsn
                    self.since_overhaul_text = "%.2f" % self.current
                # perhitungan special component
                if self.part_id.not_follow_parent == True:
                    print self.part_id.name
                    self.next_text = "%.2f" %  (float(self.part_id.tsn) + float(self.remaining))
                elif self.part_id.part_id.not_follow_parent == True:
                    print self.part_id.name
                    self.next_text = "%.2f" %  (float(self.part_id.part_id.tsn) + float(self.remaining))
                else:
                    self.next_text = "%.2f" % ((float(self.value) - float(self.at_install)) + float(installed_at))
            elif(self.unit == 'cycles'):
                due_at = ccycles + self.remaining
                installed_at = (due_at - self.value) + self.at_install
                if(self.action_type != 'inspection'):
                    self.since_new_text = "%.1f" % (((ccycles - installed_at) + self.at_install)+self.overhaul_comp_attach_at)
                    self.since_overhaul_text =  "%.1f" % self.current
                else:
                    self.since_new_text = "%.1f" % self.part_id.csn
                    self.since_overhaul_text =  "%.1f" % self.current
                # perhitungan special component
                if self.part_id.not_follow_parent == True:
                    print self.part_id.name
                    self.next_text = "%.1f" %  (float(self.part_id.csn) + float(self.remaining))
                elif self.part_id.part_id.not_follow_parent == True:
                    print self.part_id.name
                    self.next_text = "%.1f" %  (float(self.part_id.part_id.csn) + float(self.remaining))
                else:
                    self.next_text =  "%.1f" % ((float(self.value) - float(self.at_install)) + float(installed_at))
            elif(self.unit == 'rins'):
                due_at = crins + self.remaining
                installed_at = (due_at - self.value) + self.at_install
                if(self.action_type != 'inspection'):
                    self.since_new_text = "%.2f" % (((crins - installed_at) + self.at_install)+self.overhaul_comp_attach_at)
                    self.since_overhaul_text = "%.2f" % self.current
                else:
                    self.since_new_text = "%.2f" % self.part_id.rsn
                    self.since_overhaul_text = "%.2f" % self.current
                # perhitungan special component
                if self.part_id.not_follow_parent == True:
                    print self.part_id.name
                    self.next_text = "%.2f" %  (float(self.part_id.rsn) + float(self.remaining))
                elif self.part_id.part_id.not_follow_parent == True:
                    print self.part_id.name
                    self.next_text = "%.2f" %  (float(self.part_id.part_id.rsn) + float(self.remaining))
                else:
                    self.next_text = "%.2f" % ((float(self.value) - float(self.at_install)) + float(installed_at))
            if(self.action_type == 'oncondition'):
                self.since_overhaul_text = 'N/A'

            # IF COMPONENT SPECIAL BELUM
            if self.unit == 'hours':
                if self.part_id.not_follow_parent == True:
                    self.installed_at = self.part_id.ac_timeinstallation
                elif self.part_id.part_id.not_follow_parent == True:
                    self.installed_at = self.part_id.ac_timeinstallation - self.part_id.part_id.ac_timeinstallation
                else:
                    self.installed_at = self.part_id.ac_timeinstallation
            elif self.unit == 'cycles':
                if self.part_id.not_follow_parent == True:
                    self.installed_at = self.part_id.ac_cyclesinstallation
                elif self.part_id.part_id.not_follow_parent == True:
                    self.installed_at = self.part_id.ac_cyclesinstallation - self.part_id.part_id.ac_cyclesinstallation
                else:
                    self.installed_at = self.part_id.ac_cyclesinstallation
            elif self.unit == 'rin':
                if self.part_id.not_follow_parent == True:
                    self.installed_at = self.part_id.ac_rininstallation
                elif self.part_id.part_id.not_follow_parent == True:
                    self.installed_at = self.part_id.ac_rininstallation - self.part_id.part_id.ac_rininstallation
                else:
                    self.installed_at = self.part_id.ac_rininstallation
            else:
                self.installed_at = datetime.strptime(self.current_date, '%Y-%m-%d').strftime("%d/%m/%Y")

    @api.one
    def _get_remaining(self):
        if self.unit in ["year","month","days"]:
            if self.next_date:
                self.remaining_text = str((datetime.strptime(self.next_date, "%Y-%m-%d") - datetime.now()).days)+" Days"
        else:
            self.remaining_text = str(self.value - self.current) + '+' + str(self.extension) if self.extension != 0 else self.value - self.current

    @api.one
    def _get_last_done(self):
        if(self.part_id.id != False):
            part_id = self.part_id
            if(part_id.part_id.id != False):
                part_id = part_id.part_id
            if(part_id.fleet_id.id != False):
                chours = part_id.fleet_id.total_hours
                ccycles = part_id.fleet_id.total_landings
                crins = part_id.fleet_id.total_rins
            if(part_id.engine_id.id != False):
                chours = part_id.engine_id.engine_tsn
                ccycles = part_id.engine_id.engine_csn
                crins = part_id.engine_id.engine_rsn
            if(part_id.auxiliary_id.id != False):
                chours = part_id.auxiliary_id.auxiliary_tsn
                ccycles = part_id.auxiliary_id.auxiliary_csn
                crins = part_id.auxiliary_id.auxiliary_rsn
            if(part_id.propeller_id.id != False):
                chours = part_id.propeller_id.propeller_tsn
                ccycles = part_id.propeller_id.propeller_csn
                crins = part_id.propeller_id.propeller_rsn
        elif(self.inspection_id.id != False):
            inspection_id = self.inspection_id
            if(inspection_id.fleet_id.id != False):
                chours = inspection_id.fleet_id.total_hours
                ccycles = inspection_id.fleet_id.total_landings
                crins = inspection_id.fleet_id.total_rins
            if(inspection_id.engine_id.id != False):
                chours = inspection_id.engine_id.engine_tsn
                ccycles = inspection_id.engine_id.engine_csn
                crins = inspection_id.engine_id.engine_rsn
            if(inspection_id.auxiliary_id.id != False):
                chours = inspection_id.auxiliary_id.auxiliary_tsn
                ccycles = inspection_id.auxiliary_id.auxiliary_csn
                crins = inspection_id.auxiliary_id.auxiliary_rsn
            if(inspection_id.propeller_id.id != False):
                chours = inspection_id.propeller_id.propeller_tsn
                ccycles = inspection_id.propeller_id.propeller_csn
                crins = inspection_id.propeller_id.propeller_rsn

        if self.unit in ["year","month","days"]:
            self.last_done =  self.current_date
        else:
            # AC HOURS SEKARANG - CURRENT
            if(self.unit == 'hours'):
                self.last_done = chours - self.current
            elif(self.unit == 'cycles'):
                self.last_done = ccycles - self.current
            elif(self.unit == 'rins'):
                self.last_done = crins - self.current

    @api.one
    @api.depends('comments')
    def _get_comment(self):
        perlakuan = ''
        if(len(self.other_service_live) > 0):
            perlakuan = ' *'
            for g in self.other_service_live:
                perlakuan = perlakuan + 'or ' + str(g.service_life_reset_id.value) + ' ' + str(g.service_life_reset_id.unit) + ' ' + str(g.service_life_reset_id.action_type) + ' '
        self.comments_text = (str(self.comments) if self.comments != False else '') + str(perlakuan)

    def check_val(self):
        if self.unit in ["year","month","days"]:
            self.current_text = self.current_date
            self.next_text = self.next_date
        else:
            self.current_text = self.current
            self.next_text = self.remaining

    def _count_date_due(self):
        if(self.current_date == False):
            now = datetime.now()
            self.next_date = now.strftime("%Y-%m-%d")
        else:
            value = self.value if self.value != False else 0
            extension = self.extension if self.extension != False else 0
            if self.unit == 'year':
                dateDue = datetime.strptime(self.current_date, '%Y-%m-%d') + relativedelta(years=int(math.floor(value + extension)))
            if self.unit == 'month':
                dateDue = datetime.strptime(self.current_date, '%Y-%m-%d') + relativedelta(months=int(math.floor(value + extension)))
            if self.unit == 'days':
                dateDue = datetime.strptime(self.current_date, '%Y-%m-%d') + relativedelta(days=int(math.floor(value + extension)))
            self.next_date = dateDue.strftime("%Y-%m-%d")

    @api.onchange('current')
    def _onchange_current(self):
        self.remaining = self.value + self.extension - self.current
        self.check_val()
            
    @api.onchange('value')
    def _onchange_value(self):
        self.remaining = self.value + self.extension - self.current
        if self.unit in ["year","month","days"]:
            self._count_date_due()
        self.check_val()

    @api.onchange('unit')
    def _onchange_unit(self):
        if self.unit in ["year","month","days"]:
            self._count_date_due()
        self.check_val()

    @api.onchange('current_date')
    def _onchange_current_date(self):
        if self.unit in ["year","month","days"]:
            self._count_date_due()
        self.check_val()
                    

    @api.model
    def create(self, vals):
        vals['extension'] = 0.00
        vals['remaining'] = float(vals['value'] + vals['extension'] - vals['current'])
        if vals['unit'] in ["year","month","days"]:
            if( 'current_date' not in vals or vals['current_date'] == False):
                now = datetime.now()
                dateDue = now.strftime("%Y-%m-%d")
            else:
                if vals['unit'] == 'year':
                    dateDue = datetime.strptime(vals['current_date'], '%Y-%m-%d') + relativedelta(years=int(math.floor((vals['value'] + vals['extension']))))
                if vals['unit'] == 'month':
                    dateDue = datetime.strptime(vals['current_date'], '%Y-%m-%d') + relativedelta(months=int(math.floor((vals['value'] + vals['extension']))))
                if vals['unit'] == 'days':
                    dateDue = datetime.strptime(vals['current_date'], '%Y-%m-%d') + relativedelta(days=int(math.floor((vals['value'] + vals['extension']))))
            vals['next_date'] = dateDue
            vals['current_text'] = vals['current_date'] if 'current_date' in vals else False
            vals['next_text'] = dateDue
        else:
            vals['current_text'] = vals['current'] if vals['current'] else '0'
            vals['next_text'] = vals['remaining']
        create = super(ComponentServiceLife, self).create(vals)
        # if create.bulletin_inspection_id != False:
        #     self.bulletin_slive_inject_on_create(create.id)

    
    @api.model
    def write(self, vals):
        cur = self.env['ams.component.servicelife'].search([('id','=',self.id)])
        if 'value' in vals:
            vals['remaining'] = (vals['value'] + cur.extension) - cur.current

        currentdate = vals['current_date'] if 'current_date' in vals else self.current_date
        extension = vals['extension'] if 'extension' in vals else self.extension
        value = vals['value'] if 'value' in vals else self.value
        if self.unit in ["year","month","days"]:
            if self.unit == 'year':
                dateDue = datetime.strptime(currentdate, '%Y-%m-%d') + relativedelta(years=int(math.floor((value + extension))))
            if self.unit == 'month':
                dateDue = datetime.strptime(currentdate, '%Y-%m-%d') + relativedelta(months=int(math.floor((value + extension))))
            if self.unit == 'days':
                dateDue = datetime.strptime(currentdate, '%Y-%m-%d') + relativedelta(days=int(math.floor((value + extension))))
                dateDue = dateDue.strftime("%Y-%m-%d")
            vals['next_text'] = dateDue
            vals['next_date'] = dateDue
        # else:
        #     if vals['value'] == False:
        #         vals['value'] = 0.00
        #     vals['next_text'] = (vals['value'] + cur.extension) - cur.current

        write = super(ComponentServiceLife, self).write(vals)
        return write

    @api.one
    def unlink(self):
        self.env['ams.component.servicelife'].search([('ref_id','=',self.id)]).unlink()
        return super(ComponentServiceLife, self).unlink()

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
            'context': "{'service_life_id':" + str(self.id) + "}",
        }

    def reset(self,slive_id,date,hours,cycles,rins):
        normal_treat = ['hours','cycles','rin']
        slive = self.env['ams.component.servicelife'].search([('id','=',slive_id)])
        
        cvalue = slive.value
        pvalue = 0
        if(slive.unit == 'hours'):
            cvalue = cvalue - hours
            pvalue = hours
        elif(slive.unit == 'cycles'):
            cvalue = cvalue - cycles
            pvalue = cycles
        elif(slive.unit == 'rin'):
            cvalue = cvalue - rins
            pvalue = rins

        if(slive.unit in normal_treat):
            slive.write({
                'current' : pvalue,
                'remaining' : cvalue - pvalue,
                # 'value' : cvalue,
                'current_date' : False,
                'next_date' : False,
                'current_text' : pvalue,
                'next_text' : cvalue,
                'extension' : 0,
            })
        else:
            if slive.unit == 'year':
                dateDue = datetime.strptime(date, '%Y-%m-%d') + relativedelta(years=int(math.floor(cvalue)))
            if slive.unit == 'month':
                dateDue = datetime.strptime(date, '%Y-%m-%d') + relativedelta(months=int(math.floor(cvalue)))
            if slive.unit == 'days':
                dateDue = datetime.strptime(date, '%Y-%m-%d') + relativedelta(days=int(math.floor(cvalue)))
            dateDue = dateDue.strftime("%Y-%m-%d")
            
            slive.write({
                'current' : pvalue,
                'remaining' : cvalue - pvalue,
                # 'value' : cvalue,
                'current_date' : date,
                'next_date' : dateDue,
                'current_text' : date,
                'next_text' : dateDue,
                'extension' : 0,
            })
        # HAPUS EXTENSION