/**
 * Created by kubix on 27.12.16.
 */

united.directive('postGuildRender', function () {
    return function (scope, element, attrs) {
        if (scope.$last) {
            $('.guildCounter').tooltip({'placement': "top", trigger: "hover"});
        }
    };
});

united.controller('vendorsController', ['$scope', 'Vendors', function ($scope, Vendors) {
    $scope.vend = [];
    $scope.currentPage = 1;
    $scope.numPerPage = 10;

    $scope.numsPerPage = [
        {size: 10},
        {size: 20},
        {size: 50},
        {size: 100}
    ];

    Vendors.list(
        function (response) {
            $scope.vendorsList = response.data.vendorsList;
            $scope.randVendors = response.data.randVendors;
        });

    $scope.propertyName = '';
    $scope.reverse = true;

    $scope.sortBy = function (propertyName) {
        $scope.reverse = ($scope.propertyName === propertyName) ? !$scope.reverse : false;
        $scope.propertyName = propertyName;
    };

    $scope.pageChanged = function () {
        var startPos = ($scope.currentPage - 1) * $scope.numPerPage;
    };

    $scope.update = function (nums) {
        $scope.numPerPage = nums;
    };

}]);

united.controller('rankingsController', ['$scope', 'Rankings', function ($scope, Rankings) {
    $scope.currentPage = 1;
    $scope.numPerPage = 5;
    $scope.bgRanking = [];

    $scope.numsPerPage = [
        {size: 10},
        {size: 20},
        {size: 50},
        {size: 100}
    ];

    $scope.pageChanged = function () {
        var startPos = ($scope.currentPage - 1) * $scope.numPerPage;
    };

    $scope.update = function (nums) {
        $scope.numPerPage = nums;
    };

    Rankings.getBG(function (response) {
        $scope.bgRanking = response.data.BgRanking;
    });

}]);

united.controller('woeController', ['$scope', 'Rankings', function ($scope, Rankings) {

    $scope.woeDate = moment().day("Sunday").format("YYYY-MM-DD");
    $scope.woeDate2 = moment().day("Sunday").format("YYYY-MM-DD HH-mm-SS");
    $scope.currentPage = 1;
    $scope.numPerPage = 200;
    $scope.woeRanking = [];
    $scope.guildCount = [];
    $scope.search = {}

    $scope.classes = {
        23: 'Super Novice',
        24: 'Gunslinger',
        25: 'Ninja',
        4008: 'Lord Knight',
        4015: 'Paladin',
        4009: 'High Priest',
        4016: 'Champion',
        4010: 'High Wizard',
        4017: 'Professor',
        4011: 'Whitesmith',
        4018: 'Stalker',
        4012: 'Sniper',
        4019: 'Creator',
        4013: 'Assassin Cross',
        4020: 'Clown',
        4021: 'Gypsy',
        4049: 'Soul Linker',
        4047: 'Taekwon Master',
    }
    $scope.classIds = Object.keys($scope.classes)

    $scope.searchClass = function (val) {

    }
    $scope.searchGuild = function (val) {
        $scope.search.char_id__guild_id = String(val)+' ';
    }

    $scope.getClass = function(id) {
        return $scope.classes[id]
    }

    $scope.numsPerPage = [
        {size: 25},
        {size: 50},
        {size: 100},
        {size: 200}
    ];
    $scope.propertyName = '';
    $scope.reverse = false;
    $scope.detailsOpened = {}
    $scope.woeDetails = {}
    $scope.skillStatId = null
    $scope.skillRanking = {};
    $scope.skillStatId = {}

    $scope.getSkillRank = function (skill_id, char_id) {
        Rankings.getSkillRank(function (response) {
            $scope.skillRanking[char_id] = response.data.SkillRanking
        }, $scope.woeDate, skill_id, $scope.woeDate2);

        $scope.skillStatId[char_id] = skill_id
    }

    $scope.getSkillByChar = function(char_id) {
        return $scope.skillStatId[char_id]
    }


    $scope.toggleDetails = function (index) {
        $scope.detailsOpened[String(index)] = $scope.detailsOpened[index] ? false : true;

        if ($scope.detailsOpened[String(index)])
            Rankings.getWoEDetails(function (response) {
                $scope.woeDetails[String(index)] = {}
                $scope.woeDetails[String(index)].killer = response.data.WoEKiller;
                $scope.woeDetails[String(index)].killed = response.data.WoEKilled;
                $scope.woeDetails[String(index)].skills = response.data.Skills;
            }, $scope.woeDate, index, $scope.woeDate2);
    }

    $scope.getKills = function (char_id) {
        return $scope.woeDetails[String(char_id)].killer;
    }

    $scope.getDeaths = function (char_id) {
        return $scope.woeDetails[String(char_id)].killed;
    }

    $scope.getSkills = function (char_id) {
        return $scope.woeDetails[String(char_id)].skills;
    }

    $scope.getTime = function (date) {
        return moment(date).format("HH:mm")
    }

    $scope.showDetails = function (index) {
        return $scope.detailsOpened[String(index)];
    }

    $scope.prevDate = function () {
        $scope.woeDate = moment($scope.woeDate).subtract(7, 'days').format("YYYY-MM-DD")
        $scope.getWoe()
    }

    $scope.nextDate = function () {
        $scope.woeDate = moment($scope.woeDate).add(7, 'days').format("YYYY-MM-DD")
        $scope.getWoe()
    }

    $scope.sortBy = function (propertyName) {
        $scope.reverse = ($scope.propertyName === propertyName) ? !$scope.reverse : true;
        $scope.propertyName = propertyName;
    };
    $scope.pageChanged = function () {
        var startPos = ($scope.currentPage - 1) * $scope.numPerPage;
    };

    $scope.update = function (nums) {
        $scope.numPerPage = nums;
    };

    $scope.update2 = function (val) {
        $scope.search.char_id__class_field = String(val);
        console.log(val)
    };

    $scope.getWoe = function () {
        Rankings.getWoE(function (response) {
            $scope.woeRanking = response.data.WoERanking;
            for (var i in $scope.woeRanking) {
                $scope.woeRanking[i].char_id__guild_id = $scope.woeRanking[i].char_id__guild_id+' '
            }
            $scope.guildCount = response.data.MembersCount;
        }, $scope.woeDate);
    };

    $scope.getWoe();
}]);

united.controller('announcementsController', ['$scope', 'Announcements', '$cookies', '$sce', function ($scope, Announcements, $cookies, $sce) {
    $scope.currentPage = 1;
    $scope.numPerPage = 20;
    $scope.announcements = {};
    $scope.showAlert = !!$cookies.get('announceAlert');

    $scope.alerts = [
        {
            type: 'warning',
            msg: null
        }
    ];

    $scope.numsPerPage = [
        {size: 10},
        {size: 20},
        {size: 50},
        {size: 100}
    ];

    $scope.propertyName = '';
    $scope.reverse = true;

    $scope.sortBy = function (propertyName) {
        $scope.reverse = ($scope.propertyName === propertyName) ? !$scope.reverse : false;
        $scope.propertyName = propertyName;
    };

    $scope.pageChanged = function () {
        var startPos = ($scope.currentPage - 1) * $scope.numPerPage;
    };

    $scope.update = function (nums) {
        $scope.numPerPage = nums;
    };

    Announcements.list(function (response) {
        $scope.announcements = response.data.announcements_list;
    });

    $scope.closeAlert = function (index) {
        $cookies.put('announceAlert', true);
        $scope.alerts.splice(index, 1);
    };
}]);