odoo.define('sharpos_data', function(require){
	"use strict";
	var WebClient = require('web.WebClient');
	var utils = require('web.utils');
	WebClient.include({
	init: function(parent) {
	    this.client_options = {};
	    this._super(parent);
	    this.origin = undefined;
	    this._current_state = null;
	    this.menu_dm = new utils.DropMisordered();
	    this.action_mutex = new utils.Mutex();
	    this.set('title_part', {"zopenerp": "Pelita Air Service"});
	}
	});
});


// odoo.define('onview_action', function(require){
// 	"use strict";
// 	var AAc = require('aircraft.acquisition');
// 	AAc.extend({
// 	switch_mode: function(view_type, no_store, view_options){

//         // To get Current Module Name
//         console.log("Module Name" +this.active_view);

//         // some other code

//         // return  this._super(view_type, no_store, view_options);
// 	}
// 	});

// 	AAC.switch_mode();

// });