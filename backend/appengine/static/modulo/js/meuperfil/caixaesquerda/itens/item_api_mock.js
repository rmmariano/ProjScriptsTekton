var rest = angular.module('rest',[]);

rest.factory('ItemApi',function($rootScope){
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
                $rootScope.$digest(); /* como eh uma chamada fake, ele nao atualiza a pagina, esse comando força
                                        a pagina ser atualizada apos a execucao da chamada fake */
            },1000);

            return obj;
        }
    };
});