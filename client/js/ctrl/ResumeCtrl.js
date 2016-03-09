angular.module('myApp')
	.controller("ResumeCtrl",["$scope","$http","$routeParams",function($scope, $http, $routeParams){
		$http.get("/api/check_login/").success(function(response){
			if(response.status != "success"){
				location.href = "#/login";
			}
		})
		$http.get("/api/resume/",{
			params:{
				groupId: $routeParams.groupId 
			}
		}).success(function(response){
			if(response.status == "success"){
				if(response.count == 0){
					$scope.isExist = false;
					$scope.canEdit = true;
				}else{
					$scope.isExist = true
					$scope.canEdit = false
				}
					$scope.id=response.data.id
					$scope.email=response.data.email
					$scope.username=response.data.username
					$scope.qq=response.data.qq
					$scope.sex=response.data.sex
					$scope.age=response.data.age
					$scope.yearsOfWorking=response.data.yearsOfWorking
					$scope.school=response.data.school
					$scope.education=response.data.education
					$scope.groupId=response.data.groupId
					$scope.lastDate=response.data.lastDate
					$scope.status=response.data.status
					$scope.display= response.data.display
					$scope.content = response.data.content
					$scope.sexOptions = $T.sexOptions; 
					$scope.eduOptions = $T.eduOptions;
			}else{
				$T.toast(response.msg);
			}
		}).error(function(){
			$T.toast("服务器错误,请联系系统管理员")
		})
		$scope.delete = function(){
			$http.delete("/api/resume/",{
				params:{
					groupId: $scope.groupId
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
				'email':$scope.email,
				'groupId':$scope.groupId,
				'username':$scope.username,
				'qq':$scope.qq,
				'sex':$scope.sex,
				'age':$scope.age,
				'yearsOfWorking':$scope.yearsOfWorking,
				'school':$scope.school,
				'education':$scope.education,
				'content':$scope.content,
				'display':$scope.display
			}).success(function(response){
				if(response.status == "success"){
					$T.toast("更新成功")
					location.reload();
				}else{
					$T.toast(response.msg)
				}
			}).error(function() {
				$T.toast("服务器错误,请联系系统管理员")
			});
		}
		$scope.submit = function(){
			$http.put("/api/resume/",{
				id: $scope.id,
				email: $scope.email,
				username:$scope.username,
				qq:$scope.qq,
				sex:$scope.sex,
				age:$scope.age,
				yearsOfWorking:$scope.yearsOfWorking,
				school:$scope.school,
				education:$scope.education,
				display: $scope.display,
				content: $scope.content
			}).success(function(response){
				if(response.status == "success"){
					$T.toast("更新成功")
					location.reload()
				}else{
					$T.toast(response.msg)
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
		
	}])
	