angular.module('myApp')
	.controller("GroupResumeListCtrl",["$scope", "$http", "$cookies", function($scope, $http, $cookies){
		var list = {};
		$http.get("/api/group/resume_list/",{
			params:{
				groupID: $scope.groupID
			}
		}).success(function(response){
			if (response.status == "success") {
				$scope.items = []
				try{
					//这里直接从返回的data列表调用还是要再核对username？
					for(var i = 0; i < response.data.length; i++){
						// list[response.data[i].resumeId] = response.data[i];
						if(response.data[i].status == 0)
							response.data[i].status = "申请中";
						else if(response.data[i].status == 1)
							response.data[i].status = "允许的";
						else if(response.data[i].status == 2)
							response.data[i].status = "拒绝的";
						else
							response.data[i].status = "拉黑的";
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
		$scope.delResume = function(key){
			$http.delete("/api/group/resume_list/", {
				params:{
					resumeId: key
				}
			}).success(function(response){
				if(response.status == "success"){
					$T.toast("简历已删除");
				}else{
					$T.toast(response.msg);
				}
			}).error(function(){
				$T.toast("服务器错误,请联系系统管理员")
			})
		}
	}])
