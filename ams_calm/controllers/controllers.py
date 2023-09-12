# -*- coding: utf-8 -*-
from odoo import http

# class AmsCalm(http.Controller):
#     @http.route('/ams_calm/ams_calm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ams_calm/ams_calm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ams_calm.listing', {
#             'root': '/ams_calm/ams_calm',
#             'objects': http.request.env['ams_calm.ams_calm'].search([]),
#         })

#     @http.route('/ams_calm/ams_calm/objects/<model("ams_calm.ams_calm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ams_calm.object', {
#             'object': obj
#         })