# -*- coding: utf-8 -*-
from brasil.gov.facetada.testing import INTEGRATION_TESTING
from eea.facetednavigation.interfaces import ICriteria
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.testing.z2 import Browser
from zope.component import getMultiAdapter

import transaction
import unittest


class AplicaFacetadaTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.wt = self.portal.portal_workflow

    def setupContent(self, portal):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']
        self.folder.setTitle('Busca Multifacetada')
        self.request = self.folder.REQUEST
        subtyper = getMultiAdapter((self.folder, self.request), name=u'faceted_subtyper')
        self.assertTrue(subtyper.can_enable)
        subtyper.enable()
        self.config = getMultiAdapter((self.folder, self.request), name=u'configure_faceted.html')
        self.handler = getMultiAdapter((self.folder, self.request), name=u'faceted_configure')
        # Publicamos o conteudo
        self.wt.doActionFor(self.folder, 'publish')

    def testCriteria(self):
        self.setupContent(self.portal)
        cids = ICriteria(self.folder).keys()
        self.assertTrue(u'c1' in cids)

    def testWidget(self):
        self.setupContent(self.portal)
        _ = self.handler(wtype='checkbox', addWidget_button=True)
        criteria = self.config.get_criteria()
        criterion_id = criteria[2].getId()
        form = {
            criterion_id + '_title': 'Tipo de itens',
            criterion_id + '_widget': 'checkbox',
            criterion_id + '_vocabulary': 'brasil.gov.tipos',
            criterion_id + '_index': 'portal_type',
            'saveChanges_button': True,
        }
        _ = self.handler(**form)

        app = self.layer['app']
        transaction.commit()
        self.browser = Browser(app)
        self.folderUrl = self.folder.absolute_url()
        criterion = _
        criterion = criteria[2]
        self.assertEqual(criterion.widget, u'checkbox')
        self.assertEqual(criterion.title, u'Tipo de itens')
        self.assertEqual(criterion.index, u'portal_type')
        self.assertEqual(criterion.vocabulary, u'brasil.gov.tipos')
        self.browser.open(self.folderUrl)
        self.assertTrue('faceted-results' in self.browser.contents)
        self.assertTrue('Imagem' in self.browser.contents)
