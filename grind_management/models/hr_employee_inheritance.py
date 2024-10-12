from odoo import models, fields, api
import base64
import qrcode
from io import BytesIO
from odoo.exceptions import ValidationError


class EmployeeInheritance(models.Model):
    """THIS INHERITS EMPLOYEE TO ADD GRIND MANAGEMENT FUNCTIONS"""
    _inherit = 'hr.employee'

    grind_password = fields.Char(string="Grind Password", readonly=True)
    currency_id = fields.Many2one('res.currency', string="Currency")
    account_balance = fields.Monetary(string="Account Balance")
    employee_sales = fields.One2many('grind_sales.model','hr_employee_id',string="Hr Employee")

