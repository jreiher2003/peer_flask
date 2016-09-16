$(document).ready(function(){
    $(".nav-tabs > li > a").click(function(event){
        event.preventDefault(); // stop browser to take action for clicked anchor
        //gets displaying tab content
        var active_tab_selector = $(".nav-tabs > li.active > a").attr("href");
        //find active nav and remove 'active' class
        var active_nav = $(".nav-tabs > li.active");
        active_nav.removeClass("active");
        // add active class to selected tab
        $(this).parents("li").addClass("active");
        //hide displaying tab content
        $(active_tab_selector).removeClass("active");
        $(active_tab_selector).addClass("hide");
        // show target tab content 
        var target_tab_selector = $(this).attr("href");
        $(target_tab_selector).removeClass("hide");
        $(target_tab_selector).addClass("active");
    });
});