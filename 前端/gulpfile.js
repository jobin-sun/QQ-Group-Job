var gulp = require("gulp");
var uglify = require('gulp-uglify');
var csso = require('gulp-csso');
var concat = require('gulp-concat');
var clean = require('gulp-clean');
var templateCache = require('gulp-angular-templatecache');

var src = ".";
var dst = "./build";
gulp.task('default', function () {
    gulp.src(src + '/*.html')
        .pipe(gulp.dest(dst + '/'));

	gulp.src(src + '/tpl/*.html')
    	.pipe(templateCache("tpl.js",{
    		module:"myApp",
    		root:"tpl/"
    	}))
        .pipe(uglify())
    	.pipe(gulp.dest(dst + '/js'));

    gulp.src(src + '/js/*.js')
    	.pipe(uglify())
    	.pipe(gulp.dest( dst + '/js'));

    gulp.src(src + '/css/*.css')
        .pipe(csso())
        .pipe(gulp.dest(dst + '/css'));

    gulp.src(src + '/static/**/*')
        .pipe(gulp.dest(dst + '/static'));

});
