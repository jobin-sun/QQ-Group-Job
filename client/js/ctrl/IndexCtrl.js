angular.module('myApp')
	.controller("IndexCtrl",["$scope","$http","$cookies",function($scope, $http, $cookies){
		$http.get("/api/").success(function(response){
			if(response.status == "success"){
				$scope.email = response.data.email;
				$scope.username = response.data.username;
				$scope.qq = parseInt(response.data.qq);
				$scope.display = response.data.display;
				$scope.content = response.data.content;
			}else{
				$T.toast(response.msg)
			}
		}).error(function(){
			$T.toast("服务器错误,请联系系统管理员")
		})
		$scope.submit = function(){
			$http.put("/api/", {
				username: $scope.username,
				qq: $scope.qq,
				display: $scope.display,
				content: $scope.content
			}).success(function(response){
				if(response.status == "success"){
					$T.toast("更新成功");
					location.reload();
				}else{
					$T.toast(response.msg)
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
	}])
	