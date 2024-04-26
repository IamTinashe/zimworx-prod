# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Customer Vendor Statement',
    'version': '14.0.1.0.0',
    'category': 'Accounting', 'Contacts' 
    'summary': 'Customer- Vendor Statement',
    'sequence': '10',
    'description': 'Open any customer or vendor form and click on action--> Customer / Vendor Statement',
    "author": "Hyperthink Systems Kenya Limited",
    'website': 'https://hyperthinkkenya.co.ke',
    'depends': [
        'account', 'sign', 'account_accountant', 'account_reports', 'account_followup', 'sale_management', 'purchase',
    ],
    'data': [
        'views/statement.xml',
        'views/mail_send.xml',
        'wizard/customer_vendor_statement_wizard.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'application': False,
}
