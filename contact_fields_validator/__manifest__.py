{
    'name': 'Contact Fields Validator',
    'version': '1.0',
    'summary': 'Validates essential fields in contact records',
    'description': """
        This module adds functionality to validate essential contact fields in partner records, 
        ensuring that critical information is available before processing invoices. 
        It provides a mixin that can be reused across different models for consistent validation.
    """,
    'category': 'Customization',
    'author': 'ZimWorX',
    'website': 'https://zimworx.com',
    'depends': ['account', 'contacts', 'sale'],  # Added 'contacts' dependency for partner models
    'data': [
        # 'security/ir.model.access.csv',  # Uncomment if you need custom security rules
        # 'views/partner_views.xml',        # Uncomment if you are creating custom views for partner records
    ],
    'installable': True,
    'auto_install': False,
    'application': False,  # Set to True if this is a standalone application module
    'license': 'LGPL-3',    # Specify the license type if applicable
    'images': ['static/contact_field_validator.webp'],  # Optional: path to a banner image for the module
}
