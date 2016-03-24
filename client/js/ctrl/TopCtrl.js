angular.module('myApp')
	.controller("TopCtrl",["$rootScope", "$cookies", "myHttp", function($rootScope, $cookies, myHttp){
		if($cookies.get("logined") != "yes"){
			$rootScope.switchLogin = "user";
			return;
		}
		$rootScope.switchLogin = "";
		myHttp.get("/api/").success(function(response){
			$rootScope.user = response.data;
		})
	}])
