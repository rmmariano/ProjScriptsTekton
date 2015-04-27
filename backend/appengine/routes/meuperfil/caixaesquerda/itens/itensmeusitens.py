# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaegraph.model import Arc
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required
from tekton.gae.middleware.redirect import RedirectResponse

from gaeforms.ndb.form import ModelForm
from gaegraph.model import Node
from google.appengine.ext import ndb
from tekton import router

__author__ = 'Rodrigo'

__ctx = {'items':'','item':'','categorias':'',
         'erros':'','sucesso':-1,'safe':'',
         'path_editar':'','path_editar_form':'',
         'path_excluir':''}

@login_required
@no_csrf
def index():
    query = Item.query().order(Item.titulo)
    item_lista = query.fetch()
    query = Categoria.query().order(Categoria.categoria)
    categorias = query.fetch()
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
    __ctx['erros'] = ''
    __ctx['sucesso'] = -1
    return TemplateResponse(__ctx)

@login_required
@no_csrf
def editar(id,**itens):
    id = int(id)
    item = Item.get_by_id(id)
    item_form = ItemForm(**itens)
    itens['categoria_selecionada'] = ndb.Key(Categoria,int(itens['categoria_selecionada'])) #pega o objeto Key a partir de uma chave dada
    erros = item_form.validate()
    __ctx['path_editar'] = router.to_path(editar,id)
    if erros:
        __ctx['erros'] = erros
        __ctx['item'] = item_form
        __ctx['sucesso'] = 0
        return TemplateResponse(__ctx,'/meuperfil/caixaesquerda/itens/editar_form.html')
    else:
        item_form.fill_model(item)
        item.put()
        __ctx['sucesso'] = 1
        return RedirectResponse(router.to_path(index))



        '''
        item_form.fill_model(item)
        chave_item = item.put() #salva o item e pega a chave dele
        chave_categoria = itens['categoria_selecionada']
        tem_arco = TemArco(origin = chave_item, destination = chave_categoria) #cria o relacionamento
        tem_arco.put() #salva o relacionamento
        __ctx['sucesso'] = 1
        '''


@login_required
@no_csrf
def editar_form(_resp,id):
    id = int(id)
    item = Item.get_by_id(id)
    item_form = ItemForm()
    item_form.fill_with_model(item)
    __ctx['item'] = item
    __ctx['path_editar'] = router.to_path(editar,id)
    query = Categoria.query().order(Categoria.categoria)

    #_resp.write(item)

    __ctx['categorias'] = query.fetch()
    return TemplateResponse(__ctx,'/meuperfil/caixaesquerda/itens/editar_form.html')

@login_required
@no_csrf
def excluir(_resp,id):
    chave = ndb.Key(Item,int(id))
    chave.delete()
    return RedirectResponse(router.to_path(index))



class Item(Node):
    titulo = ndb.StringProperty(required=True)
    descricao = ndb.StringProperty(required=True)
    id_categoria = ndb.StringProperty(required=False)

class ItemForm(ModelForm):
    _model_class = Item
    _include = [Item.titulo, Item.descricao, Item.id_categoria]

class Categoria(Node):
    categoria = ndb.StringProperty(required=True)

class CategoriaForm(ModelForm):
    _model_class = Categoria
    _include = [Categoria.categoria]

class TemArco(Arc):
    origin = ndb.KeyProperty(Item,required=True)
    destination = ndb.KeyProperty(Categoria,required=True)