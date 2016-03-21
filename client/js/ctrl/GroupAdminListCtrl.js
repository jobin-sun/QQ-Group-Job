angular.module('myApp')
	.controller("GroupAdminListCtrl",["$scope","$http","$rootScope", function($scope, $http, $rootScope){
		$http.get("/api/group/admin_list/").success(function(response){
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
		$scope.post = function(){
			$http.post("/api/group/admin_list/",{
				qq: $scope.add.qq,
				nick: $scope.add.nick
			}).success(function(response){
				if(response.status == "success"){
					$T.toast("添加成功");
					$scope.sendEmail(response.data);
					$scope.add = undefined;
					$scope.showAdminAdd = false;
					$scope.items.push(response.data);
				}else{
					$T.toast(response.msg);
				}
				
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
		$scope.delete = function(item){
			$http.delete("/api/group/admin_list/",{
				params:{
					id: item.id
				}
			}).success(function(response){
				if(response.status == "success"){
					$T.toast("删除成功");
					item.hide = true;
				}else{
					$T.toast(response.msg);
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
		$scope.hide_pop = function(){
			$scope.showAdminAdd = false;
		}
		$scope.stopPropagation = function($event){
			$event.stopPropagation();
		}
		$scope.sendEmail = function(item){
			if(!item.groupId || !item.qq){
				$T.toast("群ID或管理员QQ号为空，激活邮件无法发送")
				return;
			}
			$http.get('/api/group/send_activate_mail/',{
				params:{
					qq: item.qq,
					groupId: item.groupId
				}
			})
			.success(function(response){
				if(response.status == "success"){
					$T.toast("激活邮件已发送，请提醒查收");
				}else{
					$T.toast(response.msg);
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
			
		}
	}])
	