# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required
from tekton import router
from model.db import *

__author__ = 'Rodrigo'

__ctx = {'items':'','categorias':'','salvar':'','erros':'','sucesso':0}

@login_required
@no_csrf
def index():
    __ctx['salvar'] = router.to_path(salvar)
    __ctx['sucesso'] = 0
    __ctx['items'] = ''
    query = Categoria.query().order(Categoria.categoria)
    __ctx['categorias'] = query.fetch()
    return TemplateResponse(__ctx)

@login_required
@no_csrf
def salvar(**itens):
    __ctx['salvar'] = router.to_path(salvar)
    item_form = ItemForm(**itens)
    erros = item_form.validate()
    if erros:
        __ctx['erros'] = erros
        __ctx['items'] = item_form
        __ctx['sucesso'] = 0
    else:
        item = item_form.fill_model()
        item.put()
        __ctx['sucesso'] = 1
    query = Categoria.query().order(Categoria.categoria)
    __ctx['categorias'] = query.fetch()
    return TemplateResponse(__ctx,'/meuperfil/caixaesquerda/cadastraritens/cadastraritens.html')