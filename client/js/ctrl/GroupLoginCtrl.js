angular.module('myApp')
	.controller("GroupLoginCtrl",["$scope","$http", "$cookies","$routeParams", function($scope, $http, $cookies, $routeParams){
		if($cookies.get("admin_logined") == "yes"){
			location.href = "#/group";
			return;
		}
		if($routeParams.groupId){
			$scope.groupId = parseInt($routeParams.groupId);
		}
		var reSendActivate = {};
		$scope.submit = function(){
			reSendActivate = {
				groupId: $scope.groupId,
				qq:$scope.qq
			}
			$http.post("/api/group/login/", {
				groupId: $scope.groupId,
				qq: $scope.qq,
				password:$scope.password
			}).success(function(response){
				if(response.status == "success"){
					location.href = "#/group/"
				}else{
					if(response.code == 20002){
						$scope.showActivate = true;	
					}
					$T.toast(response.msg);
				}
			}).error(function(){
				reSendActivate = undefined;
				$T.toast("服务器错误,请联系系统管理员");
			})
		}
		$scope.recover = function(){
			$http.get("/api/group/send_recover_mail",{
				params:{
					groupId: $scope.groupId,
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
			if(!reSendActivate.groupId || !reSendActivate.qq){
				$T.toast("群ID或管理员QQ号为空，激活邮件无法发送")
				return;
			}
			$http.get("/api/group/send_activate_mail/",{
				params:{
					groupId:reSendActivate.groupId,
					qq: reSendActivate.qq
				}
			}).success(function(response){
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
	