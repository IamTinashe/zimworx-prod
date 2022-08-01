
from odoo import api, fields, models, tools, _


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    def write(self, vals):
        if vals.get('message_main_attachment_id'):
            sheet = self._create_sheet_from_expenses()
            sheet.action_submit_sheet()
            sheet.approve_expense_sheets()
        return super(HrExpense, self).write(vals)
