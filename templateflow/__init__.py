# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
The Zone of Templates
=====================
"""
from .__about__ import (
    __version__, __packagename__, __author__, __copyright__,
    __credits__, __license__, __maintainer__, __email__, __status__,
    __description__, __longdesc__)

__all__ = [
    '__version__',
    '__packagename__',
    '__author__',
    '__copyright__',
    '__credits__',
    '__license__',
    '__maintainer__',
    '__email__',
    '__status__',
    '__description__',
    '__longdesc__',
]

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
