$(calculateSum);
function calculateSum() {
var risking = 0;
var winning = 0;
//iterate through each td based on class and add the values
$("td#risk_win").each(function() {
    var value = $(this).text();
    var risk = $.trim(value.split("/")[0])
    var win = $.trim(value.split("/")[1])
    //add only if the value is number
    if(!isNaN(risk) && risk.length!=0) {
        risking += parseFloat(risk);
    }
    if(!isNaN(win) && win.length!=0) {
        winning += parseFloat(win);
    }
});
$('#result').text("risk: " + risking.toFixed(4) + " / " + "win: " + winning.toFixed(4));    
};