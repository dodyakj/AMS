from odoo import models, fields, api

class Stquant(models.Model):
    _inherit = 'stock.quant'

    @api.multi
    def action_view_menu(self):
        action = self.env.ref('pelita_part.kirim_tagihan_wizard_action')
        result = action.read()[0]
        return result

class FleetEngineModel(models.Model):
    _name = 'part.model'
    _description = 'Model of a part'
    _order = 'name asc'

    name = fields.Char('Model name', required=True)
    # brand_id = fields.Many2one('part.model', 'Model', required=True, help='Model')
    # vendors = fields.Many2many('res.partner', 'fleet_vehicle_model_vendors', 'model_id', 'partner_id', string='Vendors')
    # image = fields.Binary(related='brand_id.image', string="Logo")
    # image_medium = fields.Binary(related='brand_id.image_medium', string="Logo (medium)")
    # image_small = fields.Binary(related='brand_id.image_small', string="Logo (small)")

    # @api.multi
    # @api.depends('name', 'brand_id')
    # def name_get(self):
    #     res = []
    #     for record in self:
    #         name = record.name
    #         if record.brand_id.name:
    #             name = record.brand_id.name + '/' + name
    #         res.append((record.id, name))
    #     return res

    # @api.onchange('brand_id')
    # def _onchange_brand(self):
    #     if self.brand_id:
    #         self.image_medium = self.brand_id.image
    #     else:
    #         self.image_medium = False

class Alternate(models.Model):
    _name = 'part.alternate'
    _description = 'Alternate Part'

    
    part_id = fields.Many2one('product.product',string='Part Id')
    name = fields.Many2one('product.product',string='Part')

class Pelitapart(models.Model):
    # _name = 'part.part'
    _inherit = 'product.product'
    _description = 'Part'

    short_name = fields.Char(string='Short Name')
    # name = fields.Char('Long Name', index=True, required=True, translate=True)
    ata_code = fields.Many2one('ams.ata', string="ATA Code")
    no_reorder = fields.Boolean(string='Do Not Reorder')
    serviceable = fields.Boolean(string='Serviceable')
    out_for_repair = fields.Boolean(string='Out For Repair')
    non_serviceable = fields.Boolean(string='Non Serviceable')
    open_po = fields.Boolean(string='Open P/O')
    open_wo = fields.Boolean(string='Open W/O')

    count = fields.Integer(string='Count',default=19)
    part_model_ids = fields.Many2many('part.model', string='Model')

    alternate_ids = fields.One2many('part.alternate','part_id',string='Alternate Part')