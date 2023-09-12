# -*- coding: utf-8 -*-
from odoo import http

# class AmsFmlFuelOil(http.Controller):
#     @http.route('/ams_fml_fuel_oil/ams_fml_fuel_oil/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ams_fml_fuel_oil/ams_fml_fuel_oil/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ams_fml_fuel_oil.listing', {
#             'root': '/ams_fml_fuel_oil/ams_fml_fuel_oil',
#             'objects': http.request.env['ams_fml_fuel_oil.ams_fml_fuel_oil'].search([]),
#         })

#     @http.route('/ams_fml_fuel_oil/ams_fml_fuel_oil/objects/<model("ams_fml_fuel_oil.ams_fml_fuel_oil"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ams_fml_fuel_oil.object', {
#             'object': obj
#         })