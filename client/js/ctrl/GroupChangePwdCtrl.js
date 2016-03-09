angular.module('myApp')
	.controller("GroupChangePwdCtrl",["$scope","$http", "$cookies",function($scope, $http, $cookies){
		$scope.current = 'change_pwd';
		$http.get("/api/group/check_login/").success(function(response){
			if(response.status != "success"){
				location.href = "#/group/login";
			}
		})
		$scope.submit = function(){
			$http.put("/api/group/change_pwd/", {
				password: $scope.password
			}).success(function(response){
				if(response.status == "success"){
					$T.toast("密码已修改,请重新登录");
					location.href = "#/group/logout"
				}else{
					$T.toast(response.msg);
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
	}])
	