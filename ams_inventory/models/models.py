# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from xlrd import open_workbook
import base64
import io
import pyexcel as p
import re
import tempfile
import cStringIO

class ProductStock(models.Model):
    _name = 'ams.stock'
    
    product_id = fields.Many2one('product.product', 'Product',required=True)
    bin_id = fields.Many2one('ams.bin', 'Warehouse',required=True)
    base_id = fields.Many2one('base.operation', string='Location', related='bin_id.base_id')
    stock_on_hand = fields.Float(string='Stock Available',default=0)
    stock_scrap = fields.Float(string='Scrap',default=0)



class ProductInheritance(models.Model):
    _inherit = 'product.product'

    qmap = fields.Char(string='Key-Map')
    is_part = fields.Boolean(string='Is Part', default=False)

class StockSerialInheritance(models.Model):
    _inherit = 'stock.production.lot'

    status = fields.Char(string='SysStatus')
    product_id = fields.Many2one('product.product', 'Product',domain=[('type', 'in', ['product', 'consu'])], required=True, default=lambda self:self.env.context.get('product_id',False))
    csn = fields.Float('CSN')
    cso = fields.Float('CSO')
    tsn = fields.Float('TSN')
    tso = fields.Float('TSO')
    rsn = fields.Float('RSN')
    rso = fields.Float('RIN')
    is_overhaul = fields.Boolean('Hast been Overhaul', default=False)
    unknown_new = fields.Boolean('Unknown TSN / CSN', default=False)
    tracing_loc = fields.Char('Location',compute='_compute_location')
    csn_compute = fields.Float('CSN',compute='_compute_slive')
    cso_compute = fields.Float('CSO',compute='_compute_slive')
    tsn_compute = fields.Float('TSN',compute='_compute_slive')
    tso_compute = fields.Float('TSO',compute='_compute_slive')

    servicelife_ids = fields.One2many('ams.component.servicelife', 'ref_id', 'Servicelife')

    @api.one
    @api.model
    def _compute_slive(self):
        comp_id = self.env['ams.component.part'].search(['&',('serial_number','=',self.id),('product_id','=',self.product_id.id)],limit=1)
        
        if(comp_id.id != False):
            self.csn_compute = comp_id.csn
            self.cso_compute = comp_id.cso
            self.tsn_compute = comp_id.tsn
            self.tso_compute = comp_id.tso
        else:
            self.csn_compute = self.csn
            self.cso_compute = self.cso
            self.tsn_compute = self.tsn
            self.tso_compute = self.tso


    @api.one
    @api.model
    def _compute_location(self):
        comp_id = self.env['ams.component.part'].search([('serial_number','=',self.id)])
        if(comp_id.id == False):
            self.tracing_loc = 'In Inventory'
        else:
            if(comp_id.fleet_id.id != False):
                fleet_id = self.env['aircraft.acquisition'].search([('id','=',comp_id.fleet_id.id)],limit=1) 
            elif(comp_id.engine_id.id != False):
                fleet_id = self.env['aircraft.acquisition'].search(['|','|','|',('engine_type_id','=',comp_id.engine_id.id),('engine2_type_id','=',comp_id.engine_id.id),('engine3_type_id','=',comp_id.engine_id.id),('engine4_type_id','=',comp_id.engine_id.id)],limit=1) 
            elif(comp_id.propeller_id.id != False):
                fleet_id = self.env['aircraft.acquisition'].search(['|','|','|',('propeller_type_id','=',comp_id.propeller_id.id),('propeller2_type_id','=',comp_id.propeller_id.id),('propeller3_type_id','=',comp_id.propeller_id.id),('propeller4_type_id','=',comp_id.propeller_id.id)],limit=1) 
            elif(comp_id.auxiliary_id.id != False):
                fleet_id = self.env['aircraft.acquisition'].search([('auxiliary_type_id','=',comp_id.auxiliary_id.id)],limit=1) 
            elif(comp_id.part_id.id != False):
                part_id = self.env['ams.component.part'].search([('id','=',comp_id.part_id.id)],limit=1)
                if(part_id.part_id.id != False):
                    part_id = part_id.part_id
                if(part_id.fleet_id.id != False):
                    fleet_id = self.env['aircraft.acquisition'].search([('id','=',part_id.fleet_id.id)],limit=1) 
                elif(part_id.engine_id.id != False):
                    fleet_id = self.env['aircraft.acquisition'].search(['|','|','|',('engine_type_id','=',part_id.engine_id.id),('engine2_type_id','=',part_id.engine_id.id),('engine3_type_id','=',part_id.engine_id.id),('engine4_type_id','=',part_id.engine_id.id)],limit=1) 
                elif(part_id.propeller_id.id != False):
                    fleet_id = self.env['aircraft.acquisition'].search(['|','|','|',('propeller_type_id','=',part_id.propeller_id.id),('propeller2_type_id','=',part_id.propeller_id.id),('propeller3_type_id','=',part_id.propeller_id.id),('propeller4_type_id','=',part_id.propeller_id.id)],limit=1) 
                elif(part_id.auxiliary_id.id != False):
                    fleet_id = self.env['aircraft.acquisition'].search([('auxiliary_type_id','=',part_id.auxiliary_id.id)],limit=1) 
            if 'fleet_id' in locals() or 'fleet_id' in globals():
                self.tracing_loc = 'Attached in ' + fleet_id.name


