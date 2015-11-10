var gulp = require('gulp');
    requireDir = require('require-dir');

requireDir('./gulp-tasks');
runSequence = require('run-sequence');

// Configuration 
var cfg = require('./gulp_config').cfg;

gulp.task('build', function() {
    runSequence('clear', ['roptimize', 'js', 'minify_css'],
                'copy',
                function(){
                    console.log("Build on ----> %s <---- ok!", cfg.dest);
                });
});

// default task
gulp.task('default', ['server']);

