/**
 * Created by kubix on 27.12.16.
 */
var united = angular.module('united', ['ui.bootstrap', 'ngCookies', 'ngSanitize']);
united.config(['$interpolateProvider', '$httpProvider',
    function config($interpolateProvider, $httpProvider) {

        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');

    }]);