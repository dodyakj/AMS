# -*- coding: utf-8 -*-
from odoo import http

# class AmsDaily(http.Controller):
#     @http.route('/ams_daily/ams_daily/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ams_daily/ams_daily/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ams_daily.listing', {
#             'root': '/ams_daily/ams_daily',
#             'objects': http.request.env['ams_daily.ams_daily'].search([]),
#         })

#     @http.route('/ams_daily/ams_daily/objects/<model("ams_daily.ams_daily"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ams_daily.object', {
#             'object': obj
#         })