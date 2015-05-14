var ajax_gif_img = '-ajax-gif-img', err_div = '-err-div', err_int_div = '-err-int-div', main_div = '-main-div';
var exc_sucesso_div = 'exc-sucesso-div', ex_mdl = '-ex-mdl';
var $item_id_err_div = '', $exc_sucesso_div = '', $item_id_ex_mdl = '';

function limparItem(item_id){
    $item_id_err_div = $('#'+item_id.toString()+err_div);
    $item_id_err_div.hide();
}

function excluirItem(item_id){
    var item_id = item_id.toString();
    if(item_id == ''){ return; }
    var $ajax_gif_img = $('#'+item_id+ajax_gif_img);
    $ajax_gif_img.show();
    var $item_id_main_div = $('#'+item_id+main_div);
    $item_id_err_div = $('#'+item_id+err_div);
    $item_id_err_div.hide();
    $exc_sucesso_div = $('#'+exc_sucesso_div);
    $item_id_ex_mdl = $('#'+item_id+ex_mdl);
    $.ajax({
        url: '/meuperfil/caixaesquerda/itens/itensmeusitens/excluir/'+item_id,
        data: {},
        success: function(data){
            $ajax_gif_img.hide();
            $item_id_ex_mdl.modal('hide'); /* faz o modal (junto com a tela escura) desaparecer */
            $item_id_main_div.hide(); /* faz sumir todo o main_div do item */
            $exc_sucesso_div.show();
        },
        error: function(data){
            var $item_id_err_int_div = $('#'+item_id+err_int_div);
            $item_id_err_int_div.val(data.responseJSON['error']);
            $item_id_err_div.show();
            $ajax_gif_img.hide();
        }
    });
}

/* corresponde ao cadastrar item*/
$(document).ready(function(){
    var titulo = 'titulo', descricao = 'descricao', id_categoria = 'id_categoria', add_sucesso = 'add-sucesso', ajax_gif = 'ajax-gif';
    var $tituloInput = $('#'+titulo+'-in'), $descricaoInput = $('#'+descricao+'-in'), $addSucessoDiv = $('#'+add_sucesso+'-div'), $ajax_gif = $('#'+ajax_gif+'-img');
    var doc_cat = document.getElementById(id_categoria);
    var new_item = '';

    var $rowMain = $('#row-main');

    function obterInputsItem(){ return { titulo: $tituloInput.val(), descricao: $descricaoInput.val(), id_categoria: doc_cat.options[doc_cat.selectedIndex].value }; }

    function limparInputsItem(){ $('#'+titulo+'-div').removeClass('has-error'); $('#'+titulo+'-span').text(''); $('#'+descricao+'-div').removeClass('has-error'); $('#'+descricao+'-span').text(''); $addSucessoDiv.hide(); }

    function adicionarItem(item){
        new_item = '<div id="'+item.id+'}}-main-div">'+
                    '<div class="col-sm-4 col-md-4">' +
                        '<div class="thumbnail">'+
                            '<img data-src="holder.js/100%x200" alt="100%x200" src="" data-holder-rendered="true" style="height: 200px; width: 100%; display: block;">'+
                            '<div class="caption">'+
                                '<h4>'+item.titulo+'</h4>'+
                                '<p>'+item.categoria+'</p>'+
                                '<p>';

        if (item.descricao.length >= 40) {
            new_item = new_item + item.descricao.substr(0,40);
        }else{
            new_item = new_item + item.descricao;
        }

        new_item = new_item + '</p>'+
                                '<div class="row">'+
                                    '<div class="col-sm-6 col-md-6">'+
                                        '<a href="'+item.path_editar_form+'">'+
                                            '<button type="submit" class="btn btn-info">'+
                                                '<span class="glyphicon glyphicon-pencil" aria-hidden="true"></span> Editar '+
                                            '</button>'+
                                        '</a>'+
                                    '</div>'+
                                    '<div class="col-sm-6 col-md-6">'+
                                        '<button type="button" onclick="limparItem('+item.id+');" class="btn btn-danger" data-toggle="modal" data-target="#'+item.id+'-ex-mdl">'+
                                            '<span class="glyphicon glyphicon-trash" aria-hidden="true"></span> Excluir'+
                                        '</button>'+
                                    '</div>'+
                                '</div>'+
                            '</div>'+
                        '</div>'+
                    '</div>'+
                    '<div class="modal fade" id="'+item.id+'-ex-mdl" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">'+
                        '<div class="modal-dialog">'+
                            '<div class="modal-content">'+
                                '<div class="modal-header">'+
                                    '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'+
                                    '<h4 class="modal-title" id="exampleModalLabel"> Excluir </h4>'+
                                '</div>'+
                                '<div class="modal-body">'+
                                    '<div class="form-group">'+
                                        '<h3> Deseja realmente excluir "'+ item.titulo+'"? </h3>'+
                                        '<div id="'+ item.id+'-err-div" class="alert alert-danger" role="alert" style="margin-bottom: 0px; margin-top: 20px; display: none;">'+
                                            '<span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span>'+
                                            'Ops!!! Ocorreu algum problema, tente novamente mais tarde!'+
                                            '<div id="'+ item.id +'-err-int-div"></div>'+
                                        '</div>'+
                                    '</div>'+
                                '</div>'+
                                '<div class="modal-footer">'+
                                    '<center>'+
                                        '<button id="'+ item.id +'-btn" onclick="excluirItem('+ item.id +');" class="btn btn-primary"><span class="glyphicon glyphicon-ok" aria-hidden="true"></span> Sim </button>'+
                                        '<button type="button" class="btn btn-default" data-dismiss="modal"> <span class="glyphicon glyphicon-remove" aria-hidden="true"></span> Não </button> '+
                                        '<img id="'+ item.id +'-ajax-gif-img" src="/static/img/ajax.gif" style="display: none; margin-left: 20px;"/>'+
                                    '</center>'+
                                '</div>'+
                            '</div>'+
                        '</div>'+
                    '</div>'+
                '</div>';

        console.log(new_item);

        $rowMain.append(new_item);
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
            url: '/meuperfil/caixaesquerda/itens/itensmeusitens/salvar',
            data: obterInputsItem(),
            success: function(data){
                $tituloInput.val(''); $descricaoInput.val(''); limparInputsItem(); $addSucessoDiv.show(); doc_cat[0].selected = true; $ajax_gif.hide();
                adicionarItem(data);
            },
            error: function(data){
                for (propriedade in data.responseJSON){
                    if (data.responseJSON[propriedade] != ''){
                        $('#'+propriedade+'-div').addClass('has-error'); $('#'+propriedade+'-span').text(data.responseJSON[propriedade]);
                    }
                }
                $ajax_gif.hide();
            }
        });
    });
});