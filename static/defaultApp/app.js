(function () {
  
    var app = angular.module('serviceApp', ['ngRoute', 'ngSanitize','ngAnimate','ngTouch','wc.directives', 'ui.bootstrap', 'infinite-scroll','breeze.angular','toaster'],
	function($httpProvider) {
	  // Use x-www-form-urlencoded Content-Type
	  $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';

	  /**
	   * The workhorse; converts an object to x-www-form-urlencoded serialization.
	   * @param {Object} obj
	   * @return {String}
	   */
	  var param = function(obj) {
		var query = '', name, value, fullSubName, subName, subValue, innerObj, i;

		for(name in obj) {

		  value = obj[name];
		  if(value instanceof Array) {
			for(i=0; i<value.length; ++i) {
			  subValue = value[i];
			  fullSubName = name + '[' + i + ']';
			  innerObj = {};
			  innerObj[fullSubName] = subValue;
			  query += param(innerObj) + '&';
			}
		  }
		  else if(value instanceof Object) {
			for(subName in value) {
			  subValue = value[subName];
			  fullSubName = name + '[' + subName + ']';
			  innerObj = {};
			  innerObj[fullSubName] = subValue;
			  query += param(innerObj) + '&';
			}
		  }
		  else if(value !== undefined && value !== null)
			query += encodeURIComponent(name) + '=' + encodeURIComponent(value) + '&';
		}

		return query.length ? query.substr(0, query.length - 1) : query;
	  };

	  // Override $http service's default transformRequest
	  $httpProvider.defaults.transformRequest = [function(data) {
		return angular.isObject(data) && String(data) !== '[object File]' ? param(data) : data;
	  }];
	});

	app.factory('displayModel', function() {
    	  return {
    	    displayModel: 'block'
    	  }
	});

    app.config(['$routeProvider', function ($routeProvider) {
        var viewBase = '/born_service/static/defaultApp/views/';
        $routeProvider
	        .when('/services', {
	            controller: 'ServiceController',
	            templateUrl: viewBase + 'services/services.html',
	            controllerAs: 'vm'
	        })
			.when('/services/:serviceId', {
	            controller: 'ServiceController',
	            templateUrl: viewBase + 'services/servicesDetail.html',
	            controllerAs: 'vm'
	        })
			.when('/orders', {
	        	controller: 'OrderController',
	        	templateUrl: viewBase + 'orders/orders.html',
	        	controllerAs: 'vm'
	        })
			.when('/orders/:orderId', {
	        	controller: 'OrderController',
	        	templateUrl: viewBase + 'orders/ordersDetail.html',
	        	controllerAs: 'vm'
	        })
			.when('/contents', {
	        	controller: 'ContentController',
	        	templateUrl: viewBase + 'contents/contents.html',
	        	controllerAs: 'vm',
	        })
	        .when('/contents/:contentId', {
	        	controller: 'ContentController',
	        	templateUrl: viewBase + 'contents/contentDetail.html',
	        	controllerAs: 'vm'
	        })
	        .when('/register/:serviceId', {
	        	controller: 'RegisterController',
	        	templateUrl: viewBase + 'services/register.html',
	        	controllerAs: 'vm'
	        })	        

            .otherwise({ redirectTo: '/services' });
    }]);
    
}());


