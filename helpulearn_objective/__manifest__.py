# -*- coding: utf-8 -*-
{
    'name': "HelpULearn Objective",

    'summary': """
        Module that allows you to set learning objectives
    """,

    'description': """
        This module is part of a larger Learning Management System. This module specifically allows you to set learning
        objective. 
        
        What makes this different from normal learning objectives as that objectives here are related to other objectivs
        creating a knowledge tree. The learning of the objective can then be related to instruction, assessment and grading
        resources.        
    """,

    'author': "IvyWeb (Pty) Ltd",
    'website': "http://www.ivyweb.co.za",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Gamification',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'helpulearn'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/taxonomy.xml',
#        'views/templates.xml',
        'data/helpulearn.cognitive.dimension.csv',
        'data/helpulearn.cognitive.subtype.csv',
        'data/helpulearn.knowledge.dimension.csv',
        'data/helpulearn.knowledge.subtype.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
