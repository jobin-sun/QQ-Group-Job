angular.module('myApp').directive('errSrc', function() {
  return {
    link: function(scope, element, attrs) {
      element.bind('error', function() {
      	console.log(333)
        if (attrs.src != attrs.errSrc) {
          attrs.$set('src', attrs.errSrc);
        }
      });
    }
  }
});