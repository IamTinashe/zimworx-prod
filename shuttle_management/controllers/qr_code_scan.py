from odoo import http
from odoo.http import request
from werkzeug.utils import redirect

class ShuttleManagement(http.Controller):

    @http.route('/shuttle/driver_portal', type='http', auth='none', website=True)
    def driver_portal(self, **kwargs):
        # Check if driver ID is in cookies
        driver_id = request.httprequest.cookies.get('driver_id')

        if not driver_id:
            # If not, redirect to driver ID submission page
            return request.redirect('/shuttle/enter_driver_id')

        # Fetch driver-related data using driver_id
        # driver = request.env['res.partner'].sudo().search([('id', '=', driver_id), ('is_driver', '=', True)], limit=1)

        if not driver:
            # If driver not found, clear the cookie and redirect to enter_driver_id page
            response = request.redirect('/shuttle/enter_driver_id')
            response.delete_cookie('driver_id')
            return response

        # Render the driver portal page with driver-related data
        return request.render('shuttle_management.driver_portal_template', {'driver': driver})

    @http.route('/shuttle/enter_driver_id', type='http', auth='none', website=True)
    def enter_driver_id(self, **kwargs):
        # Render a simple form to enter driver ID
        return request.render('shuttle_management.enter_driver_id_template')

    @http.route('/shuttle/save_driver_id', type='http', auth='none', csrf=False, website=True, methods=['POST'])
    def save_driver_id(self, **kwargs):
        driver_id = kwargs.get('driver_id')

        # Check if the driver ID is valid
        # driver = request.env['res.partner'].sudo().search([('id', '=', driver_id), ('is_driver', '=', True)], limit=1)
        # if not driver:
        #     # If invalid, redirect back to the driver ID form with an error message
        #     return request.redirect('/shuttle/enter_driver_id?error=invalid_driver_id')

        # Save the driver ID in cookies
        response = request.redirect('/shuttle/driver_portal')
        response.set_cookie('driver_id', driver_id, max_age=60*60*24*30)  # Cookie expires in 30 days

        return response
