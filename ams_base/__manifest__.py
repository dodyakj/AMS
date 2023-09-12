# -*- coding: utf-8 -*-
{
    'name': "ams_base",

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
    'depends': ['base','ib_base_pelita','inputmask_widget','pelita_master_data','pelita_operation','product','stock','paiis_corrective','fleet','maintenance','search_table_widget'],

    # always loaded
    'data': [
        'data/location.xml',
        'security/ir.model.access.csv',
        'audit/internal_schedule.xml',
        'audit/internal_car.xml',
        'wizard/wizard_view.xml',
        'views/ata_definition_views.xml',
        'views/base_operation.xml',
        'views/inspection.xml',
        'data/data.xml',
        'views/views.xml',
        'views/service_life.xml',
        'views/component.xml',
        'views/engine.xml',
        'views/auxiliary.xml',
        'views/propeller.xml',
        'views/aircraft.xml',
        'views/daily_utilz.xml',
        'views/master_part_list.xml',
        'views/gse.xml',
        'views/tool.xml',
        'views/hangar.xml',
        'views/manual_change.xml',
        'views/bin.xml',
        'views/config.xml',
        'views/serviceable_history.xml',
        'data/config.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
	'installable': True,
    'application': True,
}