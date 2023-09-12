# -*- coding: utf-8 -*-
{
    'name': "ams_tdr",

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
    'depends': ['base','ams_base','stock','inputmask_widget'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        'views/templates.xml',
        'report/report_mtr.xml',
        'report/report_maintenance_tracking.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
	'installable': True,
    'application': True,
}