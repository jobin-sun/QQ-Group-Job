angular.module('myApp')
	.controller("ResumesListCtrl",["$scope","$http","$cookies",function($scope, $http, $cookies){
		$http.get("/api/check_login/").success(function(response){
			if(response.status != "success"){
				location.href = "#/login";
			}
		})
		var sexOb = ['保密', '男', '女'];
		var eduOb = ['大专以下', '大专', '本科', '硕士', '硕士以上'];
		var statusOb = ['申请中', '允许的', '拒绝的', '拉黑的'];
		$http.get("/api/resumes_list/").success(function(response){
			console.log(response);
			if(response.status == "success"){
				$scope.items = [];
				for(var i=0; i < response.data.length; i++){
					var ob = {
						'email':response.data[i].email,
						'username':response.data[i].username,
						'qq':response.data[i].qq,
						'sex':sexOb[response.data[i].sex],
						'age':response.data[i].age,
						'yearsOfWorking':response.data[i].yearsOfWorking,
						'school':response.data[i].school,
						'education':eduOb[response.data[i].education],
						'content':response.data[i].content,
						'groupId':response.data[i].groupId,
						'lastDate':response.data[i].lastDate,
						'status':statusOb[response.data[i].status]
					};
					$scope.items.push(ob);
				}
			}else{
				$T.toast(response.msg);
			}
		}).error(function(){
			$T.toast("服务器错误,请联系系统管理员")
		})
	}])
	