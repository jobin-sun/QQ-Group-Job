angular.module('myApp')
	.controller("TopCtrl",["$scope","$http","$cookies","getUser", function($scope, $http, $cookies, getUser){
		if($cookies.get("logined") != "yes"){
			location.href = "#/login";
			return;
		}
		getUser(function(data){
			$scope.user = data;
		})
	}])
