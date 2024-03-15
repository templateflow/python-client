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
"""Check S3-type repo tooling."""
# import pytest
from pathlib import Path

import requests

from .. import _s3 as s3


def test_get_skel_file(monkeypatch):
    """Exercise the skeleton file generation."""
    local_md5 = s3.TF_SKEL_MD5
    monkeypatch.setattr(s3, 'TF_SKEL_MD5', 'invent')
    new_skel = s3._get_skeleton_file()
    assert new_skel is not None
    assert Path(new_skel).exists()
    assert Path(new_skel).stat().st_size > 0

    latest_md5 = (
        requests.get(s3.TF_SKEL_URL(release='master', ext='md5', allow_redirects=True))
        .content.decode()
        .split()[0]
    )
    monkeypatch.setattr(s3, 'TF_SKEL_MD5', latest_md5)
    assert s3._get_skeleton_file() is None

    monkeypatch.setattr(s3, 'TF_SKEL_MD5', local_md5)
    monkeypatch.setattr(s3, 'TF_SKEL_URL', 'http://weird/{release}/{ext}'.format)
    assert s3._get_skeleton_file() is None

    monkeypatch.setattr(
        s3, 'TF_SKEL_URL', s3.TF_SKEL_URL(release='{release}', ext='{ext}z').format
    )
    assert s3._get_skeleton_file() is None


def test_update_s3(tmp_path, monkeypatch):
    """Exercise updating the S3 skeleton."""
    newhome = tmp_path / 'templateflow'
    assert s3.update(newhome)
    assert not s3.update(newhome, overwrite=False)
    for p in (newhome / 'tpl-MNI152NLin6Sym').glob('*.nii.gz'):
        p.unlink()
    assert s3.update(newhome, overwrite=False)

    # This should cover the remote zip file fetching
    monkeypatch.setattr(s3, 'TF_SKEL_MD5', 'invent')
    assert s3.update(newhome, local=False)
    assert not s3.update(newhome, local=False, overwrite=False)
    for p in (newhome / 'tpl-MNI152NLin6Sym').glob('*.nii.gz'):
        p.unlink()
    assert s3.update(newhome, local=False, overwrite=False)
