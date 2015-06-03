# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from mock import Mock
from routes.meuperfil.caixaesquerda.itens.itensmeusitens import salvar as salvar_item
from routes.meuperfil.caixaesquerda.cadastrarcategorias.cadastrarcategorias import salvar as salvar_categoria
from model.db import *
from tekton.gae.middleware.json_middleware import JsonUnsecureResponse

class ItensMeusItensTests(GAETestCase):
    def test_sucesso(self):
        nova_categoria = {'categoria':'NovaCategoria'}
        resposta_categoria = salvar_categoria(**nova_categoria)
        categorias = Categoria.query().fetch()
        self.assertEqual(1, len(categorias))
        cat = categorias[0]
        self.assertEqual('NovaCategoria', cat.categoria)

        novo_item = {'titulo':'Teste123', 'id_categoria':str(cat.key.id()), 'descricao':'Teste123'}
        resposta = salvar_item(None,**novo_item)
        novo_item['categoria'] = 'NovaCategoria'
        self.assertIsInstance(resposta, JsonUnsecureResponse)
        del resposta.context['id']
        self.assertEqual(novo_item, resposta.context)

    def test_erro(self):
        respota_mock = Mock()
        resposta = salvar_item(respota_mock)
        respota_mock.set_status.assert_called_once_with(400)
        self.assert_can_serialize_as_json(resposta)

    def test_validacao(self):
        resp_mock = Mock()
        novo_item = {'titulo':'Teste123', 'id_categoria':'', 'descricao':'Teste123'}
        resposta = salvar_item(resp_mock,**novo_item)
        self.assertIsInstance(resposta, JsonUnsecureResponse)
        self.assertIsNone(Categoria.query().get())
        self.maxDiff = True
        self.assertDictEqual({u'errors': {'id_categoria': u'Required field'}},resposta.context)
