angular.module('myApp')
	.controller("GroupJoinCtrl",["$scope","$http", "$cookies",function($scope, $http, $cookies){
		if($cookies.get("admin_logined") == "yes"){
			location.href = "#/group";
			return;
		}
		$scope.submit = function(){
			$http.post("/api/group/join/", {
				groupId: $scope.groupId,
				groupName: $scope.groupName,
				qq: $scope.qq,
				nick: $scope.nick,
				password:$scope.password
			}).success(function(response){
				if(response.status == "success"){
					$scope.sendEmail(response.data.id);
					$scope.showBtn = false;
				}else{
					$T.toast(response.msg);
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
		$scope.sendEmail = function(id){
			$http.get('/api/group/send_activate_mail/',{
				params:{
					id: id
				}
			})
			.success(function(response){
				if(response.status == "success"){
					$T.toast("激活邮件已发送，请注意查收");
				}else{
					$T.toast(response.msg);
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
			
		}
	}])
	