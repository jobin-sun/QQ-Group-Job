angular.module('myApp')
	.controller("GroupAdminCtrl",["$scope","$http",function($scope, $http){
		$http.get("api/group/admin/",{
			params:{
				code: $scope.code
			}
		}).success(function(response){
			if (response.status == "success") {
				$scope.items = []
				try{
					for(var i = 0; i < response.data.length; i++) {
						$scope.items.push(response.data[i]);
					}
				}catch(e){}
				$scope.show = true;
			}else{
			$T.toast(response.msg);
			};
		}).error(function(){
			$T.toast("服务器错误,请联系系统管理员")
		})
	}])
	