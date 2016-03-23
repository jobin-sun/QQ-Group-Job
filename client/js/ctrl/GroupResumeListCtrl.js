angular.module('myApp')
	.controller("GroupResumeListCtrl",["$scope", "myHttp", function($scope, myHttp){
		var list = {};
		myHttp.get("/api/group/resume_list/",{
			groupId: $scope.groupId
		}).success(function(response){
			$scope.items = response.data
		})
		$scope.allow = function(resume){
			myHttp.put("/api/group/resume/",{
				resumeId: resume.id,
				status: 1
			}).success(function(response){
				$T.toast("保存成功");
				resume.status = 1;
			})
		}
		$scope.deny = function(resume){
			myHttp.put("/api/group/resume/",{
				resumeId: resume.id,
				status: 2
			}).success(function(response){
				$T.toast("保存成功");
				resume.status = 2;
			})
		}
	}])
