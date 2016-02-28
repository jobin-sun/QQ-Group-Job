angular.module('myApp')
	.controller("GroupChangePwdCtrl",["$scope","$http", "$cookies",function($scope, $http, $cookies){
		$scope.current = 'change_pwd';
		$http.get("/api/group/check_login/").success(function(response){
			if(response.status != "success"){
				location.href = "#/group/login";
			}
		})
	}])
	