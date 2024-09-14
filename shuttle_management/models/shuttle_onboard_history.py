from odoo import fields, models, api


class ShuttleOnboardHistory(models.Model):
    _name = 'shuttle_onboard_history.model'
    _description = 'Shuttle Onboard History'

    onboard_date_time = fields.Datetime(string='Onboard Date Time', required=True)
    onboard_date = fields.Date(string='Onboard Date', required=True)
    employee_id = fields.Many2one('hr.employee', string='Shuttle', required=True)
    shuttle_id = fields.Many2one('shuttles.model', string='Shuttle', readonly=True)

