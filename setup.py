# -*- coding:utf-8 -*-
from setuptools import find_packages
from setuptools import setup


version = '1.0rc1'
description = u'Suporte à busca multifacetada para Portal Padrão'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(
    name='brasil.gov.facetada',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='plonegovbr busca facetada multifacetada',
    author='PloneGovBr',
    author_email='gov@plone.org.br',
    url='https://github.com/plonegovbr/brasil.gov.facetada',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['brasil', 'brasil.gov'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # ate o momento desta correção a última versão do produto
        # eea.facetednavigation era a versão 10rc1 e não era estável
        # gerando o seguinte erro ao carregar o widget:
        # AttributeError: type object 'Widget' has no attribute 'edit_schema'
        'eea.facetednavigation < 10',
        'five.pt',
        'plone.api',
        'plone.app.contenttypes',
        'plone.app.upgrade',
        'Products.CMFPlone >=4.3',
        'Products.GenericSetup',
        'setuptools',
        'zope.i18nmessageid',
        'zope.interface',
    ],
    extras_require={
        'test': [
            'plone.app.robotframework',
            'plone.app.testing [robot] >=4.2.2',
            'plone.browserlayer',
            'plone.testing',
            'robotsuite',
        ],
    },
    entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
