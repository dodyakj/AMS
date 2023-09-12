# -*- coding: utf-8 -*-
# import pandas
from odoo import models, fields, api
import os, sys, csv, base64, io, zipfile, tempfile
from dbfpy import dbf

zippath = "E:\\AMS\\PSW.zip"
zipextract = "E:\\AMS\\extract\\"

class ams_calm_dict(models.Model):
    _name = 'calm.dict'


    file = fields.Char(string='CALM Data')
    sequence = fields.Char(string='Sequence Param')
    fleet_id = fields.Many2one('aircraft.acquisition', string='Aircraft')
    engine_id = fields.Many2one('engine.type', string='Engine')
    auxiliary_id = fields.Many2one('auxiliary.type', string='Auxiliary')
    part_id = fields.Many2one('ams.component.part', string='Part')
    inspection_id = fields.Many2one('ams.inspection', string='Inspection')
    service_life_id = fields.Many2one('ams.component.servicelife', string='Service Life')

class ams_calm(models.Model):
    _name = 'ams.calm'
    app_path = "E:\\AMS\\"

    # name = fields.Char(string='Text')
    file = fields.Binary(string='Upload', size_limit=999999)
    filename = fields.Char('File Name')


    def convert(self):
        with zipfile.ZipFile(zippath, 'r') as zip_ref:
            zip_ref.extractall(zipextract)
        for dirpath, dirnames, filenames in os.walk(zipextract):
            for filename in filenames:
                if filename.endswith('.DBF'):
                    print "Converting %s to csv" % filename
                    csv_fn = zipextract + filename[:-4]+ ".csv"
                    csv_fn_hst = zipextract + filename[:-4]+ "_hst.csv"
                    with open(csv_fn,'wb') as csvfile:
                        if os.path.exists(zipextract + filename):
                            try :
                                in_db = dbf.Dbf(zipextract + filename)
                                out_csv = csv.writer(csvfile, delimiter=";")
                                names = []
                                for field in in_db.header.fields:
                                    names.append(field.name)
                                out_csv.writerow(names)
                                try :
                                    if in_db != False:
                                        # print in_db
                                        for rec in in_db:
                                            if rec.deleted == False:
                                                out_csv.writerow(rec.fieldData)
                                except Exception as te:
                                    print(te)
                                in_db.close()
                            except Exception as te:
                                print(te)
                    with open(csv_fn_hst,'wb') as csvfile:
                        if os.path.exists(zipextract + filename):
                            try :
                                in_db = dbf.Dbf(zipextract + filename)
                                out_csv = csv.writer(csvfile, delimiter=";")
                                names = []
                                for field in in_db.header.fields:
                                    names.append(field.name)
                                out_csv.writerow(names)
                                try :
                                    if in_db != False:
                                        # print in_db
                                        for rec in in_db:
                                            if rec.deleted != False:
                                                out_csv.writerow(rec.fieldData)
                                except Exception as te:
                                    print(te)
                                in_db.close()
                            except Exception as te:
                                print(te)

    def comply(self):
        # with open("tmmptfile.zip", "wb") as fh:
        #     fh.write(self.file.decode('base64'))
        # with file("tmmptfile.zip") as f:

        # with zipfile.ZipFile("upload.zip", 'r') as zip_ref:
        #     zip_ref.extractall('./extract')


        #     for dirpath, dirnames, filenames in os.walk('./extract'):
        #         for filename in filenames:
        #             if filename.endswith('.DBF'):
        #                 print "Converting %s to csv" % filename
        #                 csv_fn = zipextract + filename[:-4]+ ".csv"
        #                 csv_fn_hst = zipextract + filename[:-4]+ "_hst.csv"
        #                 with open(csv_fn,'wb') as csvfile:
        #                     if os.path.exists(zipextract + filename):
        #                         try :
        #                             in_db = dbf.Dbf(zipextract + filename)
        #                             out_csv = csv.writer(csvfile, delimiter=";")
        #                             names = []
        #                             for field in in_db.header.fields:
        #                                 names.append(field.name)
        #                             out_csv.writerow(names)
        #                             try :
        #                                 if in_db != False:
        #                                     # print in_db
        #                                     for rec in in_db:
        #                                         if rec.deleted == False:
        #                                             out_csv.writerow(rec.fieldData)
        #                             except Exception as te:
        #                                 print(te)
        #                             in_db.close()
        #                         except Exception as te:
        #                             print(te)
        #                 with open(csv_fn_hst,'wb') as csvfile:
        #                     if os.path.exists(zipextract + filename):
        #                         try :
        #                             in_db = dbf.Dbf(zipextract + filename)
        #                             out_csv = csv.writer(csvfile, delimiter=";")
        #                             names = []
        #                             for field in in_db.header.fields:
        #                                 names.append(field.name)
        #                             out_csv.writerow(names)
        #                             try :
        #                                 if in_db != False:
        #                                     # print in_db
        #                                     for rec in in_db:
        #                                         if rec.deleted != False:
        #                                             out_csv.writerow(rec.fieldData)
        #                             except Exception as te:
        #                                 print(te)
        #                             in_db.close()
        #                         except Exception as te:
        #                             print(te)

        self.getata()

        # file = open(app_path+"extract\\FLEET.csv", "r") 
        calmdict = 0
        file_type = 1
        used = 3
        reg_name = 4
        type_name = 6
        msn = 7
        hours = 9
        cycles = 10
        location = 40
        hsinceoh = 77
        engine1 = 14
        engine2 = 15
        engine3 = 16
        engine4 = 17
        aux1 = 24
        # ro = file.readlines()
        with open(zipextract+"FLEET.csv") as myFile:  
            print 'reading FLEET.csv'
            ro = list(csv.reader(myFile, delimiter=';'))
            # CREATING ENGINE
            for g in ro:
                # print '========================================================'
                # ro = csv.reader(f, delimiter=';')
                data = g
                # print g
                # print data
                # print len(data)
                if len(data) > 40:
                    print 'data > 40'
                    if data[file_type] == 'UE' and data[used].upper() == 'TRUE':
                        print 'Engine'
                        # AC_REG = data[reg_name].replace(" ","")
                        # print AC_REG
                        engine = self.env['engine.type'].search([('name','=',data[msn])])
                        engtype = self.env['engine.engine'].search([('name','=',data[type_name])])
                        aclocation = self.env['base.operation'].search([('code','=',data[location])])

                        if(engtype.id == False):
                            engtype = self.env['engine.engine'].create({
                                'name' : data[type_name],
                                })
                        
                        if(engine.id == False):
                            tengine = self.env['engine.type'].create({
                                'name' : data[msn],
                                'engine_model' : engtype.id,
                                'esn' : data[msn],
                                'engine_tsn' : data[hours],
                                'engine_csn' : data[cycles],
                                'total_hours' : data[hsinceoh] if len(data) >= 77 else data[hours],
                                'total_cycles' : data[cycles],
                                'engine_tslsv' : data[hours],
                                'engine_cslsv' : data[cycles],
                                })
                            self.env.cr.commit()
                        elif(engine.total_hours < data[hours]):
                            engine.write({
                                'name' : data[msn],
                                'engine_model' : engtype.id,
                                'esn' : data[msn],
                                'engine_tsn' : data[hours],
                                'engine_csn' : data[cycles],
                                'total_hours' : data[hsinceoh] if len(data) >= 77 else data[hours],
                                'total_cycles' : data[cycles],
                                'engine_tslsv' : data[hours],
                                'engine_cslsv' : data[cycles],
                                })
                        calm_data = self.env['calm.dict'].search(['&',('file','=',data[calmdict]),('engine_id','=',engine.id if engine.id != False else tengine.id)])
                        if calm_data.id == False:
                            self.env['calm.dict'].create({
                                'file' : data[calmdict],
                                'engine_id' : engine.id if engine.id != False else tengine.id,
                                })
                            self.env.cr.commit()
                        # if(engine.id == False or float(engine.engine_tsn) < float(data[hours])):
                        if(True):
                            engine = self.env['engine.type'].search([('name','=',data[msn])])
                            self.env['ams.component.part'].search([('engine_id','=',engine.id)]).unlink()
                            self.env['ams.inspection'].search([('engine_id','=',engine.id)]).unlink()
                            self.set_component_engine(engine.id,data[calmdict],'M')
                            self.set_component_engine(engine.id,data[calmdict],'S')
                            self.set_inspection_engine(engine.id,data[calmdict],'')
                else:
                    print 'data <= 40 STOP!!!'
       
        with open(zipextract+"FLEET.csv") as myFile:
            # CREATING AUXILIARY
            ro = list(csv.reader(myFile, delimiter=';'))
            for g in ro:
                # print '========================================================'
                data = g
                # print g
                # print data
                # print len(data)
                if len(data) > 40:
                    print 'data > 40'
                    if data[file_type] == 'UX' and data[used].upper() == 'TRUE':
                        print 'auxiliary'
                        # AC_REG = data[reg_name].replace(" ","")
                        # print AC_REG
                        auxiliary = self.env['auxiliary.type'].search([('name','=',data[msn])])
                        engtype = self.env['auxiliary.auxiliary'].search([('name','=',data[type_name])])
                        aclocation = self.env['base.operation'].search([('code','=',data[location])])

                        if(engtype.id == False):
                            engtype = self.env['auxiliary.auxiliary'].create({
                                'name' : data[type_name],
                                })
                        
                        if(auxiliary.id == False):
                            tauxiliary = self.env['auxiliary.type'].create({
                                'name' : data[msn],
                                'auxiliary_model' : engtype.id,
                                'esn' : data[msn],
                                'auxiliary_tsn' : data[hours],
                                'auxiliary_csn' : data[cycles],
                                'total_hours' : data[hsinceoh] if len(data) >= 77 else data[hours],
                                'total_cycles' : data[cycles],
                                'auxiliary_tslsv' : data[hours],
                                'auxiliary_cslsv' : data[cycles],
                                })
                            self.env.cr.commit()
                        elif(auxiliary.auxiliary_tsn < data[hours]):
                            auxiliary.write({
                                'name' : data[msn],
                                'auxiliary_model' : engtype.id,
                                'esn' : data[msn],
                                'auxiliary_tsn' : data[hours],
                                'auxiliary_csn' : data[cycles],
                                'total_hours' : data[hsinceoh] if len(data) >= 77 else data[hours],
                                'total_cycles' : data[cycles],
                                'auxiliary_tslsv' : data[hours],
                                'auxiliary_cslsv' : data[cycles],
                                })
                        calm_data = self.env['calm.dict'].search(['&',('file','=',data[calmdict]),('auxiliary_id','=', auxiliary.id  if auxiliary.id != False else tauxiliary.id)])
                        # calm_data = self.env['calm.dict'].search([('file','=',data[calmdict])])
                        if calm_data.id == False:
                            self.env['calm.dict'].create({
                                'file' : data[calmdict],
                                'auxiliary_id' : auxiliary.id  if auxiliary.id != False else tauxiliary.id,
                                })
                            self.env.cr.commit()
                        # if(auxiliary.id == False or float(auxiliary.auxiliary_tsn) < float(data[hours])):
                        if(True):
                            auxiliary = self.env['auxiliary.type'].search([('name','=',data[msn])])
                            self.env['ams.component.part'].search([('auxiliary_id','=',auxiliary.id)]).unlink()
                            self.env['ams.inspection'].search([('auxiliary_id','=',auxiliary.id)]).unlink()
                            self.set_component_auxiliary(auxiliary.id,data[calmdict],'M')
                            self.set_component_auxiliary(auxiliary.id,data[calmdict],'S')
                            self.set_inspection_auxiliary(auxiliary.id,data[calmdict],'')
                else:
                    print 'data <= 40'
        with open(zipextract+"FLEET.csv") as myFile:
            # CREATING AIRCRAFT
            ro = list(csv.reader(myFile, delimiter=';'))
            for g in ro:
                # print '========================================================'
                data = g
                # print g
                # print data
                # print len(data)
                if(len(data) > 40):
                    print 'data > 40'
                    if(data[reg_name] != 'DESIGNATOR'):
                        print 'check designator'
                        # print 'Something went wrong'
                        # sys.exit(0)
                        # if len(data) > 40:
                        if data[file_type] == 'UA' and data[used].upper() == 'TRUE':
                            print 'Aircraft'
                            AC_REG = data[reg_name].replace(" ","")
                            print AC_REG
                            acraft = self.env['aircraft.acquisition'].search([('name','=',AC_REG)])
                            actype = self.env['aircraft.aircraft'].search([('name','=',data[type_name])])
                            aclocation = self.env['base.operation'].search([('code','=',data[location])])

                            if(actype.id == False):
                                typeid = self.env['aircraft.type'].create({
                                    'name' : data[type_name],
                                    })
                                actype = self.env['aircraft.aircraft'].create({
                                    'name' : data[type_name],
                                    'aircraft_type_id' : typeid.id,
                                    'aircraft_categ' : 'fixedwing',
                                    'active' : True,
                                    })
                            
                            if(acraft.id == False):
                                tacraft = self.env['aircraft.acquisition'].create({
                                    'name' : AC_REG,
                                    'license_plate' : AC_REG,
                                    'aircraft_name' : actype.id,
                                    'aircraft_type_id' : actype.aircraft_type_id.id,
                                    'vin_sn' : data[msn],
                                    'total_hours' : data[hours],
                                    'total_landings' : data[cycles],
                                    'location' : aclocation.id,
                                    'engine_type_id' : False if data[engine1] == '' else self.env['calm.dict'].search(['&',('file','=',data[engine1]),('engine_id','!=',False)]).engine_id.id,
                                    'engine2_type_id' : False if data[engine2] == '' else self.env['calm.dict'].search(['&',('file','=',data[engine2]),('engine_id','!=',False)]).engine_id.id,
                                    'engine3_type_id' : False if data[engine3] == '' else self.env['calm.dict'].search(['&',('file','=',data[engine3]),('engine_id','!=',False)]).engine_id.id,
                                    'engine4_type_id' : False if data[engine4] == '' else self.env['calm.dict'].search(['&',('file','=',data[engine4]),('engine_id','!=',False)]).engine_id.id,
                                    'auxiliary_type_id' : False if data[aux1] == '' else self.env['calm.dict'].search(['&',('file','=',data[aux1]),('auxiliary_id','!=',False)]).auxiliary_id.id,
                                    })
                                self.env.cr.commit()
                            elif(acraft.total_hours < data[hours]):
                                acraft.write({
                                    'name' : AC_REG,
                                    'license_plate' : AC_REG,
                                    'aircraft_name' : actype.id,
                                    'aircraft_type_id' : actype.aircraft_type_id.id,
                                    'vin_sn' : data[msn],
                                    'total_hours' : data[hours],
                                    'total_landings' : data[cycles],
                                    'location' : aclocation.id,
                                    'engine_type_id' : False if data[engine1] == '' else self.env['calm.dict'].search(['&',('file','=',data[engine1]),('engine_id','!=',False)]).engine_id.id,
                                    'engine2_type_id' : False if data[engine2] == '' else self.env['calm.dict'].search(['&',('file','=',data[engine2]),('engine_id','!=',False)]).engine_id.id,
                                    'engine3_type_id' : False if data[engine3] == '' else self.env['calm.dict'].search(['&',('file','=',data[engine3]),('engine_id','!=',False)]).engine_id.id,
                                    'engine4_type_id' : False if data[engine4] == '' else self.env['calm.dict'].search(['&',('file','=',data[engine4]),('engine_id','!=',False)]).engine_id.id,
                                    'auxiliary_type_id' : False if data[aux1] == '' else self.env['calm.dict'].search(['&',('file','=',data[aux1]),('auxiliary_id','!=',False)]).auxiliary_id.id,
                                    })
                            calm_data = self.env['calm.dict'].search([('file','=',data[calmdict])])
                            if calm_data.id == False:
                                self.env['calm.dict'].create({
                                    'file' : data[calmdict],
                                    'fleet_id' : acraft.id if acraft.id != False else tacraft.id,
                                    })
                            # if(acraft.id == False or float(acraft.total_hours) < float(data[hours])):
                            acraft = self.env['aircraft.acquisition'].search([('name','=',AC_REG)])
                            self.env['ams.component.part'].search([('fleet_id','=',acraft.id)]).unlink()
                            self.env['ams.inspection'].search([('fleet_id','=',acraft.id)]).unlink()
                            self.set_component(acraft.name,data[calmdict],'M')
                            self.set_component(acraft.name,data[calmdict],'S')
                            self.set_inspection(acraft.name,data[calmdict],'')
                    else:
                        print 'check designator fail STOP!!!'
                else:
                    print 'data <= 40'
        self.comply2()

    def getata(self):
        # file = open(app_path+"extract\\ATAS.csv", "r") 

        ata_1 = 0
        ata_2 = 1
        ata_3 = 2
        atadesc = 3
        chapter = 4
        subchapter = 5

        # ro = file.readlines()
        with open(zipextract+"ATAS.csv") as myFile:  
            ro = list(csv.reader(myFile, delimiter=';'))
            # CREATING ENGINE
            for g in ro: 
                # print '========================================================'
                data = g
                # print data
                # print len(data)
                if len(data) > 4 and data[0] != 'ATA1':
                    ata_string = data[ata_1].zfill(2) + '-' + data[ata_2].zfill(2) + '-' + data[ata_3].zfill(2)
                    ata_id = self.env['ams.ata'].search([('name', '=', ata_string)])
                    if(ata_id.id == False):
                        ata_id = self.env['ams.ata'].create({
                            'name' : ata_string,
                            'chapter' : data[ata_1].zfill(2),
                            'sub_chapter' : data[ata_2].zfill(2),
                            'description' : 'ATA ' + data[atadesc],
                            })
                    else:
                        ata_id.update({
                            'name' : ata_string,
                            'chapter' : data[ata_1].zfill(2),
                            'sub_chapter' : data[ata_2].zfill(2),
                            'description' : 'ATA ' + data[atadesc],
                            })
        

    def comply2(self):
        print 'GET UTILITY'
        # reg_name = 0
        # ac_hours = 1
        # ac_cycles = 2
        # en_cycles = 3
        # en1_hours = 4
        # en2_hours = 5
        # en3_hours = 6
        # en4_hours = 7
        # aux_cycles = 8
        # aux_hours = 9
        
        with open(zipextract+"AIRUTZ.csv") as myFile:  
            ro = list(csv.reader(myFile, delimiter=';'))
            # CREATING ENGINE
            for g in ro: 
                # print '========================================================'
                data = g
                # print data
                # print len(data)
                if len(data) > 8:
                    reg_name = 0
                    ac_hours = 1
                    ac_cycles = 2
                    en_cycles = 3
                    en1_hours = 4
                    en2_hours = 5
                    en3_hours = 6
                    en4_hours = 7
                    aux_cycles = 8
                    aux_hours = 9
                else:
                    reg_name = 0
                    ac_hours = 1
                    ac_cycles = 2
                    en_cycles = 3
                    en1_hours = 4
                    en2_hours = 5
                    en3_hours = 4
                    en4_hours = 5
                    aux_cycles = 6
                    aux_hours = 7
                if len(data) >= 8 and data[0] != 'DESIG':
                    AC_REG = data[reg_name].replace(" ","")
                    print 'search airutz for ' + AC_REG
                    acraft = self.env['aircraft.acquisition'].search([('name','=',AC_REG)])
                    if acraft.id != False:
                        self.env['ams.daily'].create({
                            'fleet_id' : acraft.id,
                            'aircraft_hours' : data[ac_hours],
                            'aircraft_cycles' : data[ac_cycles],
                            'engine1_id' : acraft.engine_type_id.id,
                            'engine2_id' : acraft.engine2_type_id.id,
                            'engine3_id' : acraft.engine3_type_id.id,
                            'engine4_id' : acraft.engine4_type_id.id,
                            'engine1_hours' : data[en1_hours] if (data[en1_hours] != 0) else data[ac_hours],
                            'engine2_hours' : data[en2_hours] if (data[en2_hours] != 0) else data[ac_hours],
                            'engine3_hours' : data[en3_hours] if (data[en3_hours] != 0) else data[ac_hours],
                            'engine4_hours' : data[en4_hours] if (data[en4_hours] != 0) else data[ac_hours],
                            'engine1_cycles' : data[en_cycles],
                            'engine2_cycles' : data[en_cycles],
                            'engine3_cycles' : data[en_cycles],
                            'engine4_cycles' : data[en_cycles],
                            'auxiliary1_id' : acraft.auxiliary_type_id.id,
                            'auxiliary1_hours' : data[aux_hours] if (data[aux_hours] != 0) else data[ac_hours],
                            'auxiliary1_cycles' : data[aux_cycles],
                            })

    def set_component(self,AC_REG,calm_file,comptype):
        acraft = self.env['aircraft.acquisition'].search([('name','=',AC_REG)])
        # self.env['ams.component.part'].search([('fleet_id','=',acraft.id)]).unlink()
        print 'Reading :: ' + str(calm_file)
        if(os.path.isfile(zipextract+str(calm_file)+".csv")):
            with open(zipextract+str(calm_file)+".csv") as myFile:  
                ro = list(csv.reader(myFile, delimiter=';'))
                acraft = self.env['aircraft.acquisition'].search([('name','=',AC_REG)])
                # file = open(zipextract+str(calm_file)+".csv", "r")
                # ro = file.readlines()
                if(len(ro) >= 1):
                    if(ro[0][155] == 'CALMID'):
                        part_name = 0
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
                    
                    elif(ro[0][165] == 'CALMID'):
                        part_name = 0
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

                    for g in ro:
                        data = g

                        if len(data) > 155:
                            print data[part_name] + ' inst at ' + data[inst_date] + comptype
                            if(str(data[delete]).upper() == 'FALSE' and data[rank].find(comptype) != -1):
                                data = g

                                # PERHITUNGAN
                                comp_tso = 0
                                comp_cso = 0
                                comp_tsn = 0
                                comp_csn = 0

                                if(data[part_no].strip() == ''):
                                    product_id = self.env['product.product'].search([('name', '=', str(data[part_name]))],limit=1)
                                else:
                                    product_id = self.env['product.product'].search([('default_code', '=', data[part_no])],limit=1)

                                if(product_id.id == False):
                                    product_id = self.env['product.product'].create({
                                        'qmap':False,
                                        'is_part':True,
                                        'name':str(data[part_name]),
                                        'short_name':str(data[part_name]),
                                        'default_code':str(data[part_no]),
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
                                if(data[ata_1] != '' or data[ata_2] != '' or data[ata_3] != ''):
                                    ata_string = data[ata_1].zfill(2) + '-' + data[ata_2].zfill(2) + '-' + data[ata_3].zfill(2)
                                    ata_id = self.env['ams.ata'].search([('name', '=', ata_string)])
                                    if(ata_id.id == False):
                                        ata_id = self.env['ams.ata'].create({
                                            'name' : ata_string,
                                            'chapter' : data[ata_1].zfill(2),
                                            'sub_chapter' : data[ata_2].zfill(2),
                                            'description' : 'ATA ' + ata_string,
                                            })

                                if(data[serial] != ''):
                                    serial_id = self.env['stock.production.lot'].search(['&',('product_id','=',product_id.id),('name','=',data[serial])])
                                    if(serial_id.id == False):
                                        serial_id = self.env['stock.production.lot'].create({
                                            'product_id':product_id.id,
                                            'name':data[serial],
                                        })
                                    self.env.cr.commit()
                                    # comp = self.env['ams.component.part'].search(['&','&','&',('fleet_id','=',acraft.id),('product_id', '=' ,product_id.id),('serial_number', '=' ,serial_id.id),('item','=',data[item])], limit=1)
                                    serial_number = serial_id.id
                                else:
                                    # comp = self.env['ams.component.part'].search(['&','&',('fleet_id','=',acraft.id),('product_id', '=' ,product_id.id),('item','=',data[item])], limit=1)
                                    serial_number = False
                                # comp = self.env['calm.dict'].search(['&','&',('service_life_id','=',False),('sequence','=',data[calm_id]),('fleet_id','=',acraft.id)],limit=1).part_id
                                if(comptype == 'M'):
                                    comp = self.env['ams.component.part'].search(['&',('serial_number','=',serial_number),'&',('calm_file','=',calm_file),('calm_id','=',data[rank])])
                                else:
                                    comp = self.env['ams.component.part'].search(['&',('serial_number','=',serial_number),'&',('calm_file','=',calm_file),('calm_id','=',data[rank]+data[part_no])])
                                print data[rank]
                                if(comp.id == False):
                                    if comptype != 'M':
                                        get_calm_id = self.env['ams.component.part'].search(['&',('calm_file','=',calm_file),('calm_id','=',data[rank].replace('S','M'))])
                                        # get_calm_id = self.env['calm.dict'].search(['&','&',('fleet_id','=',acraft.id),('service_life_id','=',False),('file','=',data[rank].replace('S','M'))])
                                        # if(len(get_calm_id) > 1):
                                        #     for calms in get_calm_id:
                                        #         if(calms.part_id.ata_code.name[:5] == ata_id.name[:5]):
                                        #             get_calm_id = calms
                                    # else:
                                    #     f= open("listingcomp.txt","a+")
                                    #     f.write(AC_REG + ' : ' + g)
                                    #     f.close() 
                                    if(comptype == 'M' or (comptype != 'S' and get_calm_id.id != False)):
                                        comp = self.env['ams.component.part'].create({
                                            'calm_file' : calm_file,
                                            'calm_id' : data[rank] if comptype == 'M' else data[rank]+data[part_no],
                                            'ata_code' : ata_id.id,
                                            'is_subcomp' : True if comptype == 'S' else False,
                                            'part_id' : False if comptype == 'M' else get_calm_id.id,
                                            'fleet_id': False if comptype != 'M' else acraft.id,
                                            'product_id':product_id.id,
                                            'serial_number':serial_number,
                                            'comp_timeinstallation' : 0,
                                            'comp_cyclesinstallation' : 0,
                                            'date_installed' : data[inst_date] if (data[inst_date] != '') else False,
                                            'csn' : 0,
                                            'tsn' : 0,
                                            'is_overhaul' : False,
                                            # 'unknown_new' : False,
                                            'item' : data[item],
                                        })
                                        self.env.cr.commit()
                                    
                                    calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','=',False),('sequence','=',data[calm_id]),('file','=',data[rank]),('fleet_id','=',acraft.id)])
                                    if calm_data.id == False:
                                        self.env['calm.dict'].create({
                                            'file' : data[rank],
                                            'fleet_id' : acraft.id,
                                            'part_id' : comp.id,
                                            'sequence' : data[calm_id],
                                        })
                                        self.env.cr.commit()
                                else:
                                    comp.update({
                                        # 'fleet_id':acraft.id,
                                        'product_id':product_id.id,
                                        'serial_number':serial_number,
                                        # 'comp_timeinstallation' : 0,
                                        # 'comp_cyclesinstallation' : 0,
                                        'date_installed' : data[inst_date] if (data[inst_date] != '') else False,
                                        # 'csn' : 0,
                                        # 'tsn' : 0,
                                        # 'is_overhaul' : False,
                                        # 'unknown_new' : False,
                                        'item' : data[item],
                                    })
                                # SERVICE LIFE
                                # ON CONDITION
                                if(data[on_condition].upper() == 'TRUE'):
                                    comp.update({
                                        'tsn' : ((float(acraft.total_hours) - float(data[on_aircraft_hours])) + float(data[U2TT])),
                                        # 'tso': (float(acraft.total_hours) - float(data[on_aircraft_hours])) + float(data[on_comp_hours]),
                                        'comp_timeinstallation' : data[U2TT],
                                        'ac_timeinstallation' : data[on_aircraft_hours],
                                        'unknown_new' : False,
                                    })

                                    # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]),('file','=',data[rank]),('fleet_id','=',acraft.id)])
                                    # if calm_data.id == False:
                                    # AIRFRAME ON-CONDITION ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                                    # slive = self.env['ams.component.servicelife'].search(['&',('value','=',0),'&',('unit','=','hours'),'&',('part_id','=',comp.id),('action_type','=','oncondition')])
                                    if(True):
                                        slive = self.env['ams.component.servicelife'].create({
                                            'at_install' : float(data[U2TT]),
                                            'part_id' : comp.id,
                                            'action_type' : 'oncondition',
                                            'unit' : 'hours',
                                            'value' : 0,
                                            'current' : (float(acraft.total_hours) - float(data[on_aircraft_hours])) + float(data[U2TT]), 
                                            'comments' : data[comment],
                                        })
                                        self.env.cr.commit()
                                        # self.env['calm.dict'].create({
                                        #     'file' : data[rank],
                                        #     'fleet_id' : acraft.id,
                                        #     'part_id' : comp.id,
                                        #     'sequence' : data[calm_id],
                                        #     'service_life_id' : slive.id,
                                        # })
                                        # self.env.cr.commit()
                                    else :
                                        slive.write({
                                            'at_install' : float(data[U2TT]),
                                            'part_id' : comp.id,
                                            'action_type' : 'oncondition',
                                            'unit' : 'hours',
                                            'value' : 0,
                                            'current' : (float(acraft.total_hours) - float(data[on_aircraft_hours])) + float(data[U2TT]),
                                            'comments' : data[comment],    
                                        })
                                        self.env.cr.commit()
                                # RETIREMENT
                                if(data[retirement].upper() == 'TRUE'):
                                    tsn = (float(acraft.total_hours) - float(data[retirement_aircraft_hours]) + float(data[retirement_comp_hours])) if comp.tsn < (float(acraft.total_hours) - float(data[retirement_aircraft_hours]) + float(data[retirement_comp_hours])) else comp.tsn
                                    if(tsn > comp.tsn):
                                        comp.update({
                                            # 'unknown_new' : False,
                                            'tsn': tsn,
                                            # 'tso': (float(acraft.total_hours) - float(data[retirement_aircraft_hours]) + float(data[retirement_comp_hours])),
                                            'comp_timeinstallation' : float(data[retirement_comp_hours]),
                                            'ac_timeinstallation' : float(data[retirement_aircraft_hours]),
                                        })

                                    # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]),('file','=',data[rank]),('fleet_id','=',acraft.id)])
                                    # if calm_data.id == False:
                                    if(True):
                                        slive = self.env['ams.component.servicelife'].create({
                                            'at_install' : float(data[retirement_comp_hours]),
                                            'part_id' : comp.id,
                                            'is_major' : True,
                                            'action_type' : 'retirement',
                                            'unit' : 'hours',
                                            'value' : float(data[retirement_hours]),
                                            'current' : (float(acraft.total_hours) - float(data[retirement_aircraft_hours])) + float(data[retirement_comp_hours]), 
                                            'comments' : data[comment],
                                        })
                                        if len(data) > 165:
                                            if(data[ste_retire] != '0' and data[ste_retire] != ''):
                                                if (calm_data.service_life_id.id != False):
                                                    self.env['airworthy.ste'].create({
                                                        'service_life_id' : calm_data.service_life_id.id,
                                                        'value' : float(data[ste_retire])/float(100) * data[retirement_hours],
                                                        'status' : 'dgcaapprove',
                                                        })
                                        self.env.cr.commit()
                                        # self.env['calm.dict'].create({
                                        #     'file' : data[rank],
                                        #     'fleet_id' : acraft.id,
                                        #     'part_id' : comp.id,
                                        #     'sequence' : data[calm_id],
                                        #     'service_life_id' : slive.id,
                                        # })
                                        # self.env.cr.commit()
                                    else :
                                        slive = calm_data.service_life_id,
                                        slive.write({
                                            'at_install' : float(data[retirement_comp_hours]),
                                            'part_id' : comp.id,
                                            'is_major' : True,
                                            'action_type' : 'retirement',
                                            'unit' : 'hours',
                                            'value' : data[retirement_hours],
                                            'current' : (float(acraft.total_hours) - float(data[retirement_comp_attach_at])) + float(data[retirement_comp_hours]),
                                            'comments' : data[comment],    
                                        })
                                        self.env.cr.commit()
                                # OVERHAUL
                                if(data[overhaul].upper() == 'TRUE'):
                                    tsn = ((float(data[overhaul_comp_attach_at]) + float(data[overhaul_current]) + float(data[overhaul_comp_hours])) if float(comp.tsn) < float(float(data[overhaul_comp_attach_at]) + float(data[overhaul_current]) + float(data[overhaul_comp_hours])) else float(comp.tsn))
                                    is_overhaul = (True if tsn > (float(acraft.total_hours) - float(data[overhaul_aircraft_hours]) + float(data[overhaul_comp_hours])) else False)
                                    comp.update({
                                        'unknown_new' : False,
                                        'is_overhaul' : is_overhaul,
                                        'tsn': tsn if (tsn > comp.tsn) else comp.tsn,
                                        'tso': (float(acraft.total_hours) - float(data[overhaul_aircraft_hours]) + float(data[overhaul_comp_hours])),
                                        'comp_timeinstallation' : float(data[overhaul_comp_hours]),
                                        'ac_timeinstallation' : float(data[overhaul_aircraft_hours]),
                                    })

                                    # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]),('file','=',data[rank]),('fleet_id','=',acraft.id)])
                                    # if calm_data.id == False:
                                    if(True):
                                        slive = self.env['ams.component.servicelife'].create({
                                            'at_install' : float(data[overhaul_comp_hours]),
                                            'part_id' : comp.id,
                                            'is_major' : True,
                                            'action_type' : 'overhaul',
                                            'unit' : 'hours',
                                            'value' : float(data[overhaul_hours]),
                                            'overhaul_comp_attach_at' : float(data[overhaul_comp_attach_at]),
                                            'current' : (float(acraft.total_hours) - float(data[overhaul_aircraft_hours])) + float(data[overhaul_comp_hours]), 
                                            'comments' : data[comment],
                                        })
                                        if len(data) > 165:
                                            if(data[ste_overhaul] != '0' and data[ste_overhaul] != ''):
                                                if (calm_data.service_life_id.id != False):
                                                    self.env['airworthy.ste'].create({
                                                        'service_life_id' : calm_data.service_life_id.id,
                                                        'value' : float(data[ste_overhaul])/float(100) * data[overhaul_hours],
                                                        'status' : 'dgcaapprove',
                                                        })
                                        self.env.cr.commit()
                                        # self.env['calm.dict'].create({
                                        #     'file' : data[rank],
                                        #     'fleet_id' : acraft.id,
                                        #     'part_id' : comp.id,
                                        #     'sequence' : data[calm_id],
                                        #     'service_life_id' : slive.id,
                                        # })
                                        # self.env.cr.commit()
                                    else :
                                        slive = calm_data.service_life_id,
                                        slive.write({
                                            'at_install' : float(data[overhaul_comp_hours]),
                                            'part_id' : comp.id,
                                            'is_major' : True,
                                            'action_type' : 'overhaul',
                                            'unit' : 'hours',
                                            'value' : data[overhaul_hours],
                                            'current' : (float(acraft.total_hours) - float(data[overhaul_comp_attach_at])) + float(data[overhaul_comp_hours]),
                                            'comments' : data[comment],    
                                        })
                                        self.env.cr.commit()
                                # INSPECTION
                                if(data[inspection].upper() == 'TRUE'):
                                    tsn = (float(acraft.total_hours) - float(data[inspection_aircraft_hours]) + float(data[inspection_comp_hours])) if comp.tsn < (float(acraft.total_hours) - float(data[inspection_aircraft_hours]) + float(data[inspection_comp_hours])) else comp.tsn
                                    if(tsn > comp.tsn):
                                        comp.update({
                                            # 'unknown_new' : False,
                                            'tsn': tsn,
                                            # 'tso': (float(acraft.total_hours) - float(data[inspection_aircraft_hours]) + float(data[inspection_comp_hours])),
                                            'comp_timeinstallation' : float(data[inspection_comp_hours]),
                                            'ac_timeinstallation' : float(data[inspection_aircraft_hours]),
                                        })

                                    # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]),('file','=',data[rank]),('fleet_id','=',acraft.id)])
                                    # if calm_data.id == False:
                                    if(True):
                                        slive = self.env['ams.component.servicelife'].create({
                                            'at_install' : float(data[inspection_comp_hours]),
                                            'part_id' : comp.id,
                                            'action_type' : 'inspection',
                                            'unit' : 'hours',
                                            'value' : float(data[inspection_hours]),
                                            'current' : (float(acraft.total_hours) - float(data[inspection_aircraft_hours])) + float(data[inspection_comp_hours]), 
                                            'comments' : data[comment],
                                        })
                                        if len(data) > 165:
                                            if(data[ste_hr] != '0' and data[ste_hr] != ''):
                                                if (calm_data.service_life_id.id != False):
                                                    self.env['airworthy.ste'].create({
                                                        'service_life_id' : calm_data.service_life_id.id,
                                                        'value' : float(data[ste_hr])/float(100) * data[inspection_hours],
                                                        'status' : 'dgcaapprove',
                                                        })
                                        self.env.cr.commit()
                                        # self.env['calm.dict'].create({
                                        #     'file' : data[rank],
                                        #     'fleet_id' : acraft.id,
                                        #     'part_id' : comp.id,
                                        #     'sequence' : data[calm_id],
                                        #     'service_life_id' : slive.id,
                                        # })
                                        # self.env.cr.commit()
                                    else :
                                        slive = calm_data.service_life_id,
                                        slive.write({
                                            'at_install' : float(data[inspection_comp_hours]),
                                            'part_id' : comp.id,
                                            'action_type' : 'inspection',
                                            'unit' : 'hours',
                                            'value' : data[inspection_hours],
                                            'current' : (float(acraft.total_hours) - float(data[inspection_comp_attach_at])) + float(data[inspection_comp_hours]),
                                            'comments' : data[comment],    
                                        })
                                        self.env.cr.commit()

                                # CYCLES
                                if(data[cycles_on].upper() == 'TRUE'):
                                    if(data[cycles_type] == '1'):
                                        slive_type = 'retirement'
                                    elif(data[cycles_type] == '2'):
                                        slive_type = 'service'
                                    elif(data[cycles_type] == '3'):
                                        slive_type = 'inspection'
                                    elif(data[cycles_type] == '4'):
                                        slive_type = 'overhaul'

                                    csn = (float(acraft.total_landings) - float(data[cycle_on_install]) + float(data[comp_cycles])) if comp.tsn < (float(acraft.total_landings) - float(data[cycle_on_install]) + float(data[comp_cycles])) else comp.csn
                                    comp.update({
                                        'unknown_new' : False,
                                        'csn': (float(csn)),
                                        'cso': (float(data[cso])),
                                        'comp_cyclesinstallation' : float(data[comp_cycles]),
                                        'ac_cyclesinstallation' : float(data[aircraft_cycles]),
                                    })

                                    # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]),('file','=',data[rank]),('fleet_id','=',acraft.id)])
                                    # if calm_data.id == False:
                                    if(True):
                                        print data[comp_cycles] , ' <=> CYCLES'
                                        slive = self.env['ams.component.servicelife'].create({
                                            'at_install' : float(data[comp_cycles]),
                                            'part_id' : comp.id,
                                            'action_type' : slive_type,
                                            'unit' : 'cycles',
                                            'value' : float(data[cycles_value]),
                                            'current' : float(data[cycles_current]) + float(data[comp_cycles]),  
                                            'comments' : data[comment],
                                        })
                                        if len(data) > 165:
                                            if(data[ste_cy] != '0' and data[ste_cy] != ''):
                                                if (calm_data.service_life_id.id != False):
                                                    self.env['airworthy.ste'].create({
                                                        'service_life_id' : calm_data.service_life_id.id,
                                                        'value' : float(data[ste_cy])/float(100) * data[cycles_value],
                                                        'status' : 'dgcaapprove',
                                                        })
                                        self.env.cr.commit()
                                        # self.env['calm.dict'].create({
                                        #     'file' : data[rank],
                                        #     'fleet_id' : acraft.id,
                                        #     'part_id' : comp.id,
                                        #     'sequence' : data[calm_id],
                                        #     'service_life_id' : slive.id,
                                        # })
                                        # self.env.cr.commit()
                                    else :
                                        slive = calm_data.service_life_id,
                                        print data[comp_cycles] , ' <=> CYCLES'
                                        slive.write({
                                            'at_install' : float(data[comp_cycles]),
                                            'part_id' : comp.id,
                                            'action_type' : slive_type,
                                            'unit' : 'cycles',
                                            'value' : data[cycles_value],
                                            'current' : float(data[cycles_current]) + float(data[comp_cycles]),
                                            'comments' : data[comment],    
                                        })
                                        self.env.cr.commit()
                                # MONTH
                                if(data[month_on].upper() == 'TRUE'):
                                    if(data[month_type] == '1'):
                                        slive_type = 'inspection'
                                    elif(data[month_type] == '2'):
                                        slive_type = 'overhaul'
                                    elif(data[month_type] == '3'):
                                        slive_type = 'retirement'
                                    elif(data[month_type] == '4'):
                                        slive_type = 'service'

                                    comp.update({
                                        # 'unknown_new' : False,
                                        'date_installed' : data[month_date]
                                    })

                                    date_val = data[month_date]
                                    if(date_val == ''):
                                        date_val = data[inst_date]
                                    if(date_val != ''):
                                        # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]),('file','=',data[rank]),('fleet_id','=',acraft.id)])
                                        # if calm_data.id == False:
                                        if(True):
                                            slive = self.env['ams.component.servicelife'].create({
                                                'part_id' : comp.id,
                                                'action_type' : slive_type,
                                                'unit' : 'month',
                                                'value' : float(data[month_value]),
                                                'current' : False,
                                                'current_date' : date_val, 
                                                'comments' : data[comment],
                                            })
                                            self.env.cr.commit()
                                            # self.env['calm.dict'].create({
                                            #     'file' : data[rank],
                                            #     'fleet_id' : acraft.id,
                                            #     'part_id' : comp.id,
                                            #     'sequence' : data[calm_id],
                                            #     'service_life_id' : slive.id,
                                            # })
                                            # self.env.cr.commit()
                                        else :
                                            slive = calm_data.service_life_id,
                                            slive.write({
                                                'part_id' : comp.id,
                                                'action_type' : slive_type,
                                                'unit' : 'month',
                                                'value' : data[month_value],
                                                'current' : False,
                                                'current_date' : date_val,
                                                'comments' : data[comment],    
                                            })
                                            self.env.cr.commit()
                                # DAYS
                                if(data[days_on].upper() == 'TRUE'):
                                    if(data[days_type] == '1'):
                                        slive_type = 'inspection'
                                    elif(data[days_type] == '2'):
                                        slive_type = 'overhaul'
                                    elif(data[days_type] == '3'):
                                        slive_type = 'retirement'
                                    elif(data[days_type] == '4'):
                                        slive_type = 'service'

                                    comp.update({
                                        # 'unknown_new' : False,
                                        'date_installed' : data[days_date]
                                    })

                                    date_val = data[days_date]
                                    if(date_val == ''):
                                        date_val = data[inst_date]
                                    if(date_val != ''):
                                        # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]),('file','=',data[rank]),('fleet_id','=',acraft.id)])
                                        # if calm_data.id == False:
                                        if(True):
                                            slive = self.env['ams.component.servicelife'].create({
                                                'part_id' : comp.id,
                                                'action_type' : slive_type,
                                                'unit' : 'days',
                                                'value' : float(data[days_value]),
                                                'current' : False,
                                                'current_date' : date_val, 
                                                'comments' : data[comment],
                                            })
                                            self.env.cr.commit()
                                            # self.env['calm.dict'].create({
                                            #     'file' : data[rank],
                                            #     'fleet_id' : acraft.id,
                                            #     'part_id' : comp.id,
                                            #     'sequence' : data[calm_id],
                                            #     'service_life_id' : slive.id,
                                            # })
                                            # self.env.cr.commit()
                                        else :
                                            slive = calm_data.service_life_id,
                                            slive.write({
                                                'part_id' : comp.id,
                                                'action_type' : slive_type,
                                                'unit' : 'days',
                                                'value' : data[days_value],
                                                'current' : False,
                                                'current_date' : date_val,
                                                'comments' : data[comment],    
                                            })
                                            self.env.cr.commit()


    def set_component_engine(self,engine_id,calm_file,comptype):
        # self.env['ams.component.part'].search([('engine_id','=',engine_id)]).unlink()
        print 'Reading :: ' + str(calm_file)
        if(os.path.isfile(zipextract+str(calm_file)+".csv")):
            # file = open(zipextract+str(calm_file)+".csv", "r")
            # ro = file.readlines()
            # acraft = self.env['aircraft.acquisition'].search([('name','=',AC_REG)])
            with open(zipextract+str(calm_file)+".csv") as myFile:  
                ro = list(csv.reader(myFile, delimiter=';'))
                engine = self.env['engine.type'].search([('id','=',engine_id)])
                if(len(ro) >= 1):
                    if(ro[0][155] == 'CALMID'):
                        part_name = 0
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
                    
                    elif(ro[0][165] == 'CALMID'):
                        part_name = 0
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

                    for g in ro:
                        data = g

                        if len(data) > 155:
                            print data[part_name] + ' inst at ' + data[inst_date]
                            if(str(data[delete]).upper() == 'FALSE' and data[rank].find(comptype) != -1):
                                data = g

                                # PERHITUNGAN
                                comp_tso = 0
                                comp_cso = 0
                                comp_tsn = 0
                                comp_csn = 0

                                if(data[part_no].strip() == ''):
                                    product_id = self.env['product.product'].search([('name', '=', str(data[part_name]))],limit=1)
                                else:
                                    product_id = self.env['product.product'].search([('default_code', '=', data[part_no])],limit=1)

                                if(product_id.id == False):
                                    product_id = self.env['product.product'].create({
                                        'qmap':False,
                                        'is_part':True,
                                        'name':str(data[part_name]),
                                        'short_name':str(data[part_name]),
                                        'default_code':str(data[part_no]),
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
                                if(data[ata_1] != '' or data[ata_2] != '' or data[ata_3] != ''):
                                    ata_string = data[ata_1].zfill(2) + '-' + data[ata_2].zfill(2) + '-' + data[ata_3].zfill(2)
                                    ata_id = self.env['ams.ata'].search([('name', '=', ata_string)])
                                    if(ata_id.id == False):
                                        ata_id = self.env['ams.ata'].create({
                                            'name' : ata_string,
                                            'chapter' : data[ata_1].zfill(2),
                                            'sub_chapter' : data[ata_2].zfill(2),
                                            'description' : 'ATA ' + ata_string,
                                            })

                                if(data[serial] != ''):
                                    serial_id = self.env['stock.production.lot'].search(['&',('product_id','=',product_id.id),('name','=',data[serial])])
                                    if(serial_id.id == False):
                                        serial_id = self.env['stock.production.lot'].create({
                                            'product_id':product_id.id,
                                            'name':data[serial],
                                        })
                                    self.env.cr.commit()
                                    # comp = self.env['ams.component.part'].search(['&','&','&',('engine_id','=',engine.id),('product_id', '=' ,product_id.id),('serial_number', '=' ,serial_id.id),('item','=',data[item])], limit=1)
                                    serial_number = serial_id.id
                                else:
                                    # comp = self.env['ams.component.part'].search(['&','&',('engine_id','=',engine.id),('product_id', '=' ,product_id.id),('item','=',data[item])], limit=1)
                                    serial_number = False
                                # comp = self.env['calm.dict'].search(['&','&',('service_life_id','=',False),('sequence','=',data[calm_id]),('engine_id','=',engine.id)],limit=1).part_id
                                if(comptype == 'M'):
                                    comp = self.env['ams.component.part'].search(['&',('serial_number','=',serial_number),'&',('calm_file','=',calm_file),('calm_id','=',data[rank])])
                                else:
                                    comp = self.env['ams.component.part'].search(['&',('serial_number','=',serial_number),'&',('calm_file','=',calm_file),('calm_id','=',data[rank]+data[part_no])])
                                if(comp.id == False):
                                    if(comptype == 'M' or (comptype != 'S' and self.env['ams.component.part'].search(['&',('calm_file','=',calm_file),('calm_id','=',data[rank].replace('S','M'))]).id != False)):
                                        comp = self.env['ams.component.part'].create({
                                            'calm_file' : calm_file,
                                            'calm_id' : data[rank] if comptype == 'M' else data[rank]+data[part_no],
                                            'ata_code' : ata_id.id,
                                            'is_subcomp' : True if comptype == 'S' else False,
                                            'part_id' : False if comptype == 'M' else self.env['ams.component.part'].search(['&',('calm_file','=',calm_file),('calm_id','=',data[rank].replace('S','M'))]).id,
                                            'engine_id': False if comptype != 'M' else engine.id,
                                            'product_id':product_id.id,
                                            'serial_number':serial_number,
                                            'comp_timeinstallation' : 0,
                                            'comp_cyclesinstallation' : 0,
                                            'date_installed' : data[inst_date] if (data[inst_date] != '') else False,
                                            'csn' : 0,
                                            'tsn' : 0,
                                            'is_overhaul' : False,
                                            # 'unknown_new' : False,
                                            'item' : data[item],
                                        })
                                        self.env.cr.commit()
                                    
                                    calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','=',False),('sequence','=',data[calm_id]),('file','=',data[rank]),('engine_id','=',engine.id)])
                                    if calm_data.id == False:
                                        self.env['calm.dict'].create({
                                            'file' : data[rank],
                                            'engine_id' : engine.id,
                                            'part_id' : comp.id,
                                            'sequence' : data[calm_id],
                                        })
                                        self.env.cr.commit()
                                else:
                                    comp.update({
                                        # 'engine_id':engine.id,
                                        'product_id':product_id.id,
                                        'serial_number':serial_number,
                                        # 'comp_timeinstallation' : 0,
                                        # 'comp_cyclesinstallation' : 0,
                                        'date_installed' : data[inst_date] if (data[inst_date] != '') else False,
                                        # 'csn' : 0,
                                        # 'tsn' : 0,
                                        # 'is_overhaul' : False,
                                        # 'unknown_new' : False,
                                        'item' : data[item],
                                    })
                                # SERVICE LIFE
                                # ON CONDITION
                                if(data[on_condition].upper() == 'TRUE'):
                                    comp.update({
                                        'tsn' : (float(engine.total_hours) - float(data[on_aircraft_hours])) + float(data[U2TT]),
                                        # 'tso': (float(engine.total_hours) - float(data[on_aircraft_hours])) + float(data[on_comp_hours]),
                                        'comp_timeinstallation' : data[on_comp_hours],
                                        'ac_timeinstallation' : data[on_aircraft_hours],
                                    })

                                    # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]),('file','=',data[rank]),('engine_id','=',engine.id)])
                                    # if calm_data.id == False:
                                    if(True):
                                        slive = self.env['ams.component.servicelife'].create({
                                            'at_install' : float(data[U2TT]),
                                            'part_id' : comp.id,
                                            'action_type' : 'oncondition',
                                            'unit' : 'hours',
                                            'value' : 0,
                                            'current' : (float(engine.total_hours) - float(data[on_aircraft_hours])) + float(data[U2TT]), 
                                            'comments' : data[comment],
                                        })
                                        self.env.cr.commit()
                                        # self.env['calm.dict'].create({
                                        #     'file' : data[rank],
                                        #     'engine_id' : engine.id,
                                        #     'part_id' : comp.id,
                                        #     'sequence' : data[calm_id],
                                        #     'service_life_id' : slive.id,
                                        # })
                                        # self.env.cr.commit()
                                    else :
                                        slive = calm_data.service_life_id,
                                        slive.write({
                                            'at_install' : float(data[U2TT]),
                                            'part_id' : comp.id,
                                            'action_type' : 'oncondition',
                                            'unit' : 'hours',
                                            'value' : 0,
                                            'current' : (float(engine.total_hours) - float(data[on_aircraft_hours])) + float(data[U2TT]),
                                            'comments' : data[comment],    
                                        })
                                        self.env.cr.commit()
                                # RETIREMENT
                                if(data[retirement].upper() == 'TRUE'):
                                    tsn = (float(engine.total_hours) - float(data[retirement_aircraft_hours]) + float(data[retirement_comp_hours])) if comp.tsn < (float(engine.total_hours) - float(data[retirement_aircraft_hours]) + float(data[retirement_comp_hours])) else comp.tsn
                                    # print  float(engine.total_hours), '-', float(data[retirement_aircraft_hours]), '+', float(data[retirement_comp_hours]), '=', tsn
                                    comp.update({
                                        # 'unknown_new' : False,
                                        'tsn': tsn,
                                        # 'tso': (float(engine.total_hours) - float(data[retirement_aircraft_hours]) + float(data[retirement_comp_hours])),
                                        'comp_timeinstallation' : float(data[retirement_comp_hours]),
                                        'ac_timeinstallation' : float(data[retirement_aircraft_hours]),
                                    })

                                    # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]),('file','=',data[rank]),('engine_id','=',engine.id)])
                                    # if calm_data.id == False:
                                    if(True):
                                        slive = self.env['ams.component.servicelife'].create({
                                            'at_install' : float(data[retirement_comp_hours]),
                                            'part_id' : comp.id,
                                            'is_major' : True,
                                            'action_type' : 'retirement',
                                            'unit' : 'hours',
                                            'current' : float(data[overhaul_current])+float(data[overhaul_comp_hours]), 
                                            'value' : float(data[retirement_hours]),
                                            'comments' : data[comment],
                                        })
                                        if len(data) > 165:
                                            if(data[ste_retire] != '0' and data[ste_retire] != ''):
                                                if (calm_data.service_life_id.id != False):
                                                    self.env['airworthy.ste'].create({
                                                        'service_life_id' : calm_data.service_life_id.id,
                                                        'value' : float(data[ste_retire])/float(100) * data[retirement_hours],
                                                        'status' : 'dgcaapprove',
                                                        })
                                        self.env.cr.commit()
                                        # self.env['calm.dict'].create({
                                        #     'file' : data[rank],
                                        #     'engine_id' : engine.id,
                                        #     'part_id' : comp.id,
                                        #     'sequence' : data[calm_id],
                                        #     'service_life_id' : slive.id,
                                        # })
                                        # self.env.cr.commit()
                                    else :
                                        slive = calm_data.service_life_id,
                                        slive.write({
                                            'at_install' : float(data[retirement_comp_hours]),
                                            'part_id' : comp.id,
                                            'is_major' : True,
                                            'action_type' : 'retirement',
                                            'unit' : 'hours',
                                            'value' : data[retirement_hours],
                                            'current' : float(data[retirement_current]),
                                            'comments' : data[comment],    
                                        })
                                        self.env.cr.commit()
                                # OVERHAUL
                                if(data[overhaul].upper() == 'TRUE'):
                                    tsn = (float(data[overhaul_comp_attach_at]) + float(data[overhaul_current]) if float(comp.tsn) < float(data[overhaul_comp_attach_at]) + float(data[overhaul_current]) else float(comp.tsn))
                                    is_overhaul = (True if tsn > (float(engine.total_hours) - float(data[overhaul_aircraft_hours]) + float(data[overhaul_comp_hours])) else False)
                                    float(engine.total_hours), '-', float(data[retirement_aircraft_hours]), '+', float(data[retirement_comp_hours]), '=', tsn
                                    comp.update({
                                        'unknown_new' : False,
                                        'is_overhaul' : is_overhaul,
                                        'tsn': tsn,
                                        'tso': (float(engine.total_hours) - float(data[overhaul_aircraft_hours]) + float(data[overhaul_comp_hours])),
                                        'comp_timeinstallation' : float(data[overhaul_comp_hours]),
                                        'ac_timeinstallation' : float(data[overhaul_aircraft_hours]),
                                    })

                                    # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]),('file','=',data[rank]),('engine_id','=',engine.id)])
                                    # if calm_data.id == False:
                                    if(True):
                                        slive = self.env['ams.component.servicelife'].create({
                                            'at_install' : float(data[overhaul_comp_hours]),
                                            'part_id' : comp.id,
                                            'is_major' : True,
                                            'action_type' : 'overhaul',
                                            'unit' : 'hours',
                                            'value' : float(data[overhaul_hours]),
                                            'current' : float(data[overhaul_current])+float(data[overhaul_comp_hours]), 
                                            'comments' : data[comment],
                                        })
                                        if len(data) > 165:
                                            if(data[ste_overhaul] != '0' and data[ste_overhaul] != ''):
                                                if (calm_data.service_life_id.id != False):
                                                    self.env['airworthy.ste'].create({
                                                        'service_life_id' : calm_data.service_life_id.id,
                                                        'value' : float(data[ste_overhaul])/float(100) * data[overhaul_hours],
                                                        'status' : 'dgcaapprove',
                                                        })
                                        self.env.cr.commit()
                                        # self.env['calm.dict'].create({
                                        #     'file' : data[rank],
                                        #     'engine_id' : engine.id,
                                        #     'part_id' : comp.id,
                                        #     'sequence' : data[calm_id],
                                        #     'service_life_id' : slive.id,
                                        # })
                                        # self.env.cr.commit()
                                    else :
                                        slive = calm_data.service_life_id,
                                        slive.write({
                                            'at_install' : float(data[overhaul_comp_hours]),
                                            'part_id' : comp.id,
                                            'is_major' : True,
                                            'action_type' : 'overhaul',
                                            'unit' : 'hours',
                                            'current' : float(data[overhaul_current])+float(data[overhaul_comp_hours]), 
                                            'value' : data[overhaul_hours],
                                            'comments' : data[comment],    
                                        })
                                        self.env.cr.commit()
                                # INSPECTION
                                if(data[inspection].upper() == 'TRUE'):
                                    tsn = (float(engine.total_hours) - float(data[retirement_aircraft_hours]) + float(data[retirement_comp_hours])) if comp.tsn < (float(engine.total_hours) - float(data[retirement_aircraft_hours]) + float(data[retirement_comp_hours])) else comp.tsn
                                    comp.update({
                                        # 'unknown_new' : False,
                                        'tsn': tsn,
                                        # 'tso': (float(engine.total_hours) - float(data[inspection_aircraft_hours]) + float(data[inspection_comp_hours])),
                                        'comp_timeinstallation' : float(data[inspection_comp_hours]),
                                        'ac_timeinstallation' : float(data[inspection_aircraft_hours]),
                                    })

                                    # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]),('file','=',data[rank]),('engine_id','=',engine.id)])
                                    # if calm_data.id == False:
                                    if(True):
                                        slive = self.env['ams.component.servicelife'].create({
                                            'at_install' : float(data[inspection_comp_hours]),
                                            'part_id' : comp.id,
                                            'action_type' : 'inspection',
                                            'unit' : 'hours',
                                            'value' : float(data[inspection_hours]),
                                            'current' : float(data[inspection_current]), 
                                            'comments' : data[comment],
                                        })
                                        if len(data) > 165:
                                            if(data[ste_hr] != '0' and data[ste_hr] != ''):
                                                if (calm_data.service_life_id.id != False):
                                                    self.env['airworthy.ste'].create({
                                                        'service_life_id' : calm_data.service_life_id.id,
                                                        'value' : float(data[ste_hr])/float(100) * data[inspection_hours],
                                                        'status' : 'dgcaapprove',
                                                        })
                                        self.env.cr.commit()
                                        # self.env['calm.dict'].create({
                                        #     'file' : data[rank],
                                        #     'engine_id' : engine.id,
                                        #     'part_id' : comp.id,
                                        #     'sequence' : data[calm_id],
                                        #     'service_life_id' : slive.id,
                                        # })
                                        # self.env.cr.commit()
                                    else :
                                        slive = calm_data.service_life_id,
                                        slive.write({
                                            'at_install' : float(data[inspection_comp_hours]),
                                            'part_id' : comp.id,
                                            'action_type' : 'inspection',
                                            'unit' : 'hours',
                                            'value' : data[inspection_hours],
                                            'current' : float(data[inspection_current]), 
                                            'comments' : data[comment],    
                                        })
                                        self.env.cr.commit()

                                # CYCLES
                                if(data[cycles_on].upper() == 'TRUE'):
                                    if(data[cycles_type] == '1'):
                                        slive_type = 'retirement'
                                    elif(data[cycles_type] == '2'):
                                        slive_type = 'service'
                                    elif(data[cycles_type] == '3'):
                                        slive_type = 'inspection'
                                    elif(data[cycles_type] == '4'):
                                        slive_type = 'overhaul'

                                    csn = (float(data[aircraft_cycles]) - float(data[cycle_on_install]) + float(data[comp_cycles])) if comp.tsn < (float(data[aircraft_cycles]) - float(data[cycle_on_install]) + float(data[comp_cycles])) else comp.csn
                                    comp.update({
                                        # 'unknown_new' : False,
                                        'csn': (float(csn)),
                                        'cso': (float(data[cso])),
                                        'comp_cyclesinstallation' : float(data[comp_cycles]),
                                        'ac_cyclesinstallation' : float(data[aircraft_cycles]),
                                    })

                                    # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]),('file','=',data[rank]),('engine_id','=',engine.id)])
                                    # if calm_data.id == False:
                                    if(True):
                                        print data[comp_cycles] , ' <=> CYCLES'
                                        slive = self.env['ams.component.servicelife'].create({
                                            'at_install' : float(data[comp_cycles]),
                                            'part_id' : comp.id,
                                            'action_type' : slive_type,
                                            'unit' : 'cycles',
                                            'value' : float(data[cycles_value]),
                                            'current' : float(data[cycles_current]) + float(data[comp_cycles]), 
                                            'comments' : data[comment],
                                        })
                                        if len(data) > 165:
                                            if(data[ste_cy] != '0' and data[ste_cy] != ''):
                                                if (calm_data.service_life_id.id != False):
                                                    self.env['airworthy.ste'].create({
                                                        'service_life_id' : calm_data.service_life_id.id,
                                                        'value' : float(data[ste_cy])/float(100) * data[cycles_value],
                                                        'status' : 'dgcaapprove',
                                                        })
                                        self.env.cr.commit()
                                        # self.env['calm.dict'].create({
                                        #     'file' : data[rank],
                                        #     'engine_id' : engine.id,
                                        #     'part_id' : comp.id,
                                        #     'sequence' : data[calm_id],
                                        #     'service_life_id' : slive.id,
                                        # })
                                        # self.env.cr.commit()
                                    else :
                                        print data[comp_cycles] , ' <=> CYCLES'
                                        slive = calm_data.service_life_id,
                                        slive.write({
                                            'at_install' : float(data[comp_cycles]),
                                            'part_id' : comp.id,
                                            'action_type' : slive_type,
                                            'unit' : 'cycles',
                                            'value' : data[cycles_value],
                                            'current' : float(data[cycles_current]) + float(data[comp_cycles]),
                                            'comments' : data[comment],    
                                        })
                                        self.env.cr.commit()
                                # MONTH
                                if(data[month_on].upper() == 'TRUE'):
                                    if(data[month_type] == '1'):
                                        slive_type = 'inspection'
                                    elif(data[month_type] == '2'):
                                        slive_type = 'overhaul'
                                    elif(data[month_type] == '3'):
                                        slive_type = 'retirement'
                                    elif(data[month_type] == '4'):
                                        slive_type = 'service'

                                    comp.update({
                                        # 'unknown_new' : False,
                                        'date_installed' : data[month_date]
                                    })

                                    date_val = data[month_date]
                                    if(date_val == ''):
                                        date_val = data[inst_date]
                                    if(date_val != ''):
                                        # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]),('file','=',data[rank]),('engine_id','=',engine.id)])
                                        # if calm_data.id == False:
                                        if(True):
                                            slive = self.env['ams.component.servicelife'].create({
                                                'part_id' : comp.id,
                                                'action_type' : slive_type,
                                                'unit' : 'month',
                                                'value' : float(data[month_value]),
                                                'current' : False,
                                                'current_date' : date_val, 
                                                'comments' : data[comment],
                                            })
                                            self.env.cr.commit()
                                            # self.env['calm.dict'].create({
                                            #     'file' : data[rank],
                                            #     'engine_id' : engine.id,
                                            #     'part_id' : comp.id,
                                            #     'sequence' : data[calm_id],
                                            #     'service_life_id' : slive.id,
                                            # })
                                            # self.env.cr.commit()
                                        else :
                                            slive = calm_data.service_life_id,
                                            slive.write({
                                                'part_id' : comp.id,
                                                'action_type' : slive_type,
                                                'unit' : 'month',
                                                'value' : data[month_value],
                                                'current' : False,
                                                'current_date' : date_val,
                                                'comments' : data[comment],    
                                            })
                                            self.env.cr.commit()
                                # DAYS
                                if(data[days_on].upper() == 'TRUE'):
                                    if(data[days_type] == '1'):
                                        slive_type = 'inspection'
                                    elif(data[days_type] == '2'):
                                        slive_type = 'overhaul'
                                    elif(data[days_type] == '3'):
                                        slive_type = 'retirement'
                                    elif(data[days_type] == '4'):
                                        slive_type = 'service'

                                    comp.update({
                                        # 'unknown_new' : False,
                                        'date_installed' : data[days_date]
                                    })

                                    date_val = data[days_date]
                                    if(date_val == ''):
                                        date_val = data[inst_date]
                                    if(date_val != ''):
                                        # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]),('file','=',data[rank]),('engine_id','=',engine.id)])
                                        # if calm_data.id == False:
                                        if(True):
                                            slive = self.env['ams.component.servicelife'].create({
                                                'part_id' : comp.id,
                                                'action_type' : slive_type,
                                                'unit' : 'days',
                                                'value' : float(data[days_value]),
                                                'current' : False,
                                                'current_date' : date_val, 
                                                'comments' : data[comment],
                                            })
                                            self.env.cr.commit()
                                            # self.env['calm.dict'].create({
                                            #     'file' : data[rank],
                                            #     'engine_id' : engine.id,
                                            #     'part_id' : comp.id,
                                            #     'sequence' : data[calm_id],
                                            #     'service_life_id' : slive.id,
                                            # })
                                            # self.env.cr.commit()
                                        else :
                                            slive = calm_data.service_life_id,
                                            slive.write({
                                                'part_id' : comp.id,
                                                'action_type' : slive_type,
                                                'unit' : 'days',
                                                'value' : data[days_value],
                                                'current' : False,
                                                'current_date' : date_val,
                                                'comments' : data[comment],    
                                            })
                                            self.env.cr.commit()

    def set_component_auxiliary(self,auxiliary_id,calm_file,comptype):
        # self.env['ams.component.part'].search([('auxiliary_id','=',auxiliary_id)]).unlink()
        print 'Reading :: ' + str(calm_file)
        if(os.path.isfile(zipextract+str(calm_file)+".csv")):
            # file = open(zipextract+str(calm_file)+".csv", "r")
            # engine = self.env['engine.type'].search([('id','=',engine_id)])
            # auxiliary = self.env['auxiliary.type'].search([('id','=',auxiliary_id)])
            # ro = file.readlines()
            with open(zipextract+str(calm_file)+".csv") as myFile:  
                ro = list(csv.reader(myFile, delimiter=';'))
                auxiliary = self.env['auxiliary.type'].search([('id','=',auxiliary_id)])
                if(len(ro) >= 1):
                    if(ro[0][155] == 'CALMID'):
                        part_name = 0
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
                    
                    elif(ro[0][165] == 'CALMID'):
                        part_name = 0
                        part_des = 97
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

                    for g in ro:
                        data = g

                        if len(data) > 155:
                            print data[part_name] + ' inst at ' + data[inst_date]
                            if(str(data[delete]).upper() == 'FALSE' and data[rank].find(comptype) != -1):
                                data = g

                                # PERHITUNGAN
                                comp_tso = 0
                                comp_cso = 0
                                comp_tsn = 0
                                comp_csn = 0

                                if(data[part_no].strip() == ''):
                                    product_id = self.env['product.product'].search([('name', '=', str(data[part_name]))],limit=1)
                                else:
                                    product_id = self.env['product.product'].search([('default_code', '=', data[part_no])],limit=1)

                                if(product_id.id == False):
                                    product_id = self.env['product.product'].create({
                                        'qmap':False,
                                        'is_part':True,
                                        'name':str(data[part_name]),
                                        'short_name':str(data[part_name]),
                                        'default_code':str(data[part_no]),
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
                                if(data[ata_1] != '' or data[ata_2] != '' or data[ata_3] != ''):
                                    ata_string = data[ata_1].zfill(2) + '-' + data[ata_2].zfill(2) + '-' + data[ata_3].zfill(2)
                                    ata_id = self.env['ams.ata'].search([('name', '=', ata_string)])
                                    if(ata_id.id == False):
                                        ata_id = self.env['ams.ata'].create({
                                            'name' : ata_string,
                                            'chapter' : data[ata_1].zfill(2),
                                            'sub_chapter' : data[ata_2].zfill(2),
                                            'description' : 'ATA ' + ata_string,
                                            })

                                if(data[serial] != ''):
                                    serial_id = self.env['stock.production.lot'].search(['&',('product_id','=',product_id.id),('name','=',data[serial])])
                                    if(serial_id.id == False):
                                        serial_id = self.env['stock.production.lot'].create({
                                            'product_id':product_id.id,
                                            'name':data[serial],
                                        })
                                    self.env.cr.commit()
                                    # comp = self.env['ams.component.part'].search(['&','&','&',('auxiliary_id','=',auxiliary.id),('product_id', '=' ,product_id.id),('serial_number', '=' ,serial_id.id),('item','=',data[item])], limit=1)
                                    serial_number = serial_id.id
                                else:
                                    # comp = self.env['ams.component.part'].search(['&','&',('auxiliary_id','=',auxiliary.id),('product_id', '=' ,product_id.id),('item','=',data[item])], limit=1)
                                    serial_number = False
                                # comp = self.env['calm.dict'].search(['&','&',('service_life_id','=',False),('sequence','=',data[calm_id]),('auxiliary_id','=',auxiliary.id)],limit=1).part_id
                                if(comptype == 'M'):
                                    comp = self.env['ams.component.part'].search(['&',('serial_number','=',serial_number),'&',('calm_file','=',calm_file),('calm_id','=',data[rank])])
                                else:
                                    comp = self.env['ams.component.part'].search(['&',('serial_number','=',serial_number),'&',('calm_file','=',calm_file),('calm_id','=',data[rank]+data[part_no])])
                                if(comp.id == False):
                                    if(comptype == 'M' or (comptype != 'S' and self.env['ams.component.part'].search(['&',('calm_file','=',calm_file),('calm_id','=',data[rank].replace('S','M'))]).id != False)):
                                        comp = self.env['ams.component.part'].create({
                                            'calm_file' : calm_file,
                                            'calm_id' : data[rank] if comptype == 'M' else data[rank]+data[part_no],
                                            'ata_code' : ata_id.id,
                                            'is_subcomp' : True if comptype == 'S' else False,
                                            'part_id' : False if comptype == 'M' else self.env['ams.component.part'].search(['&',('calm_file','=',calm_file),('calm_id','=',data[rank].replace('S','M'))]).id,
                                            'auxiliary_id': False if comptype != 'M' else auxiliary.id,
                                            'product_id':product_id.id,
                                            'serial_number':serial_number,
                                            'comp_timeinstallation' : 0,
                                            'comp_cyclesinstallation' : 0,
                                            'date_installed' : data[inst_date] if (data[inst_date] != '') else False,
                                            'csn' : 0,
                                            'tsn' : 0,
                                            'is_overhaul' : False,
                                            # 'unknown_new' : False,
                                            'item' : data[item],
                                        })
                                        self.env.cr.commit()
                                    
                                    calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','=',False),('sequence','=',data[calm_id]),('file','=',data[rank]),('auxiliary_id','=',auxiliary.id)])
                                    if calm_data.id == False:
                                        self.env['calm.dict'].create({
                                            'file' : data[rank],
                                            'auxiliary_id' : auxiliary.id,
                                            'part_id' : comp.id,
                                            'sequence' : data[calm_id],
                                        })
                                        self.env.cr.commit()
                                else:
                                    comp.update({
                                        # 'auxiliary_id':auxiliary.id,
                                        'product_id':product_id.id,
                                        'serial_number':serial_number,
                                        # 'comp_timeinstallation' : 0,
                                        # 'comp_cyclesinstallation' : 0,
                                        'date_installed' : data[inst_date] if (data[inst_date] != '') else False,
                                        # 'csn' : 0,
                                        # 'tsn' : 0,
                                        # 'is_overhaul' : False,
                                        # 'unknown_new' : False,
                                        'item' : data[item],
                                    })
                                # SERVICE LIFE
                                # ON CONDITION
                                if(data[on_condition].upper() == 'TRUE'):
                                    comp.update({
                                        'tsn' : (float(auxiliary.total_hours) - float(data[on_aircraft_hours])) + float(data[U2TT]),
                                        # 'tso': (float(auxiliary.total_hours) - float(data[on_aircraft_hours])) + float(data[on_comp_hours]),
                                        'comp_timeinstallation' : data[on_comp_hours],
                                        'ac_timeinstallation' : data[on_aircraft_hours],
                                    })

                                    # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]),('file','=',data[rank]),('auxiliary_id','=',auxiliary.id)])
                                    # if calm_data.id == False:
                                    if(True):
                                        slive = self.env['ams.component.servicelife'].create({
                                            'at_install' : float(data[U2TT]),
                                            'part_id' : comp.id,
                                            'action_type' : 'oncondition',
                                            'unit' : 'hours',
                                            'value' : 0,
                                            'current' : (float(auxiliary.total_hours) - float(data[on_aircraft_hours])) + float(data[U2TT]), 
                                            'comments' : data[comment],
                                        })
                                        self.env.cr.commit()
                                        # self.env['calm.dict'].create({
                                        #     'file' : data[rank],
                                        #     'auxiliary_id' : auxiliary.id,
                                        #     'part_id' : comp.id,
                                        #     'sequence' : data[calm_id],
                                        #     'service_life_id' : slive.id,
                                        # })
                                        # self.env.cr.commit()
                                    else :
                                        slive = calm_data.service_life_id,
                                        slive.write({
                                            'at_install' : float(data[U2TT]),
                                            'part_id' : comp.id,
                                            'action_type' : 'oncondition',
                                            'unit' : 'hours',
                                            'value' : 0,
                                            'current' : (float(auxiliary.total_hours) - float(data[on_aircraft_hours])) + float(data[U2TT]),
                                            'comments' : data[comment],    
                                        })
                                        self.env.cr.commit()
                                # RETIREMENT
                                if(data[retirement].upper() == 'TRUE'):
                                    tsn = (float(auxiliary.total_hours) - float(data[retirement_aircraft_hours]) + float(data[retirement_comp_hours])) if comp.tsn < (float(auxiliary.total_hours) - float(data[retirement_aircraft_hours]) + float(data[retirement_comp_hours])) else comp.tsn
                                    comp.update({
                                        # 'unknown_new' : False,
                                        'tsn': tsn,
                                        # 'tso': (float(auxiliary.total_hours) - float(data[retirement_aircraft_hours]) + float(data[retirement_comp_hours])),
                                        'comp_timeinstallation' : float(data[retirement_comp_hours]),
                                        'ac_timeinstallation' : float(data[retirement_aircraft_hours]),
                                    })

                                    # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]),('file','=',data[rank]),('auxiliary_id','=',auxiliary.id)])
                                    # if calm_data.id == False:
                                    if(True):
                                        slive = self.env['ams.component.servicelife'].create({
                                            'at_install' : float(data[retirement_comp_hours]),
                                            'part_id' : comp.id,
                                            'is_major' : True,
                                            'action_type' : 'retirement',
                                            'unit' : 'hours',
                                            'value' : float(data[retirement_hours]),
                                            'current' : float(data[retirement_current]), 
                                            'comments' : data[comment],
                                        })
                                        if len(data) > 165:
                                            if(data[ste_retire] != '0' and data[ste_retire] != ''):
                                                if (calm_data.service_life_id.id != False):
                                                    self.env['airworthy.ste'].create({
                                                        'service_life_id' : calm_data.service_life_id.id,
                                                        'value' : float(data[ste_retire])/float(100) * data[retirement_hours],
                                                        'status' : 'dgcaapprove',
                                                        })
                                        self.env.cr.commit()
                                        # self.env['calm.dict'].create({
                                        #     'file' : data[rank],
                                        #     'auxiliary_id' : auxiliary.id,
                                        #     'part_id' : comp.id,
                                        #     'sequence' : data[calm_id],
                                        #     'service_life_id' : slive.id,
                                        # })
                                        # self.env.cr.commit()
                                    else :
                                        slive = calm_data.service_life_id,
                                        slive.write({
                                            'at_install' : float(data[retirement_comp_hours]),
                                            'part_id' : comp.id,
                                            'is_major' : True,
                                            'action_type' : 'retirement',
                                            'unit' : 'hours',
                                            'value' : data[retirement_hours],
                                            'current' : float(data[retirement_current]), 
                                            'comments' : data[comment],    
                                        })
                                        self.env.cr.commit()
                                # OVERHAUL
                                if(data[overhaul].upper() == 'TRUE'):
                                    tsn = (float(data[overhaul_comp_attach_at]) + float(data[overhaul_current]) if float(comp.tsn) < float(data[overhaul_comp_attach_at]) + float(data[overhaul_current]) else float(comp.tsn))
                                    is_overhaul = (True if tsn > (float(auxiliary.total_hours) - float(data[overhaul_aircraft_hours]) + float(data[overhaul_comp_hours])) else False)
                                    comp.update({
                                        'unknown_new' : False,
                                        'is_overhaul' : is_overhaul,
                                        'tsn': tsn,
                                        'tso': (float(auxiliary.total_hours) - float(data[overhaul_aircraft_hours]) + float(data[overhaul_comp_hours])),
                                        'comp_timeinstallation' : float(data[overhaul_comp_hours]),
                                        'ac_timeinstallation' : float(data[overhaul_aircraft_hours]),
                                    })

                                    # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]),('file','=',data[rank]),('auxiliary_id','=',auxiliary.id)])
                                    # if calm_data.id == False:
                                    if(True):
                                        slive = self.env['ams.component.servicelife'].create({
                                            'at_install' : float(data[overhaul_comp_hours]),
                                            'part_id' : comp.id,
                                            'is_major' : True,
                                            'action_type' : 'overhaul',
                                            'unit' : 'hours',
                                            'value' : float(data[overhaul_hours]),
                                            'current' : float(data[overhaul_current]), 
                                            'comments' : data[comment],
                                        })
                                        if len(data) > 165:
                                            if(data[ste_overhaul] != '0' and data[ste_overhaul] != ''):
                                                if (calm_data.service_life_id.id != False):
                                                    self.env['airworthy.ste'].create({
                                                        'service_life_id' : calm_data.service_life_id.id,
                                                        'value' : float(data[ste_overhaul])/float(100) * data[overhaul_hours],
                                                        'status' : 'dgcaapprove',
                                                        })
                                        self.env.cr.commit()
                                        # self.env['calm.dict'].create({
                                        #     'file' : data[rank],
                                        #     'auxiliary_id' : auxiliary.id,
                                        #     'part_id' : comp.id,
                                        #     'sequence' : data[calm_id],
                                        #     'service_life_id' : slive.id,
                                        # })
                                        # self.env.cr.commit()
                                    else :
                                        slive = calm_data.service_life_id,
                                        slive.write({
                                            'at_install' : float(data[overhaul_comp_hours]),
                                            'part_id' : comp.id,
                                            'is_major' : True,
                                            'action_type' : 'overhaul',
                                            'unit' : 'hours',
                                            'value' : data[overhaul_hours],
                                            'current' : float(data[overhaul_current]), 
                                            'comments' : data[comment],    
                                        })
                                        self.env.cr.commit()
                                # INSPECTION
                                if(data[inspection].upper() == 'TRUE'):
                                    tsn = (float(auxiliary.total_hours) - float(data[inspection_aircraft_hours]) + float(data[inspection_comp_hours])) if comp.tsn < (float(auxiliary.total_hours) - float(data[inspection_aircraft_hours]) + float(data[inspection_comp_hours])) else comp.tsn
                                    comp.update({
                                        # 'unknown_new' : False,
                                        'tsn': tsn,
                                        # 'tso': (float(auxiliary.total_hours) - float(data[inspection_aircraft_hours]) + float(data[inspection_comp_hours])),
                                        'comp_timeinstallation' : float(data[inspection_comp_hours]),
                                        'ac_timeinstallation' : float(data[inspection_aircraft_hours]),
                                    })

                                    # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]),('file','=',data[rank]),('auxiliary_id','=',auxiliary.id)])
                                    # if calm_data.id == False:
                                    if(True):
                                        slive = self.env['ams.component.servicelife'].create({
                                            'at_install' : float(data[inspection_comp_hours]),
                                            'part_id' : comp.id,
                                            'action_type' : 'inspection',
                                            'unit' : 'hours',
                                            'value' : float(data[inspection_hours]),
                                            'current' : float(data[inspection_current]), 
                                            'comments' : data[comment],
                                        })
                                        if len(data) > 165:
                                            if(data[ste_hr] != '0' and data[ste_hr] != ''):
                                                if (calm_data.service_life_id.id != False):
                                                    self.env['airworthy.ste'].create({
                                                        'service_life_id' : calm_data.service_life_id.id,
                                                        'value' : float(data[ste_hr])/float(100) * data[inspection_hours],
                                                        'status' : 'dgcaapprove',
                                                        })
                                        self.env.cr.commit()
                                        # self.env['calm.dict'].create({
                                        #     'file' : data[rank],
                                        #     'auxiliary_id' : auxiliary.id,
                                        #     'part_id' : comp.id,
                                        #     'sequence' : data[calm_id],
                                        #     'service_life_id' : slive.id,
                                        # })
                                        # self.env.cr.commit()
                                    else :
                                        slive = calm_data.service_life_id,
                                        slive.write({
                                            'at_install' : float(data[inspection_comp_hours]),
                                            'part_id' : comp.id,
                                            'action_type' : 'inspection',
                                            'unit' : 'hours',
                                            'value' : data[inspection_hours],
                                            'current' : float(data[inspection_current]), 
                                            'comments' : data[comment],    
                                        })
                                        self.env.cr.commit()
                                # CYCLES
                                if(data[cycles_on].upper() == 'TRUE'):
                                    if(data[cycles_type] == '1'):
                                        slive_type = 'retirement'
                                    elif(data[cycles_type] == '2'):
                                        slive_type = 'service'
                                    elif(data[cycles_type] == '3'):
                                        slive_type = 'inspection'
                                    elif(data[cycles_type] == '4'):
                                        slive_type = 'overhaul'

                                    csn = (float(data[aircraft_cycles]) - float(data[cycle_on_install]) + float(data[comp_cycles])) if comp.tsn < (float(data[aircraft_cycles]) - float(data[cycle_on_install]) + float(data[comp_cycles])) else comp.csn
                                    comp.update({
                                        # 'unknown_new' : False,
                                        'csn': (float(csn)),
                                        'cso': (float(data[cso])),
                                        'comp_cyclesinstallation' : float(data[comp_cycles]),
                                        'ac_cyclesinstallation' : float(data[aircraft_cycles]),
                                    })

                                    # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]),('file','=',data[rank]),('auxiliary_id','=',auxiliary.id)])
                                    # if calm_data.id == False:
                                    if(True):
                                        print data[comp_cycles] , ' <=> CYCLES'
                                        slive = self.env['ams.component.servicelife'].create({
                                            'at_install' : float(data[comp_cycles]),
                                            'part_id' : comp.id,
                                            'action_type' : slive_type,
                                            'unit' : 'cycles',
                                            'value' : float(data[cycles_value]),
                                            'current' : float(data[cycles_current]) + float(data[comp_cycles]), 
                                            'comments' : data[comment],
                                        })
                                        if len(data) > 165:
                                            if(data[ste_cy] != '0' and data[ste_cy] != ''):
                                                if (calm_data.service_life_id.id != False):
                                                    self.env['airworthy.ste'].create({
                                                        'service_life_id' : calm_data.service_life_id.id,
                                                        'value' : float(data[ste_cy])/float(100) * data[cycles_value],
                                                        'status' : 'dgcaapprove',
                                                        })
                                        self.env.cr.commit()
                                        # self.env['calm.dict'].create({
                                        #     'file' : data[rank],
                                        #     'auxiliary_id' : auxiliary.id,
                                        #     'part_id' : comp.id,
                                        #     'sequence' : data[calm_id],
                                        #     'service_life_id' : slive.id,
                                        # })
                                        # self.env.cr.commit()
                                    else :
                                        print data[comp_cycles] , ' <=> CYCLES'
                                        slive = calm_data.service_life_id,
                                        slive.write({
                                            'at_install' : float(data[comp_cycles]),
                                            'part_id' : comp.id,
                                            'action_type' : slive_type,
                                            'unit' : 'cycles',
                                            'value' : data[cycles_value],
                                            'current' : float(data[cycles_current]) + float(data[comp_cycles]),
                                            'comments' : data[comment],    
                                        })
                                        self.env.cr.commit()
                                # MONTH
                                if(data[month_on].upper() == 'TRUE'):
                                    if(data[month_type] == '1'):
                                        slive_type = 'inspection'
                                    elif(data[month_type] == '2'):
                                        slive_type = 'overhaul'
                                    elif(data[month_type] == '3'):
                                        slive_type = 'retirement'
                                    elif(data[month_type] == '4'):
                                        slive_type = 'service'

                                    comp.update({
                                        # 'unknown_new' : False,
                                        'date_installed' : data[month_date]
                                    })

                                    date_val = data[month_date]
                                    if(date_val == ''):
                                        date_val = data[inst_date]
                                    if(date_val != ''):
                                        # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]),('file','=',data[rank]),('auxiliary_id','=',auxiliary.id)])
                                        # if calm_data.id == False:
                                        if(True):
                                            slive = self.env['ams.component.servicelife'].create({
                                                'part_id' : comp.id,
                                                'action_type' : slive_type,
                                                'unit' : 'month',
                                                'value' : float(data[month_value]),
                                                'current' : False,
                                                'current_date' : date_val, 
                                                'comments' : data[comment],
                                            })
                                            self.env.cr.commit()
                                            # self.env['calm.dict'].create({
                                            #     'file' : data[rank],
                                            #     'auxiliary_id' : auxiliary.id,
                                            #     'part_id' : comp.id,
                                            #     'sequence' : data[calm_id],
                                            #     'service_life_id' : slive.id,
                                            # })
                                            # self.env.cr.commit()
                                        else :
                                            slive = calm_data.service_life_id,
                                            slive.write({
                                                'part_id' : comp.id,
                                                'action_type' : slive_type,
                                                'unit' : 'month',
                                                'value' : data[month_value],
                                                'current' : False,
                                                'current_date' : date_val,
                                                'comments' : data[comment],    
                                            })
                                            self.env.cr.commit()
                                # DAYS
                                if(data[days_on].upper() == 'TRUE'):
                                    if(data[days_type] == '1'):
                                        slive_type = 'inspection'
                                    elif(data[days_type] == '2'):
                                        slive_type = 'overhaul'
                                    elif(data[days_type] == '3'):
                                        slive_type = 'retirement'
                                    elif(data[days_type] == '4'):
                                        slive_type = 'service'

                                    comp.update({
                                        # 'unknown_new' : False,
                                        'date_installed' : data[days_date]
                                    })

                                    date_val = data[days_date]
                                    if(date_val == ''):
                                        date_val = data[inst_date]
                                    if(date_val != ''):
                                        # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]),('file','=',data[rank]),('auxiliary_id','=',auxiliary.id)])
                                        # if calm_data.id == False:
                                        if(True):
                                            slive = self.env['ams.component.servicelife'].create({
                                                'part_id' : comp.id,
                                                'action_type' : slive_type,
                                                'unit' : 'days',
                                                'value' : float(data[days_value]),
                                                'current' : False,
                                                'current_date' : date_val, 
                                                'comments' : data[comment],
                                            })
                                            self.env.cr.commit()
                                            # self.env['calm.dict'].create({
                                            #     'file' : data[rank],
                                            #     'auxiliary_id' : auxiliary.id,
                                            #     'part_id' : comp.id,
                                            #     'sequence' : data[calm_id],
                                            #     'service_life_id' : slive.id,
                                            # })
                                            # self.env.cr.commit()
                                        else :
                                            slive = calm_data.service_life_id,
                                            slive.write({
                                                'part_id' : comp.id,
                                                'action_type' : slive_type,
                                                'unit' : 'days',
                                                'value' : data[days_value],
                                                'current' : False,
                                                'current_date' : date_val,
                                                'comments' : data[comment],    
                                            })
                                            self.env.cr.commit()

    def set_inspection(self,AC_REG,calm_file,comptype):
        acraft = self.env['aircraft.acquisition'].search([('name','=',AC_REG)])
        self.env['ams.inspection'].search([('fleet_id','=',acraft.id)]).unlink()
        print 'Inspection Reading :: ' + str(calm_file)
        if(os.path.isfile(zipextract+str(calm_file)+".csv")):
            with open(zipextract+str(calm_file)+".csv") as myFile:  
                ro = list(csv.reader(myFile, delimiter=';'))
                acraft = self.env['aircraft.acquisition'].search([('name','=',AC_REG)])
                # file = open(zipextract+str(calm_file)+".csv", "r")
                # ro = file.readlines()
                slive_type = 'inspection'
                if(len(ro) >= 1):
                    if(ro[0][155] == 'CALMID'):
                        part_name = 0
                        last_time_insp = 94
                        rhll = 82
                        date_inst = 6
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
                    
                    elif(ro[0][165] == 'CALMID'):
                        part_name = 0
                        part_desc = 95
                        part_no = 1
                        last_time_insp = 94
                        rhll = 82
                        date_inst = 6
                        since_time_insp = 93
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

                    for g in ro:
                        data = g

                        if len(data) > 155:
                            print 'inspection ::' + str(data[part_name]) + ' desc : ' + str(data[part_desc])+ ' last : ' + str(data[rhll])+ ' since : ' + str(data[since_time_insp])
                            if(str(data[delete]).upper() == 'FALSE' and data[rank] == ''):
                                data = g

                                # PERHITUNGAN
                                comp_tso = 0
                                comp_cso = 0
                                comp_tsn = 0
                                comp_csn = 0

                                ata_id = self.env['ams.ata'].search([('name', '=', 'xx-xx-xx')])
                                if(data[ata_1] != '' or data[ata_2] != '' or data[ata_3] != ''):
                                    ata_string = data[ata_1].zfill(2) + '-' + data[ata_2].zfill(2) + '-' + data[ata_3].zfill(2)
                                    ata_id = self.env['ams.ata'].search([('name', '=', ata_string)])
                                    if(ata_id.id == False):
                                        ata_id = self.env['ams.ata'].create({
                                            'name' : ata_string,
                                            'chapter' : data[ata_1].zfill(2),
                                            'sub_chapter' : data[ata_2].zfill(2),
                                            'description' : 'ATA ' + ata_string,
                                            })

                                # comp = self.env['calm.dict'].search(['&','&',('service_life_id','=',False),('sequence','=',data[calm_id] + 'insp'),('file','=',data[rank]),('fleet_id','=',acraft.id)],limit=1).inspection_id
                                # if(comp.id == False):
                                comp = self.env['ams.inspection'].create({
                                    'fleet_id' : acraft.id,
                                    'inspection_type' : str(data[part_name]),
                                    'desc' : str(data[part_desc]),
                                    'ata_code' : ata_id.id,
                                    'one_time_insp' : False,
                                    'last_insp' : data[rhll],
                                    'since_insp' : data[since_time_insp],
                                    'install_at' : data[date_inst],
                                })
                                self.env.cr.commit()
                                    
                                #     calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','=',False),('sequence','=',data[calm_id] + 'insp'),('file','=',data[rank]),('fleet_id','=',acraft.id)])
                                #     if calm_data.id == False:
                                #         self.env['calm.dict'].create({
                                #             'file' : data[rank],
                                #             'fleet_id' : acraft.id,
                                #             'inspection_id' : comp.id,
                                #             'sequence' : data[calm_id] + 'insp',
                                #         })
                                #         self.env.cr.commit()
                                # else:
                                #     comp.update({
                                #         'fleet_id' : acraft.id,
                                #         'inspection_type' : str(data[part_name]),
                                #         'desc' : str(data[part_name]),
                                #         'ata_code' : ata_id.id,
                                #         'one_time_insp' : False,
                                #     })
                                # SERVICE LIFE
                                # INSPECTION
                                if(data[inspection].upper() == 'TRUE'):
                                    # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id] + 'insp'),('file','=',data[rank]),('fleet_id','=',acraft.id)])
                                    # if calm_data.id == False:
                                    slive = self.env['ams.component.servicelife'].create({
                                        'inspection_id' : comp.id,
                                        'action_type' : 'inspection',
                                        'unit' : 'hours',
                                        'value' : float(data[inspection_hours]),
                                        'current' : float(acraft.total_hours) - float(data[rhll]), 
                                        'comments' : data[comment],
                                    })
                                    # if len(data) > 165:
                                    #     if(data[ste_hr] != '0' and data[ste_hr] != ''):
                                    #         if (calm_data.service_life_id.id != False):
                                    #             self.env['airworthy.ste'].create({
                                    #                 'service_life_id' : calm_data.service_life_id.id,
                                    #                 'value' : float(data[ste_hr])/float(100) * data[inspection_hours],
                                    #                 'status' : 'dgcaapprove',
                                    #                 })
                                    self.env.cr.commit()
                                    # else :
                                    #     slive = calm_data.service_life_id,
                                    #     slive.write({
                                    #         'inspection_id' : comp.id,
                                    #         'action_type' : 'inspection',
                                    #         'unit' : 'hours',
                                    #         'value' : data[inspection_hours],
                                    #         'current' : (float(acraft.total_hours) - float(data[inspection_comp_attach_at])) + float(data[inspection_comp_hours]),
                                    #         'comments' : data[comment],    
                                    #     })
                                    #     self.env.cr.commit()

                                # CYCLES
                                if(data[cycles_on].upper() == 'TRUE'):
                                    if(data[cycles_type] == '1'):
                                        slive_type = 'retirement'
                                    elif(data[cycles_type] == '2'):
                                        slive_type = 'service'
                                    elif(data[cycles_type] == '3'):
                                        slive_type = 'inspection'
                                    elif(data[cycles_type] == '4'):
                                        slive_type = 'overhaul'

                                    # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id] + 'insp'),('file','=',data[rank]),('fleet_id','=',acraft.id)])
                                    # if calm_data.id == False:
                                    slive = self.env['ams.component.servicelife'].create({
                                        'inspection_id' : comp.id,
                                        'action_type' : slive_type,
                                        'unit' : 'cycles',
                                        'value' : float(data[cycles_value]),
                                        'current' : float(data[cycles_current]) + float(data[comp_cycles]), 
                                        'comments' : data[comment],
                                    })
                                    # if len(data) > 165:
                                    #     if(data[ste_cy] != '0' and data[ste_cy] != ''):
                                    #         if (slive.id != False):
                                    #             self.env['airworthy.ste'].create({
                                    #                 'service_life_id' : slive.id,
                                    #                 'value' : float(data[ste_cy])/float(100) * data[cycles_value],
                                    #                 'status' : 'dgcaapprove',
                                    #                 })
                                    self.env.cr.commit()
                                    # else :
                                    #     slive = slive,
                                    #     slive.write({
                                    #         'inspection_id' : comp.id,
                                    #         'action_type' : slive_type,
                                    #         'unit' : 'cycles',
                                    #         'value' : data[cycles_value],
                                    #         'current' : float(data[cycles_current]) + float(data[comp_cycles]),
                                    #         'comments' : data[comment],    
                                    #     })
                                    #     self.env.cr.commit()
                                # MONTH
                                if(data[month_on].upper() == 'TRUE'):
                                    if(data[month_type] == '1'):
                                        slive_type = 'inspection'
                                    elif(data[month_type] == '2'):
                                        slive_type = 'overhaul'
                                    elif(data[month_type] == '3'):
                                        slive_type = 'retirement'
                                    elif(data[month_type] == '4'):
                                        slive_type = 'service'

                                    date_val = data[month_date]
                                    if(date_val == ''):
                                        date_val = data[inst_date]
                                    if(date_val != ''):
                                        # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id] + 'insp'),('file','=',data[rank]),('fleet_id','=',acraft.id)])
                                        # if calm_data.id == False:
                                        slive = self.env['ams.component.servicelife'].create({
                                            'inspection_id' : comp.id,
                                            'action_type' : slive_type,
                                            'unit' : 'month',
                                            'value' : float(data[month_value]),
                                            'current' : False,
                                            'current_date' : date_val, 
                                            'comments' : data[comment],
                                        })
                                        self.env.cr.commit()
                                        # else :
                                        #     slive = slive,
                                        #     slive.write({
                                        #         'inspection_id' : comp.id,
                                        #         'action_type' : slive_type,
                                        #         'unit' : 'month',
                                        #         'value' : data[month_value],
                                        #         'current' : False,
                                        #         'current_date' : date_val,
                                        #         'comments' : data[comment],    
                                        #     })
                                        #     self.env.cr.commit()
                                # DAYS
                                if(data[days_on].upper() == 'TRUE'):
                                    if(data[days_type] == '1'):
                                        slive_type = 'inspection'
                                    elif(data[days_type] == '2'):
                                        slive_type = 'overhaul'
                                    elif(data[days_type] == '3'):
                                        slive_type = 'retirement'
                                    elif(data[days_type] == '4'):
                                        slive_type = 'service'

                                    date_val = data[days_date]
                                    if(date_val == ''):
                                        date_val = data[inst_date]
                                    if(date_val != ''):
                                        # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id] + 'insp'),('file','=',data[rank]),('fleet_id','=',acraft.id)])
                                        # if calm_data.id == False:
                                        slive = self.env['ams.component.servicelife'].create({
                                            'inspection_id' : comp.id,
                                            'action_type' : slive_type,
                                            'unit' : 'days',
                                            'value' : float(data[days_value]),
                                            'current' : False,
                                            'current_date' : date_val, 
                                            'comments' : data[comment],
                                        })
                                        self.env.cr.commit()
                                        # else :
                                        #     slive = slive,
                                        #     slive.write({
                                        #         'inspection_id' : comp.id,
                                        #         'action_type' : slive_type,
                                        #         'unit' : 'days',
                                        #         'value' : data[days_value],
                                        #         'current' : False,
                                        #         'current_date' : date_val,
                                        #         'comments' : data[comment],    
                                        #     })
                                        #     self.env.cr.commit()

    def set_inspection_engine(self,engine_id,calm_file,comptype):
        self.env['ams.inspection'].search([('engine_id','=',engine_id)]).unlink()
        print 'Inspection Reading :: ' + str(calm_file)
        if(os.path.isfile(zipextract+str(calm_file)+".csv")):
            with open(zipextract+str(calm_file)+".csv") as myFile:  
                ro = list(csv.reader(myFile, delimiter=';'))
                # engine = self.env['aircraft.acquisition'].search([('name','=',AC_REG)])
                engine = self.env['engine.type'].search([('id','=',engine_id)])
                # file = open(zipextract+str(calm_file)+".csv", "r")
                # ro = file.readlines()
                slive_type = 'inspection'
                if(len(ro) >= 1):
                    if(ro[0][155] == 'CALMID'):
                        part_name = 0
                        part_desc = 95
                        part_no = 1
                        last_time_insp = 94
                        rhll = 82
                        date_inst = 6
                        since_time_insp = 93
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
                    
                    elif(ro[0][165] == 'CALMID'):
                        part_name = 0
                        part_desc = 95
                        part_no = 1
                        last_time_insp = 94
                        rhll = 82
                        date_inst = 6
                        since_time_insp = 93
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

                    for g in ro:
                        data = g

                        if len(data) > 155:
                            print 'inspection ::' + str(data[part_name]) + ' desc : ' + str(data[part_desc])+ ' last : ' + str(data[rhll])+ ' since : ' + str(data[since_time_insp])
                            if(str(data[delete]).upper() == 'FALSE' and data[rank] == ''):
                                data = g

                                # PERHITUNGAN
                                comp_tso = 0
                                comp_cso = 0
                                comp_tsn = 0
                                comp_csn = 0

                                ata_id = self.env['ams.ata'].search([('name', '=', 'xx-xx-xx')])
                                if(data[ata_1] != '' or data[ata_2] != '' or data[ata_3] != ''):
                                    ata_string = data[ata_1].zfill(2) + '-' + data[ata_2].zfill(2) + '-' + data[ata_3].zfill(2)
                                    ata_id = self.env['ams.ata'].search([('name', '=', ata_string)])
                                    if(ata_id.id == False):
                                        ata_id = self.env['ams.ata'].create({
                                            'name' : ata_string,
                                            'chapter' : data[ata_1].zfill(2),
                                            'sub_chapter' : data[ata_2].zfill(2),
                                            'description' : 'ATA ' + ata_string,
                                            })

                                # comp = self.env['calm.dict'].search(['&','&',('service_life_id','=',False),('sequence','=',data[calm_id]+'insp'),('file','=',data[rank]),('engine_id','=',engine.id)],limit=1).inspection_id
                                # if(comp.id == False):
                                comp = self.env['ams.inspection'].create({
                                    'engine_id' : engine.id,
                                    'inspection_type' : str(data[part_name]),
                                    'desc' : str(data[part_desc]),
                                    'ata_code' : ata_id.id,
                                    'one_time_insp' : False,
                                    'last_insp' : data[rhll],
                                    'since_insp' : data[since_time_insp],
                                    'install_at' : data[date_inst],
                                })
                                self.env.cr.commit()
                                    
                                #     calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','=',False),('sequence','=',data[calm_id]+'insp'),('file','=',data[rank]),('engine_id','=',engine.id)])
                                #     if calm_data.id == False:
                                #         self.env['calm.dict'].create({
                                #             'file' : data[rank],
                                #             'engine_id' : engine.id,
                                #             'inspection_id' : comp.id,
                                #             'sequence' : data[calm_id]+'insp',
                                #         })
                                #         self.env.cr.commit()
                                # else:
                                #     comp.update({
                                #         'engine_id' : engine.id,
                                #         'inspection_type' : str(data[part_name]),
                                #         'desc' : str(data[part_name]),
                                #         'ata_code' : ata_id.id,
                                #         'one_time_insp' : False,
                                #     })
                                # SERVICE LIFE
                                # INSPECTION
                                if(data[inspection].upper() == 'TRUE'):
                                    # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]+'insp'),('file','=',data[rank]),('engine_id','=',engine.id)])
                                    # if calm_data.id == False:
                                    slive = self.env['ams.component.servicelife'].create({
                                        'inspection_id' : comp.id,
                                        'action_type' : 'inspection',
                                        'unit' : 'hours',
                                        'value' : float(data[inspection_hours]),
                                        'current' : float(engine.engine_tsn) - float(data[rhll]), 
                                        'comments' : data[comment],
                                    })
                                    # if len(data) > 165:
                                    #     if(data[ste_hr] != '0' and data[ste_hr] != ''):
                                    #         if (slive.id != False):
                                    #             self.env['airworthy.ste'].create({
                                    #                 'service_life_id' : slive.id,
                                    #                 'value' : float(data[ste_hr])/float(100) * data[inspection_hours],
                                    #                 'status' : 'dgcaapprove',
                                    #                 })
                                    self.env.cr.commit()
                                    # else :
                                    #     slive = slive,
                                    #     slive.write({
                                    #         'inspection_id' : comp.id,
                                    #         'action_type' : 'inspection',
                                    #         'unit' : 'hours',
                                    #         'value' : data[inspection_hours],
                                    #         'current' : (float(engine.total_hours) - float(data[inspection_comp_attach_at])) + float(data[inspection_comp_hours]),
                                    #         'comments' : data[comment],    
                                    #     })
                                    #     self.env.cr.commit()

                                # CYCLES
                                if(data[cycles_on].upper() == 'TRUE'):
                                    if(data[cycles_type] == '1'):
                                        slive_type = 'retirement'
                                    elif(data[cycles_type] == '2'):
                                        slive_type = 'service'
                                    elif(data[cycles_type] == '3'):
                                        slive_type = 'inspection'
                                    elif(data[cycles_type] == '4'):
                                        slive_type = 'overhaul'

                                    # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]+'insp'),('file','=',data[rank]),('engine_id','=',engine.id)])
                                    # if calm_data.id == False:
                                    slive = self.env['ams.component.servicelife'].create({
                                        'inspection_id' : comp.id,
                                        'action_type' : slive_type,
                                        'unit' : 'cycles',
                                        'value' : float(data[cycles_value]),
                                        'current' : float(data[cycles_current]) + float(data[comp_cycles]), 
                                        'comments' : data[comment],
                                    })
                                    # if len(data) > 165:
                                    #     if(data[ste_cy] != '0' and data[ste_cy] != ''):
                                    #         if (slive.id != False):
                                    #             self.env['airworthy.ste'].create({
                                    #                 'service_life_id' : slive.id,
                                    #                 'value' : float(data[ste_cy])/float(100) * data[cycles_value],
                                    #                 'status' : 'dgcaapprove',
                                    #                 })
                                    self.env.cr.commit()
                                    # else :
                                    #     slive = slive,
                                    #     slive.write({
                                    #         'inspection_id' : comp.id,
                                    #         'action_type' : slive_type,
                                    #         'unit' : 'cycles',
                                    #         'value' : data[cycles_value],
                                    #         'current' : float(data[cycles_current]) + float(data[comp_cycles]),
                                    #         'comments' : data[comment],    
                                    #     })
                                    #     self.env.cr.commit()
                                # MONTH
                                if(data[month_on].upper() == 'TRUE'):
                                    if(data[month_type] == '1'):
                                        slive_type = 'inspection'
                                    elif(data[month_type] == '2'):
                                        slive_type = 'overhaul'
                                    elif(data[month_type] == '3'):
                                        slive_type = 'retirement'
                                    elif(data[month_type] == '4'):
                                        slive_type = 'service'

                                    date_val = data[month_date]
                                    if(date_val == ''):
                                        date_val = data[inst_date]
                                    if(date_val != ''):
                                        # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]+'insp'),('file','=',data[rank]),('engine_id','=',engine.id)])
                                        # if calm_data.id == False:
                                        slive = self.env['ams.component.servicelife'].create({
                                            'inspection_id' : comp.id,
                                            'action_type' : slive_type,
                                            'unit' : 'month',
                                            'value' : float(data[month_value]),
                                            'current' : False,
                                            'current_date' : date_val, 
                                            'comments' : data[comment],
                                        })
                                        self.env.cr.commit()
                                        # else :
                                        #     slive = slive,
                                        #     slive.write({
                                        #         'inspection_id' : comp.id,
                                        #         'action_type' : slive_type,
                                        #         'unit' : 'month',
                                        #         'value' : data[month_value],
                                        #         'current' : False,
                                        #         'current_date' : date_val,
                                        #         'comments' : data[comment],    
                                        #     })
                                        #     self.env.cr.commit()
                                # DAYS
                                if(data[days_on].upper() == 'TRUE'):
                                    if(data[days_type] == '1'):
                                        slive_type = 'inspection'
                                    elif(data[days_type] == '2'):
                                        slive_type = 'overhaul'
                                    elif(data[days_type] == '3'):
                                        slive_type = 'retirement'
                                    elif(data[days_type] == '4'):
                                        slive_type = 'service'

                                    date_val = data[days_date]
                                    if(date_val == ''):
                                        date_val = data[inst_date]
                                    if(date_val != ''):
                                        # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]+'insp'),('file','=',data[rank]),('engine_id','=',engine.id)])
                                        # if calm_data.id == False:
                                        slive = self.env['ams.component.servicelife'].create({
                                            'inspection_id' : comp.id,
                                            'action_type' : slive_type,
                                            'unit' : 'days',
                                            'value' : float(data[days_value]),
                                            'current' : False,
                                            'current_date' : date_val, 
                                            'comments' : data[comment],
                                        })
                                        self.env.cr.commit()
                                        # else :
                                        #     slive = slive,
                                        #     slive.write({
                                        #         'inspection_id' : comp.id,
                                        #         'action_type' : slive_type,
                                        #         'unit' : 'days',
                                        #         'value' : data[days_value],
                                        #         'current' : False,
                                        #         'current_date' : date_val,
                                        #         'comments' : data[comment],    
                                        #     })
                                        #     self.env.cr.commit()
    def set_inspection_auxiliary(self,auxiliary_id,calm_file,comptype):
        self.env['ams.inspection'].search([('auxiliary_id','=',auxiliary_id)]).unlink()
        print 'Inspection Reading :: ' + str(calm_file)
        if(os.path.isfile(zipextract+str(calm_file)+".csv")):
            with open(zipextract+str(calm_file)+".csv") as myFile:  
                ro = list(csv.reader(myFile, delimiter=';'))
                # auxiliary = self.env['aircraft.acquisition'].search([('name','=',AC_REG)])
                auxiliary = self.env['auxiliary.type'].search([('id','=',auxiliary_id)])
                # file = open(zipextract+str(calm_file)+".csv", "r")
                # ro = file.readlines()
                slive_type = 'inspection'
                if(len(ro) >= 1):
                    if(ro[0][155] == 'CALMID'):
                        part_name = 0
                        part_desc = 95
                        part_no = 1
                        last_time_insp = 94
                        rhll = 82
                        date_inst = 6
                        since_time_insp = 93
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
                    
                    elif(ro[0][165] == 'CALMID'):
                        part_name = 0
                        part_desc = 95
                        part_no = 1
                        last_time_insp = 94
                        rhll = 82
                        date_inst = 6
                        since_time_insp = 93
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

                    for g in ro:
                        data = g

                        if len(data) > 155:
                            print 'inspection ::' + str(data[part_name]) + ' desc : ' + str(data[part_desc])+ ' last : ' + str(data[rhll])+ ' since : ' + str(data[since_time_insp])
                            if(str(data[delete]).upper() == 'FALSE' and data[rank] == ''):
                                data = g

                                # PERHITUNGAN
                                comp_tso = 0
                                comp_cso = 0
                                comp_tsn = 0
                                comp_csn = 0

                                ata_id = self.env['ams.ata'].search([('name', '=', 'xx-xx-xx')])
                                if(data[ata_1] != '' or data[ata_2] != '' or data[ata_3] != ''):
                                    ata_string = data[ata_1].zfill(2) + '-' + data[ata_2].zfill(2) + '-' + data[ata_3].zfill(2)
                                    ata_id = self.env['ams.ata'].search([('name', '=', ata_string)])
                                    if(ata_id.id == False):
                                        ata_id = self.env['ams.ata'].create({
                                            'name' : ata_string,
                                            'chapter' : data[ata_1].zfill(2),
                                            'sub_chapter' : data[ata_2].zfill(2),
                                            'description' : 'ATA ' + ata_string,
                                            })

                                # comp = self.env['calm.dict'].search(['&','&',('service_life_id','=',False),('sequence','=',data[calm_id]+'insp'),('file','=',data[rank]),('auxiliary_id','=',auxiliary.id)],limit=1).inspection_id
                                # if(comp.id == False):
                                comp = self.env['ams.inspection'].create({
                                    'auxiliary_id' : auxiliary.id,
                                    'inspection_type' : str(data[part_name]),
                                    'desc' : str(data[part_desc]),
                                    'ata_code' : ata_id.id,
                                    'one_time_insp' : False,
                                    'last_insp' : data[rhll],
                                    'install_at' : data[date_inst],
                                    'since_insp' : data[since_time_insp],
                                })
                                self.env.cr.commit()
                                    
                                #     calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','=',False),('sequence','=',data[calm_id]+'insp'),('file','=',data[rank]),('auxiliary_id','=',auxiliary.id)])
                                #     if calm_data.id == False:
                                #         self.env['calm.dict'].create({
                                #             'file' : data[rank],
                                #             'auxiliary_id' : auxiliary.id,
                                #             'inspection_id' : comp.id,
                                #             'sequence' : data[calm_id]+'insp',
                                #         })
                                #         self.env.cr.commit()
                                # else:
                                #     comp.update({
                                #         'auxiliary_id' : auxiliary.id,
                                #         'inspection_type' : str(data[part_name]),
                                #         'desc' : str(data[part_name]),
                                #         'ata_code' : ata_id.id,
                                #         'one_time_insp' : False,
                                #     })
                                # SERVICE LIFE
                                # INSPECTION
                                if(data[inspection].upper() == 'TRUE'):
                                    # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]+'insp'),('file','=',data[rank]),('auxiliary_id','=',auxiliary.id)])
                                    # if calm_data.id == False:
                                    slive = self.env['ams.component.servicelife'].create({
                                        'inspection_id' : comp.id,
                                        'action_type' : 'inspection',
                                        'unit' : 'hours',
                                        'value' : float(data[inspection_hours]),
                                        'current' : float(auxiliary.auxiliary_tsn) - float(data[rhll]), 
                                        'comments' : data[comment],
                                    })
                                    # if len(data) > 165:
                                    #     if(data[ste_hr] != '0' and data[ste_hr] != ''):
                                    #         if (slive.id != False):
                                    #             self.env['airworthy.ste'].create({
                                    #                 'service_life_id' : slive.id,
                                    #                 'value' : float(data[ste_hr])/float(100) * data[inspection_hours],
                                    #                 'status' : 'dgcaapprove',
                                    #                 })
                                    self.env.cr.commit()
                                    # else :
                                    #     slive = slive,
                                    #     slive.write({
                                    #         'inspection_id' : comp.id,
                                    #         'action_type' : 'inspection',
                                    #         'unit' : 'hours',
                                    #         'value' : data[inspection_hours],
                                    #         'current' : (float(auxiliary.total_hours) - float(data[inspection_comp_attach_at])) + float(data[inspection_comp_hours]),
                                    #         'comments' : data[comment],    
                                    #     })
                                    #     self.env.cr.commit()

                                # CYCLES
                                if(data[cycles_on].upper() == 'TRUE'):
                                    if(data[cycles_type] == '1'):
                                        slive_type = 'retirement'
                                    elif(data[cycles_type] == '2'):
                                        slive_type = 'service'
                                    elif(data[cycles_type] == '3'):
                                        slive_type = 'inspection'
                                    elif(data[cycles_type] == '4'):
                                        slive_type = 'overhaul'

                                    # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]+'insp'),('file','=',data[rank]),('auxiliary_id','=',auxiliary.id)])
                                    # if calm_data.id == False:
                                    slive = self.env['ams.component.servicelife'].create({
                                        'inspection_id' : comp.id,
                                        'action_type' : slive_type,
                                        'unit' : 'cycles',
                                        'value' : float(data[cycles_value]),
                                        'current' : float(data[cycles_current]) + float(data[comp_cycles]), 
                                        'comments' : data[comment],
                                    })
                                    # if len(data) > 165:
                                    #     if(data[ste_cy] != '0' and data[ste_cy] != ''):
                                    #         if (slive.id != False):
                                    #             self.env['airworthy.ste'].create({
                                    #                 'service_life_id' : slive.id,
                                    #                 'value' : float(data[ste_cy])/float(100) * data[cycles_value],
                                    #                 'status' : 'dgcaapprove',
                                    #                 })
                                    self.env.cr.commit()
                                    # else :
                                    #     slive = slive,
                                    #     slive.write({
                                    #         'inspection_id' : comp.id,
                                    #         'action_type' : slive_type,
                                    #         'unit' : 'cycles',
                                    #         'value' : data[cycles_value],
                                    #         'current' : float(data[cycles_current]) + float(data[comp_cycles]),
                                    #         'comments' : data[comment],    
                                    #     })
                                    #     self.env.cr.commit()
                                # MONTH
                                if(data[month_on].upper() == 'TRUE'):
                                    if(data[month_type] == '1'):
                                        slive_type = 'inspection'
                                    elif(data[month_type] == '2'):
                                        slive_type = 'overhaul'
                                    elif(data[month_type] == '3'):
                                        slive_type = 'retirement'
                                    elif(data[month_type] == '4'):
                                        slive_type = 'service'

                                    date_val = data[month_date]
                                    if(date_val == ''):
                                        date_val = data[inst_date]
                                    if(date_val != ''):
                                        # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]+'insp'),('file','=',data[rank]),('auxiliary_id','=',auxiliary.id)])
                                        # if calm_data.id == False:
                                        slive = self.env['ams.component.servicelife'].create({
                                            'inspection_id' : comp.id,
                                            'action_type' : slive_type,
                                            'unit' : 'month',
                                            'value' : float(data[month_value]),
                                            'current' : False,
                                            'current_date' : date_val, 
                                            'comments' : data[comment],
                                        })
                                        self.env.cr.commit()
                                        # else :
                                        #     slive = slive,
                                        #     slive.write({
                                        #         'inspection_id' : comp.id,
                                        #         'action_type' : slive_type,
                                        #         'unit' : 'month',
                                        #         'value' : data[month_value],
                                        #         'current' : False,
                                        #         'current_date' : date_val,
                                        #         'comments' : data[comment],    
                                        #     })
                                        #     self.env.cr.commit()
                                # DAYS
                                if(data[days_on].upper() == 'TRUE'):
                                    if(data[days_type] == '1'):
                                        slive_type = 'inspection'
                                    elif(data[days_type] == '2'):
                                        slive_type = 'overhaul'
                                    elif(data[days_type] == '3'):
                                        slive_type = 'retirement'
                                    elif(data[days_type] == '4'):
                                        slive_type = 'service'

                                    date_val = data[days_date]
                                    if(date_val == ''):
                                        date_val = data[inst_date]
                                    if(date_val != ''):
                                        # calm_data = self.env['calm.dict'].search(['&','&','&',('service_life_id','!=',False),('sequence','=',data[calm_id]+'insp'),('file','=',data[rank]),('auxiliary_id','=',auxiliary.id)])
                                        # if calm_data.id == False:
                                        slive = self.env['ams.component.servicelife'].create({
                                            'inspection_id' : comp.id,
                                            'action_type' : slive_type,
                                            'unit' : 'days',
                                            'value' : float(data[days_value]),
                                            'current' : False,
                                            'current_date' : date_val, 
                                            'comments' : data[comment],
                                        })
                                        self.env.cr.commit()
                                        # else :
                                        #     slive = slive,
                                        #     slive.write({
                                        #         'inspection_id' : comp.id,
                                        #         'action_type' : slive_type,
                                        #         'unit' : 'days',
                                        #         'value' : data[days_value],
                                        #         'current' : False,
                                        #         'current_date' : date_val,
                                        #         'comments' : data[comment],    
                                        #     })
                                        #     self.env.cr.commit()
