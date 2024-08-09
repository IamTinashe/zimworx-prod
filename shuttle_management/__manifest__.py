# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Shuttle Management',
    'version': '24.0.1',
    'author': 'Estain Makaudze',
    'summary': 'Invoices & Payments',
    'sequence': -100,
    'description': """This is a module for shuttle management""",
    'category': 'Accounting/Accounting',
    'website': 'https://zimworx.odoo.com',
    'depends': ['contacts','mail','hr'],
    'data': [
        # security -- data -- views --reports
        'security/ir.model.access.csv',
        'views/main_menus.xml',
        'wizards/onboard_employee_for_shuttle.xml',
        'views/hr_employee_inheritance.xml',
        'views/hr_employee_driver_inheritance.xml',
        'views/shuttles_model.xml',
        'views/shuttle_routes_model.xml',
        'views/weekday_model.xml',
        # 'views/default_views.xml',
        # 'report/default_report.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'auto_install': False,
}