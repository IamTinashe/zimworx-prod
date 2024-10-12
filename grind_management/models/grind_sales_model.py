from odoo import models, fields, api, _

class GrindSales(models.Model):
    _name = 'grind_sales.model'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Grind Sales Management'
    _rec_name='sale_order_number'

    sale_order_number = fields.Char(string="Sale Order Number", default=lambda self: _('New'), required=True, readonly=True)
    hr_employee_id = fields.Many2one('hr.employee', string="Employee")
    product_inventory = fields.Many2one('grind_inventory.model', string="Product")
    product_menu = fields.Many2one('grind_menu.model', string="Menu")
    currency_id = fields.Many2one('res.currency', string="Currency")
    sale_date = fields.Datetime(string="Sale Date", default=fields.Datetime.now, required=True)
    total_amount = fields.Monetary(string="Total Amount", compute="_compute_total_amount", store=True)
    payment_status = fields.Selection([
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
    ], string="Payment Status", default='pending')
    sale_product = fields.Selection([
        ('product', 'Product'),
        ('menu', 'menu'),
    ], string="Sale Product Type",)
    salesperson = fields.Many2one('res.users', string="Salesperson", readonly=1, default=lambda self: self.env.user)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['sale_order_number'] = self.env['ir.sequence'].next_by_code('sale_order_number.seq')
        res = super(GrindSales, self).create(vals)
        return res
