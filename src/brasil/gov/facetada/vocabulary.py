# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from eea.faceted.vocabularies.utils import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class OrdenacaoVocabulary(object):
    """Vocabulary factory for ordering.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        vocab = [
            (u'effective', u'mais antigo'),
            (u'effective_reverse', u'mais recente'),
            (u'sortable_title', u'A - Z'),
            (u'sortable_title_reverse', u'Z - A'), ]
        items = [SimpleTerm(k, k, v) for k, v in vocab]
        return SimpleVocabulary(items)


OrdenacaoVocabularyFactory = OrdenacaoVocabulary()


class TiposVocabulary(object):
    """Vocabulary factory for types.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        vocab = [
            (u'File', u'Arquivo'),
            (u'Audio', u'Áudio'),
            (u'Image', u'Imagem'),
            (u'sc.embedder', u'Multimídia'),
            (u'collective.nitf.content', u'Notícia'),
            (u'Document', u'Página'), ]
        items = [SimpleTerm(k, k, v) for k, v in vocab]
        return SimpleVocabulary(items)


TiposVocabularyFactory = TiposVocabulary()


class ImageScaleVocabulary(object):
    """ Create a vocabulary of image scales available in the site """
    implements(IVocabularyFactory)

    def __call__(self, context):
        properties_tool = getToolByName(self, 'portal_properties')
        imagescales_properties = getattr(properties_tool, 'imaging_properties', None)
        raw_scales = getattr(imagescales_properties, 'allowed_sizes', None)

        image_scales = {}
        for line in raw_scales:
            line = line.strip()
            if line:
                splits = line.split(' ')
                if len(splits) == 2:
                    name = line
                    image_scales[name] = (splits[0], )
        return SimpleVocabulary.fromValues(image_scales)


ImageScaleVocabularyFactory = ImageScaleVocabulary()
