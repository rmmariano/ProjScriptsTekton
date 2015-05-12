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