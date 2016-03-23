angular.module('myApp')
	.controller("TopCtrl",["$rootScope", "$cookies", "myHttp", function($rootScope, $cookies, myHttp){
		if($cookies.get("logined") != "yes"){
			location.href = "#/login";
			return;
		}
		myHttp.get("/api/").success(function(response){
			$rootScope.user = response.data;
		})
	}])
