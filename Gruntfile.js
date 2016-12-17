module.exports = function(grunt) {
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.initConfig({
        cssmin: {
          options: {
            shorthandCompacting: false,
            roundingPrecision: -1
          },
          target: {
            files: {
              'app/static/dist/css_build/build.min.css': ['app/static/css/bootswatch/cosmo/bootstrap.css','app/static/css/style.css', 'app/static/css/nav.css', 'app/static/css/base_user.css', 'app/static/css/profile.css','app/static/css/moble_under_768.css', 'app/static/css/stats_table_styles.css', 'app/static/css/dataTables/jquery.dataTables.min.css', 'app/static/css/footer.css',],
              'app/static/dist/css_build/cosmo_bootstrap.min.css': ['app/static/css/bootswatch/cosmo/bootstrap.css']
            }
          }
        },
        uglify: {
          options: {
            mangle: false
          },
          my_target: {
            files: {
              'app/static/dist/js_build/build.min.js': ['app/static/js/jquery-form-validator/jquery.form-validator.min.js', 'app/static/js/jquery-form-validator/security.js', 'app/static/js/DataTables/dataTables.min.js', 'app/static/js/DataTables/dataTables.bootstrap.min.js', 'app/static/js/create_bet_tabs.js', 'app/static/js/select_team.js', 'app/static/js/nfl_team_stats_tabs.js', 'app/static/js/nav_dropdown.js', 'app/static/js/all_tablesortings.js', 'app/static/js/jquery.qrcode.min.js', 'app/static/js/alert_up.js', 'app/static/js/calculate_sum.js', 'app/static/js/disabled_buttons.js', 'app/static/js/tooltip_popover.js', 'app/static/js/tabs_jumping.js'],
              'app/static/dist/js_build/bootstrap.min.js': ['app/static/js/bootstrap/bootstrap.js']
            }
          }
        }
    });
    grunt.registerTask('default', ['cssmin', 'uglify'])
}

// 'app/static/js/jquery/jquery.min.js', 'app/static/js/bootstap/boostrap.js',
// 'app/static/css/font-awesome/font-awesome.min.css',  