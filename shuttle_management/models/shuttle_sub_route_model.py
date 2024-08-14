from odoo import fields, models, api


class ShuttleSubRoute(models.Model):
    """THIS IS A MODEL JOINED TO SHUTTLE ROUTES WHICH DEFINE SUB ROUTES WITHIN MAIN ROUTES"""
    _name = 'shuttle.sub.route'
    _description = 'Shuttle Sub-Route'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string='Sub-Route Name',)
    route_id = fields.Many2one('shuttle_routes.model', string='Main Route', required=True, ondelete='cascade')
    total_employees_available = fields.Integer(string='Total Employees available')
    # start_location = fields.Many2one('route_start_location.model', string='Start Location', required=True)
    end_location = fields.Many2one('route_end_location.model', string='End Location', required=True)

