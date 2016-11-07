$(document).ready(function() {
    $('table#public__board').DataTable( {
        "iDisplayLength": -1,
        "order": [[ 5, "desc" ]]
    } );
} );

$(document).ready(function() {
  // call the tablesorter plugin
  $("table#offense_season_stats").DataTable({
     "pageLength": 50,
     "order": [[2,"desc"]],
  });
  $('table#offense_passing_season_stats').DataTable({
    "pageLength": 50,
    "order": [[5,"desc"]],  
    });
  $('table#offense_rushing_season_stats').DataTable({
    "pageLength": 50,
    "order": [[3, "desc"]],
    });
  $('table#offense_receiving_season_stats').DataTable({
    "pageLength": 50,
    "order": [[3, "desc"]],
    });
  $('table#offense_downs_season_stats').DataTable({
    "pageLength": 50,
    "order": [[2, "desc"]],
    });
  
  
   
  $('table#defense_season_stats').DataTable({
   "pageLength": 50,
   "order": [[2,'asc']],
  }); 
  $('table#defense_passing_season_stats').DataTable({
    "pageLength": 50,
    "order": [[5,'asc']],
  });
  $('table#defense_rushing_season_stats').DataTable({
    "pageLength": 50,
    "order": [[3,'asc']],
  });
  $('table#defense_receiving_season_stats').DataTable({
    "pageLength": 50,
    "order": [[3,'asc']],
  });
  $('table#defense_downs_season_stats').DataTable({
    "pageLength": 50,
    "order": [[2,'asc']],
  });
  $('table#defense_tsif_season_stats').DataTable({
    "pageLength": 50,
    "order": [[5,'desc']],
  });

  $('table#special_kicking_season_stats').DataTable({
    "pageLength": 50,
    "order": [[2,'desc']],
   });
  $('table#special_punting_season_stats').DataTable({
    "pageLength": 50,
    "order": [[4,'desc']],
    });
  $('table#special_returns_season_stats').DataTable({
    "pageLength": 50,
    "order": [[4,'desc']],
    });
  $("table#graded_bets_table").DataTable({
     "pageLength": 10,
     "order":[[2,'desc']],
    });
  $("table#pending_bets_table").DataTable({
     "pageLength": 25,
     "order":[[0,'desc']],
    });

  
});