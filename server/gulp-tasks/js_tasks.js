/** Build JS files */
var gulp = require('gulp');
    rjs = require('gulp-requirejs');
    jshint = require('gulp-jshint');
    stylish = require('jshint-stylish');
    sourcemaps = require('gulp-sourcemaps');
    concat = require('gulp-concat');
    uglify = require('gulp-uglify');
    merge = require('merge-stream');

// Configuration 
var cfg = require('../gulp_config').cfg;

// Vars
var js_min = require('../gulp_config').js_min; 
var libs_min = require('../gulp_config').libs_min; 


/** test js */
gulp.task('test_js', function(){
    return gulp.src(['js/**/*.js'], { cwd: cfg.cwd })
               .pipe(jshint({multistr: true}))
               .pipe(jshint.reporter('default'))
               .pipe(jshint.reporter(stylish));
});

/** requirejs optimizer */
gulp.task('roptimize', function() {
    rjs({
        mainConfigFile : cfg.cwd+"js/app.js",
        baseUrl: cfg.cwd+"js",
        name: "app",
        optimizeAllPluginResources: true,
        removeCombined: true,
        out: 'app-opt.js',
    })
    .pipe(gulp.dest(cfg.opt_path));
});

gulp.task('js', ['test_js'], function () {
    var js = gulp.src(['opt/app-opt.js'] , { cwd: cfg.cwd })
        .pipe(sourcemaps.init())
        .pipe(uglify())
        .pipe(concat(js_min))
        // .pipe(sourcemaps.write('./'))
        .pipe(gulp.dest(cfg.dest+'js'));
    
    var libs = gulp.src(['libs/requirejs/require.js'], { cwd: cfg.cwd })
        .pipe(sourcemaps.init())
        .pipe(uglify())
        .pipe(concat(libs_min))
        // .pipe(sourcemaps.write('./'))
        .pipe(gulp.dest(cfg.dest+'libs'));

    return merge(js,libs);
    
});
