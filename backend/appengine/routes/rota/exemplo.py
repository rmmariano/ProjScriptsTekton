# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required

__author__ = 'Rodrigo'

@login_not_required
@no_csrf
def index():
    return TemplateResponse(template_path='/exemplo.html')

'''
@login_not_required
@no_csrf
def index(_handler):
    #_handler.redirect('/rota/exemplo/funcao')

    path = router.topath(funcao) #gera o caminho para chegar a função 'funcao' , não precisando
                            #escrever manualmente que nem acima
    _handler.redirect(path)

@login_not_required
@no_csrf
def funcaoo(_resp, _req, nome):
    nome = _req.get('nome')
    _resp.write('Nome: '+nome)
    _resp.write('\nNome: %s'%(nome))

#ou

@login_not_required
@no_csrf
def funcao(_resp, nome): #já entende o 'nome' como um parâmetro recebido pela url
    _resp.write('Nome: '+nome)
    _resp.write('\nNome: %s'%(nome))
'''

@login_not_required
@no_csrf
def funcao(_resp, nome = "Amaimon", sobrenome = "Santos"): #sobrenome = "Santos", coloca um valor default
                            #caso não insira nada para a variavel
    _resp.write(nome+' '+sobrenome)
    _resp.write(' - %s %s'%(nome,sobrenome))