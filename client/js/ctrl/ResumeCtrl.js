angular.module('myApp')
	.controller("ResumeCtrl",["$scope","$http","$routeParams","$cookies", function($scope, $http, $routeParams, $cookies){
		if($cookies.get("logined") != "yes"){
			$scope.showLogin = true;
		}
		$scope.edit = "edit/";
		if($routeParams.edit == "edit"){
			$scope.canEdit = true;
			$scope.edit = ""
		}
		$http.get("/api/resume/",{
			params:{
				groupId: $routeParams.groupId 
			}
		}).success(function(response){
			if(response.status == "success"){
				if(response.count == 0){
					$scope.isExist = false;
					location.href = "#/resume/edit/"+$routeParams.groupId;
				}else{
					$scope.isExist = true;
				}
				response.data.qq = parseInt(response.data.qq);
				$scope.data = response.data;
				$scope.data.sexOptions = $T.sexOptions; 
				$scope.data.eduOptions = $T.eduOptions;
			}else{
				$T.toast(response.msg);
			}
		}).error(function(){
			$T.toast("服务器错误,请联系系统管理员")
		})
		$scope.delete = function(){
			$http.delete("/api/resume/",{
				params:{
					groupId: $scope.data.groupId
				}
			}).success(function(response){
				if(response.status == "success"){
					$T.toast("更新成功")
					location.href = "#/resumes_list"
				}else{
					$T.toast(response.msg)
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
		$scope.post = function() {
			$http.post('/api/resume/',{
				'email':$scope.data.email,
				'jobTitle': $scope.data.jobTitle,
				'groupId':$scope.data.groupId,
				'username':$scope.data.username,
				'qq':$scope.data.qq,
				'sex':$scope.data.sex,
				'age':$scope.data.age,
				'yearsOfWorking':$scope.data.yearsOfWorking,
				'school':$scope.data.school,
				'education':$scope.data.education,
				'content':$scope.data.content,
				'display':$scope.data.display
			}).success(function(response){
				if(response.status == "success"){
					$T.toast("更新成功")
					location.href = "#/resume/"+$scope.data.groupId

				}else{
					$T.toast(response.msg)
				}
			}).error(function() {
				$T.toast("服务器错误,请联系系统管理员")
			});
		}
		$scope.submit = function(){
			$http.put("/api/resume/",{
				id: $scope.data.id,
				jobTitle: $scope.data.jobTitle,
				email: $scope.data.email,
				username:$scope.data.username,
				qq:$scope.data.qq,
				sex:$scope.data.sex,
				age:$scope.data.age,
				yearsOfWorking:$scope.data.yearsOfWorking,
				school:$scope.data.school,
				education:$scope.data.education,
				display: $scope.data.display,
				content: $scope.data.content
			}).success(function(response){
				if(response.status == "success"){
					$T.toast("更新成功")
					$scope.canEdit = false;
				}else{
					$T.toast(response.msg)
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}

		$scope.loginSubmit = function(){
			$http.post("/api/login/", {
				qq: $scope.loginQQ,
				password: $scope.loginPassword
			}).success(function(response){
				if(response.status == "success"){
					location.reload();
				}else{
					$T.toast(response.msg);
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
		
	}])
	