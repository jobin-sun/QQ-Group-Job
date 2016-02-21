angular.module('myApp')
	.controller("ApplyCtrl", ["$scope", "$http", "$routeParams", function($scope, $http, $routeParams) {
		$http.get("/api/check_login/").success(function(response) {
			if (response.status != "success") {
				location.href = "#/login";
			}
		})
		if ($routeParams.groupId) {
			$scope.groupId = $routeParams.groupId;
			$http.get('/api/resume/', {
				params: {
					groupId: $routeParams.groupId
				}
			}).success(function(response) {
				if (response.status == 'success') {
					if (response.count == 0) {
						$scope.email = response.data.email;
						$scope.username = response.data.username;
						$scope.qq = parseInt(response.data.qq);
						$scope.sex = 1;response.data.sex;
						$scope.age = response.data.age;
						$scope.yearsOfWorking = response.data.yearsOfWorking;
						$scope.school = response.data.school;
						$scope.education = response.data.education;
						$scope.showApply = true;

					} else if (response.count == 1) {
						$scope.email = response.data.email;
						$scope.username = response.data.username;
						$scope.qq = parseInt(response.data.qq);
						$scope.sex = response.data.sex;
						$scope.age = response.data.age;
						$scope.yearsOfWorking = response.data.yearsOfWorking;
						$scope.school = response.data.school;
						$scope.education = response.data.education;
						$scope.lastDate = response.data.lastDate;
						$scope.content = response.data.content;
						$scope.display = response.data.display;
						$scope.status = response.data.status;
					}

				} else {
					$T.toast(response.msg);
				}
			})
		} else {

		}

		$scope.submit = function() {
			$http.post('/api/resume/',{
				'email':$scope.email,
				'groupId':$scope.groupId,
				'username':$scope.username,
				'qq':String($scope.qq),
				'sex':$scope.sex,
				'age':$scope.age,
				'yearsOfWorking':$scope.yearsOfWorking,
				'school':$scope.school,
				'education':$scope.education,
				'content':$scope.content,
				'display':$scope.display
			}).success(function(response){
				console.log(response);
			}).error(function() {
				$T.toast("服务器错误,请联系系统管理员")
			});
		}
	}])