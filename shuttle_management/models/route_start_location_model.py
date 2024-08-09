from odoo import fields, models, api

class RouteStartModel(models.Model):
    """THIS MODEL IS FOR HAVING LOCATIONS OF ROUTE START MODEL"""
    _name = 'route_start_location.model'
    _description = 'Route Start Location'
    _rec_name = 'route_start'


    route_start = fields.Char(string='Route Start Location')
