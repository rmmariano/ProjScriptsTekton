# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaeforms.ndb.form import ModelForm
from gaegraph.model import Node
from google.appengine.ext import ndb

__author__ = 'Rodrigo'

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