angular.module('myApp')
	.controller("HrLogoutCtrl",["$scope","$http","$cookies",function($scope, $http, $cookies){
		$cookies.remove("auth_code");
		if($cookies.get("auth_groupId")){
			location.href="#/hr/"+$cookies.get("auth_groupId")
		}else{
			location.href="#/hr"
		}
	}])
	