from odoo import api, fields, models


class AccountReport(models.AbstractModel):
    _inherit = 'account.report'

    def get_pdf(self, options, minimal_layout=True):
        account_type = options.get('filter_account_type')
        if account_type in ['receivable', 'payable']:
            minimal_layout = False
        return super(AccountReport, self).get_pdf(options, minimal_layout)

    # @api.model
    # def _get_templates(self):
    #     # OVERRIDE
    #     templates = super(ReportAccountAgedPartner, self)._get_templates()
    #     templates['main_template'] = 'zimworkx_reports.main_template_aged'
    #     return templates
