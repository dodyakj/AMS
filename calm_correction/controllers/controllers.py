# -*- coding: utf-8 -*-
from odoo import http

# class CalmCorrection(http.Controller):
#     @http.route('/calm_correction/calm_correction/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/calm_correction/calm_correction/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('calm_correction.listing', {
#             'root': '/calm_correction/calm_correction',
#             'objects': http.request.env['calm_correction.calm_correction'].search([]),
#         })

#     @http.route('/calm_correction/calm_correction/objects/<model("calm_correction.calm_correction"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('calm_correction.object', {
#             'object': obj
#         })