angular.module('myApp')
	.controller("NewPwdCtrl",["$scope","myHttp", "$routeParams", "helper", function($scope, myHttp, $routeParams, helper){
		helper.hideLogin();
		var token = $routeParams.token;
		$scope.submit = function(){
			myHttp.put("/api/recover/", {
				token: token,
				password: $scope.password
			}).success(function(response){
				$T.toast("密码已生效，您可以登录了");
			})
		}
	}])
	