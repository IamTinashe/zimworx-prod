from odoo import fields, models, api

class ApplicantsZimbojobs(models.Model):
    _name = "applicant.zimbojobs"

    name = fields.Char(string="name")