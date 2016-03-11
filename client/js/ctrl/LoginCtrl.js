angular.module('myApp')
	.controller("LoginCtrl",["$scope","$http", "$cookies",function($scope, $http, $cookies){
		if($cookies.get("logined") == "yes"){
			location.href = "#/index";
			return;
		}
		$scope.submit = function(){
			$http.post("/api/login/", {
				qq: $scope.qq,
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
	