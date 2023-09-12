# -*- coding: utf-8 -*-
{
    'name': "ams_menu",

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

    'depends': ['base','ams_base','ams_dashboard','ams_camp','ams_codectr','ams_training','ams_airworthy','ams_fml','ams_document','ams_bulletin','pelita_master_data','hr','fleet','sale','project','maintenance','mrp','purchase','ams_security','swr_datepicker','ams_inventory','ams_daily','ams_tdr','ams_order','ams_report','ams_reliability'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/menu.xml',
        'views/disabled_menu.xml',
        'views/templates.xml',
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
    'demo': [
        'demo/demo.xml',
    ],
	'installable': True,
    'application': True,
    'auto_install': True,
}