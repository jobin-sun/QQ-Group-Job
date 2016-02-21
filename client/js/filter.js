angular.module('myApp').filter('strSex',function(){
	var sexOb = ['保密', '男', '女'];
    return function(v){
        return sexOb[v];
    }
}).filter('strEdu',function(){
	var eduOb = ['大专以下', '大专', '本科', '硕士', '硕士以上'];
    return function(v){
        return eduOb[v];
    }
}).filter('strStatus',function(){
	var statusOb = ['申请中', '允许的', '拒绝的', '拉黑的'];
    return function(v){
        return statusOb[v];
    }
});