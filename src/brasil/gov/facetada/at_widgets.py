# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.public import StringWidget


class ImageSelectionUploadWidget(StringWidget):
    security = ClassSecurityInfo()

    _properties = StringWidget._properties.copy()
    _properties.update({
        'macro': 'ImageSelectionUpload',
    })


registerWidget(ImageSelectionUploadWidget,
               title='ImageSelectionUpload',
               description='Widget para seleção e upload de imagem.',
               used_for=('Products.Archetypes.public.StringField', )
               )
