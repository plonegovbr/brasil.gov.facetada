# -*- coding: utf-8 -*-
from brasil.gov.facetada.config import PROJECTNAME
from brasil.gov.facetada.interfaces import IBrowserLayer
from brasil.gov.facetada.testing import FUNCTIONAL_TESTING
from brasil.gov.facetada.testing import INTEGRATION_TESTING
from plone.browserlayer.utils import registered_layers
# from Products.GenericSetup.upgrade import listUpgradeSteps

import unittest2 as unittest


class Plone43TestCase(unittest.TestCase):

    layer = FUNCTIONAL_TESTING


class BaseTestCase(unittest.TestCase):
    """Base test case to be used by other tests."""

    layer = INTEGRATION_TESTING

    profile = 'brasil.gov.facetada:default'

    def setUp(self, from_version='1000', to_version='1010'):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.wt = self.portal['portal_workflow']
        self.st = self.portal['portal_setup']
        self.from_version = from_version
        self.to_version = to_version

    def _get_upgrade_step(self, title):
        """Get one of the upgrade steps.

        Keyword arguments:
        title -- the title used to register the upgrade step
        """
        self.st.setLastVersionForProfile(self.profile, self.from_version)
        upgrades = self.st.listUpgrades(self.profile)
        steps = [s for s in upgrades[0] if s['title'] == title]
        return steps[0] if steps else None

    def _do_upgrade_step(self, step):
        """Execute an upgrade step.

        Keyword arguments:
        step -- the step we want to run
        """
        request = self.layer['request']
        request.form['profile_id'] = self.profile
        request.form['upgrades'] = [step['id']]
        self.st.manage_doUpgrades(request=request)

    def _how_many_upgrades_to_do(self):
        self.st.setLastVersionForProfile(self.profile, self.from_version)
        upgrades = self.st.listUpgrades(self.profile)
        assert len(upgrades) > 0
        return len(upgrades[0])


class TestInstall(BaseTestCase):
    """Ensure product is properly installed."""

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME),
                        '%s not installed' % PROJECTNAME)

    def test_browser_layer_installed(self):
        self.assertIn(IBrowserLayer, registered_layers())

    def test_version(self):
        self.assertEqual(
            self.st.getLastVersionForProfile(self.profile),
            (u'1000',)
        )


# class TestUpgrade(BaseTestCase):
#     """Ensure product upgrades work."""
#
#     def test_to1010_available(self):
#
#         upgradeSteps = listUpgradeSteps(self.st,
#                                         self.profile,
#                                         '1000')
#         step = [step for step in upgradeSteps
#                 if (step[0]['dest'] == ('1010',))
#                 and (step[0]['source'] == ('1000',))]
#         self.assertEqual(len(step), 1)


class TestUninstall(BaseTestCase):
    """Ensure product is properly uninstalled."""

    def setUp(self):
        BaseTestCase.setUp(self)
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browser_layer_removed_uninstalled(self):
        self.assertNotIn(IBrowserLayer, registered_layers())