class ams_inventory_import(models.Model):
    _name = 'ams_inventory.import'

    date_import = fields.Datetime(string='Import Date')
    ih_09   = fields.Binary(string='IH09 (List Master Part)', required=True)
    name_ih = fields.Char(string='IH09 (List Master Part)')
    iq_09   = fields.Binary(string='IQ09 (List Serial Number)', required=True)
    name_iq = fields.Char(string='IQ09 (List Serial Number)')
    mb_52   = fields.Binary(string='MB52 (Stock Quantity)', required=True)
    name_mb = fields.Char(string='MB52 (Stock Quantity)')
    status  = fields.Boolean()

    @api.multi
    def process_data_master_part(self, id):
        # r_data = self.search([('id','=', self.id)], limit=1)
        r_data = self.search([('id','=', id)], limit=1)
        ih_09 = r_data.ih_09
        iq_09 = r_data.iq_09
        mb_52 = r_data.mb_52

        # statusimport 
        ih_status = False
        iq_status = False
        mb_status = False

        # print "===================================="
        # print 'PROCESSED MASTER DATA'
        # print r_data
        # print "===================================="
        
        if(ih_09):

            try:
                #################
                #OPEN WORKBOOK ##
                #################
                wb = open_workbook(file_contents = base64.decodestring(ih_09))
                sheet = wb.sheets()[0]

                ######################################
                ## CREATE RAW DATA FROM SPREADSHEET ##
                ######################################
                raw_data = []
                for row_no in range(sheet.nrows):
                    zero_col = 0
                    if row_no < 0:
                        fields = map(lambda row:row.value.encode('utf-8'), sheet.row(row_no))
                    else:
                        for col in sheet.row(row_no):
                            if not col.value:
                                zero_col = zero_col + 1
                        if zero_col < sheet.ncols:
                            raw_data.append(map(lambda row:isinstance(row.value, str) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))

                ## GET HEADER SPREADSHEET
                header = map(lambda x:x.lower(), raw_data[0])
                
                ## DATA PROCCESS
                if 'material' in header:
                    index_qmap = header.index('material')
                    index_name = [idx for idx, s in enumerate(header) if 'description' in s]
                    
                        
                    for i in xrange(1,len(raw_data)):

                        product_name = ""
                        if index_name:
                            product_name = raw_data[i][index_name[0]]

                        ## search data product by qmap
                        product_by_qmap = self.env['product.product'].search([('qmap','=',raw_data[i][index_qmap])], limit=1)

                        if product_by_qmap.id == False:
                            self.env['product.product'].create({
                                'qmap':raw_data[i][index_qmap],
                                'short_name':product_name,
                                'name':product_name,
                                'purchase_ok':True,
                                'categ_id':1,
                                'type':'product',
                                'tracking':'none',
                                'invoice_policy':'order',
                                'purchase_method':'receive',
                            })
                            self.env.cr.commit()
                            ih_status = True
                    

            except Exception as e:
                raise ValidationError('An error occurred, %s' %(e))

            # print 'IH09'
            # with open("ih09.xlsx", "wb") as fh:
            #     fh.write(ih_09.decode('base64'))
            # with file("ih09.xlsx") as f:
            #     text = f.read()
            # data_array = text.split('\n')

            # for g in range(ih09.nrows):
                # n += 1
                # # data = data_array[g].split('\t')
                # serial = ih09.cell_value(n, 5)
                # qmap = ih09.cell_value(n, 2)
                # print "==================================="
                # print ih09.cell_value(n, 1)
                # print serial
                # print qmap
                # print "==================================="

                # same_product_by_qmap = self.env['product.product'].search([('qmap','=',qmap)])
                # same_product_by_serial = self.env['product.product'].search([('default_code','=',serial)])
                # if(same_product_by_qmap):
                #     self.env['product.product'].search([('qmap','=',qmap)]).write({
                #             'name':ih09.cell_value(n, 3),
                #             'short_name':ih09.cell_value(n, 3),
                #             'default_code':ih09.cell_value(n, 5),
                #             'purchase_ok':True,
                #             'categ_id':1,
                #             'type':'product',
                #             'tracking':'none',
                #             'invoice_policy':'order',
                #             'purchase_method':'receive',
                #         })
                # elif(same_product_by_serial):
                #     self.env['product.product'].search([('default_code','=',serial)]).write({
                #             'qmap':ih09.cell_value(n, 2),
                #             'name':ih09.cell_value(n, 3),
                #             'short_name':ih09.cell_value(n, 3),
                #             'default_code':ih09.cell_value(n, 5),
                #             'purchase_ok':True,
                #             'categ_id':1,
                #             'type':'product',
                #             'tracking':'none',
                #             'invoice_policy':'order',
                #             'purchase_method':'receive',
                #         })
                # else:
                #     self.env['product.product'].create({
                #             'qmap':ih09.cell_value(n, 2),
                #             'name':ih09.cell_value(n, 3),
                #             'short_name':ih09.cell_value(n, 3),
                #             'default_code':ih09.cell_value(n, 5),
                #             'purchase_ok':True,
                #             'categ_id':1,
                #             'type':'product',
                #             'tracking':'none',
                #             'invoice_policy':'order',
                #             'purchase_method':'receive',
                #         })
                # self.env.cr.commit()
        if(iq_09):
            

            try:

                #################
                #OPEN WORKBOOK ##
                #################
                wb = open_workbook(file_contents = base64.decodestring(iq_09))
                sheet = wb.sheets()[0]

                ######################################
                ## CREATE RAW DATA FROM SPREADSHEET ##
                ######################################
                raw_data = []
                for row_no in range(sheet.nrows):
                    zero_col = 0
                    if row_no < 0:
                        fields = map(lambda row:row.value.encode('utf-8'), sheet.row(row_no))
                    else:
                        for col in sheet.row(row_no):
                            if not col.value:
                                zero_col = zero_col + 1
                        if zero_col < sheet.ncols:
                            raw_data.append(map(lambda row:isinstance(row.value, str) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
                    
                ## GET HEADER SPREADSHEET
                header = map(lambda x:x.lower(), raw_data[0])
                
                ## DATA PROCESS
                if 'material' in header:
                    index_qmap   = header.index('material')
                    index_serial = [idx for idx, s in enumerate(header) if 'serial' in s]
                    index_name   = [idx for idx, s in enumerate(header) if 'description' in s]

                    for i in xrange(1,len(raw_data)):
                        
                        ## SET PRODUCT NAME FROM MATERIAL
                        product_name    = ""
                        if index_name:
                            product_name = raw_data[i][index_name[0]]

                        ## Search data product
                        product_by_qmap     = self.env['product.product'].search([('qmap','=',raw_data[i][index_qmap])], limit=1)
                        product_by_serial   = self.env['product.product'].search([('default_code','=',raw_data[i][index_serial[0]])], limit=1)

                        if (product_by_qmap.id == False and product_by_serial.id == False) or (product_by_qmap.id != False and product_by_serial.id == False):
                            self.env['product.product'].create({
                                'qmap':raw_data[i][index_qmap],
                                'default_code': raw_data[i][index_serial[0]],
                                'short_name':product_name,
                                'name':product_name,
                                'purchase_ok':True,
                                'categ_id':1,
                                'type':'product',
                                'tracking':'none',
                                'invoice_policy':'order',
                                'purchase_method':'receive',
                            })
                            self.env.cr.commit()
                            iq_status = True
                    

            except Exception as e:
                raise ValidationError('An error occurred, %s' %(e))

            # print 'IQ09'
            # with open("iq09.xlsx", "wb") as fh:
            #     fh.write(iq_09.decode('base64'))
            # with file("iq09.xlsx") as f:
            #     text = f.read()
            # # data_array = text.split('\n')
            # wb = open_workbook("iq09.xlsx") 
            # iq09 = wb.sheet_by_index(0) 
              
            # iq09.cell_value(0, 0) 
            # print 'Jumlah'+ str(iq09.nrows)
            # n = 0
            # for g in range(iq09.nrows):
                # n += 1
                # # data = data_array[g].split('\t')
                # print iq09.cell_value(n, 1)
                # serial = str(iq09.cell_value(n, 5))
                # qmap = str(iq09.cell_value(n, 2))

                # if(serial.find('E+') != -1):
                    # serial = float(serial)
                    # serial = int(serial)

                # CEK ADA GK PRODUCT TSB
                # product_by_qmap = self.env['product.product'].search([('qmap','=',qmap)])

                # if(product_by_qmap):
                    # product_id = product_by_qmap.id
                # else:
                    # product_id = self.env['product.product'].create({
                    #         'qmap':str(iq09.cell_value(n, 2)),
                    #         'name':str(iq09.cell_value(n, 3)),
                    #         'short_name':str(iq09.cell_value(n, 3)),
                    #         'default_code':str(iq09.cell_value(n, 4)),
                    #         'purchase_ok':True,
                    #         'categ_id':1,
                    #         'type':'product',
                    #         'tracking':'none',
                    #         'invoice_policy':'order',
                    #         'purchase_method':'receive',
                    #     }).id
                    # self.env.cr.commit()

                # serial_by_sn = self.env['stock.production.lot'].search(['&',('product_id.id','=',product_id),('name','=',serial)])
                # if(serial_by_sn):
                    # DO NOTHING
                    # print 'NOT SAVED'
                # else:
                	# self.env['stock.production.lot'].create({
                 #            'product_id':product_id,
                 #            'name':serial,
                 #            'status':str(iq09.cell_value(n, 9)),
                 #        })
                	# self.env.cr.commit()
        if(mb_52):
            
            try:

                #################
                #OPEN WORKBOOK ##
                #################
                wb = open_workbook(file_contents = base64.decodestring(mb_52))
                sheet = wb.sheets()[0]

                ######################################
                ## CREATE RAW DATA FROM SPREADSHEET ##
                ######################################
                raw_data = []
                for row_no in range(sheet.nrows):
                    zero_col = 0
                    if row_no < 0:
                        fields = map(lambda row:row.value.encode('utf-8'), sheet.row(row_no))
                    else:
                        for col in sheet.row(row_no):
                            if not col.value:
                                zero_col = zero_col + 1
                        if zero_col < sheet.ncols:
                            raw_data.append(map(lambda row:isinstance(row.value, str) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
                    
                ## GET HEADER SPREADSHEET
                header = map(lambda x:x.lower(), raw_data[0])
                
                ## DATA PROCESS
                if 'material' in header:
                    index_qmap   = header.index('material')
                    index_stock  = [idx for idx, s in enumerate(header) if 'stock' in s]

                    for i in xrange(1,len(raw_data)):
                        
                        ## Search data product
                        product_by_qmap     = self.env['product.product'].search([('qmap','=',raw_data[i][index_qmap])])
                        
                        for prod in product_by_qmap:
                            if prod.id != False:
                                product_qty = self.env['stock.change.product.qty'].create({
                                        'product_id': product_by_qmap.id,
                                        'new_quantity': raw_data[i][index_stock[0]],
                                    })
                                product_qty.change_product_qty()
                                mb_status = True
                            else:
                                product_qty = self.env['stock.change.product.qty'].write({
                                        'product_id': product_by_qmap.id,
                                        'new_quantity': raw_data[i][index_stock[0]],
                                    })
                                product_qty.change_product_qty()
                                mb_status = True
                    

            except Exception as e:
                raise ValidationError('An error occurred, %s' %(e))


            # print 'MB52'
            # with open("mb52.xlsx", "wb") as fh:
            #     fh.write(mb_52.decode('base64'))
            # with file("mb52.xlsx") as f:
            #     text = f.read()
            # data_array = text.split('\n')

            # wb = open_workbook("mb52.xlsx") 
            # mb52 = wb.sheet_by_index(0) 
              
            # mb52.cell_value(0, 0) 
            # print 'Jumlah'+ str(mb52.nrows)
            # n = 0
            # for g in range(mb52.nrows):
                # n += 1
                # if mb52.cell_value(n, 0) != '':
                    # print mb52.cell_value(n, 1)
                    # name_bin = mb52.cell_value(n, 3)
                    # qmap = mb52.cell_value(n, 4)
                    # # data = data_array[g].split('\t')                
                    # # print 'Ha' + str(data[3]) + 'Ha'
                    # # bin_loc = str(data[3])
                    # bin_by_code = self.env['ams.bin'].search([('name','=',str(name_bin))])
                    # if(bin_by_code):
                        # bin_id = bin_by_code.id
                    # else:
                        # bin_id = self.env['ams.bin'].create({
                        #         'code':(str(name_bin)),
                        #         'name':(str(name_bin)),
                        #     }).id
                    # product_by_qmap = self.env['product.product'].search([('qmap','=',str(qmap))])
                    # print 'Qmap' + str(str(qmap))
                    # if(product_by_qmap):
                        # print 'Product ada'
                        # product_id = product_by_qmap.id
                        # amount = str(mb52.cell_value(n, 6)).replace(',','')
                        # scrap = str(mb52.cell_value(n, 7)).replace(',','')
                        # otw = str(mb52.cell_value(n, 9)).replace(',','')

                        # stock_by_ref = self.env['ams.stock'].search([('product_id','=',product_id),('bin_id','=',bin_id)])
                        # if(stock_by_ref):
                            # stock_by_ref.write({
                            #     'stock_on_hand' : amount,
                            #     'stock_scrap' : scrap,
                            #     })
                        # else:
                            # self.env['ams.stock'].create({
                            #         'product_id' : product_id,
                            #         'bin_id' : bin_id,
                            #         'stock_on_hand' : amount,
                            #         'stock_scrap' : scrap,
                            #     })
                        # self.env.cr.commit()

        # change status
        if ih_status and iq_status and mb_status:
            r_data.status = True

    @api.model
    def create(self, vals):
        create = super(ams_inventory_import, self).create(vals)
        self.env['ir.cron'].create({
                'name': 'Cron Check',
                'user_id': self._uid,
                'model': 'ams_inventory.import',
                'function': 'process_data_master_part',
                'args': repr([create.id])
               })
        return create