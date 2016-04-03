(function(){
var app = angular.module('food',[]);

app.controller('SearchController',['$http',function($http){
  }
]);

app.controller('formCtrl',['$http','$scope',function($http,$scope){
  this.query = '';
  // this.submit = function(){
  //   this.queryText = queryText;
  // };
  this.submit = function(){
    $http({
      url : "http://127.0.0.1:5000/query",
      method: "GET",
      params :{'query':this.query}
    }).success(function(data){
      console.log(data);
    });
    console.log(this.query);
  }
  this.returnQuery = function(){
    return this.queryText;
  }
}]);
})();
