angular.module('myApp')
	.controller("GroupResumeCtrl",["$scope", "$http", "$cookies", "$routeParams", function($scope, $http, $cookies, $routeParams){
		if($cookies.get("admin_logined") != "yes"){
			location.href = "#/group/login";
			return;
		}
		$scope.current = 'resume_list';
		var list = {};
		var oldStatus, oldRank;
		$http.get("/api/group/resume/",{
			params:{
				resumeId: $routeParams.id
			}
		}).success(function(response){
			if (response.status == "success") {
				$scope.item = response.data;
				oldStatus = response.data.status;
				oldRank = response.data.myRank;
				$scope.statusOptions = $T.statusOptions;
			}else{
				$T.toast(response.msg);
			};
		}).error(function(){
			$T.toast("服务器错误,请联系系统管理员")
		})
		$scope.put = function(){
			var param = {
				resumeId: $routeParams.id
			};
			if(oldStatus != $scope.item.status){
				param.status = $scope.item.status;
			}
			if(oldRank != $scope.item.myRank){
				param.rank = $scope.item.myRank;
			}
			$http.put("/api/group/resume/",param)
				.success(function(response){
					if(response.status == "success"){
						$T.toast("保存成功");
						location.reload();
					}else{
						$T.toast(response.msg);
					}
				}).error(function(){
					$T.toast("服务器错误,请联系系统管理员")
				})

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
