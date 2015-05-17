//inicializa o módulo para a criação do <cadastraritemform></cadastraritemform>
var itemModulo = angular.module('itemModulo',[]);

//insere a diretiva que o itemModulo fará, no caso terá a tag <cadastraritemform></cadastraritemform>
//e onde ela for citada, substituirá pelo o que a diretiva retorna.
itemModulo.directive('cadastraritemform',function(){
    return {
        restrict: 'E',
        replace: true,
        templateUrl: '/static/modulo/html/meuperfil/caixaesquerda/itens/cadastraritemform.html',
        scope:{
            itemInterno:'=',
            tituloLabel:'@',
            categoriaLabel:'@',
            descricaoLabel:'@'
        }
    };
});