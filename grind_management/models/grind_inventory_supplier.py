from odoo import fields, models, api
from datetime import date, datetime

class GrindInventorySupplier(models.Model):
    _name = 'grind_inventory.supplier'
    _description = 'Grind Inventory Supplier'
    _rec_name='name'

    name = fields.Char(string='Supplier Name', required=True)
    contact_person = fields.Char(string='Contact Person')
    phone = fields.Char(string='Phone Number')
    email = fields.Char(string='Email')
    address = fields.Char(string='Address')
    city = fields.Char(string='City', default="Harare")
    delivery_terms = fields.Text(string='Delivery Terms')
    payment_terms = fields.Text(string='Payment Terms')
    active = fields.Boolean(string='Active', default=True)

    # For tracking the date when the supplier was added
    supplier_since = fields.Date(string='Supplier Since', default=datetime.now())



