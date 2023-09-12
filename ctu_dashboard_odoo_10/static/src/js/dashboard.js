odoo.define('ctu_dashboard_odoo_10_dashboard_marketing', function (require) {
"use strict";

var Widget = require('web.Widget');
var core = require('web.core');

var MainDashboard = Widget.extend({
    template: 'dashboard_marketing',
    events: {
        'click #btn_project_requisition': 'action',
        'click #btn_rab': 'action',
        'click #btn_nup': 'action',
        'click #btn_help_app': 'action',
    },
    action: function (e) {
        switch (e.currentTarget.id) {
            case 'btn_project_requisition':
                this.do_action('ab_requisition_project.action_request_project_aviation'); 
                break;
            case 'btn_rab':
                this.do_action('ab_sipro.view_project_sales_aviation');
                break;
            case 'btn_nup':
                this.do_action('sale.action_orders');
                break;
            case 'btn_help_app':
                this.do_action('ias_help.action_help_dashboard');
                break;
            default:
                break;
        }
    },
});

core.action_registry.add('ctu_dashboard_odoo_10_dashboard_marketing', MainDashboard);

return MainDashboard;

});

odoo.define('ctu_dashboard_odoo_10_dashboard_ppc', function (require) {
    "use strict";
    
    var Widget = require('web.Widget');
    var core = require('web.core');
    
    var MainDashboard = Widget.extend({
        template: 'dashboard_ppc',
        events: {
            'click #btn_rab': 'action',
            'click #btn_mrl': 'action',
            'click #btn_pjpb': 'action',
            'click #btn_project': 'action',
            'click #btn_tasks': 'action',
            'click #btn_job_order': 'action',
            'click #btn_help_app': 'action',
        },
        action: function (e) {
            switch (e.currentTarget.id) {
                case 'btn_rab':
                    this.do_action('ias_menu.rab_action_menu_aviation');    
                    break;
                case 'btn_mrl':
                    this.do_action('ab_purchase_order.action_purchase_requisition_custom');    
                    break;
                case 'btn_pjpb':
                    this.do_action('ab_purchase_order.action_purchase_requisition_custom1');    
                    break;
                case 'btn_project':
                    this.do_action('forecast.forecast_jo_action');    
                    break;
                case 'btn_tasks':
                    this.do_action('project.action_view_task');    
                    break;
                case 'btn_job_order':
                    this.do_action('ias_jo.job_order_action_window');    
                    break;
                case 'btn_help_app':
                    this.do_action('ias_help.action_help_dashboard');
                    break;
                default:
                    break;
            }
        }
       
    });
    
    core.action_registry.add('ctu_dashboard_odoo_10_dashboard_ppc', MainDashboard);
    
    return MainDashboard;
    
});

odoo.define('ctu_dashboard_odoo_10_dashboard_scm', function (require) {
    "use strict";
    
    var Widget = require('web.Widget');
    var core = require('web.core');
    
    var MainDashboard = Widget.extend({
        template: 'dashboard_scm',
        events: {
            'click #btn_mrl': 'action',
            'click #btn_pjpb': 'action',
            'click #btn_purchase_agreement': 'action',
            'click #btn_purchase_order': 'action',
            'click #btn_work_order': 'action',
            'click #btn_spk': 'action',
            'click #btn_inventory_movement': 'action',
            'click #btn_help_app': 'action',
        },
        action: function (e) {
            switch (e.currentTarget.id) {
                case 'btn_mrl':
                    this.do_action('ab_purchase_order.action_purchase_requisition_custom');    
                    break;
                case 'btn_pjpb':
                    this.do_action('ab_purchase_order.action_purchase_requisition_custom1');    
                    break;
                case 'btn_purchase_agreement':
                    this.do_action('purchase_requisition.action_purchase_requisition');    
                    break;
                case 'btn_purchase_order':
                    this.do_action('ias_menu.purchase_form_action1');    
                    break;
                case 'btn_work_order':
                    this.do_action('ab_purchase_order.action_purchase_order_wo');    
                    break;
                case 'btn_spk':
                    this.do_action('ab_purchase_order.action_purchase_order_spk');    
                    break;
                case 'btn_inventory_movement':
                    this.do_action('stock.stock_picking_type_action');    
                    break;
                case 'btn_help_app':
                    this.do_action('ias_help.action_help_dashboard');
                    break;
                default:
                    break;
            }
        }
       
    });
    
    core.action_registry.add('ctu_dashboard_odoo_10_dashboard_scm', MainDashboard);
    
    return MainDashboard;
    
});

