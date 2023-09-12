# -*- coding: utf-8 -*-
{
    'name': "ams_inventory",

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
    'depends': ['base','product','stock','ams_base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/ppe.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/inventory.xml',
        'views/inventory_receive.xml',
        'views/inventory_request.xml',
        'report/report_ri.xml',
        'report/report_ppe.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
	'installable': True,
    'application': True,
}