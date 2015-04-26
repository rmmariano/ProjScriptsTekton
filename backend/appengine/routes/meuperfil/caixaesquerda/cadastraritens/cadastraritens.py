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


'''
categorias = {'op-lvr-mng-hq':'Livros, Mangás e HQs','op-cd-dvd-bry':'CDs, DVDs e BLU-RAYs','op-vstr':'Vestuário','op-inf':'Informática',
             'op-brq-gms':'Brinquedos e Games','op-mvs':'Móveis','op-outros':'Outros'}

categorias = dict(sorted(categorias.items(), key=itemgetter(1))) # itemgetter(1) para ordenar pelo valor, se colocar 0, ordena pela chave
            #converte para dict novamente, pois sorted retorna um list com tuplas dentro
'''

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
    itens['categoria_selecionada'] = ndb.Key(Categoria,int(itens['categoria_selecionada'])) #pega o objeto Key a partir de uma chave dada
    erros = item_form.validate()

    if erros:
        __ctx['erros'] = erros
        __ctx['items'] = item_form
    else:
        item = item_form.fill_model()

        chave_item = item.put() #salva o item e pega a chave dele
        chave_categoria = itens['categoria_selecionada']

        tem_arco = TemArco(origin = chave_item, destination = chave_categoria) #cria o relacionamento
        tem_arco.put() #salva o relacionamento

        __ctx['sucesso'] = 1

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

class ItemForm(ModelForm):
    _model_class = Item
    _include = [Item.titulo, Item.descricao]

class Categoria(Node):
    categoria = ndb.StringProperty(required=True)

class CategoriaForm(ModelForm):
    _model_class = Categoria
    _include = [Categoria.categoria]

class TemArco(Arc):
    origin = ndb.KeyProperty(Item,required=True)
    destination = ndb.KeyProperty(Categoria,required=True)