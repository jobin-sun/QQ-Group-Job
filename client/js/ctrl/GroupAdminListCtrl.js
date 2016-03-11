angular.module('myApp')
	.controller("GroupAdminListCtrl",["$scope","$http", "$cookies", function($scope, $http, $cookies){
		$scope.current = 'admin_list';
		if($cookies.get("admin_logined") != "yes"){
			location.href = "#/group/login";
			return;
		}
		$http.get("api/group/admin_list/",{
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
	