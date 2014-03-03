// Menu Show/hide
function expandNav() {
	$('#menu-toggle').addClass('active');
	$('#menu-toggle').attr('onClick', 'collapseNav()');
	$('#menu-popout').show( 'slide', {direction: 'right'} );	
}

function collapseNav() {
	$('#menu-toggle').removeClass('active');
	$('#menu-toggle').attr('onClick', 'expandNav()');
	$('#menu-popout').hide( 'slide', {direction: 'right'} );	
}

$( document ).on( "swipeleft", function( event ) {
	expandNav();
});

$( document ).on( "swiperight", function( event ) {
	collapseNav();
});

$('.admin-sidebar').on("touchmove", false);
