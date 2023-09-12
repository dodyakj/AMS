odoo.define('ams_help.dashboard', function (require) {
"use strict";
var core = require('web.core');
var formats = require('web.formats');
var Model = require('web.Model');
var session = require('web.session');
var ajax = require('web.ajax');
var KanbanView = require('web_kanban.KanbanView');
var KanbanRecord = require('web_kanban.Record');
var ActionManager = require('web.ActionManager');
var QWeb = core.qweb;

var _t = core._t;
var _lt = core._lt;

var HrDashboardView = KanbanView.extend({
    display_name: _lt('Dashboard'),
    icon: 'fa-dashboard text-red',
    searchview_hidden: true,//  To hide the search and filter bar
    events: {
    },
    init: function (parent, dataset, view_id, options) {
        this._super(parent, dataset, view_id, options);
        this.options.creatable = false;
        var uid = dataset.context.uid;
        var manual_data = true;
        var isFirefox = false;
        //Here we can bind any functions to be called before or after render.
        //_.bindAll(this, 'render', 'graph');
        //var _this = this;
        //this.render = _.wrap(this.render, function(render) {
        //    render();
        //    _this.graph();
        //    return _this;
        //});
    },
    fetch_data: function() {
		// Overwrite this function with useful data
		return $.when();
	},
	// Here we are calling a function 'get_employee_info' from model to retrieve enough data
    render: function() {
        var super_render = this._super;
        var self = this;
        var model  = new Model('ams.dashboard').call('get_document').then(function(result){
            self.isFirefox = typeof InstallTrigger !== 'undefined';
            self.manual_data =  result[0]
            return self.fetch_data().then(function(result){
                var ias_manual = QWeb.render('ams_help.dashboard', {
                    widget: self,
                });
                super_render.call(self);
                $(ias_manual).prependTo(self.$el);
                self.graph();
            })
        });
    },
    // Here we are plotting bar,pie chart
    getRandomColor: function () {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++ ) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    },
    // Here we are plotting bar,pie chart
    graph: function() {
        var self = this
        var ctx = this.$el.find('#myChart')
        // Fills the canvas with white background
        Chart.plugins.register({
          beforeDraw: function(chartInstance) {
            var ctx = chartInstance.chart.ctx;
            ctx.fillStyle = "white";
            ctx.fillRect(0, 0, chartInstance.chart.width, chartInstance.chart.height);
          }
        });
        var bg_color_list = []
        for (var i=0;i<=12;i++){
            bg_color_list.push(self.getRandomColor())
        }
        
        //Pie Chart
        
        $('#doc').DataTable( {
            dom: 'Bfrtip',
            buttons: [
                'copy', 'csv', 'excel',
                {
                    extend: 'pdf',
                    footer: 'true',
                    orientation: 'landscape',
                    title:'Employee Details',
                    text: 'PDF',
                    exportOptions: {
                        modifier: {
                            selected: true
                        }
                    }
                },
                {
                    extend: 'print',
                    exportOptions: {
                    columns: ':visible'
                    }
                },
            'colvis'
            ],
            columnDefs: [ {
                targets: -1,
                visible: false
            } ],
            lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
            pageLength: 15,
        } );
    },
    generate_payroll_pdf: function(chart){
        if (chart == 'bar'){
            var canvas = document.querySelector('#myChart');
        }
        else if (chart == 'pie') {
            var canvas = document.querySelector('#attendanceChart');
        }

        //creates image
        var canvasImg = canvas.toDataURL("image/jpeg", 1.0);
        var doc = new jsPDF('landscape');
        doc.setFontSize(20);
        doc.addImage(canvasImg, 'JPEG', 10, 10, 280, 150 );
        doc.save('report.pdf');
    },
})
// View adding to the registry
core.view_registry.add('ias_manual_dashboard', HrDashboardView);
return HrDashboardView
});
