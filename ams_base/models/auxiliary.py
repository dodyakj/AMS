# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import csv
import base64
import tempfile
import cStringIO

from datetime import date, datetime, timedelta
from odoo import fields, models, api

class AircraftAircraftAuxiliary(models.Model):
    _name = 'auxiliary.auxiliary'

    name = fields.Char(string='Name', required=True)

class AuxiliaryType(models.Model):
    _name = 'auxiliary.type'

    name = fields.Char( string='Auxiliary Name', required=True)
    auxiliary_model = fields.Many2one('auxiliary.auxiliary', string='Auxiliary Model')
    serial_number = fields.Char( string='Serial Number')
    auxiliary_lastoh = fields.Date(string='Auxiliary Overhaul')
    aircraft_status = fields.Boolean(string='Auxiliary Status',default=True)
    bel_view = fields.Boolean(string='Is Bel',default=lambda self:self.env.context.get('belcomponent',False),readonly=True,store=False)
    document_ids = fields.One2many('document.certificate','auxiliary_id', string="Document Certificate", copy=True)
    fleet_id = fields.Many2one('aircraft.acquisition', string='Fleet Id')
    auxiliary_tsn = fields.Float(string='TSN')
    auxiliary_csn = fields.Float(string='CSN')
    auxiliary_rsn = fields.Float(string='RIN Since New')
    auxiliary_tso = fields.Float(string='TSO')
    auxiliary_cso = fields.Float(string='CSO')
    auxiliary_rso = fields.Float(string='RIN Since Overhoul')
    total_hours = fields.Float(string='Total Hours', required=True, default=0)
    total_cycles = fields.Float(string='Total Landings', required=True, default=0)
    total_rins = fields.Integer(string='Total Rins')
    special_ratio_counting = fields.Boolean(string='Special ratio Counting')
    component_ids = fields.One2many('ams.component.part','auxiliary_id',string='Component', copy=True)
    inspection_ids = fields.One2many('ams.inspection','auxiliary_id',string='Inspection', copy=True)
    history_line = fields.One2many('ams.component_history','auxiliary_id',string='History', copy=True)

    is_deleted = fields.Boolean(default=False)

    @api.multi
    def do_inspection(self):
        return {
            'name': 'Inspection',
            'type': 'ir.actions.act_window',
            'res_model': 'airworthy.inspection',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': False,
            'views': [(False, 'form')],
            'target': 'new',
            'context': "{'auxiliary_id':" + str(self.id) + "}",
        }

    @api.model
    def default_get(self, flds):
        result = super(AuxiliaryType, self).default_get(flds)
        result['bel_view'] = self.env.context.get('belcomponent',False)
        # self.bel_view = self.env.context.get('belcomponent',False)
        return result

    @api.multi
    def do_document_check(self):
        return {
            'name': 'Document',
            'type': 'ir.actions.act_window',
            'res_model': 'aircraft.document',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': False,
            'views': [(False, 'form')],
            'target': 'new',
            'context': "{'auxiliary_id':" + str(self.id) + "}",
        }

    @api.multi
    def do_overhaul(self):
        return {
            'name': 'Overhoul',
            'type': 'ir.actions.act_window',
            'res_model': 'airworthy.overhaul',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': False,
            'views': [(False, 'form')],
            'target': 'new',
            'context': "{'auxiliary_id':" + str(self.id) + "}",
        }


    some_count = fields.Integer(string='Total',default=3)
    @api.multi
    def return_action_to_open(self):
        return False

    @api.multi
    def write(self, vals):
        if('total_hours' in vals or 'total_cycles' in vals or 'total_rins' in vals):
            if(self.env.context.get('manual_edit',False) == True) :
                self.env['ams.manual_changes'].create({
                    'auxiliary_id' : self.id,
                    'current_hours' : self.total_hours if ('total_hours' in vals) else False,
                    'current_cycles' : self.total_cycles if ('total_cycles' in vals) else False,
                    'current_rin' : self.total_rins if ('total_rins' in vals) else False,
                    'hours' : vals['total_hours'] if ('total_hours' in vals) else False,
                    'cycles' : vals['total_cycles'] if ('total_cycles' in vals) else False,
                    'rin' : vals['total_rins'] if ('total_rins' in vals) else False,
                    })
        write = super(AuxiliaryType, self).write(vals)
        return write

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.id:
                rec.is_deleted = True

    @api.multi
    def restore(self):
        for rec in self:
            if rec.id:
                rec.is_deleted = False


    @api.model
    def check_serviceable(self):
        servicable = True
        # check every part is available
        # A/C Comp
        for aux_comp in self.component_ids:
            if (aux_comp.no_component == True):
                servicable = False
            for ac_subcomp in aux_comp.sub_part_ids:
                if (ac_subcomp.no_component == True):
                    servicable = False
        self.aircraft_status = servicable
        return servicable

    @api.multi
    def wizard_auxiliary_import(self):
        return{
            'type': 'ir.actions.act_window',
            'name': 'Wizard Import CSV',
            'res_model': 'wizard.import.auxiliary',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'auxiliary_id': self.id,
            },
        }

