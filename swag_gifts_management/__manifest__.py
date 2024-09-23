# -*- coding: utf-8 -*-
{
    'name': "Swag Gifts Management",
    'summary': """This is an module addon menu into CRM which manages Sending of Swag to Success Client""",
    'author': "Estain Makaudze",
    'website': "https://zimworx.odoo.com/",
    'version': '16.24.0.1',
    'depends': ['base', 'crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/client_swag_gifts_model.xml',
    ],
    'license': 'LGPL-3',
    'auto_install': False,
}
