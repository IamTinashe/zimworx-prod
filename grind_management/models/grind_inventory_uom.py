from odoo import fields, models, api


class GrindInventoryUom(models.Model):
    _name = 'grind_inventory.uom'
    _description = 'Grind Inventory Units of Measurement'

    name = fields.Char(string="Unit of Measure", required=True)

