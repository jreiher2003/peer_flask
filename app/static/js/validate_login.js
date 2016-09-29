$(document).ready(function(){
    $.validate({
      form: "#loginForm",
      modules: "security",
      onModulesLoaded: function(){
        var optionalConfig = {
          width: "100%",
          fontSize: "8pt",
          padding: "4px",
          bad: "Very bad",
          weak: "Weak",
          good: "Good",
          strong: "Strong"
        };
        $("input[name='password']").displayPasswordStrength(optionalConfig);
      }
    });
});