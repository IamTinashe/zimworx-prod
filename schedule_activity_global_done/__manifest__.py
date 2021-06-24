# -*- coding: utf-8 -*-
# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

{
    'name': 'Schedule Activity with Done/Deleted Activities History',
    'version': '4.1.1',
    'price': 49.0,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'summary': """Schedule Activity with Done/Deleted Activities History Record""",
    'description': """
Schedule Activity Management Extension Done
Schedule Activity Management
Schedule Activity
employee Schedule Activity
user Schedule Activity
Activity
odoo Schedule Activity
show Schedule Activity
Odoo Schedule Activity with Done/Deleted Activities History
Odoo Schedule Activity with Done/Deleted Activities History Record

    """,
    'author': 'Probuse Consulting Service Pvt. Ltd.',
    'website': 'http://www.probuse.com',
    'support': 'contact@probuse.com',
    'images': ['static/description/image1.jpg'],
    'live_test_url' : 'https://youtu.be/KGztOX6r2WA',
    'category': 'Discuss',
    'depends': [
                'mail','schedule_activity_global',
                ],
    'data':[
        'security/ir.model.access.csv',
        'security/scheduled_activity_security.xml',
        'views/schedule_activity_history_view.xml',
    ],
    'installable' : True,
    'application' : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
