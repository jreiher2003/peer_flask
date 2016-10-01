$(document).ready(function() {
    $("#goto_team").change(function() {
        if ($(this).val() != '') {
            console.log($(this).val())
            window.location.href=$(this).val()
        }
    });
    $("#goto_season").change(function() {
        if ($(this).val() != '') {
            console.log($(this).val())
            window.location.href=$(this).val()
        }
    });
});