$(document).ready(function() {
    $("#goto").change(function() {
        if ($(this).val() != '') {
            console.log($(this).val())
            window.location.href=$(this).val()
        }
    });
});