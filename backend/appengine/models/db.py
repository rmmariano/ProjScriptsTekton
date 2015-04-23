from google.appengine.ext import ndb
from gaegraph.model import Node

__author__ = 'Rodrigo'

class Item(Node):
    titulo = ndb.StringProperty(required=True)
    #categoria = ndb.StringProperty(required=True)
    imagem = ndb.StringProperty(required=True)
    descricao = ndb.StringProperty(required=True)

