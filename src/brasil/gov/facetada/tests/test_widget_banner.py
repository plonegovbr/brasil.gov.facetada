# -*- coding: utf-8 -*-
from brasil.gov.facetada.testing import INTEGRATION_TESTING
from eea.facetednavigation.interfaces import ICriteria
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.testing.z2 import Browser
from zope.component import getMultiAdapter

import os
import transaction
import unittest

TEST_PNG_FILE = open(
    os.path.sep.join(__file__.split(os.path.sep)[:-1] + ['plonegovbr.png', ]),
    'rb'
).read()


class WidgetBannerTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.wt = self.portal.portal_workflow

    def setupContent(self, portal):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'widgetbanner')
        self.folder = self.portal['widgetbanner']
        self.folder.setTitle('Busca Multifacetada - Widget de Banner')
        self.request = self.folder.REQUEST
        # adiciona imagem
        self.portal.invokeFactory('Image',
                                  'imagem-de-plonegovbr',
                                  title='Imagem de PloneGovBR',
                                  image=TEST_PNG_FILE)
        self.imagem = self.portal['imagem-de-plonegovbr']
        self.imagemUid = self.imagem.UID()
        subtyper = getMultiAdapter((self.folder, self.request), name=u'faceted_subtyper')
        self.assertTrue(subtyper.can_enable)
        subtyper.enable()
        self.config = getMultiAdapter((self.folder, self.request), name=u'configure_faceted.html')
        self.handler = getMultiAdapter((self.folder, self.request), name=u'faceted_configure')
        # Publicamos o conteudo
        self.wt.doActionFor(self.folder, 'publish')

    def removeCriteria(self):
        cids = ICriteria(self.folder).keys()
        for cid in cids:
            ICriteria(self.folder).delete(cid)
        self.assertEqual(ICriteria(self.folder).keys(), [])

    def testBanner(self):
        self.setupContent(self.portal)
        self.removeCriteria()
        _ = self.handler(wtype='banner', addWidget_button=True)
        criteria = self.config.get_criteria()
        criterion_id = criteria[0].getId()
        self.imagemUrl = self.imagem.absolute_url()
        form = {
            criterion_id + '_title': 'Widget Banner',
            criterion_id + '_imagem': '/plone/imagem-de-plonegovbr',
            criterion_id + '_link': 'http://www.brasil.gov.br',
            criterion_id + '_widget': 'banner',
            criterion_id + '_scales': 'preview 400:400',
            'saveChanges_button': True,
        }
        _ = self.handler(**form)
        app = self.layer['app']
        transaction.commit()
        self.browser = Browser(app)
        self.folderUrl = self.folder.absolute_url()
        criterion = _
        criterion = criteria[0]
        self.assertEqual(criterion.widget, u'banner')
        self.assertEqual(criterion.title, u'Widget Banner')
        self.assertEqual(criterion.link, u'http://www.brasil.gov.br')
        self.assertEqual(criterion.scales, u'preview 400:400')
        self.browser.open(self.folderUrl)
        # Verifica se o widget foi adicionado
        self.assertTrue('faceted-banner-widget' in self.browser.contents)
        # Testa se nao houve erro de renderizacao
        self.assertTrue('exceptions.AttributeError' not in self.browser.contents)
        # Verifica se o link da imagem existe
        self.assertTrue('href="http://www.brasil.gov.br"' in self.browser.contents)
        # Verifica a browser view de ScaleImage testando scale
        self.browser.open('/plone/imagem-de-plonegovbr/@@scaleimage?scale=mini')
        self.assertTrue('"height": 85,' in self.browser.contents)
        self.assertTrue('"mimetype": "image/png", ' in self.browser.contents)
        self.assertTrue('"path": "/plone/imagem-de-plonegovbr", ' in self.browser.contents)
        self.assertTrue('"scale": "mini", ' in self.browser.contents)
        self.assertTrue('"title": "Imagem de PloneGovBR", ' in self.browser.contents)
        # Verifica a browser view de ScaleImage testando width e height
        self.browser.open('/plone/imagem-de-plonegovbr/@@scaleimage?width=200&height=200')
        self.assertTrue('"mimetype": "image/png", ' in self.browser.contents)
        self.assertTrue('"path": "/plone/imagem-de-plonegovbr", ' in self.browser.contents)
        self.assertTrue('"title": "Imagem de PloneGovBR", ' in self.browser.contents)
        # Verifica a browser view de ScaleImage testando path
        self.browser.open('/plone/@@scaleimage?path=/plone/imagem-de-plonegovbr&scale=thumb')
        self.assertTrue('"mimetype": "image/png", ' in self.browser.contents)
        self.assertTrue('"path": "/plone/imagem-de-plonegovbr", ' in self.browser.contents)
        self.assertTrue('"title": "Imagem de PloneGovBR", ' in self.browser.contents)
        # Verifica a browser view de ScaleImage testando uid
        self.browser.open('/plone/@@scaleimage?scale=thumb&uid=' + self.imagemUid)
        self.assertTrue('"mimetype": "image/png", ' in self.browser.contents)
        self.assertTrue('"path": "/plone/imagem-de-plonegovbr", ' in self.browser.contents)
        self.assertTrue('"title": "Imagem de PloneGovBR", ' in self.browser.contents)
        # Testa vocabulario de scales
        self.removeCriteria()
        _ = self.handler(wtype='checkbox', addWidget_button=True)
        criteria = self.config.get_criteria()
        criterion_id = criteria[0].getId()
        form = {
            criterion_id + '_title': 'Escalas de Imagem',
            criterion_id + '_widget': 'checkbox',
            criterion_id + '_index': 'object_provides',
            criterion_id + '_vocabulary': 'brasil.gov.imagescales',
            'saveChanges_button': True,
        }
        _ = self.handler(**form)
        app = self.layer['app']
        transaction.commit()
        self.browser = Browser(app)
        self.folderUrl = self.folder.absolute_url()
        criterion = _
        criterion = criteria[0]
        self.assertEqual(criterion.title, u'Escalas de Imagem')
        self.assertEqual(criterion.vocabulary, u'brasil.gov.imagescales')
        self.browser.open(self.folderUrl)
        self.assertTrue('listing' in self.browser.contents)
        self.assertTrue('mini' in self.browser.contents)
        self.assertTrue('large' in self.browser.contents)
        self.assertTrue('preview' in self.browser.contents)
        self.assertTrue('tile' in self.browser.contents)
        self.assertTrue('thumb' in self.browser.contents)
        self.assertTrue('icon' in self.browser.contents)
