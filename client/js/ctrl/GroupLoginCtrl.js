angular.module('myApp')
	.controller("GroupLoginCtrl",["$scope","myHttp", "$cookies","$routeParams","$rootScope", "$route", function($scope, myHttp, $cookies, $routeParams, $rootScope, $route){
		if(location.href.match(/#\/group/)){
			if($cookies.get("admin_logined") == "yes" && location.href.match(/login/)){
				location.href = "#/group";
				return;
			}
			$rootScope.switchLogin = "group";
			if($routeParams.groupId){
				$scope.groupId = parseInt($routeParams.groupId);
			}
		}
		var reSendActivate = {};
		$scope.submit = function(){
			reSendActivate = {
				groupId: $scope.groupId,
				qq:$scope.qq
			}
			myHttp.post("/api/group/login/", {
				groupId: $scope.groupId,
				qq: $scope.qq,
				password:$scope.password
			}).success(function(response){
				if(response.code == 30005){
					$scope.showActivate = true;
				}else{
					$rootScope.switchLogin = "";
					if(location.href.match(/login/)){
						location.href = "#/group/"
					}else{
						$route.reload();
					}
				}
			})
		}
		$scope.recover = function(){
			myHttp.get("/api/group/send_recover_mail",{
				groupId: $scope.groupId,
				qq: $scope.qq
			}).success(function(response){
				$T.toast("找回密码相关信息已发送到您的邮箱，请注意查收");
			})
		}
		$scope.reSendActivate = function(){
			if(!reSendActivate.groupId || !reSendActivate.qq){
				$T.toast("群ID或管理员QQ号为空，激活邮件无法发送")
				return;
			}
			myHttp.get("/api/group/send_activate_mail/",{
				groupId:reSendActivate.groupId,
				qq: reSendActivate.qq
			}).success(function(response){
				$T.toast("激活邮件已发送，请注意查收");
			})
		}
	}])
	