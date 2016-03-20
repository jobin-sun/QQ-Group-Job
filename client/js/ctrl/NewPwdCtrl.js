angular.module('myApp')
	.controller("NewPwdCtrl",["$scope","$http", "$routeParams", function($scope, $http, $routeParams){
		var token = $routeParams.token;
		$scope.submit = function(){
			$http.put("/api/recover/", {
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
	