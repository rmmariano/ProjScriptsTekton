//inicializa o módulo para a criação do <cadastraritemform></cadastraritemform>
var itemModulo = angular.module('itemModulo',[]);

//insere a diretiva que o itemModulo fará, no caso terá a tag <cadastraritemform></cadastraritemform>
//e onde ela for citada, substituirá pelo o que a diretiva retorna.
itemModulo.directive('cadastraritemform',function(){
    return {
        restrict: 'E',
        replace: true,
        templateUrl: '/static/modulo/html/meuperfil/caixaesquerda/itens/cadastraritemform.html',
        scope: {
            itemInterno:'=',
            tituloLabel:'@',
            categoriaLabel:'@',
            descricaoLabel:'@'
        },
        controller: function($scope, $http){
            $scope.salvandoFlag = false;

            $scope.salvar = function(){
                $scope.salvandoFlag = true;
                $scope.erros = {};
                $http.post(
                    '/meuperfil/caixaesquerda/itens/itensmeusitens/salvar',
                    $scope.itemInterno
                ).success(function(data){
                    console.log('sucesso');
                    console.log(data);
                    $scope.itemInterno.titulo = '';
                    $scope.itemInterno.id_categoria = '4863277368606720';
                    $scope.itemInterno.descricao = '';
                    $scope.salvandoFlag = false;
                }).error(function(data){
                    console.log('erro');
                    console.log(data);
                    $scope.erros = data;
                    $scope.salvandoFlag = false;
                });
            }
        }
    };
});