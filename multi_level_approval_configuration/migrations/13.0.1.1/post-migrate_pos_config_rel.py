# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright Domiup (<http://domiup.com>).
#
##############################################################################

def migrate(cr, version):
    if not version:
        return
    cr.execute("""
        ALTER TABLE multi_approval_type
        DROP CONSTRAINT IF EXISTS multi_approval_type_check_model_unique;
    """)
