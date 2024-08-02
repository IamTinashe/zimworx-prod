# -*- coding: utf-8 -*-
# from odoo import http


# class ShuttleManagement(http.Controller):
#     @http.route('/shuttle_management/shuttle_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/shuttle_management/shuttle_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('shuttle_management.listing', {
#             'root': '/shuttle_management/shuttle_management',
#             'objects': http.request.env['shuttle_management.shuttle_management'].search([]),
#         })

#     @http.route('/shuttle_management/shuttle_management/objects/<model("shuttle_management.shuttle_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('shuttle_management.object', {
#             'object': obj
#         })
