// prevents tabs in stats from jumping down
$('.nav-tabs li a').click( function(e) {
history.pushState( null, null, $(this).attr('href') );
});