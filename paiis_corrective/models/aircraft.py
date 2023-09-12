# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)


class paiis_corrective_aircraft(models.Model):
    _inherit = 'aircraft.acquisition'

    esn3 = fields.Char(string='ESN#3')
    esn4 = fields.Char(string='ESN#4')

    engine_type_id  = fields.Many2one('engine.type', string='Engine')
    engine2_type_id = fields.Many2one('engine.type', string='Engine')
    engine3_type_id = fields.Many2one('engine.type', string='Engine')
    engine4_type_id = fields.Many2one('engine.type', string='Engine')

    engine_type_id_before  = fields.Many2one('engine.type', string='Engine Before')
    engine2_type_id_before = fields.Many2one('engine.type', string='Engine Before')
    engine3_type_id_before = fields.Many2one('engine.type', string='Engine Before')
    engine4_type_id_before = fields.Many2one('engine.type', string='Engine Before')

    engine3_tsn = fields.Float(string='Engine#3 TSN', related='engine3_type_id.engine_tsn')
    engine3_csn = fields.Float(string='Engine#3 CSN', related='engine3_type_id.engine_csn')
    engine3_tslsv = fields.Float(string='Engine#3 TSLSV OH', related='engine3_type_id.engine_tslsv')
    engine3_tslsv_hsi = fields.Float(string='Engine#3 TSLSV HSI', related='engine3_type_id.engine_tslsv_hsi')
    engine3_cslsv = fields.Float(string='Engine#3 CSLSV OH', related='engine3_type_id.engine_cslsv')
    engine3_cslsv_hsi = fields.Float(string='Engine#3 CSLSV HSI', related='engine3_type_id.engine_cslsv_hsi')
    
    engine3_lastoh = fields.Date(string='Engine#3 Last OH', related='engine3_type_id.engine_lastoh')
    engine3_hsi = fields.Date(string='Engine#3 HSI', related='engine3_type_id.engine_hsi')

    engine4_tsn = fields.Float(string='Engine#4 TSN', related='engine4_type_id.engine_tsn')
    engine4_csn = fields.Float(string='Engine#4 CSN', related='engine4_type_id.engine_csn')
    engine4_tslsv = fields.Float(string='Engine#4 TSLSV OH', related='engine4_type_id.engine_tslsv')
    engine4_tslsv_hsi = fields.Float(string='Engine#4 TSLSV HSI', related='engine4_type_id.engine_tslsv_hsi')
    engine4_cslsv = fields.Float(string='Engine#4 CSLSV OH', related='engine4_type_id.engine_cslsv')
    engine4_cslsv_hsi = fields.Float(string='Engine#4 CSLSV HSI', related='engine4_type_id.engine_cslsv_hsi')
    
    engine4_lastoh = fields.Date(string='Engine#4 Last OH', related='engine4_type_id.engine_lastoh')
    engine4_hsi = fields.Date(string='Engine#4 HSI', related='engine4_type_id.engine_hsi')

    engine1_tsn = fields.Float(string='Engine#3 TSN', related='engine_type_id.engine_tsn')
    engine1_csn = fields.Float(string='Engine#3 CSN', related='engine_type_id.engine_csn')
    engine1_tslsv = fields.Float(string='Engine#3 TSLSV OH', related='engine_type_id.engine_tslsv')
    engine1_tslsv_hsi = fields.Float(string='Engine#3 TSLSV HSI', related='engine_type_id.engine_tslsv_hsi')
    engine1_cslsv = fields.Float(string='Engine#3 CSLSV OH', related='engine_type_id.engine_cslsv')
    engine1_cslsv_hsi = fields.Float(string='Engine#3 CSLSV HSI', related='engine_type_id.engine_cslsv_hsi')
    
    engine1_lastoh = fields.Date(string='Engine#3 Last OH', related='engine_type_id.engine_lastoh')
    engine1_hsi = fields.Date(string='Engine#3 HSI', related='engine_type_id.engine_hsi')

    engine2_tsn = fields.Float(string='Engine#4 TSN', related='engine2_type_id.engine_tsn')
    engine2_csn = fields.Float(string='Engine#4 CSN', related='engine2_type_id.engine_csn')
    engine2_tslsv = fields.Float(string='Engine#4 TSLSV OH', related='engine2_type_id.engine_tslsv')
    engine2_tslsv_hsi = fields.Float(string='Engine#4 TSLSV HSI', related='engine2_type_id.engine_tslsv_hsi')
    engine2_cslsv = fields.Float(string='Engine#4 CSLSV OH', related='engine2_type_id.engine_cslsv')
    engine2_cslsv_hsi = fields.Float(string='Engine#4 CSLSV HSI', related='engine2_type_id.engine_cslsv_hsi')
    
    engine2_lastoh = fields.Date(string='Engine#4 Last OH', related='engine2_type_id.engine_lastoh')
    engine2_hsi = fields.Date(string='Engine#4 HSI', related='engine2_type_id.engine_hsi')
    document_ids = fields.One2many('document.certificate','acquisition_id', string='Document Certificates', copy=True)
    name = fields.Char(string='Registration No', required=True, index=False)
    company_id = fields.Many2one('res.company', 'Company',
                    default=lambda self: False)

    _sql_constraints = [
        ('reg_number_company_uniq', 'unique (name,company_id)', 'Aircraft registration number must be unique per company!')
    ]

    @api.multi
    def copy(self, default):
        _logger.info("DEBBUG:" + " default " +  str(default))
        _logger.info("DEBBUG:" + " self.component_ids " +  str(self.component_ids.name_get()))
        for line in self.component_ids:
            _logger.info("DEBBUG:" + " self.component_ids " +  str(line.name_get()))
        default = dict(default or {})
        default.update({
            'name': 'PK-Copy',
            'company_id': False,
        })
        # _logger.info("DEBBUG:" + str(vals))
        return super(paiis_corrective_aircraft, self).copy(default)



    # @api.multi
    # def dub_air(self, default=None):
    #     cr = self._cr
    #     uid = self._uid
    #     default = dict(default or {})
    #     search_ids = self.env['aircraft.acquisition'].search([], order="create_date desc", limit=1)
    #     component = []
    #     utils = []
    #     for d in self.component_ids:
    #         component.append({
    #             'fleet_id' : int(d.fleet_id.id),
    #             'product_id' : int(d.product_id.id),
    #             'serial_number' : int(d.serial_number.id),
    #             'ata_code' : int(d.ata_code.id),
    #             'is_bel' : d.is_bel,
    #             })
    #     default.update({
    #      'id' : search_ids.id+1,
    #      'name' : self.name+(' Copy'),
    #      'company_id' : False,
    #      'engine_type_id': self.engine_type_id.id,
    #      'engine2_type_id': self.engine2_type_id.id,
    #      'engine3_type_id': self.engine3_type_id.id,
    #      'engine4_type_id': self.engine4_type_id.id,
    #     })
    #     return super(paiis_corrective_aircraft, self).copy(default) 

    @api.onchange('engine_type_id')
    def _onchange_engine_type_id(self):
        if self.engine_type_id:
            self.engine1_tsn = self.engine_type_id.engine_tsn
            self.engine1_csn = self.engine_type_id.engine_csn
            self.engine1_tslsv = self.engine_type_id.engine_tslsv
            self.engine1_tslsv_hsi = self.engine_type_id.engine_tslsv_hsi
            self.engine1_cslsv = self.engine_type_id.engine_tslsv_hsi
            self.engine1_cslsv_hsi = self.engine_type_id.engine_tslsv_hsi
            self.engine1_lastoh = self.engine_type_id.engine_tslsv_hsi
            

    @api.onchange('engine2_type_id')
    def _onchange_engine2_type_id(self):
        if self.engine2_type_id:
            self.engine1_tsn = self.engine2_type_id.engine_tsn
            self.engine1_csn = self.engine2_type_id.engine_csn
            self.engine1_tslsv = self.engine2_type_id.engine_tslsv
            self.engine1_tslsv_hsi = self.engine2_type_id.engine_tslsv_hsi
            self.engine1_cslsv = self.engine2_type_id.engine_tslsv_hsi
            self.engine1_cslsv_hsi = self.engine2_type_id.engine_tslsv_hsi
            self.engine1_lastoh = self.engine2_type_id.engine_tslsv_hsi
            
    @api.onchange('engine3_type_id')
    def _onchange_engine3_type_id(self):
        if self.engine_type_id:
            self.engine3_tsn = self.engine3_type_id.engine_tsn
            self.engine3_csn = self.engine3_type_id.engine_csn
            self.engine3_tslsv = self.engine3_type_id.engine_tslsv
            self.engine3_tslsv_hsi = self.engine3_type_id.engine_tslsv_hsi
            self.engine3_cslsv = self.engine3_type_id.engine_tslsv_hsi
            self.engine3_cslsv_hsi = self.engine3_type_id.engine_tslsv_hsi
            self.engine3_lastoh = self.engine3_type_id.engine_tslsv_hsi
            

    @api.onchange('engine4_type_id')
    def _onchange_engine4_type_id(self):
        if self.engine4_type_id:
            self.engine4_tsn = self.engine4_type_id.engine_tsn
            self.engine4_csn = self.engine4_type_id.engine_csn
            self.engine4_tslsv = self.engine4_type_id.engine_tslsv
            self.engine4_tslsv_hsi = self.engine4_type_id.engine_tslsv_hsi
            self.engine4_cslsv = self.engine4_type_id.engine_tslsv_hsi
            self.engine4_cslsv_hsi = self.engine4_type_id.engine_tslsv_hsi
            self.engine4_lastoh = self.engine4_type_id.engine_tslsv_hsi
                


class paiis_corrective_aircraft_type(models.Model):
    _inherit = 'aircraft.type'

    manufacture = fields.Char()


