from odoo.addons.iap.tools import iap_tools
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError

import logging
import time

_logger = logging.getLogger(__name__)

CLIENT_OCR_VERSION = 130

# list of result id that can be sent by iap-extract
SUCCESS = 0
NOT_READY = 1
ERROR_INTERNAL = 2
ERROR_NOT_ENOUGH_CREDIT = 3
ERROR_DOCUMENT_NOT_FOUND = 4
ERROR_NO_DOCUMENT_NAME = 5
ERROR_UNSUPPORTED_IMAGE_FORMAT = 6
ERROR_FILE_NAMES_NOT_MATCHING = 7
ERROR_NO_CONNECTION = 8
ERROR_SERVER_IN_MAINTENANCE = 9

ERROR_MESSAGES = {
    ERROR_INTERNAL: _("An error occurred"),
    ERROR_DOCUMENT_NOT_FOUND: _("The document could not be found"),
    ERROR_NO_DOCUMENT_NAME: _("No document name provided"),
    ERROR_UNSUPPORTED_IMAGE_FORMAT: _("Unsupported image format"),
    ERROR_FILE_NAMES_NOT_MATCHING: _("You must send the same quantity of documents and file names"),
    ERROR_NO_CONNECTION: _("Server not available. Please retry later"),
    ERROR_SERVER_IN_MAINTENANCE: _("Server is currently under maintenance. Please retry later"),
}


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    product_id = fields.Many2one('product.product', string='Product', readonly=False, tracking=True, states={'draft': [('readonly', False)], 'reported': [('readonly', False)], 'refused': [('readonly', False)]}, domain="[('can_be_expensed', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]", ondelete='restrict')
    unit_amount = fields.Float("Unit Price", compute='_compute_from_product_id_company_id', store=True, required=True,
                               copy=True,
                               states={'draft': [('readonly', False)], 'approved': [('readonly', False)],
                                       'reported': [('readonly', False)], 'refused': [('readonly', False)]},
                               digits='Product Price')
    quantity = fields.Float(required=True, readonly=False,
                            states={'draft': [('readonly', False)], 'approved': [('readonly', False)],
                                    'reported': [('readonly', False)], 'refused': [('readonly', False)]},
                            digits='Product Unit of Measure', default=1)

    # def write(self, vals):
    #     if vals.get('message_main_attachment_id'):
    #         self.check_status()
    #         sheet = self._create_sheet_from_expenses()
    #         sheet.action_submit_sheet()
    #         sheet.approve_expense_sheets()
    #     return super(HrExpense, self).write(vals)

    def action_submit_expenses(self):
        sheet = self._create_sheet_from_expenses()
        sheet.action_submit_sheet()
        sheet.approve_expense_sheets()
        return {
            'name': _('Expense Report'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hr.expense.sheet',
            'target': 'current',
            'res_id': sheet.id,
        }