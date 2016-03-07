angular.module('myApp')
	.controller("RegCtrl",["$scope","$http","$cookies",function($scope, $http, $cookies){
		$http.get("/api/check_login/").success(function(response){
			if(response.status == "success"){
				location.href = "#/index";
			}
		})
		$scope.submit = function(){
			$http.post("/api/reg/",{
				username:$scope.username,
				qq:$scope.qq,
				password:$scope.password
			}).success(function(response){
				if(response.status == "success"){
					location.href="#/login"
				}else{
					$T.toast(response.msg)
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})

		}
	}])
	