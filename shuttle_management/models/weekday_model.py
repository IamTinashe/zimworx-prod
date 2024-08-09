from odoo import fields, models, api

class WeekdayModel(models.Model):
    """THIS MODEL IS FOR HAVING univaer W"""
    _name = 'weekday.model'
    _description = 'Week Day'

    name = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday')
    ], string='Day', required=True, unique=True)

    color = fields.Integer(string='Color Index')
