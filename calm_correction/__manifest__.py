# -*- coding: utf-8 -*-
{
    'name': "calm_correction",

    'summary': """
        This modul made by
        Ciberian team""",

    'description': """
        Custom module
    """,

    'author': "PT Cendana Teknika Utama",
    'website': "http://www.cendana2000.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','ib_base_pelita','pelita_master_data','ams_base'],

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