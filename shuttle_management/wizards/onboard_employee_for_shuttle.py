from odoo import fields, models, api , _
import os
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import  ValidationError

class OnboardEmployeeForShuttle(models.TransientModel):
    _name = 'onboard_employee_for_shuttle.wizard'
    _description = 'Employee Onboard'

    employee_location = fields.Char()
    route_not_found = fields.Boolean(default=False)
    shuttle_id = fields.Many2one('shuttles.model', string='Possible Shuttle', required=True)
    shuttle_schedule_ids=fields.One2many('onboard_shuttle_schedule.wizard', 'shuttle_id', string='shuttle_schedule Shuttle')

    @api.model
    def default_get(self, fields):
        # LOAD A POSSIBLE SHUTTLE INSIDE THE SHUTTLE MODEL
        res = super().default_get(fields)
        hr_employee_id = self.env['hr.employee'].search([('id', '=', self._context.get('active_id'))])
        #check if street is not empty and return a validation
        # if hr_employee_id.street ==False:
        #     raise ValidationError(_("Please Ensure the Street of the employee is filled"))
        #load the current employee location
        res['employee_location']= f"{hr_employee_id.street} - {hr_employee_id.city}"
        #search for this location in route_end_location
        route_end_location = self.env['route_end_location.model'].search([('route_end', '=', hr_employee_id.street)])
        print(len(route_end_location))
        if len(route_end_location)==0:
            res['route_not_found']=True
            #No Shuttle found with that location return to give a validation error





        return res





    def action_allocated_schedule(self):
        """THIS FUNCTION IS FOR ONBOARDING A NEW EMPLOYEE TO A SHUTTLE, SCHEDULE AND A DRIVER"""

        #search a shuttle with possible route for the employee
        #if found search a route with possible slot
        #if not found bring every driver available for custom selection


        print("Employee Onboarded")

class ShuttleSchedules(models.TransientModel):
    """THIS DISPLAY SHUTTLE SCHEDULES ON A TEMP LEVEL"""
    _name = 'onboard_shuttle_schedule.wizard'
    _description = 'Description'

    shuttle_id = fields.Many2one('onboard_employee_for_shuttle.wizard', string='Shuttle', required=True)
    # route_name = fields.Char(string='Route Name', required=True)
    departure_time = fields.Float(string='Departure Time 24hr', required=True)
    booked_seating_capacity = fields.Integer(string='Booked Seating Capacity')
    max_seating_capacity = fields.Integer(string='Max Seating Capacity')
    is_fully_booked = fields.Selection([
        ('fully_booked', 'Full Booked'),
        ('not_fully_booked', 'Not Fully Booked'),
    ],default='not_fully_booked', string='Booking Status')
    weekday_id = fields.Many2many('weekday.model', string='Day', required=True)