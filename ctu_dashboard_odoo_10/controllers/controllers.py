# -*- coding: utf-8 -*-
from odoo import http

# class CtuDashboardOdoo10(http.Controller):
#     @http.route('/ctu_dashboard_odoo_10/ctu_dashboard_odoo_10/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ctu_dashboard_odoo_10/ctu_dashboard_odoo_10/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ctu_dashboard_odoo_10.listing', {
#             'root': '/ctu_dashboard_odoo_10/ctu_dashboard_odoo_10',
#             'objects': http.request.env['ctu_dashboard_odoo_10.ctu_dashboard_odoo_10'].search([]),
#         })

#     @http.route('/ctu_dashboard_odoo_10/ctu_dashboard_odoo_10/objects/<model("ctu_dashboard_odoo_10.ctu_dashboard_odoo_10"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ctu_dashboard_odoo_10.object', {
#             'object': obj
#         })