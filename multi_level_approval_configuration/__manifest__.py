# -*- coding: utf-8 -*-
{
    'name': 'Odoo Approval All in One',
    'version': '13.0.1.1',
    'category': 'Approvals',
    'description': """
    Setup the approval flow for all the models: Sale Order, Purchase Order, MRP Order,..
    Centralize all the approval requests in one place which help the manager reviews easily
    """,
    'summary': '''
    Setup the approval flow for all the models: Sale Order, Purchase Order, MRP Order,..
    Centralize all the approval requests in one place which help the manager reviews easily
    ''',
    'live_test_url': 'https://demo13.domiup.com',
    'author': 'Domiup',
    'price': 40,
    'currency': 'EUR',
    'license': 'OPL-1',
    'support': 'domiup.contact@gmail.com',
    'website': 'https://apps.domiup.com/slides/odoo-approval-all-in-one-1',
    'depends': [
        'multi_level_approval',
        'multi_level_approval_hr'
    ],
    'data': [
        # Security
        'security/security.xml',

        # Views
        'views/multi_approval_type_views.xml',
        'views/multi_approval_views.xml',

        # Add actions after all views.

        # Add menu after actions.

        # Wizards
        'wizard/request_approval_views.xml',
        'wizard/rework_approval_views.xml',
    ],
    'images': ['static/description/banner.gif'],
    'installable': True,
    'active': False,
    'application': True,
}
