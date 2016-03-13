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
					$T.toast(response.msg)
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})	
		};
 }]);