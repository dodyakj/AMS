# -*- coding: utf-8 -*-
from odoo import http

# class AmsReport(http.Controller):
#     @http.route('/ams_report/ams_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ams_report/ams_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ams_report.listing', {
#             'root': '/ams_report/ams_report',
#             'objects': http.request.env['ams_report.ams_report'].search([]),
#         })

#     @http.route('/ams_report/ams_report/objects/<model("ams_report.ams_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ams_report.object', {
#             'object': obj
#         })