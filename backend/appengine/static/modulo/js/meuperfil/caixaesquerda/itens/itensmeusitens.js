var ajax_gif_img = '-ajax-gif-img', err_div = '-err-div', err_int_div = '-err-int-div', main_div = '-main-div';
var exc_sucesso_div = 'exc-sucesso-div', ex_mdl = '-ex-mdl';
var $item_id_err_div = '', $exc_sucesso_div = '', $item_id_ex_mdl = '',  $id_cat_buscar = '';

var doc_cat_buscar = '';

function limparRowMain(){
    var $row_main = $('#row-main');
    $row_main.empty();
}

function adicionarItem(item){
    var new_item = '';
    var $rowMain = $('#row-main');

    new_item = '<div id="'+item.id+'-main-div">'+
                '<div class="col-sm-4 col-md-4">' +
                    '<div class="thumbnail">'+
                        '<img data-src="holder.js/100%x200" alt="100%x200" src="" data-holder-rendered="true" style="height: 200px; width: 100%; display: block;">'+
                        '<div class="caption">'+
                            '<h4>'+item.titulo+'</h4>'+
                            '<p>'+item.categoria+'</p>'+
                            '<p>';
    if (item.descricao.length >= 40) { new_item = new_item + item.descricao.substr(0,40); }
    else{ new_item = new_item + item.descricao; }
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
    $rowMain.append(new_item);
}

function listarItens(){
    var $buscar_ajax_gif_img = $('#buscar-ajax-gif-img');
    doc_cat_buscar = document.getElementById('id_cat_buscar');
    var id_cat_buscar = doc_cat_buscar.options[doc_cat_buscar.selectedIndex].value;
    var $nenhumItem = $('#nenhum-item');
    var $ocorreu_problema = $('#ocorreu-problema');

    var lst = {'id_categoria':id_cat_buscar,'buscar':'1'};

    $buscar_ajax_gif_img.show();
    $.ajax({
        url: '/meuperfil/caixaesquerda/itens/itensmeusitens/listar',
        data: {},
        success: function(data){
            limparRowMain();
            if (data.length > 0) {
                var i;
                for (i = 0; i < data.length; i++) {
                    adicionarItem(data[i]);
                }
            }else{
                $nenhumItem.show();
            }
            doc_cat_buscar[0].selected = true;
            $buscar_ajax_gif_img.hide();
        },
        error: function(data){
            limparRowMain();
            $ocorreu_problema.show();
            $buscar_ajax_gif_img.hide();
        }
    });
}

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
            $item_id_main_div.hide(); /* faz sumir t odo o main_div do item */
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

    function obterInputsItem(){ return { titulo: $tituloInput.val(), descricao: $descricaoInput.val(), id_categoria: doc_cat.options[doc_cat.selectedIndex].value }; }

    function limparInputsItem(){ $('#'+titulo+'-div').removeClass('has-error'); $('#'+titulo+'-span').text(''); $('#'+descricao+'-div').removeClass('has-error'); $('#'+descricao+'-span').text(''); $addSucessoDiv.hide(); }

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
            type: "POST",
            data: obterInputsItem(),
            success: function(data){
                $tituloInput.val(''); $descricaoInput.val(''); limparInputsItem();
                $addSucessoDiv.show(); doc_cat[0].selected = true; $ajax_gif.hide();
                adicionarItem(data);
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