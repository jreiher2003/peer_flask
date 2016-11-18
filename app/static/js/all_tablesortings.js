$(document).ready(function() {
    $('table#public__board').DataTable( {
        "iDisplayLength": -1,
        "order": [[1,"asc"]]
    } );
} );

$(document).ready(function() {
  // call the tablesorter plugin
  var t = $("table#offense_season_stats").DataTable({
     "pageLength": 50,
     "order": [[2,"desc"]],
  });
  t.on('order.dt search.dt', function () {
        t.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
  var s = $('table#offense_passing_season_stats').DataTable({
    "pageLength": 50,
    "order": [[5,"desc"]],  
    });
  s.on('order.dt search.dt', function () {
        s.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
  var w = $('table#offense_rushing_season_stats').DataTable({
    "pageLength": 50,
    "order": [[3, "desc"]],
    });
  w.on('order.dt search.dt', function () {
        w.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
  var a = $('table#offense_receiving_season_stats').DataTable({
    "pageLength": 50,
    "order": [[3, "desc"]],
    });
  a.on('order.dt search.dt', function () {
        a.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
  var b = $('table#offense_downs_season_stats').DataTable({
    "pageLength": 50,
    "order": [[2, "desc"]],
    });
  b.on('order.dt search.dt', function () {
        b.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
  
  
   
  var c = $('table#defense_season_stats').DataTable({
   "pageLength": 50,
   "order": [[2,'asc']],
  });
  c.on('order.dt search.dt', function () {
        c.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
  var d = $('table#defense_passing_season_stats').DataTable({
    "pageLength": 50,
    "order": [[5,'asc']],
  });
  d.on('order.dt search.dt', function () {
        d.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
  var f = $('table#defense_rushing_season_stats').DataTable({
    "pageLength": 50,
    "order": [[3,'asc']],
  });
  f.on('order.dt search.dt', function () {
        f.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
  var g = $('table#defense_receiving_season_stats').DataTable({
    "pageLength": 50,
    "order": [[3,'asc']],
  });
  g.on('order.dt search.dt', function () {
        g.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
  var h = $('table#defense_downs_season_stats').DataTable({
    "pageLength": 50,
    "order": [[2,'asc']],
  });
  h.on('order.dt search.dt', function () {
        h.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
  var j = $('table#defense_tsif_season_stats').DataTable({
    "pageLength": 50,
    "order": [[5,'desc']],
  });
  j.on('order.dt search.dt', function () {
        j.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();

  var k = $('table#special_kicking_season_stats').DataTable({
    "pageLength": 50,
    "order": [[2,'desc']],
   });
  k.on('order.dt search.dt', function () {
        k.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
  var l = $('table#special_punting_season_stats').DataTable({
    "pageLength": 50,
    "order": [[4,'desc']],
    });
  l.on('order.dt search.dt', function () {
        l.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
  var m = $('table#special_returns_season_stats').DataTable({
    "pageLength": 50,
    "order": [[4,'desc']],
    });
  m.on('order.dt search.dt', function () {
        m.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
  $("table#graded_bets_table").DataTable({
     "pageLength": 10,
     "order":[[2,'desc']],
    });
  $("table#pending_bets_table").DataTable({
     "pageLength": 25,
     "order":[[0,'desc']],
    });
});