***************************************************************
`.gov.br: Suporte a Busca Multifacetada`
***************************************************************

.. contents:: Conteúdo
   :depth: 2

Introdução
-----------

Este pacote provê a instalação de produto para busca multifacetada, customização de visão sumária e widget de ordenação para o `Portal Padrão <http://portalpadrao.plone.org.br>`_.

Estado deste pacote
---------------------

O **brasil.gov.facetada** tem testes automatizados e, a cada alteração em seu
código os testes são executados pelo serviço Travis.

O estado atual dos testes pode ser visto nas imagens a seguir:

.. image:: https://secure.travis-ci.org/plonegovbr/brasil.gov.facetada.png?branch=master
    :target: http://travis-ci.org/plonegovbr/brasil.gov.facetada

.. image:: https://coveralls.io/repos/plonegovbr/brasil.gov.facetada/badge.png?branch=master
    :target: https://coveralls.io/r/plonegovbr/brasil.gov.facetada

Instalação
------------

Para habilitar a instalação deste produto em um ambiente que utilize o
buildout:

1. Editar o arquivo buildout.cfg (ou outro arquivo de configuração) e
   adicionar o pacote ``brasil.gov.facetada`` à lista de eggs da instalação::

        [buildout]
        ...
        eggs =
            brasil.gov.facetada

2. Após alterar o arquivo de configuração é necessário executar
   ''bin/buildout'', que atualizará sua instalação.

3. Reinicie o Plone

4. Acesse o painel de controle e instale o produto
**.gov.br: Busca Multifacetada**.
