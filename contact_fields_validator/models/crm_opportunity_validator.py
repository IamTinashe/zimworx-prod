from odoo import models
from odoo.exceptions import UserError


class CrmOpportunityValidator:
    def __init__(self, opportunity):
        self.opportunity = opportunity
        self.missing_fields = []

    def validate_fields(self):
        # Define the stages to check
        relevant_stage_ids = [4, 12, 13]
        print(self.opportunity.stage_id)

        # Check if the opportunity's stage_id is in the relevant stages
        if self.opportunity.stage_id.id in relevant_stage_ids:
            # Perform your field checks here
            if not self.opportunity.partner_id.x_studio_roll_on_date:
                self.missing_fields.append("Roll-on Date")
            if not self.opportunity.partner_id.x_studio_arm:
                self.missing_fields.append("CSP")

            customer_group = self.opportunity.partner_id.x_studio_customer_stage  # Replace with actual field name
            if customer_group not in ['Active Customer', 'Inactive']:
                self.missing_fields.append("\n\nPlease correct the Customer Group Stage to 'Active Customer' on the "
                                           "Client Card")

            # Raise error if there are missing fields
            if self.missing_fields:
                fields_str = ", ".join(self.missing_fields)
                raise UserError(
                    f"Please update the following fields on the client card: {fields_str}"
                )
