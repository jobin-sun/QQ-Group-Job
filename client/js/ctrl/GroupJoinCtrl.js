angular.module('myApp')
	.controller("GroupJoinCtrl",["$scope","myHttp", "$cookies",function($scope, myHttp, $cookies){
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
			myHttp.post("/api/group/join/", {
				groupId: $scope.groupId,
				groupName: $scope.groupName,
				qq: $scope.qq,
				nick: $scope.nick,
				password:$scope.password
			}).success(function(response){
				$scope.sendEmail();
				$scope.showBtn = false;
			})
		}
		$scope.sendEmail = function(){
			if(!reSendActivate.groupId || !reSendActivate.qq){
				$T.toast("群ID或管理员QQ号为空，激活邮件无法发送")
				return;
			}
			myHttp.get('/api/group/send_activate_mail/',{
				groupId: reSendActivate.groupId,
				qq: reSendActivate.qq 
			}).success(function(response){
				$T.toast("激活邮件已发送，请注意查收");
			})
		}
	}])
	