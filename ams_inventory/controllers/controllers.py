# -*- coding: utf-8 -*-
from odoo import http

# class AmsInventory(http.Controller):
#     @http.route('/ams_inventory/ams_inventory/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ams_inventory/ams_inventory/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ams_inventory.listing', {
#             'root': '/ams_inventory/ams_inventory',
#             'objects': http.request.env['ams_inventory.ams_inventory'].search([]),
#         })

#     @http.route('/ams_inventory/ams_inventory/objects/<model("ams_inventory.ams_inventory"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ams_inventory.object', {
#             'object': obj
#         })