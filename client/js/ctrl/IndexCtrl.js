angular.module('myApp')
	.controller("IndexCtrl",["$scope","$http", "getUser", function($scope, $http, getUser){
		getUser(function(data){
			$scope.user = data;
			$scope.sexOptions = $T.sexOptions; 
			$scope.eduOptions = $T.eduOptions;
		})
		$scope.submit = function(){
			$http.put("/api/", {
				username: $scope.user.username,
				sex: $scope.user.sex,
				age: $scope.user.age,
				yearsOfWorking: $scope.user.yearsOfWorking,
				school: $scope.user.school,
				education: $scope.user.education
			}).success(function(response){
				if(response.status == "success"){
					$T.toast("更新成功");
					$scope.canEdit = false;
				}else{
					$T.toast(response.msg)
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
	}])
	