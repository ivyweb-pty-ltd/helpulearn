# -*- coding: utf-8 -*-
{
    'name': "helpulearn",

    'summary': "Help U Learn Knowledge description",

    'description': """
        This module is part of the helpulearn system. It describes the smallest bit of information that should reasonably 
        be grouped together. Typically what a student can absorb in 5 - 10 minutes. 
    """,

    'author': "IvyWeb (Pty) Ltd",
    'website': "https://www.ivyweb.co.za",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/helpulearn.xml',
        'views/bit.xml',
        'views/unit.xml',
        'views/unit_type.xml',
        'views/review.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}

