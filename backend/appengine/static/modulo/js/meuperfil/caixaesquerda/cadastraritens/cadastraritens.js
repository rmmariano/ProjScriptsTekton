// Load this script when page loads
$(document).ready(function(){
    var titulo = 'titulo', descricao = 'descricao', id_cat = 'id_cat';
    var add_sucesso = 'add-sucesso'

    var $tituloInput = $('#'+titulo+'-in');
    var $descricaoInput = $('#'+descricao+'-in');
    var doc_cat = document.getElementById(id_cat);
    //var itemSelecionado = doc_cat.options[doc_cat.selectedIndex].value;

    var $addSucessoDiv = $('#'+add_sucesso+'-div');

    function obterInputsItem(){
        return {
            titulo: $tituloInput.val(),
            descricao: $descricaoInput.val(),
            id_cat: doc_cat.options[doc_cat.selectedIndex].value
        };
    }

    function limparInputsItem(){
        $tituloInput.text('');
        $('#'+titulo+'-div').removeClass('has-error');
        $('#'+titulo+'-span').text('');
        $descricaoInput.text('');
        $('#'+descricao+'-div').removeClass('has-error');
        $('#'+descricao+'-span').text('');
        $addSucessoDiv.hide();
    }

    limparInputsItem();

    $('#adicionar-btn').click(function(){
        var erro = false;
        if($tituloInput.val() == ''){
            $('#'+titulo+'-div').addClass('has-error');
            $('#'+titulo+'-span').text('Insira um título!');
            erro = true;
        }
        if($descricaoInput.val() == ''){
            $('#'+descricao+'-div').addClass('has-error');
            $('#'+descricao+'-span').text('Insira uma descrição!');
            erro = true;
        }
        if(erro){ return; }

        $.ajax({
            url: '/meuperfil/caixaesquerda/cadastraritens/cadastraritens/salvar',
            data: obterInputsItem(),
            success: function(data){
                limparInputsItem();
                $addSucessoDiv.show();
            },
            error: function(data){

            },
            always: function(){
                
            }
        });
    });
});