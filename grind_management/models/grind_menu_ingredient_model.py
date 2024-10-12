from odoo import models, fields


class GrindMenuIngredient(models.Model):
    _name = 'grind_menu_ingredient.model'
    _description = 'Grind Menu Ingredient'
    _inherit = ["mail.thread", "mail.activity.mixin"]


    menu_id = fields.Many2one('grind_menu.model', string="Menu", required=True)
    grind_inventory = fields.Many2one('grind_inventory.model', string="Inventory",  domain=[('inventory_type','!=','shop_product')] ,required=True)  # Linking to the product model in inventory
    quantity = fields.Float(string="Quantity", required=True)
    # uom_id = fields.Many2one('uom.uom', string="Unit of Measure", required=True)
    cost_price = fields.Monetary(related='grind_inventory.cost_price', string="Cost Price",)
    currency_id = fields.Many2one(related='grind_inventory.currency_id', string="Currency")

