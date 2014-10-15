# -*- coding: utf-8 -*-
from brasil.gov.facetada.testing import INTEGRATION_TESTING
from eea.facetednavigation.interfaces import ICriteria
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.testing.z2 import Browser
from zope.component import getMultiAdapter

import transaction
import unittest


class WidgetOrdenarTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.wt = self.portal.portal_workflow

    def setupContent(self, portal):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'facetada')
        self.folder = self.portal['facetada']
        self.folder.setTitle('Busca Multifacetada')
        self.request = self.folder.REQUEST
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

    def testOrdenar(self):
        self.setupContent(self.portal)
        self.removeCriteria()
        _ = self.handler(wtype='ordenar', addWidget_button=True)
        criteria = self.config.get_criteria()
        criterion_id = criteria[0].getId()
        form = {
            criterion_id + '_title': 'Ordenar por',
            criterion_id + '_widget': 'ordenar',
            criterion_id + '_vocabulary': 'brasil.gov.ordenacao',
            'saveChanges_button': True,
        }
        _ = self.handler(**form)
        app = self.layer['app']
        transaction.commit()
        self.browser = Browser(app)
        self.folderUrl = self.folder.absolute_url()
        criterion = _
        criterion = criteria[0]
        self.assertEqual(criterion.widget, u'ordenar')
        self.assertEqual(criterion.title, u'Ordenar por')
        self.assertEqual(criterion.vocabulary, u'brasil.gov.ordenacao')
        self.browser.open(self.folderUrl)
        self.assertTrue('Ordenar por' in self.browser.contents)
        self.assertTrue('mais antigo' in self.browser.contents)
