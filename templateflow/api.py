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
"""TemplateFlow's Python Client.

``templateflow.api`` provides a global, high-level interface to query the TemplateFlow archive.

There are two methods to initialize a client:

    >>> from templateflow import api as client

    >>> from templateflow import TemplateFlowClient
    >>> client = TemplateFlowClient()

The latter method allows additional configuration for the client,
while ``templateflow.api`` is only configurable through environment variables.

.. autofunction:: get

.. autofunction:: ls

.. autofunction:: templates

.. autofunction:: get_metadata

.. autofunction:: get_citations
"""

from .client import TemplateFlowClient
from .conf import _cache

_client = TemplateFlowClient(cache=_cache)


def __getattr__(name: str):
    if name == 'TF_LAYOUT':
        return _cache.layout
    try:
        return getattr(_client, name)
    except AttributeError:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
