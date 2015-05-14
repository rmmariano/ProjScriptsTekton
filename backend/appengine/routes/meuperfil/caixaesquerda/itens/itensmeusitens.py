# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required
from tekton import router
from tekton.gae.middleware.redirect import RedirectResponse
from model.db import *
from tekton.gae.middleware.json_middleware import JsonUnsecureResponse

__author__ = 'Rodrigo'

__ctx = {'items':'','item':'','categorias':'','categoria_selecionada':'','erros':'','sucesso':-1,'safe':'','encontrado':-1,
         'path_editar':'','path_editar_form':'','path_excluir':'','path_pesquisar':''}

#__ctx = {'items':'','categorias':'','erros':''}

__dct = {'error':''}

@login_required
@no_csrf
def index(id_categoria = None, **itens):
    if id_categoria == None or id_categoria == 'all':
        query = Item.query().order(Item.titulo)
        item_lista = query.fetch()
        if id_categoria == 'all':
            __ctx['categoria_selecionada'] = 'all'
        else:
            __ctx['categoria_selecionada'] = ''
    else:
        query = Item.query(Item.id_categoria == id_categoria).order(Item.titulo)
        item_lista = query.fetch()
        __ctx['categoria_selecionada'] = id_categoria

    query = Categoria.query().order(Categoria.categoria)
    categorias = query.fetch()

    if len(item_lista) > 0:
        form = ItemForm()
        item_lista = [form.fill_with_model(item) for item in item_lista] #transforma a classe em dicionário para poder adicionar valores dinamicamente
        p_editar_form = router.to_path(editar_form)
        p_excluir = router.to_path(excluir)
        for item in item_lista:
            item['path_editar_form'] = '%s/%s'%(p_editar_form,item['id'])
            item['path_excluir'] = '%s/%s'%(p_excluir,item['id'])
            item['id_categoria'] = ndb.Key(Categoria,int(item['id_categoria']))
            for cat in categorias:
                if item['id_categoria'] == cat.key:
                    item['categoria'] = cat.categoria
                    break
        __ctx['itens'] = item_lista
        __ctx['encontrado'] = 1
    else:
        __ctx['encontrado'] = 0

    __ctx['categorias'] = categorias
    __ctx['erros'] = ''
    __ctx['sucesso'] = -1
    __ctx['path_index'] = router.to_path(index)
    return TemplateResponse(__ctx)

@login_required
@no_csrf
def editar(id,**itens):
    id = int(id)
    item_bd = Item.get_by_id(id)
    item_form = ItemForm(**itens)
    erros = item_form.validate()
    __ctx['path_editar'] = router.to_path(editar,id)
    if erros:
        __ctx['erros'] = erros
        __ctx['item'] = item_form
        __ctx['sucesso'] = 0
        return TemplateResponse(__ctx,'/meuperfil/caixaesquerda/itens/editar_form.html')

    item_bd.titulo = itens['titulo']
    item_bd.id_categoria = itens['id_categoria']
    item_bd.descricao = itens['descricao']
    item_bd.put()
    __ctx['erros'] = ''
    __ctx['sucesso'] = 1
    return RedirectResponse(router.to_path(index))

@login_required
@no_csrf
def editar_form(id):
    id = int(id)
    item = Item.get_by_id(id)
    item_form = ItemForm()
    item_form.fill_with_model(item)
    __ctx['item'] = item_form
    __ctx['path_editar'] = router.to_path(editar,id)
    query = Categoria.query().order(Categoria.categoria)
    categorias = query.fetch()
    __ctx['categorias'] = categorias
    return TemplateResponse(__ctx,'/meuperfil/caixaesquerda/itens/editar_form.html')

@login_required
@no_csrf
def excluir(_resp,id):
    if id != '' and id != None:
        try:
            chave = ndb.Key(Item,int(id))
            chave.delete()
        except:
            _resp.set_status(400)
            __dct['error'] = 'Ocorreu algum problema ao excluir o item!'
    else:
        _resp.set_status(400)
        __dct['error'] = 'ID do item está vazio!'
    return JsonUnsecureResponse(__dct)



#o que estava em cadastraritens.py
'''
@login_required
@no_csrf
def index():
    __ctx['items'] = ''
    query = Categoria.query().order(Categoria.categoria)
    __ctx['categorias'] = query.fetch()
    return TemplateResponse(__ctx)
'''
@login_required
@no_csrf
def salvar(_resp,**itens):
    item_form = ItemForm(**itens)
    erros = item_form.validate()
    if erros:
        _resp.set_status(400)
        dct = erros
    else:
        item = item_form.fill_model()
        item.put()
        dct = item_form.fill_with_model(item)
        log.info(dct)
    return JsonUnsecureResponse(dct)
