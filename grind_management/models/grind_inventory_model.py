# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

class GrindInventory(models.Model):
    _name = 'grind_inventory.model'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Grind Inventory'

    name = fields.Char(string="Item Name", required=True)
    item_code = fields.Char(string="Item Code", required=True, help="Unique identifier for each item")
    # category_id = fields.Many2one('product.category', string="Category", help="Category the item belongs to")
    supplier_id = fields.Many2one('res.partner', string="Supplier", help="Supplier of the item")
    currency_id = fields.Many2one('res.currency', string="Currency")
    description = fields.Text(string="Description", help="Description of the item")
    cost_price = fields.Monetary(string="Cost Price", required=True, help="Purchase price of the item")
    sale_price = fields.Monetary(string="Sale Price", required=True, help="Selling price of the item")
    quantity_available = fields.Float(string="Available Quantity", help="Quantity available in stock")
    reorder_level = fields.Float(string="Reorder Level", help="Minimum quantity before reordering is needed")
    reorder_quantity = fields.Float(string="Reorder Quantity", help="Quantity to reorder when stock is low")
    # uom_id = fields.Many2one('uom.uom', string="Unit of Measure", help="Unit of Measure for the item")
    date_added = fields.Date(string="Date Added", default=date.today(),  help="Date the item was added to inventory")
    active = fields.Boolean(string="Active", default=True, help="Is this item currently active?")
    inventory_type = fields.Selection([('shop_product', 'Shop Product'),
                                         ('ingredient', 'Ingredient'),
                                         ('both_product_ingredient', 'Both Shop Product & Ingredient'),
                                         ],
                                        'Inventory Type', required=True,)
    menu_id = fields.Many2one('grind_menu.model', string="Menu", required=True)


#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
