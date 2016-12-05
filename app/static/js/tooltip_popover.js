$(document).ready(function(){
    $("[data-toggle=popover]").popover();
    $('a#b_game_key').on('click', function(e) {e.preventDefault(); return true;});
    $("#createBCB").tooltip();
});