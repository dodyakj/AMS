# -*- coding: utf-8 -*-
{
    'name': "ams_dashboard",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "PT Cendana Teknika Utama",
    'website': "http://www.cendana2000.biz",
    'category': 'PT Cendana',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','ams_base','ams_order','ams_fml','ams_bulletin'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/dashboard_templates.xml',
        'views/dashboard_views.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
	'installable': True,
    'application': True,
}