var gulp = require("gulp");
var uglify = require('gulp-uglify');
var csso = require('gulp-csso');
var concat = require('gulp-concat');
var templateCache = require('gulp-angular-templatecache');
var inject = require('gulp-inject');
var series = require('stream-series');

var src = ".";
var dst = "./build";
gulp.task('default', function () {
    var app = gulp.src([
            src + '/js/common.js',
            src + '/js/route.js',
            src + '/js/service.js',
            src + '/js/filter.js',
            src + '/js/directive.js',
            src + '/js/ctrl/*.js'
        ])
        .pipe(concat("app.js"))
        .pipe(uglify())
        .pipe(gulp.dest(dst + '/js'));
    var tpl = gulp.src(src + '/tpl/**/*.html')
                    .pipe(templateCache("tpl.js",{
                        module:"myApp",
                        base:"/",
                        transformUrl: function(url) {
                            return url.replace(/.+?[\/\\]client[\\\/]/, '')
                        }
                    }))
                    .pipe(uglify())
                    .pipe(gulp.dest(dst + '/js'));
    gulp.src(src + '/*.html')
        .pipe(
            inject(
                series(app, tpl),
                {relative: true, ignorePath: "build"}
            )
        )
        .pipe(gulp.dest(dst + '/'));

    gulp.src(src + '/js_lib/*.js')
        .pipe(uglify())
        .pipe(gulp.dest(dst + '/js_lib'));

    gulp.src(src + '/css/*.css')
        .pipe(csso())
        .pipe(gulp.dest(dst + '/css'));

    gulp.src(src + '/images/*')
        .pipe(gulp.dest(dst + '/images'));

    gulp.src(src + '/static/**/*')
        .pipe(gulp.dest(dst + '/static'));

});
