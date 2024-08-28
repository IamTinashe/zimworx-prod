from odoo import fields, models, api


class EmployeeSchedules(models.Model):
    _name = 'employee_schedules.model'
    _description = 'Employee Schedule'

    weekday_id = fields.Many2many('weekday.model', string='Day', required=True)
    departure_time = fields.Float(string='Departure Time 24hr', required=True)
    employee_id = fields.Many2one('hr.employee', string='Shuttle', required=True)
    shuttle_id = fields.Many2one('shuttles.model', string='Shuttle', readonly=True)
    shuttle_schedule = fields.Many2one('shuttle_schedule.model', string='Shuttle Schedule', readonly=True)

