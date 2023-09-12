# -*- coding: utf-8 -*-
from odoo import http

# class PaiisCorrective(http.Controller):
#     @http.route('/paiis_corrective/paiis_corrective/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/paiis_corrective/paiis_corrective/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('paiis_corrective.listing', {
#             'root': '/paiis_corrective/paiis_corrective',
#             'objects': http.request.env['paiis_corrective.paiis_corrective'].search([]),
#         })

#     @http.route('/paiis_corrective/paiis_corrective/objects/<model("paiis_corrective.paiis_corrective"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('paiis_corrective.object', {
#             'object': obj
#         })