angular.module('myApp')
	.controller("IndexCtrl",["$scope", "myHttp", "$cookies", "$rootScope", function($scope, myHttp, $cookies, $rootScope){
		$scope.sexOptions = $T.sexOptions; 
		$scope.eduOptions = $T.eduOptions;
		$scope.submit = function(){
			myHttp.put("/api/", {
				username: $scope.user.username,
				sex: $scope.user.sex,
				age: $scope.user.age,
				yearsOfWorking: $scope.user.yearsOfWorking,
				school: $scope.user.school,
				education: $scope.user.education
			}).success(function(response){
				$T.toast("更新成功");
				$scope.canEdit = false;
			})
		}
	}])
	