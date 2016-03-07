angular.module('myApp')
	.controller("IndexCtrl",["$scope","$http","$cookies",function($scope, $http, $cookies){
		$http.get("/api/check_login/").success(function(response){
			if(response.status != "success"){
				location.href = "#/login";
			}
		})

		$http.get("/api/").success(function(response){
			if(response.status == "success"){
				$scope.username = response.data.username;
				$scope.qq = parseInt(response.data.qq);
				$scope.sexOptions = $T.sexOptions; 
    			$scope.sex = response.data.sex;
				$scope.age = response.data.age;
				$scope.yearsOfWorking = response.data.yearsOfWorking;
				$scope.school = response.data.school;
				$scope.eduOptions = $T.eduOptions;
				$scope.education = response.data.education;
			}else{
				$T.toast(response.msg)
			}
		}).error(function(){
			$T.toast("服务器错误,请联系系统管理员")
		})
		$scope.submit = function(){
			$http.put("/api/", {
				username: $scope.username,
				sex: $scope.sex,
				age: $scope.age,
				yearsOfWorking: $scope.yearsOfWorking,
				school: $scope.school,
				education: $scope.education
			}).success(function(response){
				if(response.status == "success"){
					$T.toast("更新成功");
					//location.reload();
				}else{
					$T.toast(response.msg)
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
	}])
	