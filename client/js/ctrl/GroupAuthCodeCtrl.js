angular.module('myApp')
	.controller("GroupAuthCodeCtrl",["$scope","$http", "$cookies", "getAdmin", function($scope, $http, $cookies, getAdmin){
		if($cookies.get("admin_logined") != "yes"){
			location.href = "#/group/login";
			return;
		}
		getAdmin(function(data){
			$scope.admin = data;
		})
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
					$scope.add = undefined;
					$scope.showCodeAdd = false;
					$scope.items.push(response.data);
				}else{
					$T.toast(response.msg)
				}	
			}).error(function(){
				$T.toast("服务器错误")
			})
		}
		$scope.delete = function(item){
			$http.delete("api/group/auth_code/", {
				params:{
					id: item.id
				}
			}).success(function(response){
				if(response.status == "success"){
					$T.toast("删除成功");
					item.hide = true;
				}else{
					$T.toast(response.msg)
				}
			}).error(function(){
				$T.toast("服务器错误")
			})
		}
		$scope.hide_pop = function(){
			$scope.showCodeAdd = false;
		}
		$scope.stopPropagation = function($event){
			$event.stopPropagation();
		}
	}])
	