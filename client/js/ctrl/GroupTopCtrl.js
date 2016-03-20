angular.module('myApp')
	.controller("GroupTopCtrl",["$scope","$http","$cookies","getAdmin", "$rootScope", function($scope, $http, $cookies, getAdmin, $rootScope){
		if($cookies.get("admin_logined") != "yes"){
			location.href = "#/group/login";
			return;
		}
		getAdmin(function(data){
			$rootScope.admin = data;
		})
		$scope.put = function(){
			$http.put("/api/group/admin/",{
				nick : $scope.admin.nick
			}).success(function(response){
				if (response.status == "success") {
					$T.toast("修改成功");
					$scope.admin = response.data;
					$scope.nickEdit = false;
				}else{
					$T.toast(response.msg);
				}

			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
		$scope.hide_pop = function(){
			$scope.nickEdit = false;
		}
		$scope.stopPropagation = function($event){
			$event.stopPropagation();
		}
	}])
