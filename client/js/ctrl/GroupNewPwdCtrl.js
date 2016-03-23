angular.module('myApp')
	.controller("GroupNewPwdCtrl",["$scope","myHttp", "$routeParams", function($scope, myHttp, $routeParams){
		var token = $routeParams.token;
		$scope.submit = function(){
			myHttp.put("/api/group/recover/", {
				token: token,
				password: $scope.password
			}).success(function(response){
				$T.toast("密码已生效，您可以登录了");
			})
		}
	}])
	