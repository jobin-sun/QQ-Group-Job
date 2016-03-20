angular.module('myApp').directive('err', function() {
  return {
    link: function(scope, element, attrs) {
      element.bind('error', function() {
        if (attrs.src != attrs.err) {
          attrs.$set('src', attrs.err);
        }
      });
    }
  }
});