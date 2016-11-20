$(document).ready(function() {
    $('table#public__board').DataTable( {
        "pageLength": 10,
        "iDisplayLength": -1,
        "order": [[1,"asc"]]
    } );
});

$(document).ready(function() {
  // call the tablesorter plugin
  var tt = $("table#offense_season_stats").DataTable({
     "pageLength": 50,
     "order": [[2,"desc"]],
  });
  tt.on('order.dt search.dt', function () {
        tt.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
  var ss = $('table#offense_passing_season_stats').DataTable({
    "pageLength": 50,
    "order": [[5,"desc"]],  
    });
  ss.on('order.dt search.dt', function () {
        ss.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
  var ww = $('table#offense_rushing_season_stats').DataTable({
    "pageLength": 50,
    "order": [[3, "desc"]],
    });
  ww.on('order.dt search.dt', function () {
        ww.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
  var aa = $('table#offense_receiving_season_stats').DataTable({
    "pageLength": 50,
    "order": [[3, "desc"]],
    });
  aa.on('order.dt search.dt', function () {
        aa.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
  var bb = $('table#offense_downs_season_stats').DataTable({
    "pageLength": 50,
    "order": [[2, "desc"]],
    });
  bb.on('order.dt search.dt', function () {
        bb.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
  
  
   
  var cc = $('table#defense_season_stats').DataTable({
   "pageLength": 50,
   "order": [[2,'asc']],
  });
  cc.on('order.dt search.dt', function () {
        cc.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
  var dd = $('table#defense_passing_season_stats').DataTable({
    "pageLength": 50,
    "order": [[5,'asc']],
  });
  dd.on('order.dt search.dt', function () {
        dd.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
  var ff = $('table#defense_rushing_season_stats').DataTable({
    "pageLength": 50,
    "order": [[3,'asc']],
  });
  ff.on('order.dt search.dt', function () {
        ff.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
  var gg = $('table#defense_receiving_season_stats').DataTable({
    "pageLength": 50,
    "order": [[3,'asc']],
  });
  gg.on('order.dt search.dt', function () {
        gg.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
  var hh = $('table#defense_downs_season_stats').DataTable({
    "pageLength": 50,
    "order": [[2,'asc']],
  });
  hh.on('order.dt search.dt', function () {
        hh.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
  var jj = $('table#defense_tsif_season_stats').DataTable({
    "pageLength": 50,
    "order": [[5,'desc']],
  });
  jj.on('order.dt search.dt', function () {
        jj.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();

  var kk = $('table#special_kicking_season_stats').DataTable({
    "pageLength": 50,
    "order": [[2,'desc']],
   });
  kk.on('order.dt search.dt', function () {
        kk.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
  var ll = $('table#special_punting_season_stats').DataTable({
    "pageLength": 50,
    "order": [[4,'desc']],
    });
  ll.on('order.dt search.dt', function () {
        ll.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
  var zz = $('table#special_returns_season_stats').DataTable({
    "pageLength": 50,
    "order": [[4,'desc']],
    });
  zz.on('order.dt search.dt', function () {
        zz.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
});
$(document).ready(function() {
  $("table#graded_bets_table").DataTable({
     "pageLength": 10,
     "order":[[2,'desc']],
    });
  $("table#pending_bets_table").DataTable({
     "pageLength": 25,
     "order":[[0,'desc']],
    });
});