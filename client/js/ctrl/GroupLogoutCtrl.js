angular.module('myApp')
	.controller("GroupLogoutCtrl",["$scope","$http","$cookies",function($scope, $http, $cookies){
		$http.get("/api/group/logout/").success(function(response){
			if(response.status == "success"){
				location.href = "#/group/login";
			}else{
				$T.toast("退出失败")
			}
		})
		
	}])
	