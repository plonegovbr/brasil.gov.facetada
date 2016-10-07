# -*- coding: utf-8 -*-
""" Banner widget
"""
from Products.Archetypes.public import Schema
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.CMFCore.utils import getToolByName
from brasil.gov.facetada.at_widgets import ImageSelectionUploadWidget
from eea.facetednavigation import EEAMessageFactory as _
from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
import logging


logger = logging.getLogger('brasil.gov.facetada.faceted.widgets.banner')

EditSchema = Schema((
    StringField('imagem',
                schemata='default',
                required=True,
                widget=ImageSelectionUploadWidget(
                    label=_(u'Imagem'),
                    description=_(u'Selecao ou upload de imagem'),
                    i18n_domain='brasil.gov.facetada'
                )
                ),

    StringField('link',
                schemata='default',
                widget=StringWidget(
                    label=_(u'Link'),
                    description=_(u'Informe o link para o banner'),
                    i18n_domain='brasil.gov.facetada'
                )
                ),

    StringField('scales',
                schemata='default',
                required=True,
                vocabulary_factory='brasil.gov.imagescales',
                widget=SelectionWidget(
                    label=_(u'Tamanho da imagem'),
                    description=_(u'Selecao do tamanho da imagem'),
                    i18n_domain='brasil.gov.facetada'
                )
                ),
))


class Widget(AbstractWidget):
    """ Banner widget

    The following contexts can be used within tal expressions:

    context   -- faceted navigable context
    referer   -- request.HTTP_REFERER object. Use this if you load
                 faceted from another place (like: portal_relations)
    request   -- faceted navigable REQUEST object
    widget    -- Banner Widget instance
    criterion -- Banner Criterion instance

    """
    widget_type = 'banner'
    widget_label = _('Banner')
    view_js = '++resource++brasil.gov.facetada.faceted.widgets.banner.view.js'

    index = ViewPageTemplateFile('widget.pt')
    edit_schema = AbstractWidget.edit_schema.copy() + EditSchema
    edit_schema['title'].default = 'Banner'

    def scale(self):
        """Retorna imagem no tamanho selecionado
        """
        if self.data.imagem and self.data.scales:
            catalog = getToolByName(self.context, 'portal_catalog')
            image = None
            brain = catalog(path={'query': self.data.imagem, 'depth': 0})
            if brain:
                image = brain[0].getObject()
            scales = image.restrictedTraverse('@@images')
            # scales come like u'preview 400:400'
            # so I take the scale information from it
            thumb = scales.scale('image', self.data.scales.split(' ')[0])
            return {
                'src': thumb.url,
                'alt': image.Description(),
                'width': thumb.width,
                'height': thumb.height,
            }
