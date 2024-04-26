from odoo import fields, models, api


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        self.ensure_one()
        res = super(PurchaseOrderInherit, self).button_confirm()
        template = self.env.ref("purchase.email_template_edi_purchase_done")
        template.send_mail(self.id, True)
        return res
