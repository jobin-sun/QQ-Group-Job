angular.module('myApp')
	.controller("IndexCtrl",["$scope","$http","$cookies", "getUser", function($scope, $http, $cookies, getUser){
		if($cookies.get("logined") != "yes"){
			location.href = "#/login";
			return;
		}
		getUser(function(data){
			$scope.username = data.username;
			$scope.qq = parseInt(data.qq);
			$scope.sexOptions = $T.sexOptions; 
    		$scope.sex = data.sex;
			$scope.age = data.age;
			$scope.yearsOfWorking = data.yearsOfWorking;
			$scope.school = data.school;
			$scope.eduOptions = $T.eduOptions;
			$scope.education = data.education;
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
					location.reload();
				}else{
					$T.toast(response.msg)
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
	}])
	