# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
#
# Copyright 2024 The NiPreps Developers <nipreps@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# We support and encourage derived works from this project, please read
# about our expectations at
#
#     https://www.nipreps.org/community/licensing/
#
"""TemplateFlow is the Zone of Templates."""
from datetime import datetime as _dt
from datetime import timezone as _tz

__packagename__ = 'templateflow'
__copyright__ = f'{_dt.now(tz=_tz.utc).year} The NiPreps Developers'
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

from . import api
from .conf import update

__all__ = [
    '__copyright__',
    '__packagename__',
    '__version__',
    'api',
    'update',
]
