from odoo import models, fields, api

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
    salesperson = fields.Many2one(related='company.user_id', string='Salesperson')
    follow_up_done = fields.Boolean(string='Follow Up Done', default=False)