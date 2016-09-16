$('#bet_tabs').on('click', 'a[data-toggle="tab"]', function(e) {
      e.preventDefault();

      var $link = $(this);

      if (!$link.parent().hasClass('active')) {

        //remove active class from other tab-panes
        $('.tab-content:not(.' + $link.attr('href').replace('#','') + ') .tab-pane').removeClass('active');

        // click first submenu tab for active section
        $('a[href="' + $link.attr('href') + '_all"][data-toggle="tab"]').click();

        // activate tab-pane for active section
        $('.tab-content.' + $link.attr('href').replace('#','') + ' .tab-pane:first').addClass('active');
      }

});

$(document).ready(function(){
    var $ptext = $("#ptext");
    var homeTeam = $("#home_team").val();
    var awayTeam = $("#away_team").val();
    var overUnder = $("#over_under").val();
    var homePS = $("#home_ps").val();
    var awayPS = $("#away_ps").val();
    var homeML = $("#home_ml").val();
    var awayML = $("#away_ml").val();
    var amount = $("#amount").val();
    $("#form-container").click(function() {
       console.log(homeTeam);
       console.log(awayTeam);
       console.log(overUnder);
       console.log(homePS);
       console.log(awayPS);
       console.log(homeML);
       console.log(awayML);
       console.log(amount);
    
    });
});





