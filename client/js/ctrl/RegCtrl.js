angular.module('myApp')
	.controller("RegCtrl",["$scope","myHttp","$cookies",function($scope, myHttp, $cookies){
		if($cookies.get("logined") == "yes"){
			location.href = "#/index";
			return;
		}
		$scope.submit = function(){
			myHttp.post("/api/reg/",{
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
			})

		}
		$scope.sendEmail = function(){
			myHttp.get("/api/send_activate_mail/?qq="+$scope.qq)
			.success(function(response){
				$T.toast("激活邮件已发送，请注意查收");
			})
		}
	}])
	