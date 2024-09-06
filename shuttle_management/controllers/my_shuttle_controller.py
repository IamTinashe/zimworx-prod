# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class ShuttleManagement(http.Controller):
    @http.route('/my_shuttle', type='http', auth='public', website=True)
    def my_shuttle(self, **kwargs):
        """GIVE A MAIN PAGE OF A SHUTTLE MANAGEMENT SYSTEM"""
        #CHECK IF THE DRIVER COOKIES IS WITH THE ID IS NOT YET EXIPRED IF EXIPRED ASK FOR AUTH
        driver_id = request.httprequest.cookies.get('driver_id')
        if driver_id == None:
            #render a fake login for asking for driver_id
            return request.redirect('/my_shuttle/login')

        return request.render('shuttle_management.my_shuttle_template')

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
            response.set_cookie('driver_id', driver_id, max_age=30)  # 30 seconds expiration
            return response


#     @http.route('/shuttle_management/shuttle_management/objects/<model("shuttle_management.shuttle_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('shuttle_management.object', {
#             'object': obj
#         })
