from odoo import fields, models, api


class ShuttleSubRoute(models.Model):
    """THIS IS A MODEL JOINED TO SHUTTLE ROUTES WHICH DEFINE SUB ROUTES WITHIN MAIN ROUTES"""
    _name = 'shuttle.sub.route'
    _description = 'Shuttle Sub-Route'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string='Sub-Route Name', required=True)
    route_id = fields.Many2one('shuttle_routes.model', string='Main Route', required=True, ondelete='cascade')
    start_location = fields.Char(string='Start Location', required=True)
    end_location = fields.Char(string='End Location', required=True)
    sub_route_distance_km = fields.Float(string='Sub-Route Distance (KM)')
    estimated_sub_route_duration = fields.Float(string='Estimated Duration (Hours)')
    sequence = fields.Integer(string='Sequence', default=10)
    active = fields.Boolean(string='Active', default=True)
    total_employees_available = fields.Float(string='Total Employees available')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.ref('base.USD'))
    cost = fields.Monetary(string='Cost')

