angular.module('myApp')
	.controller("ChangePwdCtrl",["$scope","$http","$cookies",function($scope, $http, $cookies){
		if($cookies.get("logined") != "yes"){
			location.href = "#/login";
			return;
		}
		$scope.submit = function(){
			$http.put("/api/change_pwd/", {
				password: $scope.password
			}).success(function(response){
				if(response.status == "success"){
					$T.toast("密码已修改,请重新登录");
					location.href = "#/logout"
				}else{
					$T.toast(response.msg);
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
	}])
	