$(document).ready(function() {
    $('table#public__board').DataTable( {
        "iDisplayLength": -1,
        "order": [[ 5, "desc" ]]
    } );
} );

$(document).ready(function() {
  // call the tablesorter plugin
  $("#offense_season_stats").DataTable({
    // // debug: true,
    // widgets: ["zebra"],
    // theme: 'blue',
    // 'order': [[2,1]]
  });
  $('#offense_passing_season_stats').DataTable({
    // debug: true,
    // widgets: ["zebra"],
    // theme: 'blue',
    // sortList: [[5,1]]
    });
  $('#offense_rushing_season_stats').tablesorter({
    // debug: true,
    widgets: ["zebra"],
    theme: 'blue',
    sortList: [[3,1]]
    });
  $('#offense_receiving_season_stats').tablesorter({
    // debug: true,
    widgets: ["zebra"],
    theme: 'blue',
    sortList: [[3,1]]
    });
  $('#offense_downs_season_stats').tablesorter({
    // debug: true,
    widgets: ["zebra"],
    theme: 'blue',
    sortList: [[2,1]]
    });
  
  
   
    $('#defense_season_stats').tablesorter({
    // debug: true,
    widgets: ["zebra"],
    theme: 'blue',
    sortList: [[2,0]]
    }); 
    $('#defense_passing_season_stats').tablesorter({
    // debug: true,
    widgets: ["zebra"],
    theme: 'blue',
    sortList: [[5,0]]
    });
    $('#defense_rushing_season_stats').tablesorter({
    // debug: true,
    widgets: ["zebra"],
    theme: 'blue',
    sortList: [[3,0]]
    });
    $('#defense_receiving_season_stats').tablesorter({
    // debug: true,
    widgets: ["zebra"],
    theme: 'blue',
    sortList: [[3,0]]
    });
    $('#defense_downs_season_stats').tablesorter({
    // debug: true,
    widgets: ["zebra"],
    theme: 'blue',
    sortList: [[2,0]]
    });
    $('#defense_tsif_season_stats').tablesorter({
    // debug: true,
    widgets: ["zebra"],
    theme: 'blue',
    sortList: [[5,1]]
    });

    $('#special_kicking_season_stats').tablesorter({
    // debug: true,
    widgets: ["zebra"],
    theme: 'blue',
    sortList: [[2,1]]
    });
    $('#special_punting_season_stats').tablesorter({
    // debug: true,
    widgets: ["zebra"],
    theme: 'blue',
    sortList: [[4,1]]
    });
    $('#special_returns_season_stats').tablesorter({
    // debug: true,
    widgets: ["zebra"],
    theme: 'blue',
    sortList: [[4,1]]
    });
    $("#graded_bets_table").tablesorter({
        dateFormat: "uk",
        sortList: [[0,1]],
    });
    $("#pending_bets_table").tablesorter({
        dateFormat: "uk",
        sortList: [[0,1]],
    });

  
});