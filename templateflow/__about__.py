# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""\
Group inference and reporting of neuroimaging studies require that individual's \
features are spatially aligned into a common frame where their location can be \
called standard. \
To that end, a multiplicity of brain templates with anatomical annotations \
(i.e., atlases) have been published. \
However, a centralized resource that allows programmatic access to templates is \
lacking. \
TemplateFlow is a modular, version-controlled resource that allows researchers \
to use templates "off-the-shelf" and share new ones. \
"""
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

__packagename__ = 'templateflow'
__author__ = 'The CRN developers'
__copyright__ = 'Copyright 2019, Center for Reproducible Neuroscience, Stanford University'
__credits__ = ['Oscar Esteban']
__license__ = '3-clause BSD'
__maintainer__ = 'Oscar Esteban'
__email__ = 'code@oscaresteban.es'
__status__ = 'Prototype'

__description__ = """\
TemplateFlow's Python Client - TemplateFlow is the Zone of neuroimaging templates.
"""
__longdesc__ = __doc__
__url__ = 'https://github.com/poldracklab/{}'.format(__packagename__)

DOWNLOAD_URL = (
    'https://pypi.python.org/packages/source/{name[0]}/{name}/{name}-{ver}.tar.gz'.format(
        name=__packagename__, ver=__version__))
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Image Recognition',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
]

REQUIRES = [
    'datalad',
]

SETUP_REQUIRES = []
REQUIRES += SETUP_REQUIRES

LINKS_REQUIRES = []
TESTS_REQUIRES = [
    'pytest',
    'pytest-xdist',
]

EXTRA_REQUIRES = {
    'doc': [],
    'tests': TESTS_REQUIRES,
}

# Enable a handle to install all extra dependencies at once
EXTRA_REQUIRES['all'] = list(EXTRA_REQUIRES.values())
