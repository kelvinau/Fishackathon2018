app.config(function($stateProvider, $urlRouterProvider) {

    var mainState = {
      name: 'main',
      resolve: {
        userLoggedIn: function ($q, requestService, $rootScope) {
          var deferred = $q.defer();
          requestService.send('get',  URL + 'seller/is_logged_in', {}).then(function(res) {
              $rootScope.firstLoaded = true;
              if (res.data.data.logged_in) {
                $rootScope.user = res.data.data.user;
              }
              deferred.resolve();
          });
          return deferred.promise;
        }
    }
    }

    var loginState = {
      name: 'main.login',
      url: '/login',
      templateUrl: '/partial/login.html',
      controller: 'loginCtrl',
      resolve: {
        userLoggedIn: function($rootScope, $state) {
          if ($rootScope.user) {
            $state.go('main.list');
          }
          return;
        }
      }
    }
  
    var signupState = {
      name: 'main.signup',
      url: '/signup',
      templateUrl: '/partial/signup.html',
      controller: 'signupCtrl',
      resolve: {
        userLoggedIn: function($rootScope, $state) {
          if ($rootScope.user) {
            $state.go('main.list');
          }
          return;
        }
      }
    }
  
    var submitState = {
      name: 'main.submit',
      url: '/submit',
      templateUrl: '/partial/submit.html',
      controller: 'submitCtrl',
      resolve: {
        userLoggedIn: function($rootScope, $state) {
          if (!$rootScope.user) {
            $state.go('main.login');
          }
          return;
        }
      }
    }
  
    var listState = {
      name: 'main.list',
      url: '/list',
      templateUrl: '/partial/list.html',
      controller: 'listCtrl',
      resolve: {
        userLoggedIn: function($rootScope, $state) {
          if (!$rootScope.user) {
            $state.go('main.login');
          }
          return;
        }
      }
    }
    
    var overviewState = {
      name: 'main.overview',
      url: '/overview',
      templateUrl: '/partial/overview.html',
      controller: 'overviewCtrl',
      resolve: {
        userLoggedIn: function($rootScope, $state) {
          if (!$rootScope.user) {
            $state.go('main.login');
          }
          return;
        }
      }
    }

    $stateProvider.state(mainState);
    $stateProvider.state(overviewState);
    $stateProvider.state(loginState);
    $stateProvider.state(signupState);
    $stateProvider.state(submitState);
    $stateProvider.state(listState);
  });