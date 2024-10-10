from odoo import fields, models, api
from datetime import datetime
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError



class EmployeeSchedules(models.Model):
    _name = 'employee_schedules.model'
    _description = 'Employee Schedule'

    weekday_id = fields.Many2many('weekday.model', string='Day', required=True)
    departure_time = fields.Float(string='Departure Time 24hr', required=True)
    employee_id = fields.Many2one('hr.employee', string='Shuttle', required=True)
    shuttle_id = fields.Many2one('shuttles.model', string='Shuttle', readonly=True)
    shuttle_schedule = fields.Many2one('shuttle_schedule.model', string='Shuttle Schedule', readonly=True)
    display_departure_time = fields.Char(string='Display Departure Time 24hr',  required=True)


    @api.onchange('departure_time')
    def onchange_departure_time(self):
        """CONVETES DEPARTURE TIME TO A DISPLAYABLE TIME IN DISPLAY DEPARTURE TIME"""
        for rec in self:
            hours = int(rec.departure_time)
            minutes = round((rec.departure_time - hours) * 60)
            time_str = f"{hours:02}:{minutes:02}"
            try:
                rec.display_departure_time = datetime.strptime(time_str, '%H:%M').strftime('%H:%M')
            except ValueError:
                raise ValidationError(_('Please renter your time in format of H:M eg 13:00'))

    @api.model_create_multi
    def create(self, vals_list):
        res = super(EmployeeSchedules, self).create(vals_list)
        self.onchange_departure_time()
        return res