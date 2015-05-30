# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from model.db import *
from tekton.gae.middleware.json_middleware import JsonUnsecureResponse
from distutils import log

__author__ = 'Rodrigo'

__ctx = {'items':'','categorias':'','erros':''}


'''
@login_not_required
@no_csrf
def index():
    __ctx['items'] = ''
    query = Categoria.query().order(Categoria.categoria)
    __ctx['categorias'] = query.fetch()
    return TemplateResponse(__ctx)

@login_not_required
@no_csrf
def salvar(_resp,**itens):
    item_form = ItemForm(**itens)
    erros = item_form.validate()
    if erros:
        _resp.set_status(400)
        dct = erros
    else:
        item = item_form.fill_model()
        item.put()
        dct = item_form.fill_with_model(item)
        log.info(dct)
    return JsonUnsecureResponse(dct)
'''