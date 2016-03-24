angular.module('myApp')
	.controller("LoginCtrl",["$scope", "$cookies", "myHttp", "$rootScope", "$route", function($scope, $cookies, myHttp, $rootScope, $route){
		if(location.href.match(/#\/group/)){
			return;
		}
		if($cookies.get("logined") == "yes"){
			location.href = "#/index";
			return;
		}
		$rootScope.switchLogin = "user";
		var reSendActivateQQ;
		$scope.submit = function(){
			reSendActivateQQ = $scope.qq;
			myHttp.post("/api/login/", {
				qq: $scope.qq,
				password: $scope.password
			}).success(function(response){
				$rootScope.switchLogin = "";
				if(location.href.match(/login/)){
					location.href = "#/index";
				}else{
					$route.reload();
				}
			})
		}
		$scope.recover = function(){
			myHttp.get("/api/send_recover_mail",{
				qq: $scope.qq
			}).success(function(response){
				$T.toast("找回密码相关信息已发送到您的邮箱，请注意查收");
			})
		}
		$scope.reSendActivate = function(){
			if(!reSendActivateQQ){
				$T.toast("QQ号为空，无法发送")
				return;
			}
			myHttp.get("/api/send_activate_mail/?qq="+reSendActivateQQ)
			.success(function(response){
				$T.toast("激活邮件已发送，请注意查收");
			})
		}
	}])
	