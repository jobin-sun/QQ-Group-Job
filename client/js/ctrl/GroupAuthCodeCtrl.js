angular.module('myApp')
	.controller("GroupAuthCodeCtrl",["$scope","$http", "$cookies",function($scope, $http, $cookies){
		$scope.current = 'auth_code';
		if($cookies.get("admin_logined") != "yes"){
			location.href = "#/group/login";
			return;
		}
	}])
	