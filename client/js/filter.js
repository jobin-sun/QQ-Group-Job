angular.module('myApp').filter('strSex',function(){
    return function(v){
        if($T.sexOptions[v])
            return $T.sexOptions[v].name
        else
            return ""
    }
}).filter('strEdu',function(){
    return function(v){
        if($T.eduOptions[v])
            return $T.eduOptions[v].name
        else
            return ""
    }
}).filter('strStatus',function(){
    return function(v){
        if($T.statusOptions[v])
            return $T.statusOptions[v].name;
        else
            return ""
    }
}).filter('strBool',function(){
    return function(v){
        if(v)
            return '是';
        else
            return "否"
    }
}).filter('strRank',function(){
    return function(v){
        if(v == -1)
            return "未评分";
        else
            return v
    }
});;