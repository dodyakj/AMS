# -*- coding: utf-8 -*-
from odoo import http

# class SimpleMenu(http.Controller):
#     @http.route('/simple_menu/simple_menu/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/simple_menu/simple_menu/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('simple_menu.listing', {
#             'root': '/simple_menu/simple_menu',
#             'objects': http.request.env['simple_menu.simple_menu'].search([]),
#         })

#     @http.route('/simple_menu/simple_menu/objects/<model("simple_menu.simple_menu"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('simple_menu.object', {
#             'object': obj
#         })