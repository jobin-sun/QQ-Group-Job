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
		$http.get("/api/").success(function(response){
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
				content: $scope.content
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
		$http.get("/api/logout/").success(function(response){
			if(response.status == "success"){
				location.href = "#/login";
			}else{
				$T.toast("退出失败")
			}
		})
		
	}])
	.controller("LoginCtrl",["$scope","$http", "$cookies",function($scope, $http, $cookies){
		$http.get("/api/check_login/").success(function(response){
			if(response.status == "success"){
				location.href = "#/index";
			}
		})
		$scope.submit = function(){
			$http.post("/api/login/", {
				email: $scope.email,
				password: $scope.password
			}).success(function(response){
				if(response.status == "success"){
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
		$http.get("/api/check_login/").success(function(response){
			if(response.status == "success"){
				location.href = "#/index";
			}
		})
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
		$http.get("/api/check_login/").success(function(response){
			if(response.status != "success"){
				location.href = "#/login";
			}
		})
		$scope.submit = function(){
			$http.put("/api/change_pwd/", {
				password: $scope.password
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