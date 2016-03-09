angular.module('myApp')
	.controller("GroupLoginCtrl",["$scope","$http", "$cookies",function($scope, $http, $cookies){
		$http.get("/api/group/check_login/").success(function(response){
			if(response.status == "success"){
				location.href = "#/group";
			}
		})
		$scope.submit = function(){
			$http.post("/api/group/login/", {
				groupId: $scope.groupId,
				adminQQ: $scope.adminQQ,
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
	