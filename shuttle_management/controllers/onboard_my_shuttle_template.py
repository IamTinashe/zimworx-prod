# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from datetime import datetime, timedelta



class ShuttleOnboardManagement(http.Controller):
    @http.route('/my_shuttle/onboard/<int:schedule_id>', type='http', auth='public', website=True)
    def my_shuttle_onboard(self,schedule_id, **kwargs):
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
                [('weekday_id', 'in', shuttle_schedule.weekday_id.ids), ('shuttle_schedule', '=', shuttle_schedule.id)])

            return request.render('shuttle_management.onboard_my_shuttle_template',{
                'shuttle_schedule':shuttle_schedule,
                'shuttle_id':shuttle_id,
                'employee_schedules':employee_schedules,
            })

    @http.route('/my_shuttle/scan_qr', type='http', auth='public', website=True)
    def my_shuttle_scan_qr(self, **kwargs):
        driver_id = request.httprequest.cookies.get('driver_id')
        if driver_id == None:
            # render a fake login for asking for driver_id
            return request.redirect('/my_shuttle/login')
        else:
            return request.render('shuttle_management.onboard_scan_qr_code')

    @http.route('/my_shuttle/confirm_onboard', type='json', auth='public')
    def my_shuttle_confirm_onboard(self, **kwargs):
        driver_id = request.httprequest.cookies.get('driver_id')
        if driver_id == None:
            return request.redirect('/my_shuttle/login')
        else:
            print(0/1)
            print("we are here")
            return {'success': True}