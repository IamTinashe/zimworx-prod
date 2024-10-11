from odoo import models
from .partner_field_validator import PartnerFieldValidator  # Ensure correct import


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    def write(self, vals):
        res = super(AccountMoveInherit, self).write(vals)
        self._check_missing_partner_fields()  # Check for missing fields after writing
        return res

    def _check_missing_partner_fields(self):
        validator = PartnerFieldValidator(self.partner_id)
        validator.validate_fields()  # Call the validate method
