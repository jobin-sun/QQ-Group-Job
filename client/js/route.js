angular.module('myApp', ["ngRoute", "ngCookies"])
	.config(['$routeProvider', function($routeProvider) {
		$routeProvider.when('/login', {
			templateUrl: 'tpl/login.html',
			controller: 'LoginCtrl'
		}).when('/reg', {
			templateUrl: 'tpl/reg.html',
			controller: 'RegCtrl'
		}).when('/index', {
			templateUrl: 'tpl/index.html',
			controller: 'IndexCtrl'
		}).when('/list', {
			templateUrl: 'tpl/list.html',
			controller: 'ListCtrl'
		}).when('/logout', {
			template: '',
			controller: 'LogoutCtrl'
		}).when('/change_pwd', {
			templateUrl: 'tpl/change_pwd.html',
			controller: 'ChangePwdCtrl'
		}).when('/group/list', {
			templateUrl: 'tpl/group_list.html',
			controller: 'GroupListCtrl'
		}).when('/group/change_pwd', {
			templateUrl: 'tpl/change_pwd.html',
			controller: 'ChangePwdCtrl'
		}).when('/group/admin', {
			templateUrl: 'tpl/group_admin.html',
			controller: 'GroupAdminCtrl'
		}).otherwise({redirectTo: '/login'});
	}]);