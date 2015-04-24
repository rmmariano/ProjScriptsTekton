# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required
from operator import itemgetter
from tekton import router
#from backend.appengine.models.db import Item
from google.appengine.ext import ndb
from gaegraph.model import Node
from tekton.gae.middleware.redirect import RedirectResponse

__author__ = 'Rodrigo'

categorias = {'op-lvr-mng-hq':'Livros, Mangás e HQs','op-cd-dvd-bry':'CDs, DVDs e BLU-RAYs','op-vstr':'Vestuário','op-inf':'Informática',
             'op-brq-gms':'Brinquedos e Games','op-mvs':'Móveis','op-outros':'Outros'}

categorias = dict(sorted(categorias.items(), key=itemgetter(1))) # itemgetter(1) para ordenar pelo valor, se colocar 0, ordena pela chave
            #converte para dict novamente, pois sorted retorna um list com tuplas dentro

@login_required
@no_csrf
def index():
    contexto = {'categorias':categorias,'salvar':router.to_path(salvar)}
    return TemplateResponse(contexto,template_path='/meuperfil/caixaesquerda/cadastraritens/cadastraritens.html')

@login_required
@no_csrf
def salvar(**itens):
    novo_item = Item(titulo = itens['titulo'], #categoria = itens['select'],
                     imagem = itens['imagem'], descricao = itens['descricao'])
    novo_item.put() #eh aqui que salva no DB
    return RedirectResponse('/meuperfil/caixaesquerda/cadastraritens/cadastraritens')

class Item(Node):
    titulo = ndb.StringProperty(required=True)
    #categoria = ndb.StringProperty(required=True)
    imagem = ndb.StringProperty(required=True)
    descricao = ndb.StringProperty(required=True)