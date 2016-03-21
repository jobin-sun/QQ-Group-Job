angular.module('myApp')
	.controller("TopCtrl",["$rootScope", "$http", "$cookies", "getUser", function($rootScope, $http, $cookies, getUser){
		if($cookies.get("logined") != "yes"){
			location.href = "#/login";
			return;
		}
		getUser(function(data){
			$rootScope.user = data;
		})
	}])
