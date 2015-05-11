var ajax_gif_img = 'ajax-gif-img', err_div = '-err-div', err_int_div = '-err-int-div', main_div = '-main-div';
var $item_id_err_div = '';

function limparItem(item_id){
    $item_id_err_div = $('#'+item_id.toString()+err_div);
    $item_id_err_div.hide();
}

function excluirItem(item_id){
    var item_id = item_id.toString();
    if(item_id == ''){ return; }
    var $ajax_gif_img = $('#'+item_id+ajax_gif_img);
    $ajax_gif_img.show();
    var item_id_main_div = $('#'+item_id+main_div);
    $item_id_err_div = $('#'+item_id+err_div);
    $item_id_err_div.hide();
    $.ajax({
        url: '/meuperfil/caixaesquerda/itens/itensmeusitens/excluir/'+item_id,
        data: {},
        success: function(data){
            item_id_main_div.hide();
            $ajax_gif_img.hide();
        },
        error: function(data){
            var item_id_err_int_div = $('#'+item_id+err_int_div);
            item_id_err_int_div.val(data.responseJSON['error']);
            $item_id_err_div.show();
            $ajax_gif_img.hide();
        }
    });
}