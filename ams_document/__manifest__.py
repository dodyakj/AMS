# -*- coding: utf-8 -*-
{
    'name': "ams_document",

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
    'depends': ['base','ams_base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/mel_extention.xml',
        'views/enginering_order.xml',
        'views/enginering_order_report.xml',
        'views/maintenance_intruction.xml',
        'views/maintenance_intruction_report.xml',
        'views/one_time_inspection.xml',
        'views/one_time_inspection_report.xml',
        'views/technical_information.xml',
        'views/technical_information_report.xml',
        'report/report_maintenance_due.xml',
        'report/maintenance_due.xml',
        # 'report/report_maintenance_tracking.xml',
        # 'report/maintenance_tracking.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        
    ],
	'installable': True,
    'application': True,
}