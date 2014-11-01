# -*- coding: utf-8 -*-
from Products.CMFPlone import interfaces as st_interfaces
from Products.CMFQuickInstallerTool import interfaces as qi_interfaces
from zope.interface import implements

PROJECTNAME = 'brasil.gov.facetada'


class HiddenProducts(object):
    implements(qi_interfaces.INonInstallable)

    def getNonInstallableProducts(self):
        return [
        ]


class HiddenProfiles(object):
    implements(st_interfaces.INonInstallable)

    def getNonInstallableProfiles(self):
        return [
            u'brasil.gov.facetada:uninstall',
        ]
