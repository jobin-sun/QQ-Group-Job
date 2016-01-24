var app = angular.module('myApp', ["ngRoute", "ngCookies"]);
	app.config(['$routeProvider', function($routeProvider) {
		$routeProvider.when('/login', {
			templateUrl: 'tpl/login.html',
			controller: 'LoginCtrl'
		}).when('/reg', {
			templateUrl: 'tpl/reg.html',
			controller: 'RegCtrl'
		}).when('/index', {
			templateUrl: 'tpl/index.html',
			controller: 'IndexCtrl'
		}).when('/list', {
			templateUrl: 'tpl/list.html',
			controller: 'ListCtrl'
		}).when('/logout', {
			template: '',
			controller: 'LogoutCtrl'
		}).when('/change_pwd', {
			templateUrl: 'tpl/change_pwd.html',
			controller: 'ChangePwdCtrl'
		}).otherwise({redirectTo: '/login'});
	}]);
	app.controller("IndexCtrl",["$scope","$http",function($scope, $http){
		$http.get("/user").success(function(response){
			if(response.status == "success"){
				$scope.email = response.data.email;
				$scope.username = response.data.username;
				$scope.qq = parseInt(response.data.qq);
				$scope.display = response.data.display;
				$scope.content = response.data.content;
			}else{
				alert(response.msg)
			}
		}).error(function(){
			alert("服务器错误,请联系系统管理员")
		})
		$scope.submit = function(){
			$http.put("/user", {
				username: $scope.username,
				qq: $scope.qq,
				display: $scope.display,
				content: $scope.content
			}).success(function(response){
				if(response.status == "success"){
					alert("更新成功");
					location.reload();
				}else{
					alert(response.msg)
				}
			}).error(function(){
				alert("服务器错误,请联系系统管理员")
			})
		}
	}])
	.controller("ListCtrl",["$scope","$http",function($scope, $http){
		var list = {};
		$scope.submit = function(){
			$http.get("/user/list?code="+ $scope.code).success(function(response){
				if (response.status == "success") {
					$scope.items = []
					try{
						for(var i = 0; i < response.data.length; i++){
							list[response.data[i].userEmail] = response.data[i];
							$scope.items.push(response.data[i].userEmail);
						}
					}catch(e){}
					$scope.show = true;
				}else{
					alert(response.msg);
				};
			}).error(function(){
				alert("服务器错误,请联系系统管理员")
			})
		}
		$scope.getInfo = function(key){
			$scope.email = list[key].userEmail;
			$scope.editDate = list[key].addDate;
			$scope.name = "loading...";
			$scope.qq = "loading...";
			$scope.content = list[key].content;
			$http.get("/user/profile?email="+key).success(function(response){
				if(response.status == "success"){
					$scope.name = response.data.username;
					$scope.qq = response.data.qq;
				}else{
					alert(response.msg)
				}
			}).error(function(){
				$scope.class = "red";
				$scope.name = "加载失败";
				$scope.qq = "加载失败";
			});
		}
		
	}])
	.controller("LogoutCtrl",["$scope","$http","$cookies",function($scope, $http, $cookies){
		$cookies.remove("email");
		$cookies.remove("token");
		location.href = "#/login";
	}])
	.controller("LoginCtrl",["$scope","$http", "$cookies",function($scope, $http, $cookies){
		var email = $cookies.get("email");
		var token = $cookies.get("token");
		if(email &&　token){
			location.href = "#/index";
			return;
		}
		$scope.submit = function(){
			$http.post("/user/login", {
				email: $scope.email,
				password: $scope.password
			}).success(function(response){
				if(response.status == "success"){
					location.href = "#/index"
				}else{
					alert(response.msg);
				}
			}).error(function(){
				alert("服务器错误,请联系系统管理员")
			})
		}
	}])
	.controller("RegCtrl",["$scope","$http","$cookies",function($scope, $http, $cookies){
		var email = $cookies.get("email");
		var token = $cookies.get("token");
		if(email &&　token){
			location.href = "#/index";
			return;
		}
		$scope.submit = function(){
			$http.post("/user/reg",{
				email:$scope.email,
				username:$scope.username,
				qq:$scope.qq,
				password:$scope.password
			}).success(function(response){
				if(response.status == "success"){
					location.href="#/login"
				}else{
					alert(response.msg)
				}
			}).error(function(){
				alert("服务器错误,请联系系统管理员")
			})

		}
	}])
	.controller("ChangePwdCtrl",["$scope","$http",function($scope, $http){
		$scope.submit = function(){
			$http.put("/user/change_pwd", {
				password: $scope.password
			}).success(function(response){
				if(response.status == "success"){
					alert("密码已修改,请重新登录");
					location.href = "#/logout"
				}else{
					alert(response.msg);
				}
			}).error(function(){
				alert("服务器错误,请联系系统管理员")
			})
		}
	}])