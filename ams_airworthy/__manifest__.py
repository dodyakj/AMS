# -*- coding: utf-8 -*-
{
    'name': "ams_airworthy",

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
        'views/templates.xml',
        'views/airworthy.xml',
        'views/service.xml',
        'views/hsi.xml',
        'views/mel.xml',
        'views/ste.xml',
        'views/log.xml',
        'views/aircraft_document.xml',
        'views/aircraft_logbook.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
	'installable': True,
    'application': True,
}