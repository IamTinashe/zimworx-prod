from odoo import fields, models, api

class RouteEndModel(models.Model):
    """THIS MODEL IS FOR HAVING LOCATIONS OF ROUTE ENDS"""
    _name = 'route_end_location.model'
    _description = 'Route End Location'
    _rec_name='route_end'


    route_end = fields.Char(string='Route End Location')