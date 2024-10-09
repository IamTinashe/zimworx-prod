from odoo import models, fields, api
from datetime import date
import requests


class ClientSwagGiftsManagement(models.Model):
    _name = 'client_swag_gifts.model'
    _description = 'Swag Gift'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    box_number = fields.Char(string='Box #', required=True)
    name = fields.Many2one('res.partner', string='Name', required=True)
    company = fields.Many2one('res.partner', string='Company', required=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ], string='Status', default='pending')
    street = fields.Char(related='company.street',string='Street')
    street2 = fields.Char(related='company.street2',string='Street 2')
    city = fields.Char(related='company.city',string='City')
    state_id = fields.Many2one(related='company.state_id',string='State')
    zip = fields.Char(related='company.zip',string='zip')
    phone = fields.Char(related='company.phone',string='Phone Number')
    email = fields.Char(string='Email',related='company.email',)
    tracking_number = fields.Char(string='Tracking No.')
    ship_date = fields.Date(string='Ship Date')
    delivery_date = fields.Date(string='Delivery Date')
    date_delivered = fields.Date(string='Date Delivered')
    salesperson = fields.Many2one('res.users', string='Salesperson')
    follow_up_done = fields.Boolean(string='Follow Up Done', default=False)

    def set_to_shipped(self):
        self.status = 'shipped'

    def set_to_delivered(self):
        self.status = 'delivered'
        self.date_delivered = date.today()

    def reset_to_pending(self):
        self.status = 'pending'


    def authenticate_fedex_api(self):
        """THIS GENERATES A TOCKEN WHICH IS USED FOR FEDEX API """
        url = "https://apis-sandbox.fedex.com/oauth/token"
        payload = {
            'grant_type': 'client_credentials',
            'client_id': 'l797489fb42f0249bd9bf47e78d755d367',
            'client_secret': '4d416060714d4f258da47ce240db6ff1',
        }
        headers = {
            'Content-Type': "application/x-www-form-urlencoded"
        }
        response = requests.post(url, data=payload, headers=headers)
        response_date=response.text['access_token']
        print(response_date.get("access_token"))
        return response