class AuxiliarySpare(models.Model):
    _name = 'auxiliary.spare'

    name = fields.Many2one('auxiliary.type','Auxiliary Spare', required=True)
    acquisition_id = fields.Many2one('aircraft.acquisition',string ='Auxiliary Spare for')
    description = fields.Text('Description')
    date_pemasangan = fields.Date('Tanggal Pemasangan')
    date_penurunan = fields.Date('Tanggal Penurunan')
    propeller_type_id = fields.Many2one('propeller.type','Propeller Type')
    esn = fields.Char(string='ESN')
    rgb = fields.Char(string='RGB S/N')
    propeller = fields.Char(string='Propeller S/N')
    auxiliary_tsn = fields.Char(string='TSN')
    auxiliary_csn = fields.Char(string='CSN')
    tslsv = fields.Char(string='TSLSV')
    cslsv = fields.Char(string='CSLSV')
    lessor = fields.Char(string='Lessor')
    start_lease = fields.Date('Start Lease')
    normal_termination = fields.Date('Normal Termination')

class WizardImportAuxiliary(models.Model):
    _name   = 'wizard.import.auxiliary'

    file         = fields.Binary('File')
    filename     = fields.Char(string="Filename")
    auxiliary_id = fields.Many2one('auxiliary.type', 'Auxiliary Name', default=lambda self:self._context.get('auxiliary_id',False))

    @api.multi
    def import_auxiliary(self, comptype='M'):
        
        auxiliary_id = self.auxiliary_id.id

        if auxiliary_id != False:
            self.auxiliary_id.component_ids.unlink()
            self.auxiliary_id.inspection_ids.unlink()
            self.env.cr.commit()

            filedata = base64.b64decode(self.file)
            input = cStringIO.StringIO(filedata)
            input.seek(0)
       
            (fileno, fp_name) = tempfile.mkstemp('.csv', 'openerp_')
            file = open(fp_name, "w")
            file.write(filedata)
            file.close()
               
            ro = list(csv.reader(open(fp_name,"rb"), delimiter=';'))

            if len(ro) >= 1:
                if ro[0][155] == 'CALMID':
                    part_name = 0
                    last_time_insp = 94
                    rhll = 82
                    since_time_insp = 93
                    part_desc = 95
                    part_no = 1
                    serial = 2
                    ata_1 = 3
                    ata_2 = 4
                    ata_3 = 5
                    rank = 68
                    inst_date = 6
                    item = 90
                    calm_id = 155
                    delete = 156

                    cycle_on_install = 8
                    csn = 9
                    cso = 11

                    on_condition = 26
                    U2TT = 48
                    on_condition_hours = 49
                    on_aircraft_hours = 47
                    on_comp_hours = 46

                    comment = 79

                    retirement = 33
                    retirement_hours = 34
                    retirement_aircraft_hours = 36
                    retirement_comp_hours = 35
                    retirement_comp_attach_at = 37
                    retirement_current = 37

                    overhaul = 27
                    overhaul_hours = 28
                    overhaul_aircraft_hours = 30
                    overhaul_comp_hours = 29
                    overhaul_comp_attach_at = 31
                    overhaul_current = 32

                    inspection = 16
                    inspection_hours = 17
                    inspection_aircraft_hours = 19
                    inspection_comp_hours = 18
                    inspection_comp_attach_at = 20
                    inspection_current = 21

                    cycles_on = 7
                    cycles_type = 159
                    cycles_value = 8
                    cycles_current = 11
                    aircraft_cycles = 10
                    comp_cycles = 9
                    comp_cycles_attach_at = 11

                    month_on = 22
                    month_type = 24
                    month_value = 23
                    month_date = 25

                    days_on = 12
                    days_type = 14
                    days_value = 13
                    days_date = 15
                elif ro[0][165] == 'CALMID':
                    part_name = 0
                    last_time_insp = 94
                    rhll = 82
                    since_time_insp = 93
                    part_desc = 95
                    part_no = 1
                    serial = 2
                    ata_1 = 3
                    ata_2 = 4
                    ata_3 = 5
                    rank = 68
                    inst_date = 6
                    item = 90
                    calm_id = 165
                    delete = 166
                    ste_hr = 172
                    ste_cy = 173
                    ste_overhaul = 174
                    ste_retire = 175

                    cycle_on_install = 8
                    csn = 9
                    cso = 11

                    on_condition = 26
                    U2TT = 48
                    on_condition_hours = 49
                    on_aircraft_hours = 47
                    on_comp_hours = 46

                    comment = 79

                    retirement = 33
                    retirement_hours = 34
                    retirement_aircraft_hours = 36
                    retirement_comp_hours = 35
                    retirement_comp_attach_at = 37
                    retirement_current = 37

                    overhaul = 27
                    overhaul_hours = 28
                    overhaul_aircraft_hours = 30
                    overhaul_comp_hours = 29
                    overhaul_comp_attach_at = 31
                    overhaul_current = 32

                    inspection = 16
                    inspection_hours = 17
                    inspection_aircraft_hours = 19
                    inspection_comp_hours = 18
                    inspection_comp_attach_at = 20
                    inspection_current = 21

                    cycles_on = 7
                    cycles_type = 169
                    cycles_value = 8
                    cycles_current = 11
                    aircraft_cycles = 10
                    comp_cycles = 9
                    comp_cycles_attach_at = 11

                    month_on = 22
                    month_type = 24
                    month_value = 23
                    month_date = 25

                    days_on = 12
                    days_type = 14
                    days_value = 13
                    days_date = 15

                ro.pop(0)
                ro.sort(key=lambda elem: elem[rank])
                for g in ro:
                    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                    # IF COMPONENT ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                    if(str(g[rank][:1]) == 'M' or str(g[rank][:1]) == 'S'):
                        print str(g[part_name])
                        comptype = str(g[rank][:1])
                        if g[part_no].strip() == "":
                            product_id = self.env['product.product'].search([('name', '=', str(g[part_name]))],limit=1)
                        else:
                            product_id = self.env['product.product'].search([('default_code', '=', g[part_no])],limit=1)

                        if(product_id.id == False):
                            product_id = self.env['product.product'].create({
                                'qmap':False,
                                'is_part':True,
                                'name':str(g[part_name]),
                                'short_name':str(g[part_name]),
                                'default_code':str(g[part_no]),
                                'purchase_ok':True,
                                'categ_id':self.env.ref('ib_base_pelita.product_category_pas').id,
                                'type':'product',
                                'tracking':'none',
                                'invoice_policy':'order',
                                'purchase_method':'receive',
                            })
                            self.env.cr.commit()
                        else:
                            product_id.update({
                                'is_part':True,
                                'categ_id':self.env.ref('ib_base_pelita.product_category_pas').id,
                                })
                            self.env.cr.commit()

                        ata_id = self.env['ams.ata'].search([('name', '=', 'xx-xx-xx')])
                        if(g[ata_1] != '' or g[ata_2] != '' or g[ata_3] != ''):
                            ata_string = g[ata_1].zfill(2) + '-' + g[ata_2].zfill(2) + '-' + g[ata_3].zfill(2)
                            ata_id = self.env['ams.ata'].search([('name', '=', ata_string)])
                            if(ata_id.id == False):
                                ata_id = self.env['ams.ata'].create({
                                    'name' : ata_string,
                                    'chapter' : g[ata_1].zfill(2),
                                    'sub_chapter' : g[ata_2].zfill(2),
                                    'description' : 'ATA ' + ata_string,
                                    })
                                self.env.cr.commit()
                        if(g[serial] != ''):
                            serial_id = self.env['stock.production.lot'].search(['&',('product_id','=',product_id.id),('name','=',g[serial])])
                            if(serial_id.id == False):
                                serial_id = self.env['stock.production.lot'].create({
                                    'product_id':product_id.id,
                                    'name':g[serial],
                                })
                            self.env.cr.commit()
                            serial_number = serial_id.id
                        else:
                            serial_number = False

                        if(comptype == 'M'):
                            comp = self.env['ams.component.part'].search(['&',('serial_number','=',serial_number),'&',('auxiliary_id','=',auxiliary_id),('calm_id','=',g[rank])])
                        else:
                            comp = self.env['ams.component.part'].search(['&',('serial_number','=',serial_number),'&',('auxiliary_id','=',auxiliary_id),('calm_id','=',g[rank]+g[part_no])])
                        
                        if(comp.id == False):
                            if comptype != 'M':
                                get_calm_id = self.env['ams.component.part'].search(['&',('auxiliary_id','=',auxiliary_id),('calm_id','=',g[rank].replace('S','M'))])
                            comp = self.env['ams.component.part'].create({
                                'calm_file' : self.filename,
                                'calm_id' : g[rank] if comptype == 'M' else g[rank]+g[part_no],
                                'ata_code' : ata_id.id,
                                'is_subcomp' : True if comptype == 'S' else False,
                                'part_id' : False if comptype == 'M' else get_calm_id.id,
                                'auxiliary_id': False if comptype != 'M' else auxiliary_id,
                                'product_id':product_id.id,
                                'serial_number':serial_number,
                                'comp_timeinstallation' : 0,
                                'comp_cyclesinstallation' : 0,
                                'date_installed' : g[inst_date] if (g[inst_date] != '') else False,
                                'csn' : 0,
                                'tsn' : 0,
                                'is_overhaul' : False,
                                # 'unknown_new' : False,
                                'item' : g[item],
                            })
                            self.env.cr.commit()
                        else:
                            comp.update({
                                'product_id':product_id.id,
                                'serial_number':serial_number,
                                'date_installed' : g[inst_date] if (g[inst_date] != '') else False,
                            })

                        # SERVICE LIFE
                        # ON CONDITION
                        if(g[on_condition].upper() == 'TRUE'):
                            comp.update({
                                'tsn' : ((float(self.auxiliary_id.total_hours) - float(g[on_aircraft_hours])) + float(g[U2TT])),
                                # 'tso': (float(self.fleet_id.total_hours) - float(g[on_aircraft_hours])) + float(g[on_comp_hours]),
                                'comp_timeinstallation' : g[U2TT],
                                'ac_timeinstallation' : g[on_aircraft_hours],
                                'unknown_new' : False,
                            })

                            # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',g[calm_id]),('file','=',g[rank]),('fleet_id','=',self.fleet_id.id)])
                            # if calm_data.id == False:
                            # AIRFRAME ON-CONDITION ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                            # slive = self.env['ams.component.servicelife'].search(['&',('value','=',0),'&',('unit','=','hours'),'&',('part_id','=',comp.id),('action_type','=','oncondition')])
                            if(True):
                                slive = self.env['ams.component.servicelife'].create({
                                    'at_install' : float(g[U2TT]),
                                    'part_id' : comp.id,
                                    'action_type' : 'oncondition',
                                    'unit' : 'hours',
                                    'value' : 0,
                                    'current' : (float(self.auxiliary_id.total_hours) - float(g[on_aircraft_hours])) + float(g[U2TT]), 
                                    'comments' : g[comment],
                                })
                                self.env.cr.commit()
                                # self.env['calm.dict'].create({
                                #     'file' : g[rank],
                                #     'fleet_id' : self.fleet_id.id,
                                #     'part_id' : comp.id,
                                #     'sequence' : g[calm_id],
                                #     'service_life_id' : slive.id,
                                # })
                                # self.env.cr.commit()
                            else :
                                slive.write({
                                    'at_install' : float(g[U2TT]),
                                    'part_id' : comp.id,
                                    'action_type' : 'oncondition',
                                    'unit' : 'hours',
                                    'value' : 0,
                                    'current' : (float(self.auxiliary_id.total_hours) - float(g[on_aircraft_hours])) + float(g[U2TT]),
                                    'comments' : g[comment],    
                                })
                                self.env.cr.commit()
                        # RETIREMENT
                        if(g[retirement].upper() == 'TRUE'):
                            tsn = (float(self.auxiliary_id.total_hours) - float(g[retirement_aircraft_hours]) + float(g[retirement_comp_hours])) if comp.tsn < (float(self.auxiliary_id.total_hours) - float(g[retirement_aircraft_hours]) + float(g[retirement_comp_hours])) else comp.tsn
                            if(tsn > comp.tsn):
                                comp.update({
                                    # 'unknown_new' : False,
                                    'tsn': tsn,
                                    # 'tso': (float(self.fleet_id.total_hours) - float(g[retirement_aircraft_hours]) + float(g[retirement_comp_hours])),
                                    'comp_timeinstallation' : float(g[retirement_comp_hours]),
                                    'ac_timeinstallation' : float(g[retirement_aircraft_hours]),
                                })

                            # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',g[calm_id]),('file','=',g[rank]),('fleet_id','=',self.fleet_id.id)])
                            # if calm_data.id == False:
                            if(True):
                                slive = self.env['ams.component.servicelife'].create({
                                    'at_install' : float(g[retirement_comp_hours]),
                                    'part_id' : comp.id,
                                    'is_major' : True,
                                    'action_type' : 'retirement',
                                    'unit' : 'hours',
                                    'value' : float(g[retirement_hours]),
                                    'current' : (float(self.auxiliary_id.total_hours) - float(g[retirement_aircraft_hours])) + float(g[retirement_comp_hours]), 
                                    'comments' : g[comment],
                                })
                                # if len(g) > 165:
                                #     if(g[ste_retire] != '0' and g[ste_retire] != ''):
                                #         if (calm_data.service_life_id.id != False):
                                #             self.env['airworthy.ste'].create({
                                #                 'service_life_id' : calm_data.service_life_id.id,
                                #                 'value' : float(g[ste_retire])/float(100) * g[retirement_hours],
                                #                 'status' : 'dgcaapprove',
                                #                 })
                                self.env.cr.commit()
                                # self.env['calm.dict'].create({
                                #     'file' : g[rank],
                                #     'fleet_id' : self.fleet_id.id,
                                #     'part_id' : comp.id,
                                #     'sequence' : g[calm_id],
                                #     'service_life_id' : slive.id,
                                # })
                                # self.env.cr.commit()
                            else :
                                # slive = calm_data.service_life_id,
                                # slive.write({
                                #     'at_install' : float(g[retirement_comp_hours]),
                                #     'part_id' : comp.id,
                                #     'is_major' : True,
                                #     'action_type' : 'retirement',
                                #     'unit' : 'hours',
                                #     'value' : g[retirement_hours],
                                #     'current' : (float(self.auxiliary_id.total_hours) - float(g[retirement_comp_attach_at])) + float(g[retirement_comp_hours]),
                                #     'comments' : g[comment],    
                                # })
                                self.env.cr.commit()
                        # OVERHAUL
                        if(g[overhaul].upper() == 'TRUE'):
                            tsn = ((float(g[overhaul_comp_attach_at]) + float(g[overhaul_current]) + float(g[overhaul_comp_hours])) if float(comp.tsn) < float(float(g[overhaul_comp_attach_at]) + float(g[overhaul_current]) + float(g[overhaul_comp_hours])) else float(comp.tsn))
                            is_overhaul = (True if tsn > (float(self.auxiliary_id.total_hours) - float(g[overhaul_aircraft_hours]) + float(g[overhaul_comp_hours])) else False)
                            comp.update({
                                'unknown_new' : False,
                                'is_overhaul' : is_overhaul,
                                'tsn': tsn if (tsn > comp.tsn) else comp.tsn,
                                'tso': (float(self.auxiliary_id.total_hours) - float(g[overhaul_aircraft_hours]) + float(g[overhaul_comp_hours])),
                                'comp_timeinstallation' : float(g[overhaul_comp_hours]),
                                'ac_timeinstallation' : float(g[overhaul_aircraft_hours]),
                            })

                            # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',g[calm_id]),('file','=',g[rank]),('fleet_id','=',self.fleet_id.id)])
                            # if calm_data.id == False:
                            if(True):
                                slive = self.env['ams.component.servicelife'].create({
                                    'at_install' : float(g[overhaul_comp_hours]),
                                    'part_id' : comp.id,
                                    'is_major' : True,
                                    'action_type' : 'overhaul',
                                    'unit' : 'hours',
                                    'value' : float(g[overhaul_hours]),
                                    'overhaul_comp_attach_at' : float(g[overhaul_comp_attach_at]),
                                    'current' : (float(self.auxiliary_id.total_hours) - float(g[overhaul_aircraft_hours])) + float(g[overhaul_comp_hours]), 
                                    'comments' : g[comment],
                                })
                                # if len(g) > 165:
                                #     if(g[ste_overhaul] != '0' and g[ste_overhaul] != ''):
                                #         if (calm_data.service_life_id.id != False):
                                #             self.env['airworthy.ste'].create({
                                #                 'service_life_id' : calm_data.service_life_id.id,
                                #                 'value' : float(g[ste_overhaul])/float(100) * g[overhaul_hours],
                                #                 'status' : 'dgcaapprove',
                                #                 })
                                self.env.cr.commit()
                                # self.env['calm.dict'].create({
                                #     'file' : g[rank],
                                #     'fleet_id' : self.fleet_id.id,
                                #     'part_id' : comp.id,
                                #     'sequence' : g[calm_id],
                                #     'service_life_id' : slive.id,
                                # })
                                # self.env.cr.commit()
                            else :
                                # slive = calm_data.service_life_id,
                                # slive.write({
                                #     'at_install' : float(g[overhaul_comp_hours]),
                                #     'part_id' : comp.id,
                                #     'is_major' : True,
                                #     'action_type' : 'overhaul',
                                #     'unit' : 'hours',
                                #     'value' : g[overhaul_hours],
                                #     'current' : (float(self.auxiliary_id.total_hours) - float(g[overhaul_comp_attach_at])) + float(g[overhaul_comp_hours]),
                                #     'comments' : g[comment],    
                                # })
                                self.env.cr.commit()
                        # INSPECTION
                        if(g[inspection].upper() == 'TRUE'):
                            tsn = (float(self.auxiliary_id.total_hours) - float(g[inspection_aircraft_hours]) + float(g[inspection_comp_hours])) if comp.tsn < (float(self.auxiliary_id.total_hours) - float(g[inspection_aircraft_hours]) + float(g[inspection_comp_hours])) else comp.tsn
                            if(tsn > comp.tsn):
                                comp.update({
                                    # 'unknown_new' : False,
                                    'tsn': tsn,
                                    # 'tso': (float(self.fleet_id.total_hours) - float(g[inspection_aircraft_hours]) + float(g[inspection_comp_hours])),
                                    'comp_timeinstallation' : float(g[inspection_comp_hours]),
                                    'ac_timeinstallation' : float(g[inspection_aircraft_hours]),
                                })

                            # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',g[calm_id]),('file','=',g[rank]),('fleet_id','=',self.fleet_id.id)])
                            # if calm_data.id == False:
                            if(True):
                                slive = self.env['ams.component.servicelife'].create({
                                    'at_install' : float(g[inspection_comp_hours]),
                                    'part_id' : comp.id,
                                    'action_type' : 'inspection',
                                    'unit' : 'hours',
                                    'value' : float(g[inspection_hours]),
                                    'current' : (float(self.auxiliary_id.total_hours) - float(g[inspection_aircraft_hours])) + float(g[inspection_comp_hours]), 
                                    'comments' : g[comment],
                                })
                                # if len(g) > 165:
                                #     if(g[ste_hr] != '0' and g[ste_hr] != ''):
                                #         if (calm_data.service_life_id.id != False):
                                #             self.env['airworthy.ste'].create({
                                #                 'service_life_id' : calm_data.service_life_id.id,
                                #                 'value' : float(g[ste_hr])/float(100) * g[inspection_hours],
                                #                 'status' : 'dgcaapprove',
                                #                 })
                                self.env.cr.commit()
                                # self.env['calm.dict'].create({
                                #     'file' : g[rank],
                                #     'fleet_id' : self.fleet_id.id,
                                #     'part_id' : comp.id,
                                #     'sequence' : g[calm_id],
                                #     'service_life_id' : slive.id,
                                # })
                                # self.env.cr.commit()
                            else :
                                # slive = calm_data.service_life_id,
                                # slive.write({
                                #     'at_install' : float(g[inspection_comp_hours]),
                                #     'part_id' : comp.id,
                                #     'action_type' : 'inspection',
                                #     'unit' : 'hours',
                                #     'value' : g[inspection_hours],
                                #     'current' : (float(self.auxiliary_id.total_hours) - float(g[inspection_comp_attach_at])) + float(g[inspection_comp_hours]),
                                #     'comments' : g[comment],    
                                # })
                                self.env.cr.commit()

                        # CYCLES
                        if(g[cycles_on].upper() == 'TRUE'):
                            if(g[cycles_type] == '1'):
                                slive_type = 'retirement'
                            elif(g[cycles_type] == '2'):
                                slive_type = 'service'
                            elif(g[cycles_type] == '3'):
                                slive_type = 'inspection'
                            elif(g[cycles_type] == '4'):
                                slive_type = 'overhaul'

                            csn = (float(self.auxiliary_id.total_cycles) - float(g[cycle_on_install]) + float(g[comp_cycles])) if comp.tsn < (float(self.auxiliary_id.total_cycles) - float(g[cycle_on_install]) + float(g[comp_cycles])) else comp.csn
                            comp.update({
                                'unknown_new' : False,
                                'csn': (float(csn)),
                                'cso': (float(g[cso])),
                                'comp_cyclesinstallation' : float(g[comp_cycles]),
                                'ac_cyclesinstallation' : float(g[aircraft_cycles]),
                            })

                            # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',g[calm_id]),('file','=',g[rank]),('fleet_id','=',self.fleet_id.id)])
                            # if calm_data.id == False:
                            if(True):
                                print g[comp_cycles] , ' <=> CYCLES'
                                slive = self.env['ams.component.servicelife'].create({
                                    'at_install' : float(g[comp_cycles]),
                                    'part_id' : comp.id,
                                    'action_type' : slive_type,
                                    'unit' : 'cycles',
                                    'value' : float(g[cycles_value]),
                                    'current' : float(g[cycles_current]) + float(g[comp_cycles]),  
                                    'comments' : g[comment],
                                })
                                # if len(g) > 165:
                                #     if(g[ste_cy] != '0' and g[ste_cy] != ''):
                                #         if (calm_data.service_life_id.id != False):
                                #             self.env['airworthy.ste'].create({
                                #                 'service_life_id' : calm_data.service_life_id.id,
                                #                 'value' : float(g[ste_cy])/float(100) * g[cycles_value],
                                #                 'status' : 'dgcaapprove',
                                #                 })
                                self.env.cr.commit()
                                # self.env['calm.dict'].create({
                                #     'file' : g[rank],
                                #     'fleet_id' : self.fleet_id.id,
                                #     'part_id' : comp.id,
                                #     'sequence' : g[calm_id],
                                #     'service_life_id' : slive.id,
                                # })
                                # self.env.cr.commit()
                            else :
                                # slive = calm_data.service_life_id,
                                # print g[comp_cycles] , ' <=> CYCLES'
                                # slive.write({
                                #     'at_install' : float(g[comp_cycles]),
                                #     'part_id' : comp.id,
                                #     'action_type' : slive_type,
                                #     'unit' : 'cycles',
                                #     'value' : g[cycles_value],
                                #     'current' : float(g[cycles_current]) + float(g[comp_cycles]),
                                #     'comments' : g[comment],    
                                # })
                                self.env.cr.commit()
                        # MONTH
                        if(g[month_on].upper() == 'TRUE'):
                            if(g[month_type] == '1'):
                                slive_type = 'inspection'
                            elif(g[month_type] == '2'):
                                slive_type = 'overhaul'
                            elif(g[month_type] == '3'):
                                slive_type = 'retirement'
                            elif(g[month_type] == '4'):
                                slive_type = 'service'

                            if g[month_date] != '':
                                d = str(g[month_date]).split('/')
                                if len(d) == 3:
                                    comp.update({
                                        # 'unknown_new' : False,
                                        'date_installed' : datetime.strptime(g[month_date], '%m/%d/%Y').strftime("%Y-%m-%d")
                                    })
                                else:
                                    comp.update({
                                        # 'unknown_new' : False,
                                        'date_installed' : datetime.strptime(g[month_date], '%Y-%m-%d').strftime("%Y-%m-%d")
                                    })

                            date_val = g[month_date]
                            if(date_val == ''):
                                date_val = g[inst_date]
                            if(date_val != ''):
                                # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',g[calm_id]),('file','=',g[rank]),('fleet_id','=',self.fleet_id.id)])
                                # if calm_data.id == False:
                                if(True):
                                    slive = self.env['ams.component.servicelife'].create({
                                        'part_id' : comp.id,
                                        'action_type' : slive_type,
                                        'unit' : 'month',
                                        'value' : float(g[month_value]),
                                        'current' : False,
                                        'current_date' : date_val, 
                                        'comments' : g[comment],
                                    })
                                    self.env.cr.commit()
                                    # self.env['calm.dict'].create({
                                    #     'file' : g[rank],
                                    #     'fleet_id' : self.fleet_id.id,
                                    #     'part_id' : comp.id,
                                    #     'sequence' : g[calm_id],
                                    #     'service_life_id' : slive.id,
                                    # })
                                    # self.env.cr.commit()
                                else :
                                    # slive = calm_data.service_life_id,
                                    # slive.write({
                                    #     'part_id' : comp.id,
                                    #     'action_type' : slive_type,
                                    #     'unit' : 'month',
                                    #     'value' : g[month_value],
                                    #     'current' : False,
                                    #     'current_date' : date_val,
                                    #     'comments' : g[comment],    
                                    # })
                                    self.env.cr.commit()
                        # DAYS
                        if(g[days_on].upper() == 'TRUE'):
                            if(g[days_type] == '1'):
                                slive_type = 'inspection'
                            elif(g[days_type] == '2'):
                                slive_type = 'overhaul'
                            elif(g[days_type] == '3'):
                                slive_type = 'retirement'
                            elif(g[days_type] == '4'):
                                slive_type = 'service'

                            if g[days_date] != '':
                                d = str(g[days_date]).split('/')
                                if len(d) == 3:
                                    comp.update({
                                        # 'unknown_new' : False,
                                        'date_installed' : datetime.strptime(g[days_date], '%m/%d/%Y').strftime("%Y-%m-%d")
                                    })
                                else:
                                    comp.update({
                                        # 'unknown_new' : False,
                                        'date_installed' : datetime.strptime(g[days_date], '%Y-%m-%d').strftime("%Y-%m-%d")
                                    })

                            date_val = g[days_date]
                            if(date_val == ''):
                                date_val = g[inst_date]
                            if(date_val != ''):
                                # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',g[calm_id]),('file','=',g[rank]),('fleet_id','=',self.fleet_id.id)])
                                # if calm_data.id == False:
                                if(True):
                                    slive = self.env['ams.component.servicelife'].create({
                                        'part_id' : comp.id,
                                        'action_type' : slive_type,
                                        'unit' : 'days',
                                        'value' : float(g[days_value]),
                                        'current' : False,
                                        'current_date' : date_val, 
                                        'comments' : g[comment],
                                    })
                                    self.env.cr.commit()
                                    # self.env['calm.dict'].create({
                                    #     'file' : g[rank],
                                    #     'fleet_id' : self.fleet_id.id,
                                    #     'part_id' : comp.id,
                                    #     'sequence' : g[calm_id],
                                    #     'service_life_id' : slive.id,
                                    # })
                                    # self.env.cr.commit()
                                else :
                                    # slive = calm_data.service_life_id,
                                    # slive.write({
                                    #     'part_id' : comp.id,
                                    #     'action_type' : slive_type,
                                    #     'unit' : 'days',
                                    #     'value' : g[days_value],
                                    #     'current' : False,
                                    #     'current_date' : date_val,
                                    #     'comments' : g[comment],    
                                    # })
                                    self.env.cr.commit()


                    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                    # IF INSPECTION :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                    else:
                        if len(g) > 155:
                            print 'inspection ::' + str(g[part_name]) + ' desc : ' + str(g[part_desc])+ ' last : ' + str(g[rhll])+ ' since : ' + str(g[since_time_insp])
                            if(str(g[delete]).upper() == 'FALSE' and g[rank] == ''):
                                # PERHITUNGAN
                                comp_tso = 0
                                comp_cso = 0
                                comp_tsn = 0
                                comp_csn = 0
                                slive_type = 'inspection'

                                ata_id = self.env['ams.ata'].search([('name', '=', 'xx-xx-xx')])
                                if(g[ata_1] != '' or g[ata_2] != '' or g[ata_3] != ''):
                                    ata_string = g[ata_1].zfill(2) + '-' + g[ata_2].zfill(2) + '-' + g[ata_3].zfill(2)
                                    ata_id = self.env['ams.ata'].search([('name', '=', ata_string)])
                                    if(ata_id.id == False):
                                        ata_id = self.env['ams.ata'].create({
                                            'name' : ata_string,
                                            'chapter' : g[ata_1].zfill(2),
                                            'sub_chapter' : g[ata_2].zfill(2),
                                            'description' : 'ATA ' + ata_string,
                                            })
                                        self.env.cr.commit()

                                insp = self.env['ams.inspection'].create({
                                    'auxiliary_id' : self.auxiliary_id.id,
                                    'inspection_type' : str(g[part_name]),
                                    'desc' : str(g[part_desc]),
                                    'ata_code' : ata_id.id,
                                    'one_time_insp' : False,
                                    'last_insp' : g[rhll],
                                    'since_insp' : g[since_time_insp],
                                    'install_at' : g[inst_date],
                                })
                                self.env.cr.commit()

                                # SERVICE LIFE
                                # INSPECTION
                                if(g[inspection].upper() == 'TRUE'):
                                    slive = self.env['ams.component.servicelife'].create({
                                        'inspection_id' : insp.id,
                                        'action_type' : 'inspection',
                                        'unit' : 'hours',
                                        'value' : float(g[inspection_hours]),
                                        'current' : float(self.auxiliary_id.total_hours) - float(g[rhll]), 
                                        'comments' : g[comment],
                                    })
                                    self.env.cr.commit()

                                # CYCLES
                                if(g[cycles_on].upper() == 'TRUE'):
                                    if(g[cycles_type] == '1'):
                                        slive_type = 'retirement'
                                    elif(g[cycles_type] == '2'):
                                        slive_type = 'service'
                                    elif(g[cycles_type] == '3'):
                                        slive_type = 'inspection'
                                    elif(g[cycles_type] == '4'):
                                        slive_type = 'overhaul'

                                    slive = self.env['ams.component.servicelife'].create({
                                        'inspection_id' : insp.id,
                                        'action_type' : slive_type,
                                        'unit' : 'cycles',
                                        'value' : float(g[cycles_value]),
                                        'current' : float(g[cycles_current]) + float(g[comp_cycles]), 
                                        'comments' : g[comment],
                                    })
                                    self.env.cr.commit()
                                # MONTH
                                if(g[month_on].upper() == 'TRUE'):
                                    if(g[month_type] == '1'):
                                        slive_type = 'inspection'
                                    elif(g[month_type] == '2'):
                                        slive_type = 'overhaul'
                                    elif(g[month_type] == '3'):
                                        slive_type = 'retirement'
                                    elif(g[month_type] == '4'):
                                        slive_type = 'service'

                                    date_val = g[month_date]
                                    if(date_val == ''):
                                        date_val = g[inst_date]
                                    if(date_val != ''):
                                        slive = self.env['ams.component.servicelife'].create({
                                            'inspection_id' : insp.id,
                                            'action_type' : slive_type,
                                            'unit' : 'month',
                                            'value' : float(g[month_value]),
                                            'current' : False,
                                            'current_date' : date_val, 
                                            'comments' : g[comment],
                                        })
                                        self.env.cr.commit()
                                # DAYS
                                if(g[days_on].upper() == 'TRUE'):
                                    if(g[days_type] == '1'):
                                        slive_type = 'inspection'
                                    elif(g[days_type] == '2'):
                                        slive_type = 'overhaul'
                                    elif(g[days_type] == '3'):
                                        slive_type = 'retirement'
                                    elif(g[days_type] == '4'):
                                        slive_type = 'service'

                                    date_val = g[days_date]
                                    if(date_val == ''):
                                        date_val = g[inst_date]
                                    if(date_val != ''):
                                        slive = self.env['ams.component.servicelife'].create({
                                            'inspection_id' : insp.id,
                                            'action_type' : slive_type,
                                            'unit' : 'days',
                                            'value' : float(g[days_value]),
                                            'current' : False,
                                            'current_date' : date_val, 
                                            'comments' : g[comment],
                                        })
                                        self.env.cr.commit()