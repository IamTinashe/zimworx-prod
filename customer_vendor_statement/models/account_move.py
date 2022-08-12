from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move.line'

    account_internal_type = fields.Selection(related='account_id.user_type_id.type', string="Internal Type", readonly=True, store=True)