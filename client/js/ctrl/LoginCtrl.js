angular.module('myApp')
	.controller("LoginCtrl",["$scope","$http", "$cookies",function($scope, $http, $cookies){
		$http.get("/api/check_login/").success(function(response){
			if(response.status == "success"){
				location.href = "#/index";
			}
		})
		$scope.submit = function(){
			$http.post("/api/login/", {
				email: $scope.email,
				password: $scope.password
			}).success(function(response){
				if(response.status == "success"){
					location.href = "#/index"
				}else{
					$T.toast(response.msg);
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
	}])
	