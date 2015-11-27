var gulp = require('gulp');
    merge = require('merge-stream');
    htmlreplace = require('gulp-html-replace');
    minifyHTML = require('gulp-minify-html');

// Configuration 
var cfg = require('../gulp_config').cfg;

var js_min = require('../gulp_config').js_min; 
var libs_min = require('../gulp_config').libs_min;
var lib_cartodb_min = require('../gulp_config').lib_cartodb_min;
var css_min = require('../gulp_config').css_min; 


gulp.task('copy', function () {
    var opts = {
        conditionals: true,
        spare:true
    };

    var html = gulp.src('*.html', { cwd: cfg.cwd })
        .pipe(htmlreplace({
            js: {
                src: [['js/'+js_min, 'libs/'+libs_min]],
                tpl: '<script data-main="%s" src="%s"></script>'
            },
            cartodb: {
                src: [['libs/'+lib_cartodb_min]],
                tpl: '<script type="text/javascript" src="%s"></script>'
            },
            css: ['css/'+css_min]
        }))
        .pipe(minifyHTML(opts))
        .pipe(gulp.dest(cfg.dest));

    var libs = gulp.src(['libs/cartodb.js/cartodb.js'], { cwd: cfg.cwd })
        .pipe(gulp.dest(cfg.dest+'libs'));
    
    var favicon = gulp.src('favicon.ico', { cwd: cfg.cwd })
        .pipe(gulp.dest(cfg.dest));

    var img = gulp.src('img/*', { cwd: cfg.cwd })
        .pipe(gulp.dest(cfg.dest+'img'));

    var jquery_ui_img = gulp.src('libs/jquery-ui/themes/smoothness/images/*', { cwd: cfg.cwd })
        .pipe(gulp.dest(cfg.dest+'css/images'));

    var data = gulp.src('data/*', { cwd: cfg.cwd })
        .pipe(gulp.dest(cfg.dest+'data'));

    return merge(html, libs, favicon, img, jquery_ui_img, data);
});