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
});