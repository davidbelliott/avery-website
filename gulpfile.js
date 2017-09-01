var gulp = require('gulp');
var sass = require('gulp-sass');

gulp.task('sass', function() {
    return gulp.src('./avery_website/assets/sass/*.sass')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('./avery_website/static/css'));
});

gulp.task('sass:watch', function() {
    gulp.watch('./avery_website/assets/sass/*.sass', ['sass']);
});

gulp.task('default', ['sass:watch']);
