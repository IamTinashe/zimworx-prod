# -*- coding: utf-8 -*-
# from odoo import http


# class GrindManagement(http.Controller):
#     @http.route('/grind_management/grind_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/grind_management/grind_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('grind_management.listing', {
#             'root': '/grind_management/grind_management',
#             'objects': http.request.env['grind_management.grind_management'].search([]),
#         })

#     @http.route('/grind_management/grind_management/objects/<model("grind_management.grind_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('grind_management.object', {
#             'object': obj
#         })
