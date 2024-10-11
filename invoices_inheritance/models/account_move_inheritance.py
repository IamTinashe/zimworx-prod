from odoo import fields, models, api
from odoo.exceptions import UserError



class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    def write(self, vals):
        res = super(AccountMoveInherit, self).write(vals)
        for record in self:
            missing_fields = []
            # Check if each field is present and add to `missing_fields` if not.
            if not record.partner_id.phone:
                missing_fields.append("Phone Number")
            if not record.partner_id.email:
                missing_fields.append("Email")
            if not record.partner_id.x_studio_number_of_locations:
                missing_fields.append("Number of Locations")
            if not record.partner_id.x_studio_roll_on_date:
                missing_fields.append("Roll On Date")
            if not record.partner_id.x_studio_dso_or_single:
                missing_fields.append("DSO or Single")
            if not record.partner_id.x_studio_rcm_program:
                missing_fields.append("RCM Program")
            if not record.partner_id.x_studio_bus_type_or_specialty:
                missing_fields.append("Business Type or Specialty")
            if not record.partner_id.country_id:
                missing_fields.append("Country")
            if not record.partner_id.state_id:
                missing_fields.append("State")
            if not record.partner_id.x_studio_arm:
                missing_fields.append("ARM")
            if not record.partner_id.x_studio_customer_group:
                missing_fields.append("Customer Group")
            # If there are missing fields, raise a UserError with the list of fields
            if missing_fields:
                fields_str = ", ".join(missing_fields)  # Create a comma-separated string of missing fields
                raise UserError(
                    f"Please contact the responsible salesperson to update the client card. The following fields are missing: {fields_str}")
        return res

