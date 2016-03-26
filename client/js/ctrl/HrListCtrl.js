angular.module('myApp')
	.controller("HrListCtrl",["$scope","myHttp", '$routeParams','$cookies', 'helper', function($scope, myHttp, $routeParams, $cookies, helper){
		helper.hideLogin();
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
			myHttp.get("/api/hr/list/",{
					groupId: $scope.groupId,
					code: $scope.code
			}).success(function(response){
				$scope.items = response.data
			})
		}
		$scope.submit = function(){
			myHttp.get("/api/hr/list/",{
				groupId: $scope.groupId,
				code: $scope.code
			}).success(function(response){
				$cookies.put("auth_code", $scope.code);
				$cookies.put("auth_groupId", $scope.groupId);
				$scope.items = response.data;
				$scope.show = true;
			})
		}
	}])
