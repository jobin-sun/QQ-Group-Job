angular.module('myApp')
	.controller("GroupChangePwdCtrl",["$scope","$http", function($scope, $http){
		$scope.submit = function(){
			$http.put("/api/group/change_pwd/", {
				password: $scope.password
			}).success(function(response){
				$T.toast("密码已修改,请重新登录");
				location.href = "#/group/logout"
			})
		}
	}])
	