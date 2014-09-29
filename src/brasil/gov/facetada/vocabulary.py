# -*- coding: utf-8 -*-
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
            (u'effective',
             u'mais antigo'),
            (u'effective_reverse',
             u'mais recente'),
            (u'sortable_title',
             u'A - Z'),
            (u'sortable_title_reverse',
             u'Z - A'), ]
        items = [SimpleTerm(k, k, v) for k, v in vocab]
        return SimpleVocabulary(items)

OrdenacaoVocabularyFactory = OrdenacaoVocabulary()
