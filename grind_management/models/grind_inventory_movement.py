from odoo import fields, models, api, _
from datetime import date, datetime


class GrindInventoryMovement(models.Model):
    _name = 'grind_inventory.movement'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Grind Inventory Movements'

    name = fields.Char(string="Reference", required=True, copy=False, readonly=True, default=lambda self: _('New'))
    grind_inventory_id = fields.Many2one('grind_inventory.model', string='Product', required=True)
    grind_sales = fields.Many2one('grind_sales.model', string='Grind Sales')
    movement_date = fields.Datetime(string='Movement Date', default=datetime.now(), required=True)
    quantity = fields.Float(string='Quantity', required=True)
    grind_inventory_uom_id = fields.Many2one('grind_inventory.uom', related='grind_inventory_id.grind_inventory_uom_id',string='Unit of Measure', required=True)
    movement_type = fields.Selection([
        ('stock_in', 'Stock In'),
        ('sell', 'Sell Out'),
        ('balance', 'Balance')
    ], string='Movement Type', required=True, tracking=True)
    responsible_user_id = fields.Many2one('res.users', string='Handled By', default=lambda self: self.env.user , readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done')
    ], string='Status', default='draft')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('grind_inventory_name.seq') or _('New')
        return super(GrindInventoryMovement, self).create(vals)

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_done(self):
        self.write({'state': 'done'})
