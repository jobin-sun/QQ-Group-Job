angular.module('myApp')
	.controller("GroupLoginCtrl",["$scope","$http", "$cookies",function($scope, $http, $cookies){
		if($cookies.get("admin_logined") == "yes"){
			location.href = "#/group";
			return;
		}
		$scope.submit = function(){
			$http.post("/api/group/login/", {
				groupId: $scope.groupId,
				aa: $scope.qq,
				password:$scope.password
			}).success(function(response){
				if(response.status == "success"){
					location.href = "#/group/"
				}else{
					$T.toast(response.msg);
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
	}])
	