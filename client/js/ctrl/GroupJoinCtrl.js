angular.module('myApp')
	.controller("GroupJoinCtrl",["$scope","$http", "$cookies",function($scope, $http, $cookies){
		if($cookies.get("admin_logined") == "yes"){
			location.href = "#/group";
			return;
		}
		$scope.submit = function(){
			$http.post("/api/group/join/", {
				groupId: $scope.groupId,
				groupName: $scope.groupName,
				qq: $scope.qq,
				password:$scope.password
			}).success(function(response){
				if(response.status == "success"){
					location.href = "#/group/login"
				}else{
					$T.toast(response.msg);
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
	}])
	