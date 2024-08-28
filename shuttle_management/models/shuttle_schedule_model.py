from odoo import fields, models, api


class ShuttleSchedules(models.Model):
    """THIS MANAGES SCHEDULES OF SHUTTLES AND THEIR AVAILABLIY IN POSSIBLE SCHEDULES"""
    _name = 'shuttle_schedule.model'
    _description = 'Description'

    shuttle_id = fields.Many2one('shuttles.model', string='Shuttle', required=True)
    # route_name = fields.Char(string='Route Name', required=True)
    departure_time = fields.Float(string='Departure Time 24hr', required=True)
    booked_seating_capacity = fields.Integer(string='Booked Seating Capacity')
    max_seating_capacity = fields.Integer(string='Max Seating Capacity')
    is_fully_booked = fields.Selection([
        ('fully_booked', 'Full Booked'),
        ('not_fully_booked', 'Not Fully Booked'),
    ],default='not_fully_booked', string='Booking Status')
    weekday_id = fields.Many2many('weekday.model', string='Day', required=True)
    shuttle_route=fields.Many2many('shuttle_routes.model', string='Shuttle Route')
    hr_employee=fields.Many2many('hr.employee', string='Employees')

    def name_get(self):
        result = []
        for record in self:
            # Get the names of the weekdays
            weekdays = ', '.join(record.weekday_id.mapped('name'))
            name = f"{weekdays} - {record.departure_time}"
            result.append((record.id, name))
        return result