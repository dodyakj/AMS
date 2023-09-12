# -*- coding: utf-8 -*-
from odoo import http

# class AmsAirworthy(http.Controller):
#     @http.route('/ams_airworthy/ams_airworthy/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ams_airworthy/ams_airworthy/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ams_airworthy.listing', {
#             'root': '/ams_airworthy/ams_airworthy',
#             'objects': http.request.env['ams_airworthy.ams_airworthy'].search([]),
#         })

#     @http.route('/ams_airworthy/ams_airworthy/objects/<model("ams_airworthy.ams_airworthy"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ams_airworthy.object', {
#             'object': obj
#         })