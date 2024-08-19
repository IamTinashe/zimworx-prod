from odoo import fields, models, api , _
import os
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import  ValidationError

class OnboardEmployeeForShuttle(models.TransientModel):
    _name = 'onboard_employee_for_shuttle.wizard'
    _description = 'Employee Onboard'

    employee_location = fields.Char()
    quick_note = fields.Char()
    recomodation = fields.Selection([
       ('positive','Positive'),
       ('negative','Negative')], string="Recomodation")
    route_not_found = fields.Boolean(default=False)
    schedule_found = fields.Boolean(default=False)
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
        res['employee_location']= f"{hr_employee_id.street2} - {hr_employee_id.city}"

        shuttle_recomodation_list=[]
        #search for this location in route_end_location
        route_end_location = self.env['route_end_location.model'].search([('route_end', '=', hr_employee_id.street2)])
        if len(route_end_location)==0:
            res['quick_note'] = f'Sorry the {hr_employee_id.street2} route does not exists in Routes, Please create it and Attach a Shuttle which goes to {hr_employee_id.street2}'
            res['recomodation'] = 'negative'
            #No Shuttle found with that location return to give a validation error
        else:
            #the route exits and lest try to find if there is a shuttle for that route
            for rec in route_end_location:
                print("route_end_location",route_end_location)
                #search into if there is a such route which goes that way
                shuttle_sub_routes_id = self.env['shuttle.sub.route'].search([('end_location', '=', rec.id)])
                if len(shuttle_sub_routes_id)!=0:
                    #handle a scenario where we have found a route which goes this way which is to find if the schdule meet or not fully
                    for shuttle_sub_route in shuttle_sub_routes_id:
                        #loop inside the sub route in hence accessing all the shuttle with such route
                        shuttles_schedules = self.env['shuttle_schedule.model'].search([('shuttle_route', '=', shuttle_sub_routes_id.route_id.id)])
                        if len(shuttles_schedules)!=0:
                            for shuttles_schedule in shuttles_schedules:
                                if shuttles_schedule.shuttle_id.name not in shuttle_recomodation_list:
                                    shuttle_recomodation_list.append(shuttles_schedule.shuttle_id.name)
                                #recommed those shuttles only
                                res['shuttle_id'] = shuttles_schedule.shuttle_id.id
                            res['quick_note']=f'These shuttles {shuttle_recomodation_list} are the recomodations for route of {hr_employee_id.street2}'
                            res['recomodation']='positive'
                        else:
                            res['quick_note'] = f'Sorry the Route {hr_employee_id.street2} exists but could not found any shuttle with such route'
                            res['recomodation'] = 'negative'
                            #there is no a shuttle which goes that route
                else:
                    res['quick_note'] = f'Sorry the Route {hr_employee_id.street2} exists but could not found any shuttle with such route'
                    res['recomodation'] = 'negative'
                    #handle the scenario that there is no such route which exists therefore no shuttle goes there








                # print("some shutttle within that route found", shuttle_sub_routes_id)
                #
                # shuttles_schedules = self.env['shuttle_schedule.model'].search([('shuttle_route', '=', shuttle_sub_routes_id.ids)])
                # employee_schedules = self.env['employee_schedules.model'].search([('employee_id', '=', hr_employee_id.id)])
                # shuttle_lines=[]
                # #check if there is any shuttle schdule with that employee end location
                # if len(shuttles_schedules)!=0:
                #     print("they are some shuttle schdules avaiable with the empl")
                #     for shuttles_schedule in shuttles_schedules:
                #         # for rec in shuttle.shuttle_schedule_ids:
                #         #loop through the employee schdule just try to find a match of employee schudule and available schedule
                #         for record in employee_schedules:
                #             if set(record.weekday_id.ids).intersection(set(shuttles_schedule.weekday_id.ids)):
                #                 print("rec.departure_time",shuttles_schedule.departure_time)
                #                 print("record.departure_time",record.departure_time)
                #                 #find the one in the match if there is any which is free which match with schdule
                #                 if rec.departure_time == record.departure_time and rec.is_fully_booked !='fully_booked':
                #                     #if a match of schedule time pass that shuttle to shuttle id and break the whole loop
                #                     res['shuttle_id']=shuttles_schedule.id
                #                     res['schedule_found']=True
                #                     res['quick_note']=f'{shuttles_schedule.shuttle_id.name} contains a possible slot on {record.departure_time} departure_time slots'
                #                     # Loop through the shuttle schedule so that it can be seen for display
                #                     for final_shuttle_schedule in shuttles_schedule.shuttle_id.shuttle_schedule_ids:
                #                         shuttle_line={
                #                             'departure_time':final_shuttle_schedule.departure_time,
                #                             'booked_seating_capacity':final_shuttle_schedule.booked_seating_capacity,
                #                             'max_seating_capacity':final_shuttle_schedule.max_seating_capacity,
                #                             'is_fully_booked':final_shuttle_schedule.is_fully_booked,
                #                             'weekday_id':final_shuttle_schedule.weekday_id,
                #                         }
                #                         shuttle_lines.append((0, 0, shuttle_line))
                #                     res['shuttle_schedule_ids'] = shuttle_lines
                    #                 complete_break_loop=True
                    #                 break
                    #         else:
                    #             #save that not specific scddule found for this but there is pontential shuttle which goes into that direction
                    #             res['schedule_found'] == False
                    #             departure_time=record.departure_time
                    #             possible_shuttle=shuttle.id
                    #
                    #         # make it break since it have got a quick schdule suggestion
                    #         if complete_break_loop==True:
                    #             break
                    #     if complete_break_loop == True:
                    #         break
                    #     if complete_break_loop == True:
                    #         break
                    #
                    # #lest take instance where find a shuttle with a possible route without any of that schedule
                    # if res['schedule_found'] == False:
                    #     res['shuttle_id'] = possible_shuttle
                    #     res['schedule_found'] = False
                    #     res['quick_note'] = f'{possible_shuttle.name} pass through this route but doesnt contains {departure_time} departure_time slot. Please consider add this Employee Schedule on this shuttle or find another schedule'
                    #     # Loop through the shuttle schedule so that it can be seen for displa
                    #     for final_shuttle_schedule in possible_shuttle.shuttle_schedule_ids:
                    #         shuttle_line = {
                    #             'departure_time': final_shuttle_schedule.departure_time,
                    #             'booked_seating_capacity': final_shuttle_schedule.booked_seating_capacity,
                    #             'max_seating_capacity': final_shuttle_schedule.max_seating_capacity,
                    #             'is_fully_booked': final_shuttle_schedule.is_fully_booked,
                    #             'weekday_id': final_shuttle_schedule.weekday_id,
                    #         }
                    #         shuttle_lines.append((0, 0, shuttle_line))
                    #     res['shuttle_schedule_ids'] = shuttle_lines
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