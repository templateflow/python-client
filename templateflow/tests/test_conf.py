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
"""Tests the config module."""
from pathlib import Path

import pytest

from .. import api, conf


@pytest.mark.skipif(conf.TF_USE_DATALAD, reason='S3 only')
def test_update_s3(tmp_path):
    conf.TF_HOME = tmp_path / 'templateflow'
    conf.TF_HOME.mkdir(exist_ok=True)

    # replace TF_SKEL_URL with the path of a legacy skeleton
    _skel_url = conf._s3.TF_SKEL_URL
    conf._s3.TF_SKEL_URL = (
        'https://github.com/templateflow/python-client/raw/0.5.0/'
        'templateflow/conf/templateflow-skel.{ext}'.format
    )
    # initialize templateflow home, making sure to pull the legacy skeleton
    conf.update(local=False)
    # ensure we can grab a file
    assert Path(api.get('MNI152NLin2009cAsym', resolution=2, desc='brain', suffix='mask')).exists()
    # and ensure we can't fetch one that doesn't yet exist
    assert not api.get('Fischer344', hemi='L', desc='brain', suffix='mask')

    # refresh the skeleton using the most recent skeleton
    conf._s3.TF_SKEL_URL = _skel_url
    conf.update(local=True, overwrite=True)
    assert Path(api.get('Fischer344', hemi='L', desc='brain', suffix='mask')).exists()
