from odoo import fields, models, api


class drivers_schedule(models.Model):
    """THIS MODEL IS FOR ENTERING ALL SHUTTLE AND MANAGING THEIR DRIVERS, SHUTTLES ETC"""
    _name = 'drivers_schedule.model'
    _description = 'Shuttle Record'
    _inherit = ["mail.thread", "mail.activity.mixin"]