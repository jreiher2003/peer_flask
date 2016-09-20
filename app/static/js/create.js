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
    $("#form-container").submit(function(e) {
    e.preventDefault();

    var gameKey = $("form#form-container").find("input#game_key").val();
    if (gameKey) {
      console.log(gameKey);
    } else {
      gameKey = ""
      console.log(gameKey)
    }
    // var values = $(this).serialize();
    var overUnder = $("div#totals.tab-pane.active").find("input#over_under").val();
    if (overUnder) {
      console.log(overUnder);
    } else {
      overUnder = "";
      console.log(gameKey);
    }

    var homeTeam = $("div#home.tab-pane.active").find("input#home_team").val();
    if (homeTeam) {
      console.log(homeTeam);
    } else {
      homeTeam = ""
      console.log(homeTeam);
    }
    var homePS = $("div#home_spread1.tab-pane.active").find("input#home_ps").val();
    if (homePS) {
      console.log(homePS);
    } else {
      homePS = "";
      console.log(homePS);
    }
    var homeML = $("div#home_ml.tab-pane.active").find("input#home_ml").val();
    if (homeML) {
    console.log(homeML);
    } else {
      homeML = "";
      console.log(homeML);
    }
    
    var awayTeam = $("div#away.tab-pane.active").find("input#away_team").val();
    if (awayTeam) {
      console.log(awayTeam);
    } else {
      awayTeam = ""
      console.log(awayTeam);
    }
    var awayPS = $("div#away_spread1.tab-pane.active").find("input#away_ps").val();
    if (awayPS) {
      console.log(awayPS);
    } else {
      awayPS = "";
      console.log(awayPS);
    }
    var awayML = $("div#away_ml.tab-pane.active").find("input#away_ml").val();
    if (awayML) {
      console.log(awayML);
    } else {
      awayML = "";
      console.log(awayML);
    }
    var amount = $("#amount").val();
    if (amount) {
      console.log(amount);
    } else {
      amount = "";
      console.log(amount);
    }
    var $ptext = $("#ptext");
    $.ajax({
      type: "POST",
      url: "/nfl/confirm/",
      // data: $("#form-container").serialize(),
      data: {
        "game_key": gameKey,
        "over_under": overUnder,
        "home_team": homeTeam,
        "home_ml": homeML,
        "home_ps": homePS,
        "away_team": awayTeam,
        "away_ml": awayML,
        "away_ps": awayPS,
        "amount": amount
      },
      // success: function(response) {
      //       },
      //       error: function(error) {
      //           console.log(error);
      //       }
      success: function(response,data) {
        console.log(response, data);
        if (data) {
          $ptext.text("Bet is submitting " + gameKey + "Redirecting...");
          setTimeout(function() {
            window.location.href = "/nfl/confirm/"+gameKey+"/";
          }, 3000);
        } else {
            $ptext.text("Failed to make a server-side call");
        }
      }
    });
    // return false;
    });
});





