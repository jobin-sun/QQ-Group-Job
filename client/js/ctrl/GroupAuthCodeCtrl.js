angular.module('myApp')
	.controller("GroupAuthCodeCtrl",["$scope","myHttp", function($scope, myHttp){
		myHttp.get("/api/group/auth_code/").success(function(response){
			$scope.items = response.data
			$scope.qq2nick = {};
			for(var i = 0; i < response.qq2nick.length; i++){
				$scope.qq2nick[response.qq2nick[i].qq] = response.qq2nick[i].nick;
			}
		})
		$scope.post = function(){
			myHttp.post("/api/group/auth_code/", {
				code: $scope.add.code
			}).success(function(response){
				$scope.add = undefined;
				$scope.showCodeAdd = false;
				$scope.items.push(response.data);
			})
		}
		$scope.delete = function(item){
			myHttp.delete("/api/group/auth_code/", {
				id: item.id
			}).success(function(response){
				$T.toast("删除成功");
				item.hide = true;
			})
		}
		$scope.hide_pop = function(){
			$scope.showCodeAdd = false;
		}
		$scope.stopPropagation = function($event){
			$event.stopPropagation();
		}
	}])
	