
openerp.dashboard = function (instance, local) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;
    var model_obj = new instance.web.Model('ir.model.data');
    var view_wo = model_obj.call('get_object_reference',["ams.work.order", "ams_order.work_order_ams_form"]);
    var view_mwo = model_obj.call('get_object_reference',["ams.mwo", "ams_order.mwork_order_ams_form"]);

   
};