var gulp = require('gulp');
var sass = require('gulp-sass');
var uncss = require('gulp-uncss');

gulp.task('sass', function() {
    return gulp.src('./avery_website/assets/sass/*.sass')
        .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
        /*.pipe(uncss({
            html: ['./avery_website/templates/*.html'],
            ignore: ['\.navbar-fixed-top']
        }))*/
        .pipe(gulp.dest('./avery_website/static/css'));
});

gulp.task('sass:watch', function() {
    gulp.watch('./avery_website/assets/sass/*.sass', ['sass']);
});

gulp.task('default', ['sass', 'sass:watch']);
