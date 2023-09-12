# -*- coding: utf-8 -*-
from odoo import http

# class AmsFml(http.Controller):
#     @http.route('/ams_fml/ams_fml/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ams_fml/ams_fml/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ams_fml.listing', {
#             'root': '/ams_fml/ams_fml',
#             'objects': http.request.env['ams_fml.ams_fml'].search([]),
#         })

#     @http.route('/ams_fml/ams_fml/objects/<model("ams_fml.ams_fml"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ams_fml.object', {
#             'object': obj
#         })