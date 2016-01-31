angular.module('myApp')
	.controller("LogoutCtrl",["$scope","$http","$cookies",function($scope, $http, $cookies){
		$http.get("/api/logout/").success(function(response){
			if(response.status == "success"){
				location.href = "#/login";
			}else{
				$T.toast("退出失败")
			}
		})
		
	}])
	