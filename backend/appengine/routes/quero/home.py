# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from config.template_middleware import TemplateResponse

__author__ = 'Rodrigo'

#default é @login_required
@no_csrf
def index():
    return TemplateResponse()