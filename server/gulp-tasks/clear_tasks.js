/** clean tasks */
var gulp = require('gulp');
    del = require('del');

// Configuration 
var cfg = require('../gulp_config').cfg;

gulp.task('clear', function() {
    del(['../build/**/*'],{force: true});
});
