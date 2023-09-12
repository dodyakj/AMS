# -*- coding: utf-8 -*-
from odoo import http

# class EmsBulletin(http.Controller):
#     @http.route('/ams_bulletin/ams_bulletin/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ams_bulletin/ams_bulletin/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ams_bulletin.listing', {
#             'root': '/ams_bulletin/ams_bulletin',
#             'objects': http.request.env['ams_bulletin.ams_bulletin'].search([]),
#         })

#     @http.route('/ams_bulletin/ams_bulletin/objects/<model("ams_bulletin.ams_bulletin"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ams_bulletin.object', {
#             'object': obj
#         })