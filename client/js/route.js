angular.module('myApp', ["ngRoute", "ngCookies"])
	.config(['$routeProvider', function($routeProvider) {
		$routeProvider.when('/login', {
			templateUrl: 'tpl/user/login.html',
			controller: 'LoginCtrl'
		}).when('/reg', {
			templateUrl: 'tpl/user/reg.html',
			controller: 'RegCtrl'
		}).when('/index', {
			templateUrl: 'tpl/user/index.html',
			controller: 'IndexCtrl'
		}).when('/hr/list/:groupId', {
			templateUrl: 'tpl/hr/list.html',
			controller: 'ListCtrl'
		}).when('/logout', {
			template: '',
			controller: 'LogoutCtrl'
		}).when('/change_pwd', {
			templateUrl: 'tpl/user/change_pwd.html',
			controller: 'ChangePwdCtrl'
		}).when('/groups_list', {
			templateUrl: 'tpl/user/groups_list.html',
			controller: 'GroupsListCtrl'
		}).when('/resumes_list', {
			templateUrl: 'tpl/user/resumes_list.html',
			controller: 'ResumesListCtrl'
		
		}).when('/hr/list', {
			templateUrl: 'tpl/hr/list.html',
			controller: 'ListCtrl'
		}).when('/group/resume_list/', {
			templateUrl: 'tpl/user/group_resume_list.html',
			controller: 'GroupResumeListCtrl'
		}).when('/group/change_pwd', {
			templateUrl: 'tpl/user/change_pwd.html',
			controller: 'ChangePwdCtrl'
		}).when('/group/admin_list/', {
			templateUrl: 'tpl/user/group_admin_list.html',
			controller: 'GroupAdminListCtrl'
		}).otherwise({redirectTo: '/login'});
	}]);