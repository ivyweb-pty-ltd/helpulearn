# -*- coding: utf-8 -*-
{
    'name': "grading",

    'summary': """
        Attach grading - measurement of activity value to learning
        """,

    'description': """
        Grading is how we measure the effectiveness of an activity.
        
        It basically measures when an activity was executed, what the retention rate and what
        is the stability
    """,

    'author': "Jacobus Erasmus",
    'website': "http://www.helpulearn.co.za",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'objective'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
