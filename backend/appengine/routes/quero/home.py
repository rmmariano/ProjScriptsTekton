# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from config.template_middleware import TemplateResponse
from gaepermission.decorator import login_required

__author__ = 'Rodrigo'

#default é @login_required
@login_required
@no_csrf
def index():
    return TemplateResponse()