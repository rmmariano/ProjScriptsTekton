//inicializa o módulo para a criação do <cadastraritemform></cadastraritemform>
var itemModulo = angular.module('itemModulo',['rest']);

//insere a diretiva que o itemModulo fará, no caso terá a tag <cadastraritemform></cadastraritemform>
//e onde ela for citada, substituirá pelo o que a diretiva retorna.
itemModulo.directive('cadastraritemform',function(){
    // '=' faz binding bidirecional , '@' da o resultado de uma expressao, '&' uma expressao para funcoes
    return {
        restrict: 'E',
        replace: true,
        templateUrl: '/static/modulo/html/meuperfil/caixaesquerda/itens/cadastraritemform.html',
        scope: {
            itemInterno:'=',
            tituloLabel:'@',
            categoriaLabel:'@',
            descricaoLabel:'@',
            saveComplete: '&'
        },
        controller: function($scope, ItemApi){
            $scope.salvandoFlag = false;

            $scope.salvar = function(){
                $scope.salvandoFlag = true;
                $scope.erros = {};
                var promessa = ItemApi.salvar($scope.itemInterno);
                promessa.success(function(data){
                    $scope.itemInterno.titulo = '';
                    $scope.itemInterno.id_categoria = '4863277368606720';
                    $scope.itemInterno.descricao = '';
                    $scope.salvandoFlag = false;

                    if ($scope.saveComplete != undefined) {
                        $scope.saveComplete({'item': data});
                    }
                });
                promessa.error(function(data){
                    $scope.erros = data;
                    $scope.salvandoFlag = false;
                });
            }
        }
    };
});

//diretiva <mostraritens></mostraritens> // mostraritens
itemModulo.directive('mostraritens',function(){
    return {
        //restrict: 'E',
        restrict: 'A',
        replace: true,
        templateUrl: '/static/modulo/html/meuperfil/caixaesquerda/itens/mostraritens.html',
        scope: {
            itemInterno:'='
        },
        controller: function(){

        }
    };
});