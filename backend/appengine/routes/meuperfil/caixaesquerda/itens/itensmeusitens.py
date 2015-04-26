# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required
from tekton.gae.middleware.redirect import RedirectResponse

from gaeforms.ndb.form import ModelForm
from gaegraph.model import Node
from google.appengine.ext import ndb
from tekton import router

__author__ = 'Rodrigo'

__ctx = {'items':'','item':'','erros':'','sucesso':-1,
         'path_editar':'','path_editar_form':'',
         'path_excluir':''}

@login_required
@no_csrf
def index():
    query = Item.query().order(Item.titulo)
    item_lista = query.fetch()

    form = ItemForm()

    item_lista = [form.fill_with_model(item) for item in item_lista]

    p_editar_form = router.to_path(editar_form)
    p_excluir = router.to_path(excluir)
    for item in item_lista:
        item['path_editar_form'] = '%s/%s'%(p_editar_form,item['id'])
        item['path_excluir'] = '%s/%s'%(p_excluir,item['id'])

    __ctx['itens'] = item_lista
    __ctx['erros'] = ''
    __ctx['sucesso'] = -1

    return TemplateResponse(__ctx)

@login_required
@no_csrf
def editar(id,**itens):
    id = int(id)
    item = Item.get_by_id(id)
    item_form = ItemForm(**itens)
    erros = item_form.validate()

    __ctx['path_editar'] = router.to_path(editar,id)
    if erros:
        __ctx['erros'] = erros
        __ctx['sucesso'] = 0
        __ctx['item'] = item_form
        return TemplateResponse(__ctx,'/meuperfil/caixaesquerda/itens/editar_form.html')
    else:
        item_form.fill_model(item)
        item.put()
        __ctx['sucesso'] = 1

        return RedirectResponse(router.to_path(index))


@login_required
@no_csrf
def editar_form(id):
    id = int(id)
    item = Item.get_by_id(id)
    item_form = ItemForm()
    item_form.fill_with_model(item)
    __ctx['item'] = item
    __ctx['path_editar'] = router.to_path(editar,id)
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