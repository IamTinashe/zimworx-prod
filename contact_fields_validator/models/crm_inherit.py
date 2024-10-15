from odoo import models
from .partner_field_validator import PartnerFieldValidator  # Ensure correct import
from .crm_opportunity_validator import CrmOpportunityValidator

class CRMInherit(models.Model):
    _inherit = 'crm.lead'  # Replace with the actual model name

    def write(self, vals):
        res = super(CRMInherit, self).write(vals)
        self._check_missing_partner_fields()  # Check for missing fields after writing
        return res

    def _check_missing_partner_fields(self):
        validator = PartnerFieldValidator(self.partner_id)
        validator.validate_fields()

    def write(self, vals):
        res = super(CRMInherit, self).write(vals)

        # Check if the stage is updated to one of the relevant stages
        for record in self:
            if 'stage_id' in vals:
                # Fetch the new stage
                new_stage = self.env['crm.stage'].browse(vals['stage_id'])
                validator = CrmOpportunityValidator(record)
                validator.validate_fields()  # Validate fields when the stage changes

        return res