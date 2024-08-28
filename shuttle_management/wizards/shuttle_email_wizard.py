from odoo import models, fields, api

class ShuttleEmailWizard(models.TransientModel):
    _name = 'shuttle_email.wizard'
    _description = 'Send Shuttle Details Email Wizard'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    email_to = fields.Char(string='Recipient Email', required=True)
    subject = fields.Char(string='Subject', required=True, default='Shuttle Details Notification')
    body = fields.Text(string='Email Body', required=True)

    @api.model
    def default_get(self, fields):
        res = super(ShuttleEmailWizard, self).default_get(fields)
        employee = self.env['hr.employee'].search([('id', '=', self._context.get('active_id'))])
        res.update({
            'employee_id': employee.id,
            'email_to': employee.work_email,
            'body': self._prepare_email_body(employee)
        })
        return res

    def _prepare_email_body(self, employee):
        # Prepare the default email body with shuttle details
        body = f"""
        Dear {employee.name},

        Here are your shuttle details:

        Please be on time and have a safe journey.

        Regards,
        Shuttle Management Team
        """
        return body

    def send_email(self):
        # Send email logic
        template = self.env.ref('shuttle_management.shuttle_email_template')
        template.write({
            'email_to': self.email_to,
            'subject': self.subject,
            'body_html': self.body,
        })
        template.send_mail(self.employee_id.id, force_send=True)
