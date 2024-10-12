from odoo import fields, models, api


class GrindInventoryCategory(models.Model):
    _name = 'grind_inventory.category'
    _description = 'Grind Inventory'
    _rec_name='name'

    name = fields.Char(string="Category")
