$(document).ready(function(){
  $(function(){
    $('#public__board').tablesorter(); 
  });
  // $(function(){
  //   $('#offense_season_stats').tablesorter(); 
  // });
  $(function(){
    $('#defense_season_stats').tablesorter(); 
  });
});

$(function() {
  // call the tablesorter plugin
  $("#offense_season_stats").tablesorter({
    theme: 'blue'
  });
   
    $('#defense_season_stats').tablesorter({
        theme: 'blue'
    }); 
 

  // Make table cell focusable
  // http://css-tricks.com/simple-css-row-column-highlighting/
  if ( $('.focus-highlight').length ) {
    $('.focus-highlight').find('th, td')
      .attr('tabindex', '0')
      // add touch device support
      .on('touchstart', function() {
        $(this).focus();
      });
  }

// store the currently selected tab in the hash value
    $("ul.nav-tabs > li > a").on("shown.bs.tab", function(e) {
      var id = $(e.target).attr("href").substr(1);
      console.log("id " + id);
      window.location.hash = id;
    });

    // on load of the page: switch to the currently selected tab
    var hash = window.location.hash;
    console.log("hash " +hash)
    $('#offense_season_stats a[href="' + hash + '"]').tab('show');

     // on load of the page: switch to the currently selected tab
    var hash = window.location.hash;
    console.log("hash " +hash)
    $('#defense_season_stats a[href="' + hash + '"]').tab('show');


});