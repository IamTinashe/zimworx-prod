# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CrmLeadInheritance(models.Model):
    _inherit = 'crm.lead'


    @api.onchange('x_studio_seat_type')
    def onchange_x_studio_seat_type(self):
        """WHEN SEAT TYPE CHANGE TO REPLACEMENT UPDATE x_studio_sales_person WITH user_id"""
        for record in self:
            if record.x_studio_seat_type=='Replacement Seats' and not record.x_studio_salesperson:
                record.x_studio_salesperson= record.user_id.id

