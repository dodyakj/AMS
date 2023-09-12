setTimeout(function(){
	$(".o_sub_menu_content > .oe_secondary_menu > .oe_secondary_submenu").each(function( index ) {
	  $(this).slideUp(200);
	});

	$(".oe_secondary_menu_section").each(function( index ) {
	  $(this).click(function(){
	  		if($(this).hasClass("gi_active") == false){
		  		$(".gi_active").removeClass("gi_active");
		  		$(".o_sub_menu_content > .oe_secondary_menu > .oe_secondary_submenu").each(function( index ) {
				  $(this).slideUp(200);
	  			  // $(this).find( '.oe_secondary_submenu' ).show();
				});
		  		$(this).next().slideDown(200);
		  		$(this).addClass("gi_active");
	  		};
			$(".oe_secondary_submenu > li > .oe_secondary_submenu").each(function( index ) {
			  $(this).show();
			});
			setTimeout(function(){
			  	$(".oe_secondary_submenu > li > .oe_secondary_submenu").each(function( index ) {
				  $(this).show();
				});
			}, 3000);
	  });
	});
}, 5000);

