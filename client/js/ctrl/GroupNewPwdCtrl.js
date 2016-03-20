angular.module('myApp')
	.controller("GroupNewPwdCtrl",["$scope","$http", "$routeParams", function($scope, $http, $routeParams){
		var token = $routeParams.token;
		$scope.submit = function(){
			$http.put("/api/group/recover/", {
				token: token,
				password: $scope.password
			}).success(function(response){
				if(response.status == "success"){
					$T.toast("密码已生效，您可以登录了");
				}else{
					$T.toast(response.msg);
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
	}])
	