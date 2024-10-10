from odoo import models, fields, api

class ShuttleEmailWizard(models.TransientModel):
    _name = 'shuttle_email.wizard'
    _description = 'Send Shuttle Details Email Wizard'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    email_to = fields.Char(string='Recipient Email', required=True)
    subject = fields.Char(string='Subject', required=True, default='Shuttle Details Notification and Request for QR Code Collection')
    body = fields.Text(string='Email Body', required=True)
    user_id = fields.Many2one('res.users', string='Current User', default=lambda self: self.env.user)

    @api.model
    def default_get(self, fields):
        res = super(ShuttleEmailWizard, self).default_get(fields)
        employee = self.env['hr.employee'].search([('id', '=', self._context.get('active_id'))])
        employee_schedules_id = self.env['employee_schedules.model'].search([('employee_id', '=', employee.id)])
        #get the shuttle the person is using

        res.update({
            'employee_id': employee.id,
            'email_to': employee.work_email,
            'body': self._prepare_email_body(employee_schedules_id)
        })
        return res

    def _prepare_email_body(self, employee_schedules_id):
        # If multiple schedules are present, iterate and create a list of details for each
        if len(employee_schedules_id) > 1:
            shuttle_details = ""
            for schedule in employee_schedules_id:
                days = ', '.join(weekday.name for weekday in schedule.weekday_id)
                shuttle_details += f"""
                  - Shuttle Driver: {schedule.shuttle_id.driver_id.name}   
                  - Shuttle Name: {schedule.shuttle_id.name}  
                  - Days: {days} 
                  - Departure Time: {schedule.display_departure_time} 
                  ---------------------------------------------
                """
            body = f"""
            Dear {employee_schedules_id[0].employee_id.name},

            We are pleased to inform you that your shuttle service is scheduled. 
            Please collect your QR Code, which will be required for onboarding, from Desk 12 on the 13th Floor.
            
            The shuttles you will be using are as follows:
                    {shuttle_details}

            We kindly request you to be always punctual to ensure smooth onboarding process.

            Warm Regards,
            
            Shuttle Management Team
            """
        else:
            # If there's only one schedule, use the one format
            days = ', '.join(weekday.name for weekday in employee_schedules_id.weekday_id)
            body = f"""
            Dear {employee_schedules_id.employee_id.name},

            We are pleased to inform you that your shuttle service is scheduled. 
            Please collect your QR Code, which will be required for onboarding, from Desk 12 on the 13th Floor

            Below are the details of your assigned shuttle:
                    - Driver: {employee_schedules_id.shuttle_id.driver_id.name}
                    - Shuttle Name: {employee_schedules_id.shuttle_id.name}
                    - Scheduled Days: {days}
                    - Departure Time: {employee_schedules_id.display_departure_time}

            We kindly request you to be punctual to ensure a smooth onboarding process. We wish you a safe and pleasant journey!

            Warm Regards,
            
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
        template.send_mail(self.id, force_send=True)
        self.employee_id.write({'onboarding_stage':'qr_code_printed'})

