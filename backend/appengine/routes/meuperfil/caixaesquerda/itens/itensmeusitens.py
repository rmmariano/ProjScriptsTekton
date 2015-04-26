# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required

from gaeforms.ndb.form import ModelForm
from gaegraph.model import Node
from google.appengine.ext import ndb
from tekton import router

__author__ = 'Rodrigo'

__ctx = {'items':'','item':'','erros':'','sucesso':0,
         'path_editar':'','path_editar_form':'',
         'path_excluir':''}

@login_required
@no_csrf
def index():
    query = Item.query().order(Item.titulo)
    __ctx['itens'] = query.fetch()
    __ctx['path_editar_form'] = router.to_path(editar_form)
    __ctx['path_excluir'] = router.to_path(excluir)
    return TemplateResponse(__ctx)

@login_required
@no_csrf
def editar(_resp,**item):
    item['id'] = int(item['id'])

    _resp.write(item)

    '''
    item_form = ItemForm(**itens)
    erros = item_form.validate()

    __ctx['path_editar'] = router.to_path(editar)
    __ctx['path_excluir'] = router.to_path(excluir)

    if erros:
        __ctx['erros'] = erros
        __ctx['items'] = item_form
        __ctx['sucesso'] = 0
    else:
        item = item_form.fill_model()
        item.put()
        __ctx['sucesso'] = 1
    '''
    '''
    __ctx['sucesso'] = 1
    __ctx['item'] = item
    __ctx['path_editar'] = router.to_path(editar)
    return TemplateResponse(__ctx,'/meuperfil/caixaesquerda/itens/editar_form.html')
    '''

@login_required
@no_csrf
def editar_form(id):
    item = Item.get_by_id(int(id))
    __ctx['item'] = item
    __ctx['path_editar'] = router.to_path(editar)
    return TemplateResponse(__ctx,'/meuperfil/caixaesquerda/itens/editar_form.html')

'''
    item_form = ItemForm(**itens)
    erros = item_form.validate()
    __ctx['salvar'] = router.to_path(salvar)
    if erros:
        __ctx['erros'] = erros
        __ctx['items'] = item_form
    else:
        item = item_form.fill_model()
        item.put()
        __ctx['sucesso'] = 1
    return TemplateResponse(__ctx,'/meuperfil/caixaesquerda/cadastraritens/cadastraritens.html')
'''


@login_required
@no_csrf
def excluir(_resp,**itens):

    _resp.write('excluir , '+str(itens))
    return TemplateResponse(__ctx,'/meuperfil/caixaesquerda/itens/itensmeusitens.html')




class Item(Node):
    titulo = ndb.StringProperty(required=True)
    descricao = ndb.StringProperty(required=True)

class ItemForm(ModelForm):
    _model_class = Item
    _include = [Item.titulo, Item.descricao]