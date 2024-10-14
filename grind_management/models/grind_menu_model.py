from odoo import models, fields
from datetime import date, datetime

class GrindMenu(models.Model):
    _name = 'grind_menu.model'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Grind Menu'

    name = fields.Char(string="Menu Name", required=True)
    menu_code = fields.Char(string="Menu Code", required=True, help="Unique identifier for each menu")
    ingredients_ids = fields.One2many('grind_menu_ingredient.model', 'menu_id', string="Ingredients",)
    sale_price = fields.Monetary(string="Sale Price", required=True, help="Selling price of this menu")
    cost_price = fields.Monetary(string="Cost Price", required=True, help="Cost price of making this menu")
    description = fields.Text(string="Description")
    currency_id = fields.Many2one('res.currency', string="Currency")
    active = fields.Boolean(string="Active", default=True)
    date_added = fields.Date(string="Date Added", default=datetime.now(),  help="Date the item was added to menu")

