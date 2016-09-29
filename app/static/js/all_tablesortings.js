$(document).ready(function(){
  $(function(){
    $('#public__board').tablesorter(); 
  });
  
});

$(function() {
  // call the tablesorter plugin
  $("#offense_season_stats").tablesorter({
    theme: 'blue'
  });
  $('#offense_passing_season_stats').tablesorter({
        theme: 'blue'
    });
  $('#offense_rushing_season_stats').tablesorter({
        theme: 'blue'
    });
  $('#offense_receiving_season_stats').tablesorter({
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



});