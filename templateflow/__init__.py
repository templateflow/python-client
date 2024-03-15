# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""TemplateFlow is the Zone of Templates."""
__packagename__ = 'templateflow'
__copyright__ = '2020, The TemplateFlow developers'
try:
    from ._version import __version__
except ModuleNotFoundError:
    from importlib.metadata import PackageNotFoundError, version
    try:
        __version__ = version(__packagename__)
    except PackageNotFoundError:
        __version__ = '0+unknown'
    del version
    del PackageNotFoundError

import os

from . import api
from .conf import TF_USE_DATALAD, update

if not TF_USE_DATALAD and os.getenv('TEMPLATEFLOW_AUTOUPDATE', '1') not in (
    'false',
    'off',
    '0',
    'no',
    'n',
):
    # trigger skeleton autoupdate
    update(local=True, overwrite=False, silent=True)

__all__ = [
    '__copyright__',
    '__packagename__',
    '__version__',
    'api',
    'update',
]
