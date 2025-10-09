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

from importlib import reload
from pathlib import Path

import pytest
import requests

import templateflow
import templateflow.conf._s3
from templateflow import api as tf
from templateflow import conf as tfc

from .data import load_data


def test_get_skel_file(tmp_path, monkeypatch):
    """Exercise the skeleton file generation."""

    home = (tmp_path / 's3-skel-file').resolve()

    md5content = b'anything'

    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 200
            ok = True
            content = md5content

        return MockResponse()

    monkeypatch.setattr(requests, 'get', mock_get)

    # Mismatching the local MD5 causes an update
    new_skel = tfc._s3._get_skeleton_file(timeout=10)
    assert new_skel is not None
    assert Path(new_skel).exists()
    assert Path(new_skel).read_bytes() == b'anything'

    md5content = tfc._s3.load_data.readable('templateflow-skel.md5').read_bytes()
    # Matching the local MD5 skips the update
    assert tfc._s3._get_skeleton_file(timeout=10) is None

    # Bad URL fails to update
    monkeypatch.setattr(tfc._s3, 'TF_SKEL_URL', 'http://weird/{release}/{ext}'.format)
    assert tfc._s3._get_skeleton_file(timeout=10) is None

    monkeypatch.setattr(
        tfc._s3, 'TF_SKEL_URL', tfc._s3.TF_SKEL_URL(release='{release}', ext='{ext}z').format
    )
    assert tfc._s3._get_skeleton_file(timeout=10) is None


def test_update_s3(tmp_path, monkeypatch):
    """Exercise updating the S3 skeleton."""

    newhome = (tmp_path / 's3-update').resolve()

    assert tfc._s3.update(newhome, timeout=10)
    assert not tfc._s3.update(newhome, overwrite=False, timeout=10)
    for p in (newhome / 'tpl-MNI152NLin6Sym').glob('*.nii.gz'):
        p.unlink()
    assert tfc._s3.update(newhome, overwrite=False, timeout=10)

    # This should cover the remote zip file fetching
    # monkeypatch.setattr(tfc._s3, 'TF_SKEL_MD5', 'invent')
    assert tfc._s3.update(newhome, local=False, timeout=10)
    assert not tfc._s3.update(newhome, local=False, overwrite=False, timeout=10)
    for p in (newhome / 'tpl-MNI152NLin6Sym').glob('*.nii.gz'):
        p.unlink()
    assert tfc._s3.update(newhome, local=False, overwrite=False, timeout=10)


def mock_get(*args, **kwargs):
    class MockResponse:
        status_code = 400

    return MockResponse()


def test_s3_400_error(monkeypatch):
    """Simulate a 400 error when fetching the skeleton file."""

    reload(tfc)
    reload(tf)

    monkeypatch.setattr(requests, 'get', mock_get)
    with pytest.raises(RuntimeError, match=r'Failed to download .* code 400'):
        templateflow.client._s3_get(
            tfc._cache.config,
            Path(tfc.TF_LAYOUT.root)
            / 'tpl-MNI152NLin2009cAsym/tpl-MNI152NLin2009cAsym_res-02_T1w.nii.gz',
        )


def test_bad_skeleton(tmp_path, monkeypatch):
    newhome = (tmp_path / 's3-update').resolve()
    client = templateflow.client.TemplateFlowClient(root=newhome, use_datalad=False)

    assert client.cache.layout.root == str(newhome)

    paths = client.ls('MNI152NLin2009cAsym', resolution='02', suffix='T1w', desc=None)
    assert paths
    path = Path(paths[0])
    assert path.read_bytes() == b''

    error_file = load_data.readable('error_response.xml')
    path.write_bytes(error_file.read_bytes())

    # Test directly before testing through API paths
    templateflow.client._truncate_s3_errors(paths)
    assert path.read_bytes() == b''

    path.write_bytes(error_file.read_bytes())

    monkeypatch.setattr(requests, 'get', mock_get)
    with pytest.raises(RuntimeError):
        client.get('MNI152NLin2009cAsym', resolution='02', suffix='T1w', desc=None)

    # Running get clears bad files before attempting to download
    assert path.read_bytes() == b''
