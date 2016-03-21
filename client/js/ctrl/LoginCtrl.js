angular.module('myApp')
	.controller("LoginCtrl",["$scope","$http", "$cookies",function($scope, $http, $cookies){
		if($cookies.get("logined") == "yes"){
			location.href = "#/index";
			return;
		}
		var reSendActivateQQ;
		$scope.submit = function(){
			reSendActivateQQ = $scope.qq;
			$http.post("/api/login/", {
				qq: $scope.qq,
				password: $scope.password
			}).success(function(response){
				if(response.status == "success"){
					location.href = "#/index"
				}else{
					if(response.code == 10002){
						$scope.showActivate = true;	
					}
					$T.toast(response.msg);
				}
			}).error(function(){
				reSendActivateQQ = undefined;
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
		$scope.recover = function(){
			$http.get("/api/send_recover_mail",{
				params:{
					qq: $scope.qq
				}
			}).success(function(response){
				if(response.status == "success"){
					$T.toast("找回密码相关信息已发送到您的邮箱，请注意查收");
				}else{
					$T.toast(response.msg);
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
		$scope.reSendActivate = function(){
			if(!reSendActivateQQ){
				$T.toast("QQ号为空，无法发送")
				return;
			}
			$http.get("/api/send_activate_mail/?qq="+reSendActivateQQ)
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
	