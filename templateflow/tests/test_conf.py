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

from importlib import reload
from importlib.util import find_spec
from shutil import rmtree

import pytest

from templateflow import conf as tfc

have_datalad = find_spec('datalad') is not None


def _find_message(lines, msg, reverse=True):
    if isinstance(lines, str):
        lines = lines.splitlines()

    for line in reversed(lines):
        if line.strip().startswith(msg):
            return True
    return False


@pytest.mark.parametrize('use_datalad', ['off', 'on'])
def test_conf_init(monkeypatch, tmp_path, use_datalad):
    """Check the correct functioning of config set-up."""
    home = (tmp_path / f'conf-init-{use_datalad}').resolve()
    monkeypatch.setenv('TEMPLATEFLOW_USE_DATALAD', use_datalad)
    monkeypatch.setenv('TEMPLATEFLOW_HOME', str(home))

    # First execution, the S3 stub is created (or datalad install)
    reload(tfc)
    assert tfc.TF_CACHED is False
    assert str(tfc.TF_HOME) == str(home)

    reload(tfc)
    assert tfc.TF_CACHED is True
    assert str(tfc.TF_HOME) == str(home)


@pytest.mark.parametrize('use_datalad', ['on', 'off'])
def test_setup_home(monkeypatch, tmp_path, capsys, use_datalad):
    """Check the correct functioning of the installation hook."""

    home = (tmp_path / f'setup-home-{use_datalad}').absolute()
    monkeypatch.setenv('TEMPLATEFLOW_USE_DATALAD', use_datalad)
    monkeypatch.setenv('TEMPLATEFLOW_HOME', str(home))

    use_post = tfc.env._env_to_bool('TEMPLATEFLOW_USE_DATALAD', False)
    assert use_post is (use_datalad == 'on')

    with capsys.disabled():
        reload(tfc)

    # Ensure mocks are up-to-date
    assert tfc.TF_USE_DATALAD is (use_datalad == 'on' and have_datalad)
    assert str(tfc.TF_HOME) == str(home)
    # First execution, the S3 stub is created (or datalad install)
    assert tfc.TF_CACHED is False
    assert tfc.setup_home() is False

    out = capsys.readouterr().out
    assert _find_message(out, 'TemplateFlow was not cached')
    assert (f'TEMPLATEFLOW_HOME={home}') in out
    assert home.exists()
    assert len(list(home.iterdir())) > 0

    updated = tfc.setup_home(force=True)  # Templateflow is now cached
    out = capsys.readouterr()[0]
    assert _find_message(out, 'TemplateFlow was not cached') is False

    if use_datalad == 'on' and have_datalad:
        assert _find_message(out, 'Updating TEMPLATEFLOW_HOME using DataLad')
        assert updated is True

    else:
        # At this point, S3 should be up-to-date
        assert updated is False
        assert _find_message(out, 'TEMPLATEFLOW_HOME directory (S3 type) was up-to-date.')

        # Let's force an update
        rmtree(str(home / 'tpl-MNI152NLin2009cAsym'))
        updated = tfc.setup_home(force=True)
        out = capsys.readouterr()[0]
        assert updated is True
        assert _find_message(out, 'Updating TEMPLATEFLOW_HOME using S3.')

    reload(tfc)
    assert tfc.TF_CACHED is True
    updated = tfc.setup_home()  # Templateflow is now cached
    out = capsys.readouterr()[0]
    assert not _find_message(out, 'TemplateFlow was not cached')

    if use_datalad == 'on' and have_datalad:
        assert _find_message(out, 'Updating TEMPLATEFLOW_HOME using DataLad')
        assert updated is True

    else:
        # At this point, S3 should be up-to-date
        assert updated is False
        assert _find_message(out, 'TEMPLATEFLOW_HOME directory (S3 type) was up-to-date.')

        # Let's force an update
        rmtree(str(home / 'tpl-MNI152NLin2009cAsym'))
        updated = tfc.setup_home()
        out = capsys.readouterr()[0]
        assert updated is True
        assert _find_message(out, 'Updating TEMPLATEFLOW_HOME using S3.')


def test_layout(monkeypatch, tmp_path):
    monkeypatch.setenv('TEMPLATEFLOW_USE_DATALAD', 'off')

    lines = (f'{tfc.TF_LAYOUT}').splitlines()
    assert lines[0] == 'TemplateFlow Layout'
    assert lines[1] == f' - Home: {tfc.TF_HOME}'
    assert lines[2].startswith(' - Templates:')


def test_layout_errors(monkeypatch):
    """Check regression of #71."""
    import builtins
    import sys
    from importlib import __import__ as oldimport

    @tfc.requires_layout
    def myfunc():
        return 'okay'

    def mock_import(name, globals=None, locals=None, fromlist=(), level=0):  # noqa: A002
        if name == 'bids':
            raise ModuleNotFoundError
        return oldimport(name, globals=globals, locals=locals, fromlist=fromlist, level=level)

    with monkeypatch.context() as m:
        m.setattr(tfc._cache, 'layout', None)
        with pytest.raises(RuntimeError):
            myfunc()

        m.delitem(sys.modules, 'bids')
        m.setattr(builtins, '__import__', mock_import)
        with pytest.raises(ImportError):
            myfunc()
