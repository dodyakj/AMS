# -*- coding: utf-8 -*-
from odoo import http

# class EmsBase(http.Controller):
#     @http.route('/ams_base/ams_base/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ams_base/ams_base/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ams_base.listing', {
#             'root': '/ams_base/ams_base',
#             'objects': http.request.env['ams_base.ams_base'].search([]),
#         })

#     @http.route('/ams_base/ams_base/objects/<model("ams_base.ams_base"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ams_base.object', {
#             'object': obj
#         })