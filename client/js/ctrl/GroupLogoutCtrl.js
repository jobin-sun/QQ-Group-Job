angular.module('myApp')
	.controller("GroupLogoutCtrl",["$scope","myHttp",function($scope, myHttp){
		myHttp.get("/api/group/logout/").success(function(response){
			location.href = "#/group/login";
		})
		
	}])
	