angular.module('myApp')
	.controller("ResumesListCtrl",["$scope","myHttp", function($scope, myHttp){
		myHttp.get("/api/resumes_list/").success(function(response){
			$scope.items = [];
			for(var i=0; i < response.data.length; i++){
				var ob = {
					'id':response.data[i].id,
					'email':response.data[i].email,
					'jobTitle': response.data[i].jobTitle,
					'display': response.data[i].display,
					'username':response.data[i].username,
					'qq':response.data[i].qq,
					'sex':response.data[i].sex,
					'age':response.data[i].age,
					'yearsOfWorking':response.data[i].yearsOfWorking,
					'school':response.data[i].school,
					'education':response.data[i].education,
					'groupId':response.data[i].groupId,
					'groupName': response.data[i].groupName,
					'lastDate':response.data[i].lastDate,
					'status':response.data[i].status
				};
				$scope.items.push(ob);
			}
			$scope.id2name = {}
			for(var i = 0; i < response.id2name.length; i++){
				$scope.id2name[response.id2name[i].groupId] = response.id2name[i].groupName;
			}
		})
		$scope.delete = function(item){
			$http.delete("/api/resume/",{
				params:{
					groupId: item.groupId
				}
			}).success(function(response){
				if(response.status == "success"){
					$T.toast("更新成功");
					item.hide = true;
				}else{
					$T.toast(response.msg)
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
	}])
	