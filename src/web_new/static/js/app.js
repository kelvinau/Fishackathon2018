var URL = '/api/';
var app = angular.module('fishackathon2018-challenge7', ['ui.router', 'ngAnimate', 'ui.bootstrap']);
app.run(function($transitions, $rootScope, $timeout, $state) {
    $state.go('main.login')
});

app.controller('topbarCtrl', function($scope, $rootScope, $state, requestService) {
    $scope.user = $rootScope.user;
    $scope.notificationOn = $scope.user.sms_notification;
    $scope.logout = function() {
        requestService.send('post', URL + 'seller/logout', {}).then(function(res) {
            $rootScope.user = null;
            $scope.user = null;
            $state.go('main.login');
        })
    }
    $scope.saveNotificationSetting = function($event) {
        $($event.currentTarget).blur();
        requestService.send('post', URL + 'notification/sms', {
            notification_on: $scope.notificationOn
        }).then(function(res) {
            console.log(res);
        })
    }
});

app.controller('navbarCtrl', function($scope, $rootScope, $state, requestService) {
    $scope.user = $rootScope.user;
});

app.controller('loginCtrl', function($rootScope, $state, $scope, requestService) {
  $scope.login = function() {
    var sendParams = {
        phone_number: $scope.phoneNo,
        password: $scope.psw,
    };        
    requestService.send('post', URL + 'seller/login', sendParams).then(function(res) {
      if (res.status === 200) {
          $rootScope.user = res.data.data.user;
          $state.go('main.list');
      }
    }, function() {
        alert('Incorrect login credentials');
    });
  }
})

app.controller('signupCtrl', function($scope, requestService, $rootScope, $state) {
  $scope.signup = function() {
    var sendParams = {
        name: $scope.name,
        phone_number: $scope.phoneNo,
        location: $scope.locationChosen,
        password: $scope.psw,
    };

   requestService.send('post', URL + 'seller/sign_up', sendParams).then(function(res) {
    console.log(res);
    if (res.status === 200) {
        delete sendParams.password;
        $rootScope.user = res.data.data.user;
        $state.go('main.list');
    }
   });
  };
  $scope.locationBtnClick = function(location) {
    console.log(location);
    $scope.locationChosen = location;
  }
    requestService.send('get', URL + 'regions', {}).then(function(res) {
        $scope.locations = res.data.data.map(function(location) {
            return location.location_name;
        });;
    });
    
    $scope.status = {
        isopen: false
    };

    $scope.toggled = function(open) {
        $log.log('Dropdown is now: ', open);
    };

    $scope.toggleDropdown = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.status.isopen = !$scope.status.isopen;
    };
    $scope.appendToEl = angular.element(document.querySelector('#dropdown-long-content'));
});


