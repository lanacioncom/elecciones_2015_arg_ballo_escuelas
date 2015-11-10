/** doc tasks */
var gulp = require('gulp');
    jsdoc = require("gulp-jsdoc");

// Configuration 
var cfg = require('../gulp_config').cfg;

// default task
gulp.task('make_jsdoc', function() {
    gulp.src(["js/**/*.js", "./DOC_WEBAPP/README.md"], { cwd: cfg.cwd })
        .pipe(jsdoc.parser())
        .pipe(jsdoc('./DOC_WEBAPP'));
});
