angular.module('myApp')
	.controller("GroupAuthCodeCtrl",["$scope","$http", "$cookies",function($scope, $http, $cookies){
		$scope.current = 'auth_code';
		if($cookies.get("admin_logined") != "yes"){
			location.href = "#/group/login";
			return;
		}
		$http.get("api/group/auth_code/").success(function(response){
			if(response.status == "success"){
				$scope.items = response.data
			}else{
				$T.toast(response.msg)
			}	
		}).error(function(){
			$T.toast("服务器错误")
		})
		$scope.post = function(){
			$http.post("api/group/auth_code/", {
				code: $scope.add.code
			}).success(function(response){
				if(response.status == "success"){
					location.reload();
				}else{
					$T.toast(response.msg)
				}	
			}).error(function(){
				$T.toast("服务器错误")
			})
		}
		$scope.delete = function(id){
			$http.delete("api/group/auth_code/", {
				params:{
					id: id
				}
			}).success(function(response){
				if(response.status == "success"){
					location.reload();
				}else{
					$T.toast(response.msg)
				}
			}).error(function(){
				$T.toast("服务器错误")
			})
		}
	}])
	