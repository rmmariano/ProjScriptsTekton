# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton import router
from model.db import *

__author__ = 'Rodrigo'

__ctx = {'categorias':'','salvar':'','erros':'','sucesso':0}

@login_not_required
@no_csrf
def index():
    __ctx['salvar'] = router.to_path(salvar)
    __ctx['sucesso'] = 0
    __ctx['categorias'] = ''
    __ctx['erros'] = ''
    return TemplateResponse(__ctx)

@login_not_required
@no_csrf
def salvar(**itens):
    __ctx['salvar'] = router.to_path(salvar)
    categoria_form = CategoriaForm(**itens)
    erros = categoria_form.validate()
    if erros:
        __ctx['erros'] = erros
        __ctx['categorias'] = categoria_form
        __ctx['sucesso'] = 0
    else:
        categoria = categoria_form.fill_model()
        categoria.put()
        __ctx['sucesso'] = 1
    return TemplateResponse(__ctx,'/meuperfil/caixaesquerda/cadastrarcategorias/cadastrarcategorias.html')