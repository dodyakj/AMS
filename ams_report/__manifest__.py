# -*- coding: utf-8 -*-
{
    'name': "ams_report",

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
    'depends': ['base','ams_base','ams_document','ams_bulletin','ams_fml','report_xlsx','report','inputmask_widget','ams_order'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/oil.xml',
        'views/part_removal.xml',
        'views/adc.xml',
        'views/inspection.xml',
        'views/general_tool.xml',
        'views/order.xml',
        'views/calibration.xml',
        'views/on_board.xml',
        'views/manual_changes.xml',
        'views/premature_value.xml',
        'views/report_tool_movement.xml',
        'views/tool.xml',
        'views/component_removal.xml',
        'views/aircraft_status.xml',
        'views/power_assurance_check.xml',
        'views/checklist.xml',
        'views/fleetwide.xml',
        'views/maintenance_planning.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
	'installable': True,
    'application': True,
}