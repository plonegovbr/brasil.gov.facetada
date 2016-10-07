# -*- coding: utf-8 -*-

""" Ordenar widget
"""

from Products.ATContentTypes.criteria import _criterionRegistry
from Products.Archetypes.public import Schema
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.CMFCore.utils import getToolByName
from eea.facetednavigation import EEAMessageFactory as _
from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget


EditSchema = Schema((
    StringField('vocabulary',
                schemata='default',
                vocabulary_factory='eea.faceted.vocabularies.PortalVocabularies',
                widget=SelectionWidget(
                    label=_(u'Filter from vocabulary'),
                    description=_(u'Vocabulary to use to filter sorting criteria. '
                                  u'Leave empty for default sorting criteria.'),
                    i18n_domain='eea'
                )
                ),
    StringField('default',
                schemata='default',
                widget=StringWidget(
                    size=25,
                    label=_(u'Default value'),
                    description=_(u'Default sorting index '
                                  u"(e.g. 'effective' or 'effective(reverse)')"),
                    i18n_domain='eea'
                )
                ),
))


class Widget(AbstractWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'ordenar'
    widget_label = _('Ordenar')
    view_js = '++resource++brasil.gov.facetada.faceted.widgets.ordenar.view.js'
    edit_js = '++resource++brasil.gov.facetada.faceted.widgets.ordenar.edit.js'
    view_css = '+++resource++brasil.gov.facetada.faceted.widgets.ordenar.view.css'
    css_class = 'faceted-ordenar-widget'

    index = ViewPageTemplateFile('widget.pt')
    edit_schema = AbstractWidget.edit_schema.copy() + EditSchema
    edit_schema['title'].default = 'Ordenar por'

    @property
    def default(self):
        """ Return default sorting values
        """
        default = self.data.get('default', '')
        if not default:
            return ()
        reverse = False
        if '(reverse)' in default:
            default = default.replace('(reverse)', '', 1)
            reverse = True
        default = default.strip()
        return (default, reverse)

    def query(self, form):
        """ Get value from form and return a catalog dict query
        """
        query = {}

        sort_on = form.get(self.data.getId(), '')
        reverse = form.get('reversed', False)
        if sort_on:
            query['sort_on'] = sort_on
        if reverse:
            query['sort_order'] = 'descending'
        else:
            query['sort_order'] = 'ascending'
        return query

    def criteriaByIndexId(self, indexId):
        """ Get criteria by index id
        """
        catalog_tool = getToolByName(self.context, 'portal_catalog')
        indexObj = catalog_tool.Indexes[indexId]
        # allow DateRecurringIndex that is unknown to atct.
        # events in plone.app.contenttypes use it for start and end
        if indexObj.meta_type == 'DateRecurringIndex':
            return ('ATFriendlyDateCriteria',
                    'ATDateRangeCriterion',
                    'ATSortCriterion')
        results = _criterionRegistry.criteriaByIndex(indexObj.meta_type)
        return results

    def validateAddCriterion(self, indexId, criteriaType):
        """Is criteriaType acceptable criteria for indexId
        """
        return criteriaType in self.criteriaByIndexId(indexId)

    def listFields(self):
        """Return a list of fields from portal_catalog.
        """
        tool = getToolByName(self.context, 'portal_atct')
        return tool.getEnabledFields()

    def listSortFields(self):
        """Return a list of available fields for sorting."""
        fields = [field for field in self.listFields()
                  if self.validateAddCriterion(field[0], 'ATSortCriterion')]
        return fields
