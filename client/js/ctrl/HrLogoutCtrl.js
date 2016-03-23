angular.module('myApp')
	.controller("HrLogoutCtrl",["$scope","$cookies",function($scope, $cookies){
		$cookies.remove("auth_code");
		if($cookies.get("auth_groupId")){
			location.href="#/hr/"+$cookies.get("auth_groupId")
		}else{
			location.href="#/hr"
		}
	}])
	