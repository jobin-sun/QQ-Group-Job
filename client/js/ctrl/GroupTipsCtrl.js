angular.module('myApp')
	.controller("GroupTipsCtrl",["$scope", "myHttp", function($scope, myHttp){
		myHttp.get("/api/group/check_group/")
		.success(function(response){
			if(response.data.status === 0){
				$scope.showWarning = true
			}
		})
	}])
	