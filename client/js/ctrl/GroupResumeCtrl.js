angular.module('myApp')
	.controller("GroupResumeCtrl",["$scope", "myHttp", "$routeParams", function($scope, myHttp, $routeParams){
		var oldStatus, oldRank;
		myHttp.get("/api/group/resume/",{
			resumeId: $routeParams.id
		}).success(function(response){
			$scope.data = response.data;
			oldStatus = response.data.status;
			oldRank = response.data.myRank;
			$scope.statusOptions = $T.statusOptions;
			$scope.rankOptions = $T.rankOptions;
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
			myHttp.put("/api/group/resume/",param)
			.success(function(response){
				$T.toast("保存成功");
			})

		}
	}])
