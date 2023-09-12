odoo.define('web.leftigi', function (require) {
"use strict";


var core = require('web.core');
var formats = require('web.formats');
var time = require('web.time');
var Widget = require('web.Widget');

var _t = core._t;

var leftigi = Widget.extend({
    template: "leftigi",
    start: function() {
        this.hide();
        console.log('mkkkkk');
    },
    
});
// core.form_tag_registry


return {
    leftigi: leftigi,
};
});