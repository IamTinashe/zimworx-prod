from odoo import models
from .partner_field_validator import PartnerFieldValidator  # Ensure correct import

class SubscriptionInherit(models.Model):
    _inherit = 'sale'  # Replace with the actual model name

    def write(self, vals):
        res = super(SubscriptionInherit, self).write(vals)
        self._check_missing_partner_fields()  # Check for missing fields after writing
        return res

    def _check_missing_partner_fields(self):
        validator = PartnerFieldValidator(self.partner_id)
        validator.validate_fields()