angular.module('myApp').service('getUser', ['$http', function($http) {
		var user;
		return function(fn){
			if(user){
				fn(user);
				return;
			}
			$http.get("/api/").success(function(response){
				if(response.status == "success"){
					user = response.data;
					fn(response.data);
				}else{
					if(response.code != 10000){
						$T.toast(response.msg)
					}
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})	
		};
 }]).service("getAdmin", ['$http', function($http){
 	var admin;
 	return function(fn){
 		if(admin){
 			fn(admin);
 			return;
 		}
 		$http.get("/api/group/admin/").success(function(response){
 			if(response.status == "success"){
					admin = response.data;
					fn(response.data);
				}else{
					if(response.code != 20000){
						$T.toast(response.msg)
					}
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})	

 	}
 }]).service("myHttp", ['$http', function($http){
 	return {
 		get:function(url, opt){
 			var successFn = function(){};
 			this.success = function(fn){
 				successFn = fn;
 			}
 			var params = {
 				params: opt
 			}
 			$http.get(url,params).error(function(response, errorCode){
 				$T.toast("服务器错误,状态码:"+errorCode)
 			}).success(function(response){
 				if(response.status == "success"){
 					successFn(response)
 				}else{
 					$T.toast(response.msg)
 				}	
 			})
 			return this;
 		},
 		post:function(url, opt){
 			var successFn = function(){};
 			this.success = function(fn){
 				successFn = fn;
 			}
 			$http.get(url,opt).error(function(response, errorCode){
 				$T.toast("服务器错误,状态码:"+errorCode)
 			}).success(function(response){
 				if(response.status == "success"){
 					successFn(response)
 				}else{
 					$T.toast(response.msg)
 				}	
 			})
 			return this;
 		},
 		put:function(url, opt){
 			var successFn = function(){};
 			this.success = function(fn){
 				successFn = fn;
 			}
 			$http.get(url,opt).error(function(response, errorCode){
 				$T.toast("服务器错误,状态码:"+errorCode)
 			}).success(function(response){
 				if(response.status == "success"){
 					successFn(response)
 				}else{
 					$T.toast(response.msg)
 				}	
 			})
 			return this;
 		},
 		delete:function(url, opt){
 			var successFn = function(){};
 			this.success = function(fn){
 				successFn = fn;
 			}
 			var params = {
 				params: opt
 			}
 			$http.get(url,params).error(function(response, errorCode){
 				$T.toast("服务器错误,状态码:"+errorCode)
 			}).success(function(response){
 				if(response.status == "success"){
 					successFn(response)
 				}else{
 					$T.toast(response.msg)
 				}	
 			})
 			return this;
 		},
 		head:function(url, opt){
 			var successFn = function(){};
 			this.success = function(fn){
 				successFn = fn;
 			}
 			var params = {
 				params: opt
 			}
 			$http.get(url,params).error(function(response, errorCode){
 				$T.toast("服务器错误,状态码:"+errorCode)
 			}).success(function(response){
 				if(response.status == "success"){
 					successFn(response)
 				}else{
 					$T.toast(response.msg)
 				}	
 			})
 			return this;
 		}
 	}
 }]);