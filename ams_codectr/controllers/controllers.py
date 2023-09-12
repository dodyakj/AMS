# -*- coding: utf-8 -*-
from odoo import http

# class EmsCodectr(http.Controller):
#     @http.route('/ams_codectr/ams_codectr/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ams_codectr/ams_codectr/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ams_codectr.listing', {
#             'root': '/ams_codectr/ams_codectr',
#             'objects': http.request.env['ams_codectr.ams_codectr'].search([]),
#         })

#     @http.route('/ams_codectr/ams_codectr/objects/<model("ams_codectr.ams_codectr"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ams_codectr.object', {
#             'object': obj
#         })