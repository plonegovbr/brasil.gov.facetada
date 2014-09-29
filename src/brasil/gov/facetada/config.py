# -*- coding: utf-8 -*-

from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implements

PROJECTNAME = 'brasil.gov.facetada'


class HiddenProfiles(object):
    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        return [
            u'brasil.gov.facetada:uninstall',
            u'brasil.gov.facetada.upgrades.v1010:default'
        ]
