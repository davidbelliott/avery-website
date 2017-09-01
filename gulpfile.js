var gulp = require('gulp');
var sass = require('gulp-sass');

gulp.task('default', function() {
    return gulp.src('./avery_website/assets/sass/*.sass')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('./avery_website/static/css'));
});
