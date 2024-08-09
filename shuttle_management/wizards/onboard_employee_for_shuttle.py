from odoo import fields, models, api , _
import os
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import  ValidationError

class OnboardEmployeeForShuttle(models.TransientModel):
    _name = 'onboard_employee_for_shuttle.wizard'
    _description = 'Employee Onboard'

    name = fields.Char()

    def action_allocated_schedule(self):
        """THIS FUNCTION IS FOR ONBOARDING A NEW EMPLOYEE TO A SHUTTLE, SCHUDULE AND A DRIVER"""

        #search a shuttle with possible route with the employee
        #if found search a route with possible slot
        #if not found bring every driver available for custom selection


        print("Employee Onboarded")
