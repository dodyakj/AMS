# -*- coding: utf-8 -*-
{
    'name': "ams_fml",

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
    'depends': ['base','web','ams_base','pelita_operation','report_xlsx','ams_inventory','stock','product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/verify.xml',
        'views/fml_detail.xml',
        'views/discripencies.xml',
        'report/template_report.xml',
        'report/report.xml',
        'report/report_verify_fml.xml',
    ],
    'qweb':[
        'static/src/xml/custom.xml',
    ],
    'js':'static/src/js/custom.js',
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
	'installable': True,
    'application': True,
}