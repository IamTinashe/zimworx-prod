from odoo import models
from odoo.exceptions import UserError

class PartnerFieldValidator:
    def __init__(self, partner):
        self.partner = partner
        self.missing_fields = []

    def validate_fields(self):
        field_checks = {
            "Email": self.partner.email,
            "Number of Locations": self.partner.x_studio_number_of_locations,
            "DSO or Single": self.partner.x_studio_dso_or_single,
            "Business Type or Specialty": self.partner.x_studio_bus_type_or_specialty,
            "Country": self.partner.country_id,
            "State": self.partner.state_id,
            "Customer Group": self.partner.x_studio_customer_group,
        }

        for field_name, field_value in field_checks.items():
            if not field_value:
                self.missing_fields.append(field_name)

        if self.missing_fields:
            fields_str = ", ".join(self.missing_fields)
            raise UserError(
                f"The information on the client card is incomplete. Please contact the responsible salesperson to "
                f"update the client card before you make changes. The following fields are missing or inaccurate: {fields_str}"
            )
