$('#bet_tabs').on('click', 'a[data-toggle="tab"]', function(e) {
      e.preventDefault();
      var $link = $(this);
      if (!$link.parent().hasClass('active')) {
        // console.log($link);
        //remove active class from other tab-panes
        $('.tab-content:not(.' + $link.attr('href').replace('#','') + ') .tab-pane').removeClass('active');
        // console.log($('.tab-content:not(.' + $link.attr('href').replace('#','') + ') .tab-pane').removeClass('active'));
        // click first submenu tab for active section
        $('a[href="' + $link.attr('href') + '_all"][data-toggle="tab"]').click();
        // console.log($('a[href="' + $link.attr('href') + '_all"][data-toggle="tab"]'));
        // activate tab-pane for active section
        $('.tab-content.' + $link.attr('href').replace('#','') + ' .tab-pane:first').addClass('active');
        // console.log($('.tab-content.' + $link.attr('href').replace('#','') + ' .tab-pane:first').addClass('active'));
      }
});

$(document).ready(function(){
    $("#form-container").submit(function() {
    var $ptext = $("#ptext");

    var gameKey = $("form#form-container").find("input#game_key").val();
    console.log(gameKey);
    // var values = $(this).serialize();
    var overUnder = $("div#totals.tab-pane.active").find("input#over_under").val();
    console.log(overUnder);

    var homeTeam = $("div#home.tab-pane.active").find("input#home_team").val();
    console.log(homeTeam);
    var homePS = $("div#home_spread1.tab-pane.active").find("input#home_ps").val();
    console.log(homePS);
    var homeML = $("div#home_ml.tab-pane.active").find("input#home_ml").val();
    console.log(homeML);
    
    var awayTeam = $("div#away.tab-pane.active").find("input#away_team").val();
    console.log(awayTeam);
    var awayPS = $("div#away_spread1.tab-pane.active").find("input#away_ps").val();
    console.log(awayPS);
    var awayML = $("div#away_ml.tab-pane.active").find("input#away_ml").val();
    console.log(awayML);
    var amount = $("#amount").val();
    console.log(amount);
    
    });
});





