openerp.ams_dashboard = function (instance, local) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;
    var model_obj = new instance.web.Model('ir.model.data')
    var view_wo = false 
    var view_mwo = false 
    model_obj.call('get_object_reference',["ams.work.order", "ams_order.work_order_ams_form"]).then( function(result){
        view_wo = result[1];
    });
    model_obj.call('get_object_reference',["ams.mwo", "ams_order.mwork_order_ams_form"]).then( function(result){
        view_mwo = result[1];
    });


    local.Dashboard = instance.Widget.extend({
        start: function () {
            var self = this;
            const aircraft_acquisition = new instance.web.Model(
                "aircraft.acquisition"
            );

            aircraft_acquisition
                .call("for_aircraft_dashboard", {
                    context: new instance.web.CompoundContext()
                })
                .then(function (results) {
                    var aircrafts = new local.AircraftsWidget(self, results.result_arr);
                    aircrafts.appendTo(self.$el);
                    console.log(results);
                });

            return this._super();
        }
    });

    local.AircraftsWidget = instance.Widget.extend({
        template: "AircraftsWidget",
        init: function (parent, aircrafts) {
            this._super(parent);
            this.aircrafts = aircrafts;
        },
        start: function () {
            for (let index = 0; index < this.aircrafts.length; index++) {
                const aircraft = this.aircrafts[index];
                const img_modal = this.$("#img_aircraft" + aircraft.id);
                const button = this.$("#modal_btn" + aircraft.id);
                const modal = this.$("#modal_aircraft" + aircraft.id);
                const close = this.$("#close_aircraft" + aircraft.id);

                button.click(function () {
                    modal.css({
                        display: "block",
                        position: "fixed"
                    });
                });

                close.click(function () {
                    modal.css({
                        display: "none"
                    });
                });
            }
            return this._super();
        }
    });

    local.MDRWdiget = instance.Widget.extend({
        template: "MDRWdiget",
        init: function (parent) {
            this._super(parent);
        },
        start: function () {
            const self = this;
            // const mdr = new instance.web.Model('ams.component.part')
            const mdr = new instance.web.Model("maintenance.due.report");
            // mdr.query(["id", "fleet_id", "hour_limit_id"])
            mdr
                .query([
                    "type",
                    "date",
                    "id",
                    "fleet_id",
                    "service_id",
                    "engine_id",
                    "auxiliary_id",
                    "propeller_id",
                    "include_attach",
                    "show_nearly",
                    "orderby",
                    "filter_ata",
                    "fill_component",
                    "fill_bulletin",
                    "fill_inspection",
                    "hour_limit_id",
                    "cycle_limit_id",
                    "rin_limit_id",
                    "calendar_limit_id",
                    "warning_hours",
                    "warning_cycles",
                    "warning_rins",
                    "warning_calendars",
                    "states",
                    "create_by",
                    "checked_by",
                    "approved_by",
                    "qc_by"
                ])
                .all()
                .then(function (results) {});

            mdr
                .call("for_mdr_dashboard", {
                    context: new instance.web.CompoundContext()
                })
                .then(function (result) {
                    const item = new local.MDRItem(self, result.parts);
                    item.appendTo(self.$("tbody"));

                    self.$("table").DataTable({
                        responsive: true,
                        aLengthMenu: [
                            [10, 25, 50, 100, 200, -1],
                            [10, 25, 50, 100, 200, "All"]
                        ],
                        iDisplayLength: 10
                    });
                });
        }
    });

    local.MDRItem = instance.Widget.extend({
        template: "MDRItem",
         events: {
            'click .view_wo': 'select_wo',
            'click .view_mwo': 'select_mwo',
        },
        select_wo: function (event) {
            var fleet = event.currentTarget.attributes[3].nodeValue;
            var service = event.currentTarget.attributes[2].nodeValue;
            // var service = event.currentTarget.attributes[3].nodeValue;
            console.log(service)
            console.log(event.currentTarget)
            console.log(event.currentTarget.attributes)
            var note =  " - Perlakuan : "+ "............."  +" <br/>- After finish, return original sign WO to Enineering or followed by email to <u>engineering@pelita-air.com</u> <br/>- Fill Material Required for any new material required in this inspection <br/>- (*) Refer To Maintenance Program <br/>";
            this.do_action({
                name: 'Work Orders',
                type: 'ir.actions.act_window',
                res_model: 'ams.work.order',
                // res_id: 1,
                // domain: [['states', '=', 'confrimed']],
                views: [[view_wo, "form"]],
                target: 'new',
                context: {'default_ac': parseInt(fleet), 'default_note': note, 'servicelife_id' : parseInt(service)},
                view_type : 'form',
                view_mode : 'form'
            });
        },
        select_mwo: function (event) {
            var fleet = event.currentTarget.attributes[2].nodeValue;
            // var service = event.currentTarget.attributes[3].nodeValue;
            this.do_action({
                name: 'Maintenance Work Orders',
                type: 'ir.actions.act_window',
                res_model: 'ams.mwo',
                // res_id: 1,
                // domain: [['states', '=', 'confrimed']],
                views: [[view_mwo, "form"]],
                target: 'new',
                context: {'default_ac': parseInt(fleet)},
                view_type : 'form',
                view_mode : 'form'
            });
        },
        init: function (parent, mdrs) {
            this._super(parent);
            var unique_part_number = [];
            for (
                let index = 0; index < this.getUnique(mdrs, "part_number").length; index++
            ) {
                unique_part_number.push(
                    this.getUnique(mdrs, "part_number")[index].part_number
                );
            }

            this.mdrs = mdrs;
            this.total = mdrs.length;
        },
        getUnique: function (arr, comp) {
            const unique = arr
                .map(e => e[comp])
                .map((e, i, final) => final.indexOf(e) === i && i)
                .filter(e => arr[e])
                .map(e => arr[e]);

            return unique;
        }
    });

    local.Chart = instance.Widget.extend({
        init: function (parent) {
            this._super(parent);

        },
    });

    instance.web.client_actions.add(
        "aircraft.acquisition.dashboard",
        "instance.ams_dashboard.Dashboard"
    );
    instance.web.client_actions.add(
        "mdr.dashboard",
        "instance.ams_dashboard.MDRWdiget"
    );
    instance.web.client_actions.add(
        "chart.dashboard",
        "instance.ams_dashboard.Chart"
    );
};