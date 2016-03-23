angular.module('myApp')
	.controller("LogoutCtrl",["$scope","myHttp",function($scope, myHttp){
		myHttp.get("/api/logout/").success(function(response){
			location.href = "#/login";
		})
		
	}])
	