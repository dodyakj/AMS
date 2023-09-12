# -*- coding: utf-8 -*-
from odoo import http

# class AmsDummy(http.Controller):
#     @http.route('/ams_security/ams_security/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ams_security/ams_security/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ams_security.listing', {
#             'root': '/ams_security/ams_security',
#             'objects': http.request.env['ams_security.ams_security'].search([]),
#         })

#     @http.route('/ams_security/ams_security/objects/<model("ams_security.ams_security"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ams_security.object', {
#             'object': obj
#         })