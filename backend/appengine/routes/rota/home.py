# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required

__author__ = 'Rodrigo'

'''
@login_not_required
@no_csrf
def index(_resp):
    _resp.write('rota')

@login_not_required
@no_csrf
def index():
    return TemplateResponse() #se não colocar nada, ele caçará o home.html
                        #pq aqui é o "rota.py"
    #return TemplateResponse(template_path='/home.html')
'''

@login_not_required
@no_csrf
def index(nome = "rod", sobrenome = "amaimon"):
    contexto = {'nome': nome, 'sobrenome': sobrenome}
    return TemplateResponse(contexto)