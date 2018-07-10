var gulp = require('gulp'),
    connect = require('gulp-connect'),
    nodemon = require('gulp-nodemon'),
    wiredep = require('wiredep');

var WATCH_FRONTEND = ['./*.html', './assets/css/*.css', './assets/js/*.js'];

gulp.task('connect', function() {
    connect.server({
        root: '.',
        livereload: true
    });
});

gulp.task('html', function() {
    gulp
        .src(WATCH_FRONTEND)
        .pipe(connect.reload());
});

gulp.task('watch', function() {
    gulp.watch(WATCH_FRONTEND, ['html']);
});

gulp.task('wiredep', wiredep.bind(null, {
    src: 'index.html'
}));

gulp.task('default', ['connect', 'watch']);
