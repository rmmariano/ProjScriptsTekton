# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaegraph.model import Arc
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required
from tekton import router

from gaeforms.ndb.form import ModelForm
from gaegraph.model import Node
from google.appengine.ext import ndb

__author__ = 'Rodrigo'

__ctx = {'items':'','categorias':'',
         'salvar':'','erros':'','sucesso':0}

@login_required
@no_csrf
def index():
    __ctx['salvar'] = router.to_path(salvar)
    __ctx['sucesso'] = 0
    query = Categoria.query().order(Categoria.categoria)
    __ctx['categorias'] = query.fetch()
    return TemplateResponse(__ctx)

@login_required
@no_csrf
def salvar(**itens):
    __ctx['salvar'] = router.to_path(salvar)
    item_form = ItemForm(**itens)
    #itens['id_categoria'] = ndb.Key(Categoria,int(itens['id_categoria'])) #pega o objeto Key a partir de uma chave dada

    #itens['id_categoria'] = int(itens['id_categoria'])
    erros = item_form.validate() #verifica se contém algum campo inválido
    if erros:
        __ctx['erros'] = erros
        __ctx['items'] = item_form
        __ctx['sucesso'] = 0
    else:
        item = item_form.fill_model()
        item.put()
        __ctx['sucesso'] = 1



        '''
        chave_item = item.put() #salva o item e pega a chave dele
        chave_categoria = itens['categoria_selecionada']
        tem_arco = TemArco(origin = chave_item, destination = chave_categoria) #cria o relacionamento
        tem_arco.put() #salva o relacionamento
        __ctx['sucesso'] = 1
        '''

    '''
    #Caso necessite adicionar mais categorias
    categorias = {'categoria':'CDs, DVDs e BLU-RAYs'}
    cat_form = CategoriaForm(**categorias)
    cat = cat_form.fill_model()
    cat.put()
    '''
    return TemplateResponse(__ctx,'/meuperfil/caixaesquerda/cadastraritens/cadastraritens.html')



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