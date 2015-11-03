(function () {

    var injectParams = ['$http', '$q'];

    var productsFactory = function ($http, $q) {
        var serviceBase = '/api/',
            factory = {};

        //获取服务列表
        factory.getServices = function () {
        	 return $http.get(serviceBase + 'services').then(function(results) {
     				return results.data;
     			});
        };

        //获取最新动态列表分页
        factory.getServicesPages = function (pageIndex) {
        	 return $http.get(serviceBase + 'services', {
     			params : {
                    index:pageIndex
     			}
     			}).then(function(results) {
     				return results.data;
     			});
        };


        //获取服务详细信息
        factory.getService = function (id) {
        	return $http.get(serviceBase + 'services/' + id).then(function(results) {
        		return results.data;
        	});
        };

        //获取我注册的服务
        factory.getOrders = function () {
        	return $http.get(serviceBase + 'orders').then(function(results) {
        		return results.data;
        	});
        };

        //获取我注册的服务详细信息
        factory.getOrder = function (id) {
        	return $http.get(serviceBase + 'orders/' + id).then(function(results) {
        		return results.data;
        	});
        };

        //获取最新动态列表
        factory.getContents = function () {
        	return $http.get(serviceBase + 'contents').then(function (results) {
        		return results.data;
        	});
        };

        //获取最新动态列表分页
        factory.getContentsPages = function (pageIndex) {
        	 return $http.get(serviceBase + 'contents', {
     			params : {
                    index:pageIndex
     			}
     			}).then(function(results) {
     				return results.data;
     			});
        };


        //获取动态详细信息
        factory.getContent = function (id) {
        	return $http.get(serviceBase + 'contents/' + id).then(function(results) {
        		return results.data;
        	});
        };

        //获取个人详细信息
        factory.getAccount = function (id) {
            return $http.get(serviceBase + 'account/' + id).then(function (results) {
                return results.data;
            });
        };

        //注册登记
        factory.register = function (account) {
            return $http.post(serviceBase + 'register', account).then(function (status) {
                return status.data;
            });
        };

        return factory;
    };

    productsFactory.$inject = injectParams;

    angular.module('serviceApp').factory('shopService', productsFactory);

}());