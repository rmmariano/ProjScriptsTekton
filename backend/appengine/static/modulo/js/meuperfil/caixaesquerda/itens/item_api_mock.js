var rest = angular.module('rest',[]);

rest.factory('ItemApi',function($http){
    return {
        salvar: function(item){
            var obj = {};
            obj.success = function(fcnSucesso){
                obj.fcnSucesso = fcnSucesso;
            };
            obj.error = function(fcnError){
                obj.fcnError = fcnError;
            };

            setTimeout(function(){
                item.id = 1;
                obj.fcnSucesso(item);
            },1000);

            return obj;
        }
    };
});