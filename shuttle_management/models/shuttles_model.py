from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ShuttlesModel(models.Model):
    """THIS MODEL IS FOR ENTERING ALL SHUTTLE AND MANAGING THEIR DRIVERS, SHUTTLES ETC"""
    _name = 'shuttles.model'
    _description = 'Shuttle Record'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string='Shuttle Name', required=True)
    vehicle_registration = fields.Char(string='Vehicle Registration', required=True)
    driver_id = fields.Many2one('hr.employee',domain=[('department_id','=',18)], string='Driver', required=True)
    driver_login_id = fields.Char(related='driver_id.driver_login_id', readonly=False, store=True)
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
    shuttle_route=fields.Many2many('shuttle_routes.model', string='Shuttle Route')
    shuttle_schedule_ids=fields.One2many('shuttle_schedule.model', 'shuttle_id', string='Shuttle Schedules')



    def name_get(self):
        result = []
        for shuttle in self:
            name = f"{shuttle.name} - {shuttle.vehicle_registration}"
            result.append((shuttle.id, name))
        return result

    @api.constrains('driver_id')
    def _check_driver_id(self):
        """CHECK IF DRIVER ID IS UNIQUE"""
        for record in self:
            if record.driver_id:
                # Search for other records with the same driver_login_id
                existing_driver = self.search([
                    ('driver_id', '=', record.driver_id),
                    ('id', '!=', record.id)  # Ensure it's not the same record
                ], limit=1)
                if existing_driver:
                    raise ValidationError('The driver must be unique. This one already have a shuttle!')
