$(document).ready(function(){
    $("#bet_tabs a").click(function (e) {
      e.preventDefault();  
        $(this).tab('show');
    });

//     // store the currently selected tab in the hash value
//     $("ul.nav-tabs > li > a").on("shown.bs.tab", function(e) {
//       var id = $(e.target).attr("href").substr(1);
//       console.log("id " + id);
//       window.location.hash = id;
//     });

//     // on load of the page: switch to the currently selected tab
//     var hash = window.location.hash;
//     console.log("hash " +hash)
//     $('#bet_tabs a[href="' + hash + '"]').tab('show');

// });
