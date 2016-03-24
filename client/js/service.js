angular.module('myApp').service("myHttp", ['$http', '$rootScope', function($http, $rootScope){
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
 					if(10000 == response.code){
	 					$rootScope.switchLogin = "user";
	 					return;
	 				}else if(20000 == response.code){
	 					$rootScope.switchLogin = "group";
	 					return;
	 				}
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
 			$http.post(url,opt).error(function(response, errorCode){
 				$T.toast("服务器错误,状态码:"+errorCode)
 			}).success(function(response){
 				if(response.status == "success"){
 					successFn(response)
 				}else{
 					if(10000 == response.code){
	 					$rootScope.switchLogin = "user";
	 					return;
	 				}else if(20000 == response.code){
	 					$rootScope.switchLogin = "group";
	 					return;
	 				}
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
 			$http.put(url,opt).error(function(response, errorCode){
 				$T.toast("服务器错误,状态码:"+errorCode)
 			}).success(function(response){
 				if(response.status == "success"){
 					successFn(response)
 				}else{
 					if(10000 == response.code){
	 					$rootScope.switchLogin = "user";
	 					return;
	 				}else if(20000 == response.code){
	 					$rootScope.switchLogin = "group";
	 					return;
	 				}
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
 			$http.delete(url,params).error(function(response, errorCode){
 				$T.toast("服务器错误,状态码:"+errorCode)
 			}).success(function(response){
 				if(response.status == "success"){
 					successFn(response)
 				}else{
 					if(10000 == response.code){
	 					$rootScope.switchLogin = "user";
	 					return;
	 				}else if(20000 == response.code){
	 					$rootScope.switchLogin = "group";
	 					return;
	 				}
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
 			$http.head(url,params).error(function(response, errorCode){
 				$T.toast("服务器错误,状态码:"+errorCode)
 			}).success(function(response){
 				if(response.status == "success"){
 					successFn(response)
 				}else{
 					if(10000 == response.code){
	 					$rootScope.switchLogin = "user";
	 					return;
	 				}else if(20000 == response.code){
	 					$rootScope.switchLogin = "group";
	 					return;
	 				}
 					$T.toast(response.msg)
 				}	
 			})
 			return this;
 		}
 	}
 }]);