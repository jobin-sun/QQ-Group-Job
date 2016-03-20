angular.module('myApp')
	.controller("HrListCtrl",["$scope","$http", '$routeParams','$cookies',function($scope, $http, $routeParams, $cookies){
		if($routeParams.groupId){
			$scope.groupId = parseInt($routeParams.groupId);
			if($scope.groupId == parseInt($cookies.get("auth_groupId"))){
				$scope.code = parseInt($cookies.get("auth_code"));
			}
		}else{
			$scope.code = parseInt($cookies.get("auth_code"));
			$scope.groupId = parseInt($cookies.get("auth_groupId"));
		}
		if($scope.code && $scope.groupId){
			$scope.show = true;
			$http.get("/api/hr/list/",{
				params:{
					groupId: $scope.groupId,
					code: $scope.code
				}
			}).success(function(response){
				if (response.status == "success") {
					$scope.items = response.data
				}else{
					$T.toast(response.msg);
				};
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
		$scope.submit = function(){
			$http.get("/api/hr/list/",{
				params:{
					groupId: $scope.groupId,
					code: $scope.code
				}
			}).success(function(response){
				if (response.status == "success") {
					$cookies.put("auth_code", $scope.code);
					$cookies.put("auth_groupId", $scope.groupId);
					$scope.items = response.data;
					$scope.show = true;
				}else{
					$T.toast(response.msg);
				};
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
	}])
