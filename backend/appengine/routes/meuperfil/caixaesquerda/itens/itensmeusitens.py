# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required
from tekton import router
from tekton.gae.middleware.redirect import RedirectResponse
from model.db import *
from tekton.gae.middleware.json_middleware import JsonUnsecureResponse
from distutils import log
from json import dumps


__author__ = 'Rodrigo'

__ctx = {'items':'','item':'','categorias':'','categoria_selecionada':'','erros':'','sucesso':-1,'safe':'','encontrado':-1,
         'path_editar':'','path_editar_form':'','path_excluir':'','path_pesquisar':'', 'path_listar':''}

#__ctx = {'items':'','categorias':'','erros':''}

__dct = {'error':''}

@login_required
@no_csrf
def index(id_categoria = None):
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
            #item['path_excluir'] = '%s/%s'%(p_excluir,item['id'])
            item['id_categoria'] = ndb.Key(Categoria,int(item['id_categoria']))
            for cat in categorias:
                if item['id_categoria'] == cat.key:
                    item['categoria'] = cat.categoria
                    item['id_categoria'] = ''
                    break
        __ctx['itens'] = item_lista
        __ctx['encontrado'] = 1
    else:
        __ctx['encontrado'] = 0
    __ctx['categorias'] = categorias
    __ctx['erros'] = ''
    __ctx['sucesso'] = -1
    __ctx['path_index'] = router.to_path(index)
    __ctx['path_salvar'] = router.to_path(salvar)
    __ctx['path_listar'] = router.to_path(listar)
    __ctx['path_excluir'] = router.to_path(excluir)
    __ctx['path_editar'] = router.to_path(editar)

    __ctx['itens'] = dumps(item_lista) #converte o item_lista para json

    return TemplateResponse(__ctx)

'''
@login_required
@no_csrf
def index(id_categoria = None, buscar = '0'):
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
            #item['path_excluir'] = '%s/%s'%(p_excluir,item['id'])
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
    __ctx['path_salvar'] = router.to_path(salvar)

    return TemplateResponse(__ctx)
'''

@login_required
@no_csrf
def listar(_resp,id_cat_buscar = None):
    categorias = (Categoria.query().order(Categoria.categoria)).fetch()
    form = ItemForm()

    if id_cat_buscar == 'all' or id_cat_buscar == None:
        item_lista = (Item.query().order(Item.titulo)).fetch()
    else:
        item_lista = (Item.query(Item.id_categoria == id_cat_buscar).order(Item.titulo)).fetch()

    if item_lista > 0:
        item_lista = [form.fill_with_model(p) for p in item_lista]
        p_editar_form = router.to_path(editar_form)
        for item in item_lista:
            item['path_editar_form'] = '%s/%s'%(p_editar_form,item['id'])
            key_cat = ndb.Key(Categoria,int(item['id_categoria']))
            for cat in categorias:
                if key_cat == cat.key:
                    item['categoria'] = cat.categoria
                    break
    else:
        item_lista = {'error':'Não foi encontrado nenhum item.'}
        _resp.set_status(400)

    return JsonUnsecureResponse(item_lista)

@login_required
@no_csrf
def editar(_resp,id,**itens):
    id = int(id)
    item_bd = Item.get_by_id(id)
    item_form = ItemForm(**itens)
    erros = item_form.validate()
    if erros:
        _resp.set_status(400)
        dct = erros
    else:
        item_bd.titulo = itens['titulo']
        item_bd.id_categoria = itens['id_categoria']
        item_bd.descricao = itens['descricao']
        item_bd.put()

        dct = item_form.fill_with_model(item_bd)

    log.info(dct)
    return JsonUnsecureResponse(dct)

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
        categorias = (Categoria.query().order(Categoria.categoria)).fetch()
        p_editar_form = router.to_path(editar_form)
        dct['path_editar_form'] = '%s/%s'%(p_editar_form,dct['id'])
        key_cat = ndb.Key(Categoria,int(dct['id_categoria']))
        for cat in categorias:
            if key_cat == cat.key:
                dct['categoria'] = cat.categoria
                break
        log.info(dct)
    return JsonUnsecureResponse(dct)

