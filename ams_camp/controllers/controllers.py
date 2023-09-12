# -*- coding: utf-8 -*-
from odoo import http

# class AmsCamp(http.Controller):
#     @http.route('/ams_camp/ams_camp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ams_camp/ams_camp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ams_camp.listing', {
#             'root': '/ams_camp/ams_camp',
#             'objects': http.request.env['ams_camp.ams_camp'].search([]),
#         })

#     @http.route('/ams_camp/ams_camp/objects/<model("ams_camp.ams_camp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ams_camp.object', {
#             'object': obj
#         })