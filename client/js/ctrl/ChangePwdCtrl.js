angular.module('myApp')
	.controller("ChangePwdCtrl",["$scope","myHttp", function($scope, myHttp){
		$scope.submit = function(){
			myHttp.put("/api/change_pwd/", {
				password: $scope.password
			}).success(function(response){
				$T.toast("密码已修改,请重新登录");
				location.href = "#/logout"
			})
		}
	}])
	