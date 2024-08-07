# -*- coding: utf-8 -*-
from odoo import models, fields, api


class EmployeeInheritance(models.Model):
    """THIS INHERITS EMPLOYEE TO ADD SHUTTLE MANAGEMENT FUNCTIONS"""
    _inherit = 'hr.employee'

    shuttles_model=fields.Many2one('shuttles.model', string='Shuttle')
    max_seating_capacity=fields.Integer(related='shuttles_model.capacity', store=True, string='Shuttle Max Seating Capacity')
    service_status=fields.Selection(related='shuttles_model.service_status', store=True, string='Shuttle Service Status')
    driver_route=fields.Many2one('shuttle_routes.model', string='Driver Route')
    drivers_schedule_ids=fields.One2many('drivers_schedule.model', 'driver_id', string='Driver Schedules')

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
