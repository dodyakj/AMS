# -*- coding: utf-8 -*-
{
    'name': "ams_bulletin",

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
    'depends': ['base','ib_base_pelita','ams_base','ams_document'],

    # always loaded
    'data': [
        'data/bulletin_data.xml',
        'views/bulletin.xml',
        'views/alteration.xml',
        'report/report_complied.xml',
        'report/report_fbr.xml',
        'report/report_alteration.xml',
        'report/report.xml',
        'security/ir.model.access.csv',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
	'installable': True,
    'application': True,
}