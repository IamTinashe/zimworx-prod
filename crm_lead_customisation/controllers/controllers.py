# -*- coding: utf-8 -*-
# from odoo import http


# class CrmLeadCustomisation(http.Controller):
#     @http.route('/crm_lead_customisation/crm_lead_customisation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crm_lead_customisation/crm_lead_customisation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('crm_lead_customisation.listing', {
#             'root': '/crm_lead_customisation/crm_lead_customisation',
#             'objects': http.request.env['crm_lead_customisation.crm_lead_customisation'].search([]),
#         })

#     @http.route('/crm_lead_customisation/crm_lead_customisation/objects/<model("crm_lead_customisation.crm_lead_customisation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crm_lead_customisation.object', {
#             'object': obj
#         })
