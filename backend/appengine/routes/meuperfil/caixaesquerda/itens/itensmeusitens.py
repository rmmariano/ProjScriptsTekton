# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required

__author__ = 'Rodrigo'

__ctx = {'itens':''}

@login_required
@no_csrf
def index(): #meuperfil/caixaesquerda/cadastraritens/cadastraritens.html
    itens = [{'titulo':'aaa','descricao':'bbb'},
             {'titulo':'qqq','descricao':'www'},
             {'titulo':'eee','descricao':'rrr'},
             {'titulo':'ttt','descricao':'uuu'}]
    __ctx['itens'] = itens
    return TemplateResponse(__ctx)