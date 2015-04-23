# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required
from operator import itemgetter

__author__ = 'Rodrigo'

categorias = {'op-lvr-mng-hq':'Livros, Mangás e HQs','op-cd-dvd-bry':'CDs, DVDs e BLU-RAYs','op-vstr':'Vestuário','op-inf':'Informática',
             'op-brq-gms':'Brinquedos e Games','op-mvs':'Móveis','op-outros':'Outros'}

categorias = dict(sorted(categorias.items(), key=itemgetter(1))) # itemgetter(1) para ordenar pelo valor, se colocar 0, ordena pela chave
            #converte para dict novamente, pois sorted retorna um list com tuplas dentro

@login_required
@no_csrf
def index():
    contexto = {'categorias':categorias}
    return TemplateResponse(contexto,template_path='/meuperfil/caixaesquerda/cadastraritens/cadastraritens.html')

@login_required
@no_csrf
def salvar(**kwargs):

    return ''
