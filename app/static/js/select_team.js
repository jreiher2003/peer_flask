$(document).ready(function() {
  $("#select_season_type, #select_season_type1").change(function() {
    if ($(this).val() != '') {
      window.location.href=$(this).val()
    }
  });
});
