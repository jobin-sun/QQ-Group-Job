angular.module('myApp')
	.controller("ResumeCtrl",["$scope","myHttp","$routeParams", function($scope, myHttp, $routeParams){
		$scope.edit = "edit/";
		if($routeParams.edit == "edit"){
			$scope.canEdit = true;
			$scope.edit = ""
		}
		myHttp.get("/api/resume/",{
			groupId: $routeParams.groupId 
		}).success(function(response){
			if(response.code == 30002){
				location.href = "#/index"
				return;
			}
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
		})
		$scope.delete = function(){
			myHttp.delete("/api/resume/",{
				groupId: $scope.data.groupId
			}).success(function(response){
				$T.toast("更新成功")
				location.href = "#/resumes_list"
			})
		}
		$scope.post = function() {
			myHttp.post('/api/resume/',{
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
				$T.toast("更新成功")
				location.href = "#/resume/"+$scope.data.groupId
			})
		}
		$scope.submit = function(){
			myHttp.put("/api/resume/",{
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
				$T.toast("更新成功")
				$scope.canEdit = false;
			})
		}

		$scope.loginSubmit = function(){
			myHttp.post("/api/login/", {
				qq: $scope.loginQQ,
				password: $scope.loginPassword
			}).success(function(response){
				location.reload();
			})
		}
		
	}])
	