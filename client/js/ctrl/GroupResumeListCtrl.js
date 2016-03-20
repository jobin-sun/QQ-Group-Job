angular.module('myApp')
	.controller("GroupResumeListCtrl",["$scope", "$http", function($scope, $http){
		var list = {};
		$http.get("/api/group/resume_list/",{
			params:{
				groupId: $scope.groupId
			}
		}).success(function(response){
			if (response.status == "success") {
				$scope.items = response.data
			}else{
				$T.toast(response.msg);
			};
		}).error(function(){
			$T.toast("服务器错误,请联系系统管理员")
		})

		$scope.allow = function(resume){
			$http.put("/api/group/resume/",{
				resumeId: resume.id,
				status: 1
			}).success(function(response){
				if(response.status == "success"){
					$T.toast("保存成功");
					resume.status = 1;
				}else{
					$T.toast(response.msg)
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
		$scope.deny = function(resume){
			$http.put("/api/group/resume/",{
				resumeId: resume.id,
				status: 2
			}).success(function(response){
				if(response.status == "success"){
					$T.toast("保存成功");
					resume.status = 2;
				}else{
					$T.toast(response.msg)
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
	}])
