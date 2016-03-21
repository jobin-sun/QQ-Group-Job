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
 }]);