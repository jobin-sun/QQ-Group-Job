angular.module('myApp')
	.controller("GroupLoginCtrl",["$scope","$http", "$cookies","$routeParams", function($scope, $http, $cookies, $routeParams){
		if($cookies.get("admin_logined") == "yes"){
			location.href = "#/group";
			return;
		}
		if($routeParams.groupId){
			$scope.groupId = parseInt($routeParams.groupId);
		}
		$scope.submit = function(){
			$http.post("/api/group/login/", {
				groupId: $scope.groupId,
				qq: $scope.qq,
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
	