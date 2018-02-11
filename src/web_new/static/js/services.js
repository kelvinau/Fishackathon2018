app.service('requestService', function($http) {
    var url = '';
    this.send = function (type, url, sendParams) {
        return $http[type](url, JSON.stringify(sendParams));
    }
});