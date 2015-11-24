/** SERVER TASKS */
var gulp = require('gulp');
    connect = require('gulp-connect');

// Configuration 
var cfg = require('../gulp_config').cfg;


gulp.task('connect', function() {
    connect.server({
        root:       cfg.cwd,
        livereload: true,
        port:       8080
    });
});

gulp.task('reload', ['test_js'], function () {
    gulp.src(cfg.cwd+'*.html')
        .pipe(connect.reload());
});
 
gulp.task('watch', function () {
  gulp.watch([cfg.cwd+'*.html',
              cfg.cwd+'**/*.css',
              cfg.cwd+'js/**/*.js'],
              ['reload']);
});

// production server
gulp.task('server_prod', function() {
    connect.server({
        root: cfg.dest,
        port: 9000
    });
});

// development server
gulp.task('server', ['connect', 'watch']);

// documentation server
gulp.task('server_doc', function() {
    connect.server({
        root: './DOC_WEBAPP',
        port: 9090
    });
});