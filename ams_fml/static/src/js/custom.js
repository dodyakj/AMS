// $(document).ready(function(){
//  $(".o_form_button_cancel").hide();
// })

openerp.ams_fml = function (instance, loca){
    var QWeb = instance.web.qweb;
    _t = instance.web._t,
    _lt = instance.web._lt;
    var self = this;

    instance.web.FormView.include({
         
        init : function() {
        	this._super.apply(this, arguments);
        },
        start : function(){
        	this._super();
            
        	// $('.fml-discard').attr({
        	// 	'href': "/web#menu_id=676&amp;action=925",
        	// 	'data-menu': "676",
        	// 	'data-action-id': "925",
        	// });

 			var fml = new instance.web.Model('ams_fml.log');
 			fml.call('get_menuId', ['Add FML'])
 			   .then(function(result){
 			   		console.log(result);
 			   		$('.fml-discard').attr({
		        		'href': "/web#menu_id="+result.menu_id+"&action="+result.actions,
		        		'data-menu': result.menu_id,
		        		'data-action-id': result.actions,
		        	});
 			   });
		},
 
 
    });


	// openerp.web.FormView.include({
	// 	init: function(){
	// 		this._super.apply(this, arguments);
	// 		console.log("SUKKKKKKKKKKKKKKKKKKKKKSES");
	// 	}
	//     // load_list: function(data) {
	//     //     this._super(data);
	//     //     // if (this.$buttons) {
	//     //     //     this.$buttons.find('.o_form_button_cancel').off().click(this.proxy('do_the_job')) ;
	//     //     //     console.log('Save & Close button method call...');
	//     //     // }
	//     // },
	//      do_the_job: function () {
	//         this.do_action({
	//             type: "ir.actions.act_window",
	//             name: "Flight Maintenance Log",
	//             res_model: "wizard.fml",
	//             views: [[false,'form']],
	//             target: 'new',
	//             view_type : 'form',
	//             view_mode : 'form',
	//             flags: {'form': {'action_buttons': true, 'options': {'mode': 'edit'}}}
	//         });
	//         return {
	//                 'type': 'ir.actions.client',
	//                 'tag': 'reload',
	//         }
	// 	}
	// });
}	