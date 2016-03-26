angular.module('myApp')
	.controller("HrResumeCtrl",["$scope","myHttp", '$routeParams','$cookies','helper', function($scope, myHttp, $routeParams, $cookies, helper){
		helper.hideLogin();
		var code = $cookies.get("auth_code");
		var groupId = $cookies.get("auth_groupId");
		var id = $routeParams.id;
		if(code && groupId && id){
			myHttp.get("/api/hr/resume/",{
				id: id,
				groupId: groupId,
				code: code
			}).success(function(response){
				$scope.data = response.data
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
