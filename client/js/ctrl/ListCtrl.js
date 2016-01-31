angular.module('myApp')
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
