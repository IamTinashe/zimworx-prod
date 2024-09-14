# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs




class ShuttleOnboardManagement(http.Controller):
    @http.route('/my_shuttle/onboard/<string:date>/<int:schedule_id>', type='http', auth='public', website=True)
    def my_shuttle_onboard(self,schedule_id, date, **kwargs):
        driver_id = request.httprequest.cookies.get('driver_id')
        if driver_id == None:
            # render a fake login for asking for driver_id
            return request.redirect('/my_shuttle/login')
        else:
            shuttle_id = request.env['shuttles.model'].search(
                [('driver_login_id', '=', driver_id)])
            #search for schedule and pass some deatils for it
            shuttle_schedule = request.env['shuttle_schedule.model'].search(
                [('shuttle_id', '=', shuttle_id.id), ('id', '=', schedule_id)])

            employee_schedules = request.env['employee_schedules.model'].search(
                [('weekday_id', 'in', shuttle_schedule.weekday_id.ids),
                 ('shuttle_schedule', '=', shuttle_schedule.id)])

            employee_schedules_list=[]
            #make a list which shows confirmed employess have a schdule
            for employee_schedule in employee_schedules:
                # create a date by either saying is the schedule for today or yesterday
                if date == 'td':
                    to_confirm_date = datetime.now().date()
                elif date == 'yt':
                    to_confirm_date = (datetime.now() - timedelta(days=1)).date()
                #search in shuttle_onboard_history
                shuttle_onboard_history = request.env['shuttle_onboard_history.model'].search(
                    [('employee_id', '=', employee_schedule.employee_id.id), ('onboard_date', '=', to_confirm_date)])
                if shuttle_onboard_history:
                    employee_schedules_list.append({
                        'name':employee_schedule.employee_id.name,
                        'display_departure_time':employee_schedule.display_departure_time,
                        'street':employee_schedule.employee_id.street,
                        'confirmed': 'Confirmed',
                    })
                else:
                    employee_schedules_list.append({
                        'name': employee_schedule.employee_id.name,
                        'display_departure_time': employee_schedule.display_departure_time,
                        'street': employee_schedule.employee_id.street,
                        'confirmed': 'Not Confirmed',
                    })




            return request.render('shuttle_management.onboard_my_shuttle_template',{
                'shuttle_schedule':shuttle_schedule,
                'shuttle_id':shuttle_id,
                'employee_schedules_list':employee_schedules_list,
                'schedule_id':schedule_id,
                'date':date,
            })

    @http.route('/my_shuttle/scan_qr/<string:date>/<int:schedule_id>', type='http', auth='public', website=True)
    def my_shuttle_scan_qr(self, schedule_id, date,**kwargs):
        driver_id = request.httprequest.cookies.get('driver_id')
        if driver_id == None:
            # render a fake login for asking for driver_id
            return request.redirect('/my_shuttle/login')
        else:
            return request.render('shuttle_management.onboard_scan_qr_code',{
                'schedule_id':schedule_id,
                'date':date,
            })

    @http.route('/my_shuttle/confirm_onboard',type='http', auth='public', csrf=False, methods=['POST'])
    def my_shuttle_confirm_onboard(self, **kwargs):
        driver_id = request.httprequest.cookies.get('driver_id')
        if driver_id == None:
            return request.redirect('/my_shuttle/login')
        else:
            qr_code_data = kwargs.get('qr_code')
            date = kwargs.get('date')
            schedule_id = kwargs.get('schedule_id')
            #if its an old qr code please handle it accodindly
            if "https://" in qr_code_data:
                parsed_url = urlparse(qr_code_data)
                query_params = parse_qs(parsed_url.query)
                ref_num = query_params.get('refNum', [None])[0]

                employee_id = request.env['hr.employee'].search(
                    [('old_qr_code', '=', ref_num)])
                if employee_id:
                    #should mark the employee as onborded
                    if date == 'td':
                        to_confirm_date = datetime.now()  # Extract only the date part
                    elif date == 'yt':
                        to_confirm_date = (datetime.now() - timedelta(days=1)) # Extract only the date part

                    shuttle_onboard_history_id = request.env['shuttle_onboard_history.model'].search([
                        ('onboard_date', '=', to_confirm_date.date()),
                        ('employee_id', '=', employee_id.id)
                    ])
                    if shuttle_onboard_history_id:
                        #the employee is already onborded
                        return f"Employee {employee_id.name} Already Confirmed"
                    else:
                        shuttle_schedule = request.env['shuttle_schedule.model'].search([('id', '=', schedule_id)])

                        shuttle_onboard_history_id = request.env['shuttle_onboard_history.model'].create({
                            'onboard_date_time':to_confirm_date,
                            'onboard_date':to_confirm_date.date(),
                            'employee_id':employee_id.id,
                            'shuttle_id':shuttle_schedule.shuttle_id.id,
                        })
                        return f"Employee {employee_id.name} Onboard Confirmed"




                else:
                    return f"Employee Not Found"

            print(qr_code_data)
            return f"QR Code received: {qr_code_data}"