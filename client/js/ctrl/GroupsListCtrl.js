angular.module('myApp')
	.controller("GroupsListCtrl",["$scope","$http","$cookies",function($scope, $http, $cookies){
		if($cookies.get("logined") != "yes"){
			location.href = "#/login";
			return;
		}
		var statusOb = ['申请中', '允许的', '拒绝的', '拉黑的'];
		$http.get('/api/groups_list/').success(function(response){
			if(response.status == 'success'){
				$scope.items = [];
				for(var i=0; i<response.data.length; i++){
					$scope.items.push({
						'groupId': response.data[i].groupId,
						'status': statusOb[response.data[i].status]
					});
				}


			}else{
				$T.toast(response.msg);
			}
		}).error(function(){
			$T.toast("服务器错误,请联系系统管理员")
		})
	}])
	