from odoo import fields, models, api

class ApplicantsZimbojobs(models.Model):
    _name = "applicant.zimboobs"

    name = fields.Char(string="name")