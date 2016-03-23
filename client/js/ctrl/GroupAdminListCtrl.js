angular.module('myApp')
	.controller("GroupAdminListCtrl",["$scope","myHttp", function($scope, myHttp){
		myHttp.get("/api/group/admin_list/").success(function(response){
			$scope.items = []
			try{
				for(var i = 0; i < response.data.length; i++) {
					$scope.items.push(response.data[i]);
				}
			}catch(e){}
			$scope.show = true;
		})
		$scope.post = function(){
			myHttp.post("/api/group/admin_list/",{
				qq: $scope.add.qq,
				nick: $scope.add.nick
			}).success(function(response){
				$T.toast("添加成功");
				$scope.sendEmail(response.data);
				$scope.add = undefined;
				$scope.showAdminAdd = false;
				$scope.items.push(response.data);
			})
		}
		$scope.delete = function(item){
			myHttp.delete("/api/group/admin_list/",{
				id: item.id
			}).success(function(response){
				$T.toast("删除成功");
				item.hide = true;
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
			myHttp.get('/api/group/send_activate_mail/',{
				qq: item.qq,
				groupId: item.groupId
			}).success(function(response){
				$T.toast("激活邮件已发送，请提醒查收");
			})
		}
	}])
	