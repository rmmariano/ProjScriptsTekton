// Load this script when page loads
$(document).ready(function(){
    var titulo = 'titulo', descricao = 'descricao', id_categoria = 'id_categoria', add_sucesso = 'add-sucesso', ajax_gif = 'ajax-gif';
    var $tituloInput = $('#'+titulo+'-in'), $descricaoInput = $('#'+descricao+'-in'), $addSucessoDiv = $('#'+add_sucesso+'-div'), $ajax_gif = $('#'+ajax_gif+'-img');
    var doc_cat = document.getElementById(id_categoria);

    function obterInputsItem(){
        return {
            titulo: $tituloInput.val(),
            descricao: $descricaoInput.val(),
            id_categoria: doc_cat.options[doc_cat.selectedIndex].value
        };
    }

    function limparInputsItem(){
        $('#'+titulo+'-div').removeClass('has-error');
        $('#'+titulo+'-span').text('');
        $('#'+descricao+'-div').removeClass('has-error');
        $('#'+descricao+'-span').text('');
        $addSucessoDiv.hide();
    }

    limparInputsItem();

    $('#adicionar-btn').click(function(){
        limparInputsItem();
        var erro = false;
        if($tituloInput.val() == ''){ $('#'+titulo+'-div').addClass('has-error'); $('#'+titulo+'-span').text('Insira um título!'); erro = true; }
        if($descricaoInput.val() == ''){ $('#'+descricao+'-div').addClass('has-error'); $('#'+descricao+'-span').text('Insira uma descrição!'); erro = true; }
        if(erro){ return; }
        $ajax_gif.show();
        $.ajax({
            url: '/meuperfil/caixaesquerda/cadastraritens/cadastraritens/salvar',
            data: obterInputsItem(),
            success: function(data){
                $tituloInput.val(''); $descricaoInput.val('');
                limparInputsItem();
                $addSucessoDiv.show();
                doc_cat[0].selected = true;
                $ajax_gif.hide();
            },
            error: function(data){
                for (propriedade in data.responseJSON){
                    if (data.responseJSON[propriedade] != ''){
                        $('#'+propriedade+'-div').addClass('has-error');
                        $('#'+propriedade+'-span').text(data.responseJSON[propriedade]);
                    }
                }
                $ajax_gif.hide();
            }
        });
    });
});