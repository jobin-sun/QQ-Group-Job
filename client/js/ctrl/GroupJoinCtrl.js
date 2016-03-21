angular.module('myApp')
	.controller("GroupJoinCtrl",["$scope","$http", "$cookies",function($scope, $http, $cookies){
		if($cookies.get("admin_logined") == "yes"){
			location.href = "#/group";
			return;
		}
		var reSendActivate;
		$scope.submit = function(){
			reSendActivate = {
				groupId: $scope.groupId,
				qq:$scope.qq
			}
			$http.post("/api/group/join/", {
				groupId: $scope.groupId,
				groupName: $scope.groupName,
				qq: $scope.qq,
				nick: $scope.nick,
				password:$scope.password
			}).success(function(response){
				if(response.status == "success"){
					$scope.sendEmail();
					$scope.showBtn = false;
				}else{
					$T.toast(response.msg);
				}
			}).error(function(){
				reSendActivate = undefined;
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
		$scope.sendEmail = function(){
			if(!reSendActivate.groupId || !reSendActivate.qq){
				$T.toast("群ID或管理员QQ号为空，激活邮件无法发送")
				return;
			}
			$http.get('/api/group/send_activate_mail/',{
				params:{
					groupId: reSendActivate.groupId,
					qq: reSendActivate.qq 
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
	