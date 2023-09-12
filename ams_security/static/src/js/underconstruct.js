


openerp.ams_security = function(instance, local) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;
    var model_obj = new instance.web.Model('ir.model.data');
    // var view_id = model_obj.call('get_object_reference',["account.invoice", "account.action_invoice_tree1"]);

    local.UnderConstruct = instance.Widget.extend({
       template: "UnderConstruct",
        start: function() {
            var deadline = new Date("des 20, 2018 15:37:25").getTime();
             
            var x = setInterval(function() {
             
            var now = new Date().getTime();
            var t = deadline - now;
            var days = Math.floor(t / (1000 * 60 * 60 * 24));
            var hours = Math.floor((t%(1000 * 60 * 60 * 24))/(1000 * 60 * 60));
            var minutes = Math.floor((t % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((t % (1000 * 60)) / 1000);
            if(document.getElementById("day") != null){
                // var idPost=document.getElementById("status").innerHTML;
                document.getElementById("day").innerHTML =days ;
                document.getElementById("hour").innerHTML =hours;
                document.getElementById("minute").innerHTML = minutes; 
                document.getElementById("second").innerHTML =seconds; 
            }
            if (t < 0) {
                    clearInterval(x);
                    // document.getElementById("demo").innerHTML = "TIME UP";
                    // document.getElementById("day").innerHTML ='0';
                    // document.getElementById("hour").innerHTML ='0';
                    // document.getElementById("minute").innerHTML ='0' ; 
                    // document.getElementById("second").innerHTML = '0'; 
                }
            }, 1000);
            var self = this;
        },
    });

    instance.web.client_actions.add(
        'under.construct', 'instance.ams_security.UnderConstruct');
}

