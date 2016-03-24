angular.module('myApp')
	.controller("GroupTopCtrl",["$scope", "myHttp", "$cookies", "$rootScope", function($scope, myHttp, $cookies, $rootScope){
		if($cookies.get("admin_logined") != "yes"){
			$rootScope.switchLogin = "group";
			return;
		}
		myHttp.get("/api/group/admin/").success(function(response){
			$rootScope.admin = response.data;
		})
		$scope.put = function(){
			myHttp.put("/api/group/admin/",{
				nick : $scope.admin.nick
			}).success(function(response){
				$T.toast("修改成功");
				$scope.admin = response.data;
				$scope.nickEdit = false;
			})
		}
		$scope.hide_pop = function(){
			$scope.nickEdit = false;
		}
		$scope.stopPropagation = function($event){
			$event.stopPropagation();
		}
	}])
