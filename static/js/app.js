(function(){
var app = angular.module('food',[]);

app.controller('SearchController',['$http',function($http){
  var search = this;
  search.results = {};
  this.submit = function(){
    $http.get('images.json').success(function(data){
      // console.log(data[0].results['https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRfjFNW0_-kdinku_amiWbT4_8VvAiroSpmpr4PCiDJDR2vDwg3H_eJpGHD']);
      for (var key in data[0].results){
        //console.log(data[0].results[key]);
        search.results[key] = data[0].results[key];
        //console.log(search.results);
      }
      //search.results = data[0];
      console.log(search.results);
    });
    //console.log(search.results);
  }

  }
]);

app.controller('formCtrl',['$http','$scope',function($http,$scope){
  this.query = '';
  // this.submit = function(){
  //   this.queryText = queryText;
  // };
  this.submit = function(){
    $http.get('images.json').success(function(data){
      console.log(data[0].results);
    });
    console.log(this.query);
  }
  this.returnQuery = function(){
    return this.queryText;
  }
}]);

app.controller('imageCtrl',['$http',function($http){
  this.imageUrls = [];
  this.addImage=function(imageUrl){
    console.log(imageUrl);
    this.imageUrls.push(imageUrl);
  };

  this.sendImages = function(){
    console.log(this.imageUrls);
    $http({
      url:'http://127.0.0.1:5000/imageTags',
      method: 'GET',
      params: {'urls':JSON.stringify(this.imageUrls)}
    }).success(function(data){
      console.log(data);
    });
  };

}]);
})();