app.controller('submitCtrl', function($scope, requestService) {
  console.log('submitCtrl loaded');

  requestService.send('get', URL + 'fish_names', {}).then(function(res) {
    $scope.items = res.data.data.map(function(item) {
        return item.common_name;
    });
  });

    $scope.fishBtnClick = function(fishy) {
            $scope.fishname = fishy;
        };
    $scope.status = {
        isopen: false
    };

    $scope.toggled = function(open) {
        $log.log('Dropdown is now: ', open);
    };

    $scope.toggleDropdown = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.status.isopen = !$scope.status.isopen;
    };

    $scope.appendToEl = angular.element(document.querySelector('#dropdown-long-content'));

    $scope.today = function() {
        $scope.date_caughted = new Date();
    };
    $scope.today();

    $scope.clear = function() {
        $scope.caught_date = null;
    };

    $scope.inlineOptions = {
        customClass: getDayClass,
        minDate: new Date(),
        showWeeks: true
    };

    $scope.dateOptions = {
        dateDisabled: disabled,
        formatYear: 'yy',
        maxDate: new Date(2020, 5, 22),
        minDate: new Date(),
        startingDay: 1
    };

    // Disable weekend selection
    function disabled(data) {
        var date = data.date,
            mode = data.mode;
        return mode === 'day' && (date.getDay() === 0 || date.getDay() === 6);
    }

    $scope.toggleMin = function() {
        $scope.inlineOptions.minDate = $scope.inlineOptions.minDate ? null : new Date();
        $scope.dateOptions.minDate = $scope.inlineOptions.minDate;
    };

    $scope.toggleMin();

    $scope.open1 = function() {
        $scope.popup1.opened = true;
    };

    $scope.open2 = function() {
        $scope.popup2.opened = true;
    };

    $scope.setDate = function(year, month, day) {
        $scope.caught_date = new Date(year, month, day);
    };

    $scope.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
    $scope.format = $scope.formats[0];
    $scope.altInputFormats = ['M!/d!/yyyy'];

    $scope.popup1 = {
        opened: false
    };

    $scope.popup2 = {
        opened: false
    };

    var tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    var afterTomorrow = new Date();
    afterTomorrow.setDate(tomorrow.getDate() + 1);
    $scope.events = [
        {
            date: tomorrow,
            status: 'full'
        },
        {
            date: afterTomorrow,
            status: 'partially'
        }
    ];

    function getDayClass(data) {
        var date = data.date,
            mode = data.mode;
        if (mode === 'day') {
            var dayToCheck = new Date(date).setHours(0,0,0,0);

            for (var i = 0; i < $scope.events.length; i++) {
                var currentDay = new Date($scope.events[i].date).setHours(0,0,0,0);

                if (dayToCheck === currentDay) {
                    return $scope.events[i].status;
                }
            }
        }

        return '';
    }

    $scope.submit = function() {
        var date = new Date($scope.caught_date);
        var string_date = date.getFullYear() + '-' + 
        (date.getMonth() + 1).toString().padStart(2, '0') +
         '-' + (date.getDate()).toString().padStart(2, '0');
        var sendParams = {
            fish_name: $scope.fishname,
            price: $scope.price,
            caught_date: string_date,
        };
        requestService.send('post', URL + 'record/submit', sendParams).then(function() {
            alert('Record added successfully!');
        })
    }


})

app.controller('listCtrl', function($scope, $rootScope, $timeout, requestService) {
    
    requestService.send('get', URL + 'records', {}).then(function(res) {
         $scope.fishrows = res.data.data.map(function(item) {
             return {
                 fish: item.fish.common_name,
                 price: item.price,
                 dateCaught: item.caught_date,
                 dateSold: item.submitted_date,
                 seller: item.seller.name,
             };
         });

        $timeout(function() {
            $('#list-table').DataTable();
        });
    });



 
})

app.controller('overviewCtrl', function(requestService, $scope, $timeout) {
    var map;
    var markers = [];

    requestService.send('get', URL + 'fish_names', {}).then(function(res) {
        $scope.fishNames = res.data.data.map(function(item) {
            return item.common_name;
        });
        setTimeout(function() {
            initMap();
            $scope.fishDropdownClick($scope.fishNames[0]);
        }, 1000);
    });

    $scope.fishDropdownClick = function(fishName, $event) {
        $scope.fishChosen = fishName;
        clearMarkers();
        setMarkers(fishName);

        setChart([820, 932, 901, 934, 1290, 1330, 1320, 50, 59, 300, 200, 500]);
    };
    function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
            zoom: 5,
            center:  new google.maps.LatLng(49.2827, -123.1207),
            streetViewControl: false,
            mapTypeControl: false,
        }); 
    }   

    function setMarkers(fishName) {
        requestService.send('get', URL + 'data/average_price?fish_name=' + fishName, {}).then(function(res) {
            angular.forEach(res.data.data, function(data, location) {
                var marker = new google.maps.Marker({
                    position: new google.maps.LatLng(data.lat, data.lng),
                    map: map,
                });
                var infowindow = new google.maps.InfoWindow({
                    content: location + ' $' + data.average.toFixed(2)
                });
                infowindow.open(map, marker);
                markers.push(marker);
            });
      })
    }
    
    function clearMarkers() {
        angular.forEach(markers, function(marker) {
            marker.setMap(null);
        });
    }
    var chart;
    $timeout(function() {
        chart = echarts.init(document.getElementById('monthly_chart'));
        //setChart([820, 932, 901, 934, 1290, 1330, 1320]);
    })
    
    function setChart(data) {
        var option = {
            xAxis: {
                type: 'category',
                data: ['2017-03', '2017-04', '2017-05', '2017-06', '2017-07', '2017-08', '2017-09',
                        '2017-10', '2017-11', '2017-12', '2018-01', '2018-02']
            },
            yAxis: {
                type: 'value'
            },
            series: [{
                type: 'line',
                data: data,
            }]
        };
        chart.setOption(option);
    }
})