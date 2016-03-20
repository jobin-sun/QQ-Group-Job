angular.module('myApp')
	.controller("RegCtrl",["$scope","$http","$cookies",function($scope, $http, $cookies){
		if($cookies.get("logined") == "yes"){
			location.href = "#/index";
			return;
		}
		$scope.submit = function(){
			$http.post("/api/reg/",{
				username:$scope.username,
				qq:$scope.qq,
				password:$scope.password
			}).success(function(response){
				if(response.status == "success"){
					$scope.sendEmail();
					$scope.showBtn = false;
				}else{
					$T.toast(response.msg)
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})

		}
		$scope.sendEmail = function(){
			$http.get("/api/send_activate_mail/?qq="+$scope.qq)
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
	