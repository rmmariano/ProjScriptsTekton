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

__ctx = {'itens':'','path_editar':'','path_excluir':''}

@login_required
@no_csrf
def index():
    query = Item.query().order(Item.titulo)
    __ctx['itens'] = query.fetch()
    __ctx['path_editar'] = router.to_path(editar)
    __ctx['path_excluir'] = router.to_path(excluir)
    return TemplateResponse(__ctx)

@login_required
@no_csrf
def editar(_resp,**itens):

    _resp.write('editar , '+str(itens))

@login_required
@no_csrf
def excluir(_resp,**itens):

    _resp.write('excluir , '+str(itens))




class Item(Node):
    titulo = ndb.StringProperty(required=True)
    descricao = ndb.StringProperty(required=True)

class ItemForm(ModelForm):
    _model_class = Item
    _include = [Item.titulo, Item.descricao]