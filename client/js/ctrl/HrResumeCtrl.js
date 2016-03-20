angular.module('myApp')
	.controller("HrResumeCtrl",["$scope","$http", '$routeParams','$cookies',function($scope, $http, $routeParams, $cookies){
		var code = $cookies.get("auth_code");
		var groupId = $cookies.get("auth_groupId");
		var id = $routeParams.id;
		if(code && groupId && id){
			$http.get("/api/hr/resume/",{
				params:{
					id: id,
					groupId: groupId,
					code: code
				}
			}).success(function(response){
				if (response.status == "success") {
					$scope.data = response.data
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
