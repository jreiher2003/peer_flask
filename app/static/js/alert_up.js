// slides alerts back up after 4 seconds.
$(".alert").delay(10000).slideUp(400, function() {
    $(this).alert('close');
});