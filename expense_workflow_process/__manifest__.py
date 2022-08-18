

{
    'name': 'Expense Process Changes',
    'category': 'HR',
    'summary': 'Expense Process Changes',
    'description': """
        Once you create the Expenses, you will attach the receipt and post the Journal entries directly. In between what all steps are there has to be omitted
    """,
    'author': 'Hyperthink Systems Kenya',
    'version': '14.0',
    'license': 'AGPL-3',
    'depends': ['hr_expense', 'hr_expense_extract'],
    'data': [
        'views/hr_expense_view.xml',
    ],
    'application': False,
    'installable': True,
}
