from odoo import fields, models, api


class ShuttlesModel(models.Model):
    """THIS MODEL IS FOR ENTERING ALL SHUTTLE AND MANAGING THEIR DRIVERS, SHUTTLES ETC"""
    _name = 'shuttles.model'
    _description = 'Shuttle Record'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string='Shuttle Name', required=True)
    vehicle_registration = fields.Char(string='Vehicle Registration', required=True)
    driver_id = fields.Many2one('hr.employee',string='Driver', required=True)
    capacity = fields.Integer(string='Seating Capacity', required=True)
    service_status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance')
    ], string='Service Status', default='active')
    location = fields.Char(string='Current Location')
    last_maintenance_date = fields.Date(string='Last Maintenance Date')
    next_maintenance_date = fields.Date(string='Next Maintenance Date')
    notes = fields.Text(string='Additional Notes')
