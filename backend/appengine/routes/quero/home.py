# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from config.template_middleware import TemplateResponse
from gaepermission.decorator import login_required

__author__ = 'Rodrigo'

#default é @login_required, porém só ADMIN pode acessar, com o @login_required explicito, qualquer um logado pode acessar
@login_required
@no_csrf
def index():
    return TemplateResponse()