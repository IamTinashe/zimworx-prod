# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class ShuttleManagement(http.Controller):
    @http.route('/my_shuttle', type='http', auth='public', website=True)
    def my_shuttle(self, **kwargs):
        return request.render('shuttle_management.my_shuttle_template')

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
