# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaeforms.ndb.form import ModelForm
from gaepermission.decorator import login_required
from operator import itemgetter
from tekton import router
from google.appengine.ext import ndb
from tekton.gae.middleware.redirect import RedirectResponse

__author__ = 'Rodrigo'

categorias = {'op-lvr-mng-hq':'Livros, Mangás e HQs','op-cd-dvd-bry':'CDs, DVDs e BLU-RAYs','op-vstr':'Vestuário','op-inf':'Informática',
             'op-brq-gms':'Brinquedos e Games','op-mvs':'Móveis','op-outros':'Outros'}

categorias = dict(sorted(categorias.items(), key=itemgetter(1))) # itemgetter(1) para ordenar pelo valor, se colocar 0, ordena pela chave
            #converte para dict novamente, pois sorted retorna um list com tuplas dentro

@login_required
@no_csrf
def index():
    contexto = {'categorias':categorias,'salvar':router.to_path(salvar),
                'errors':'', 'item':''}
    return TemplateResponse(contexto,template_path='/meuperfil/caixaesquerda/cadastraritens/cadastraritens.html')

@login_required
@no_csrf
def salvar(**itens):
    item_form = ItemForm(**itens)

    errors = item_form.validate()

    if errors:
        contexto = {'categorias':categorias,'salvar':router.to_path(salvar),
                    'errors':errors, 'item':item_form}
        return TemplateResponse(contexto,template_path='/meuperfil/caixaesquerda/cadastraritens/cadastraritens.html')
    else:
        novo_item = item_form.fill_model()
        novo_item.put()

    return RedirectResponse('/meuperfil/caixaesquerda/cadastraritens/cadastraritens')

class Item(ndb.Model):
    titulo = ndb.StringProperty(required=True)
    #categoria = ndb.StringProperty(required=True)
    imagem = ndb.StringProperty(required=True)
    descricao = ndb.StringProperty(required=True)

class ItemForm(ModelForm):
    _model_class_ = Item
    _include = [Item.titulo, Item.imagem, Item.descricao]
