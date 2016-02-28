angular.module('myApp')
	.controller("GroupJoinCtrl",["$scope","$http", "$cookies",function($scope, $http, $cookies){
		$http.get("/api/group/check_login/").success(function(response){
			if(response.status == "success"){
				location.href = "#/group";
			}
		})
		$scope.submit = function(){
			$http.post("/api/group/join/", {
				groupId: $scope.groupId,
				groupName: $scope.groupName,
				adminName: $scope.adminName,
				password:$scope.password,
				requestMsg:$scope.requestMsg
			}).success(function(response){
				if(response.status == "success"){
					//location.href = "#/index"
				}else{
					$T.toast(response.msg);
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
	}])
	