angular.module('myApp')
	.controller("GroupAuthCodeCtrl",["$scope","$http", "$cookies",function($scope, $http, $cookies){
		$scope.current = 'auth_code';
		$http.get("/api/group/check_login/").success(function(response){
			if(response.status != "success"){
				location.href = "#/group/login";
			}
		})
	}])
	