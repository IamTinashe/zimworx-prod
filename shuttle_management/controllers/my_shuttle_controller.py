# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from datetime import datetime, timedelta



class ShuttleManagement(http.Controller):
    @http.route('/my_shuttle', type='http', auth='public', website=True)
    def my_shuttle(self, **kwargs):
        """GIVE A MAIN PAGE OF A SHUTTLE MANAGEMENT SYSTEM"""
        #CHECK IF THE DRIVER COOKIES IS WITH THE ID IS NOT YET EXIPRED IF EXIPRED ASK FOR AUTH
        driver_id = request.httprequest.cookies.get('driver_id')
        if driver_id == None:
            #render a fake login for asking for driver_id
            return request.redirect('/my_shuttle/login')
        else:
            #get driver details and shuttle details
            shuttle_id = request.env['shuttles.model'].search(
                [('driver_login_id', '=', driver_id)])
            #search for today schedule
            shuttle_schedule = request.env['shuttle_schedule.model'].search(
                [('shuttle_id', '=', shuttle_id.id),('weekday_id.name', '=', datetime.now().strftime('%A').lower())])
            #search next 3days schedule
            today = datetime.now()
            date_list = [today + timedelta(days=i) for i in range(3)]
            next_3_days = [date.strftime('%A').lower() for date in date_list]
            print(next_3_days)

            next_3_days_shuttle_schedule = request.env['shuttle_schedule.model'].search(
                [('shuttle_id', '=', shuttle_id.id), ('weekday_id.name','in', next_3_days), ('confirmed_date','!=',today.strftime('%m/%d/%Y'))])

            #get yesterday unconfirmed date
            yesterday = today - timedelta(days=1)

            yesterday_unconfirmed_shuttle_schedule = request.env['shuttle_schedule.model'].search(
                [('shuttle_id', '=', shuttle_id.id), ('weekday_id.name', '=', yesterday.strftime('%A').lower()), ('confirmed_date','!=',yesterday.strftime('%m/%d/%Y'))])

        return request.render('shuttle_management.my_shuttle_template',{
            'shuttle_id':shuttle_id,
            'today':today.strftime('%A %d %b %Y'),
            'shuttle_schedule':shuttle_schedule,
            # 'next_3_days_shuttle_schedule':next_3_days_shuttle_schedule,
            'yesterday_unconfirmed_shuttle_schedule':yesterday_unconfirmed_shuttle_schedule,
        })

    @http.route('/my_shuttle/login', type='http', auth='public', website=True)
    def my_shuttle_login(self, **kwargs):
        """THIS GIVES A QUICK LOGIN PAGE FOR A DRIVER TO ENTER HIS DRIVER ID"""
        login_status = kwargs.get('login', None)
        driver_id = request.httprequest.cookies.get('driver_id')
        if driver_id == None:
            return request.render('shuttle_management.driver_login_template',  {
            'login_status': login_status,
            })
        else:
            # visit my_shuttle
            return request.redirect('/my_shuttle')

    @http.route('/my_shuttle/save_driver_id', type='http', auth='none', csrf=False, website=True, methods=['POST'])
    def save_driver_id(self, **kwargs):
        """SAVE THE DRIVER ID INTO COOKIES"""
        driver_id = kwargs.get('driver_id')
        # Check if the driver ID is valid
        driver = request.env['hr.employee'].sudo().search([('driver_login_id', '=', driver_id),('department_id','=',18)], limit=1)
        if not driver:
            # If invalid, redirect back to the driver ID form with an error message
            return request.redirect('/my_shuttle/login?login=Failed')
        else:
            # Save the driver ID in cookies
            response = request.redirect('/my_shuttle')
            response.set_cookie('driver_id', driver_id, max_age=4 * 24 * 60 * 60)  # 4 days expiration
            return response

    @http.route('/my_shuttle/logout', type='http', auth='none', csrf=False, website=True, methods=['POST'])
    def my_shuttle_logout(self, **kwargs):
        """THIS LOGOUT A SHUTTLE IN THE SHUTTLE MANAGEMENT"""
        response = request.redirect('/my_shuttle')
        response.delete_cookie('driver_id')
        return response
