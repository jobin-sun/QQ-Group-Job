angular.module('myApp')
	.controller("GroupResumeListCtrl",["$scope", "$http", "$cookies", function($scope, $http, $cookies){
		if($cookies.get("admin_logined") != "yes"){
			location.href = "#/group/login";
			return;
		}
		$scope.current = 'resume_list';
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
		$scope.openResume = function(id){
			location.href = "#/group/resume/"+id;
		}
		$scope.delete = function(resumeId){
			$http.delete("/api/group/resume/",{
				params:{
					resumeId: resumeId
				}
			}).success(function(response){
				if(response.status == "success"){
					$T.toast("简历已删除");
					location.href = "#/group/resume_list/"
				}else{
					$T.toast(response.msg)
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
	}])
