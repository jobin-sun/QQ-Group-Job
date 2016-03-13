angular.module('myApp')
	.controller("GroupAdminListCtrl",["$scope","$http", "$cookies", function($scope, $http, $cookies){
		$scope.current = 'admin_list';
		if($cookies.get("admin_logined") != "yes"){
			location.href = "#/group/login";
			return;
		}
		$http.get("api/group/admin_list/").success(function(response){
			if (response.status == "success") {
				$scope.items = []
				try{
					for(var i = 0; i < response.data.length; i++) {
						$scope.items.push(response.data[i]);
					}
				}catch(e){}
				$scope.show = true;
			}else{
			$T.toast(response.msg);
			};
		}).error(function(){
			$T.toast("服务器错误,请联系系统管理员")
		})
		$scope.post = function(){
			$http.post("api/group/admin_list/",{
				qq: $scope.add.qq,
				password: $scope.add.password
			}).success(function(response){
				console.log(response);
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
		$scope.delete = function(id){
			$http.delete("api/group/admin_list/",{
				params:{
					id: id
				}
			}).success(function(response){
				if(response.status == "success"){
					location.reload();
				}else{
					$T.toast(response.msg);
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
	}])
	