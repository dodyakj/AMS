# -*- coding: utf-8 -*-
from odoo import http

# class LeftigiWizard(http.Controller):
#     @http.route('/leftigi_wizard/leftigi_wizard/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/leftigi_wizard/leftigi_wizard/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('leftigi_wizard.listing', {
#             'root': '/leftigi_wizard/leftigi_wizard',
#             'objects': http.request.env['leftigi_wizard.leftigi_wizard'].search([]),
#         })

#     @http.route('/leftigi_wizard/leftigi_wizard/objects/<model("leftigi_wizard.leftigi_wizard"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('leftigi_wizard.object', {
#             'object': obj
#         })