odoo.define('ctu_dashboard_odoo_10_dashboard_toolroom', function (require) {
    "use strict";
    
    var Widget = require('web.Widget');
    var core = require('web.core');
    
    var MainDashboard = Widget.extend({
        template: 'dashboard_toolroom',
        events: {
            'click #btn_tools': 'action',
            'click #btn_tools_forecast': 'action',
            'click #btn_tools_borrowing': 'action',
            'click #btn_tools_returned': 'action',
            'click #btn_tools_quarantine': 'action',
            'click #btn_tools_calibration': 'action',
            'click #btn_tools_movement': 'action',
            'click #btn_help_app': 'action',
        },
        action: function (e) {
            switch (e.currentTarget.id) {
                case 'btn_tools':
                    this.do_action('aircraft.tools_tool_action');    
                    break;
                case 'btn_tools_forecast':
                    this.do_action('ab_sipro.view_usulan_anggaran_tools_action');    
                    break;
                case 'btn_tools_borrowing':
                    this.do_action('aircraft.tools_movement_action');    
                    break;
                case 'btn_tools_returned':
                    this.do_action('aircraft.tools_return_action');    
                    break;
                case 'btn_tools_quarantine':
                    this.do_action('aircraft.tools_on_quarantine_action');    
                    break;
                case 'btn_tools_calibration':
                    this.do_action('aircraft.tools_on_calibration_action');    
                    break;
                case 'btn_tools_movement':
                    this.do_action('stock.stock_picking_type_action');    
                    break;
                case 'btn_help_app':
                    this.do_action('ias_help.action_help_dashboard');
                    break;
                default:
                    break;
            }
        }
       
    });
    
    core.action_registry.add('ctu_dashboard_odoo_10_dashboard_toolroom', MainDashboard);
    
    return MainDashboard;
    
});

odoo.define('ctu_dashboard_odoo_10_dashboard_quality', function (require) {
    "use strict";
    
    var Widget = require('web.Widget');
    var core = require('web.core');
    
    var MainDashboard = Widget.extend({
        template: 'dashboard_quality',
        events: {
            'click #btn_vendor_approved': 'action',
            'click #btn_mddr': 'action',
            'click #btn_projects': 'action',
            'click #btn_rts': 'action',
            'click #btn_inventory_movement': 'action',
            'click #btn_help_app': 'action',
        },
        action: function (e) {
            switch (e.currentTarget.id) {
                case 'btn_vendor_approved':
                    this.do_action('ab_vendor_approve.action_vendor_approve3');    
                    break;
                case 'btn_mddr':
                    this.do_action('ab_sipro.action_view_mddr');    
                    break;
                case 'btn_projects':
                    this.do_action('forecast.forecast_jo_action_quality');    
                    break;
                case 'btn_rts':
                    this.do_action('ias_quality.ias_rts_action');    
                    break;
                case 'btn_inventory_movement':
                    this.do_action('stock.stock_picking_type_action');    
                    break;
                case 'btn_help_app':
                    this.do_action('ias_help.action_help_dashboard');
                    break;
                default:
                    break;
            }
        }
       
    });
    
    core.action_registry.add('ctu_dashboard_odoo_10_dashboard_quality', MainDashboard);
    
    return MainDashboard;
    
});

odoo.define('ctu_dashboard_odoo_10_dashboard_hr', function (require) {
    "use strict";
    
    var Widget = require('web.Widget');
    var core = require('web.core');
    
    var MainDashboard = Widget.extend({
        template: 'dashboard_hr',
        events: {
            'click #btn_employees': 'action',
            'click #btn_manpower_request': 'action',
            'click #btn_help_app': 'action',
        },
        action: function (e) {
            switch (e.currentTarget.id) {
                case 'btn_employees':
                    this.do_action('hr.open_view_employee_list_my');    
                    break;
                case 'btn_manpower_request':
                    this.do_action('ab_hr_custom.manpower_request_action');    
                    break;
                case 'btn_help_app':
                    this.do_action('ias_help.action_help_dashboard');
                    break;
                default:
                    break;
            }
        }
       
    });
    
    core.action_registry.add('ctu_dashboard_odoo_10_dashboard_hr', MainDashboard);
    
    return MainDashboard;
    
});