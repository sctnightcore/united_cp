/**
 * Created by kubix on 29.12.16.
 */
united.factory('Vendors', ['$http', function ($http) {
    return {
        list: function (success) {
            $http.get('/addon/vending/list/')
                .then(function (response) {
                    success(response);
                })
        }
    }

}]);
united.factory('Rankings', ['$http', function ($http) {
    return {
        getBG: function (success) {
            $http.get('/rankings/api/battleground/')
                .then(function (response) {
                    success(response);
                })
        },
        getWoE: function (success,date) {
            $http.get('/rankings/api/woe/?date='+date)
                .then(function (response) {
                    success(response);
                })
        },
        getWoEDetails: function (success,date,char_id,date2) {
            $http.get('/rankings/api/woe_char_details/?date='+date+'&char_id='+char_id)
                .then(function (response) {
                    success(response);
                })
        },
        getSkillRank: function (success,date,skill_id,date2) {
            $http.get('/rankings/api/skill/?date='+date+'&skill_id='+skill_id)
                .then(function (response) {
                    success(response);
                })
        },
    }
}]);
united.factory('Announcements', ['$http', function ($http) {
    return {
        list: function (success) {
            $http.get('/addon/announcements/list/')
                .then(function (response) {
                    success(response);
                })
        },
        characters: function (success) {
            $http.get('/addon/announcements/chars/')
                .then(function (response) {
                    success(response);
                })
        }
    }
}]);