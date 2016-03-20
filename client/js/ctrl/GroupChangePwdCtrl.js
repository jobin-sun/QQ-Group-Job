angular.module('myApp')
	.controller("GroupChangePwdCtrl",["$scope","$http", function($scope, $http){
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
	