(function(angular, R) {
    angular
        .module('AnkiCardCreator', [])
        .constant('SANITIZE_NOTES', true)
        .constant('NOTES_URL', 'assets/notes.json')
        .config(function($sceProvider) {
            $sceProvider.enabled(false);
        })
        .controller('MainCtrl', function($scope, $http, NOTES_URL, SANITIZE_NOTES) {
            $http
                .get(NOTES_URL)
                .then(function(res) {
                    $scope.notes = res.data;
                    if(SANITIZE_NOTES)
                        R.forEach(sanitizeNodeGently, R.flatten(R.pluck('notes', $scope.notes)));
                });

            function sanitizeNodeGently(note) {
                function sanitize(str) {
                    return str.replace(/<br.?\/?>/g, '<br/>');
                }
                // More than 3 '<br/>'? That's a...
                note.error = (/(?:<br ?\/?>\s*?){3,}/g).test(note.content);
                note.error = note.error || (/<([A-z][A-z0-9]*)>(.*?)<\/\1>/g).test(note.content);

                note.content = sanitize(note.content);
                note.title = sanitize(note.title);

                return note;
            }
        });
})(angular, R);
