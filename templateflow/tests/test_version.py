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
"""Test version retrieval."""
import sys
from importlib import reload
from importlib.metadata import PackageNotFoundError

import templateflow


def test_version_scm0(monkeypatch):
    """Retrieve the version."""

    class _version:
        __version__ = '10.0.0'

    monkeypatch.setitem(sys.modules, 'templateflow._version', _version)
    reload(templateflow)
    assert templateflow.__version__ == '10.0.0'


def test_version_scm1(monkeypatch):
    """Retrieve the version via importlib.metadata."""
    monkeypatch.setitem(sys.modules, 'templateflow._version', None)

    def _ver(name):
        return 'success'

    monkeypatch.setattr('importlib.metadata.version', _ver)
    reload(templateflow)
    assert templateflow.__version__ == 'success'


def test_version_scm2(monkeypatch):
    """Check version could not be interpolated."""
    monkeypatch.setitem(sys.modules, 'templateflow._version', None)

    def _raise(name):
        raise PackageNotFoundError('No get_distribution mock')

    monkeypatch.setattr('importlib.metadata.version', _raise)
    reload(templateflow)
    assert templateflow.__version__ == '0+unknown'
