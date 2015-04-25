# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
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

__ctx = {'salvar':'','erros':'','items':''}

@login_required
@no_csrf
def index():
    __ctx['salvar'] = router.to_path(salvar)
    return TemplateResponse(__ctx)

@login_required
@no_csrf
def salvar(**itens):
    item_form = ItemForm(**itens)
    erros = item_form.validate()
    __ctx['salvar'] = router.to_path(salvar)
    if erros:
        __ctx['erros'] = erros
        __ctx['items'] = item_form
    else:
        item = item_form.fill_model()
        item.put()
    return TemplateResponse(__ctx,'/meuperfil/caixaesquerda/cadastraritens/cadastraritens.html')


class Item(Node):
    titulo = ndb.StringProperty(required=True)
    descricao = ndb.StringProperty(required=True)

class ItemForm(ModelForm):
    _model_class = Item
    _include = [Item.titulo, Item.descricao]
