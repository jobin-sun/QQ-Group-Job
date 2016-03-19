angular.module('myApp')
	.controller("GroupResumeCtrl",["$scope", "$http", "$cookies", "$routeParams", "getAdmin", function($scope, $http, $cookies, $routeParams, getAdmin){
		if($cookies.get("admin_logined") != "yes"){
			location.href = "#/group/login";
			return;
		}
		getAdmin(function(data){
			$scope.admin = data;
		})
		var oldStatus, oldRank;
		$http.get("/api/group/resume/",{
			params:{
				resumeId: $routeParams.id
			}
		}).success(function(response){
			if (response.status == "success") {
				$scope.data = response.data;
				oldStatus = response.data.status;
				oldRank = response.data.myRank;
				$scope.statusOptions = $T.statusOptions;
				$scope.rankOptions = $T.rankOptions;
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
			if(oldStatus != $scope.data.status){
				param.status = $scope.data.status;
			}
			if(oldRank != $scope.data.myRank){
				param.rank = $scope.data.myRank;
			}
			$http.put("/api/group/resume/",param)
				.success(function(response){
					if(response.status == "success"){
						$T.toast("保存成功");
					}else{
						$T.toast(response.msg);
					}
				}).error(function(){
					$T.toast("服务器错误,请联系系统管理员")
				})

		}
	}])
