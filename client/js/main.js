$T = {}
$T.toast = function(txt,t){
	if(t == undefined){
		t = 3
	}
	if(txt == undefined){
		return
	}
	document.querySelector(".rz_toast_txt").innerHTML = txt;
	document.querySelector(".rz_toast_ctn").style.display = "block";
	setTimeout(function(){
		document.querySelector(".rz_toast_ctn").style.display = "";
	},t*1000)
}
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
		}).when('/group/list', {
			templateUrl: 'tpl/group_list.html',
			controller: 'GroupListCtrl'
		}).when('/group/change_pwd', {
			templateUrl: 'tpl/change_pwd.html',
			controller: 'ChangePwdCtrl'
		}).when('/group/admin', {
			templateUrl: 'tpl/group_admin.html',
			controller: 'GroupAdminCtrl'
		}).otherwise({redirectTo: '/login'});
	}]);
	app.controller("IndexCtrl",["$scope","$http","$cookies",function($scope, $http, $cookies){
		var email = $cookies.get("email");
		var token = $cookies.get("token");
		$http.get("/api/",{
			params:{
				email: email,
				token: token
			}
		}).success(function(response){
			if(response.status == "success"){
				$scope.email = response.data.email;
				$scope.username = response.data.username;
				$scope.qq = parseInt(response.data.qq);
				$scope.display = response.data.display;
				$scope.content = response.data.content;
			}else{
				$T.toast(response.msg)
			}
		}).error(function(){
			$T.toast("服务器错误,请联系系统管理员")
		})
		$scope.submit = function(){
			$http.put("/api/", {
				username: $scope.username,
				qq: $scope.qq,
				display: $scope.display,
				content: $scope.content,
				email: email,
				token: token
			}).success(function(response){
				if(response.status == "success"){
					$T.toast("更新成功");
					location.reload();
				}else{
					$T.toast(response.msg)
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
	}])
	.controller("ListCtrl",["$scope","$http",function($scope, $http){
		var list = {};
		$scope.submit = function(){
			$http.get("/api/list/",{
				params:{
					code: $scope.code
				}
			}).success(function(response){
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
					$T.toast(response.msg);
				};
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
		$scope.getInfo = function(key){
			$scope.email = list[key].userEmail;
			$scope.editDate = list[key].addDate;
			$scope.name = "loading...";
			$scope.qq = "loading...";
			$scope.content = list[key].content;
			$http.get("/api/profile/",{
				params:{
					email: key,
					code: $scope.code
				}
			}).success(function(response){
				if(response.status == "success"){
					$scope.name = response.data.username;
					$scope.qq = response.data.qq;
				}else{
					$T.toast(response.msg)
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
			$http.post("/api/login/", {
				email: $scope.email,
				password: $scope.password
			}).success(function(response){
				if(response.status == "success"){
					try{
						for(key in response.cookies){
							var d = new Date(response.cookies[key].opt.expires * 1000);
							$cookies.put(key,response.cookies[key].value, {expires: d})
						}
					}catch(e){console.log(e)}
					location.href = "#/index"
				}else{
					$T.toast(response.msg);
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
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
			$http.post("/api/reg/",{
				email:$scope.email,
				username:$scope.username,
				qq:$scope.qq,
				password:$scope.password
			}).success(function(response){
				if(response.status == "success"){
					location.href="#/login"
				}else{
					$T.toast(response.msg)
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})

		}
	}])
	.controller("ChangePwdCtrl",["$scope","$http","$cookies",function($scope, $http, $cookies){
		var email = $cookies.get("email");
		var token = $cookies.get("token");
		if(email &&　token){
			location.href = "#/index";
			return;
		}
		$scope.submit = function(){
			var email = $cookies.get("email");
			var token = $cookies.get("token");
			$http.put("/api/change_pwd/", {
				password: $scope.password,
				email: email,
				token: token
			}).success(function(response){
				if(response.status == "success"){
					$T.toast("密码已修改,请重新登录");
					location.href = "#/logout"
				}else{
					$T.toast(response.msg);
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
	}])
	.controller("GroupListCtrl",["$scope","$http",function($scope, $http){
		var list = {};
		$http.get("/api/group/list/",{
			params:{
				code: $scope.code
			}
		}).success(function(response){
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
				$T.toast(response.msg);
			};
		}).error(function(){
			$T.toast("服务器错误,请联系系统管理员")
		})
		$scope.getInfo = function(key){
			$scope.name = "loading...";
			$scope.qq = "loading...";
			$scope.content = list[key].content;
			//现在没有authcode传入，所以暂时注释掉方便测试
			// $http.get("/api/profile/",{
			// 	params:{
			// 		email: key,
			// 		code: $scope.code
			// 	}
			// }).success(function(response){
			// 	if(response.status == "success"){
			// 		$scope.name = response.data.username;
			// 		$scope.qq = response.data.qq;
			// 	}else{
			// 		$T.toast(response.msg)
			// 	}
			// }).error(function(){
			// 	$scope.class = "red";
			// 	$scope.name = "加载失败";
			// 	$scope.qq = "加载失败";
			// });
		}
	}])
	.controller("GroupAdminCtrl",["$scope","$http",function($scope, $http){
		$http.get("api/group/admin/",{
			params:{
				code: $scope.code
			}
		}).success(function(response){
			if (response.status == "success") {
				$scope.items = []
				try{
					for(var i = 0; i < response.data.length; i++) {
						$scope.items.push(response.data[i]);
					}
				}catch(e){}
				$scope.show = true;
			}else{
			$T.toast(response.msg);
			};
		}).error(function(){
			$T.toast("服务器错误,请联系系统管理员")
		})
	}])