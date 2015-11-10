/** css tasks */
var gulp = require('gulp');
    minifyCSS = require('gulp-minify-css');
    concat = require('gulp-concat');

// Configuration 
var cfg = require('../gulp_config').cfg;
var css_min = require('../gulp_config').css_min; 


gulp.task('minify_css', function () {
/** KEEP CORRECT ORDER */
    gulp.src([ 
                //LN methodology
                'libs/jquery-ui/themes/smoothness/jquery-ui.css',
                'css/styles.css',
                'css/cartodb.css',
                'css/tooltip.css',
                'css/draw_controls.css',
                'css/leaflet_draw.css',
                'css/overlay.css',
                'css/styles_max_1100.css',
                'css/styles_max_0960.css',
                'css/styles_max_0850.css',
                'css/styles_max_0768.css',
                'css/styles_max_0640.css',
                // Project specific needs
                'css/styles_max_0455.css'
            ], { cwd: cfg.cwd })
    .pipe(minifyCSS())
    .pipe(concat(css_min))
    .pipe(gulp.dest(cfg.dest+'css'));

});
