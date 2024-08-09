from odoo import fields, models, api


class ShuttleRouteModel(models.Model):
    """THIS IS FOR MANAGEMENT OF ALL DIFFERENTS ROUTES WHICH THE SHUTTLES WILL BE MOVING AROUND AND ALLOCATED"""
    _name = 'shuttle_routes.model'
    _description = 'Shuttle Route'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string='Route Name', required=True)
    main_route_start = fields.Many2one('route_start_location.model', string='Main Route Start', required=True)
    main_route_end = fields.Many2one('route_end_location.model', string='Main Route End', required=True)
    distance_km = fields.Float(string='Total Distance (KM)')
    total_employees_available = fields.Integer(string='Total Employees available')
    estimated_duration = fields.Float(string='Estimated Duration (Hours)')
    sub_route_ids = fields.One2many('shuttle.sub.route', 'route_id', string='Sub Routes')
    active = fields.Boolean(string='Active', default=True)
    notes = fields.Text(string='Additional Notes')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.ref('base.USD'))
    cost = fields.Monetary(string='Cost')

    def name_get(self):
        result = []
        for route in self:
            name = f"{route.main_route_start.route_start} to {route.main_route_end.route_end}"
            result.append((route.id, name))
        return result

