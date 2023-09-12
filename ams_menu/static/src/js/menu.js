odoo.define('new_menu', function (require) {
"use strict";
var UserMenu = require('web.UserMenu');
// Modify behaviour of addons/web/static/src/js/widgets/user_menu.js
UserMenu.include({
    on_menu_new_menu: function () {
        // your new menu action
    }
});
});