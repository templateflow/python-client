# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
import pytest
from shutil import rmtree
from importlib import reload
from templateflow import conf as tfc


@pytest.mark.parametrize("use_datalad", ["off", "on"])
def test_conf_init(monkeypatch, tmp_path, capsys, use_datalad):
    """Check the correct functioning of config set-up."""
    home = (tmp_path / "-".join(("tf", "dl", use_datalad))).resolve()
    monkeypatch.setenv("TEMPLATEFLOW_USE_DATALAD", use_datalad)
    monkeypatch.setenv("TEMPLATEFLOW_HOME", str(home))

    # First execution, the S3 stub is created (or datalad install)
    reload(tfc)
    assert tfc.TF_CACHED is False
    assert str(tfc.TF_HOME) == str(home)

    reload(tfc)
    assert tfc.TF_CACHED is True
    assert str(tfc.TF_HOME) == str(home)


@pytest.mark.parametrize("use_datalad", ["off", "on"])
def test_setup_home(monkeypatch, tmp_path, capsys, use_datalad):
    """Check the correct functioning of the installation hook."""
    home = (tmp_path / "-".join(("tf", "dl", use_datalad))).resolve()
    monkeypatch.setenv("TEMPLATEFLOW_USE_DATALAD", use_datalad)
    monkeypatch.setenv("TEMPLATEFLOW_HOME", str(home))

    reload(tfc)
    # First execution, the S3 stub is created (or datalad install)
    assert tfc.TF_CACHED is False
    assert tfc.setup_home() is False
    out = capsys.readouterr()[0]
    assert out.startswith("TemplateFlow was not cached")
    assert ("TEMPLATEFLOW_HOME=%s" % home) in out
    assert home.exists()
    assert len(list(home.iterdir())) > 0

    updated = tfc.setup_home(force=True)  # Templateflow is now cached
    out = capsys.readouterr()[0]
    assert not out.startswith("TemplateFlow was not cached")

    if use_datalad == "on":
        assert out.startswith("Updating TEMPLATEFLOW_HOME using DataLad")
        assert updated is True

    elif use_datalad == "off":
        # At this point, S3 should be up-to-date
        assert updated is False
        assert out.startswith("TEMPLATEFLOW_HOME directory (S3 type) was up-to-date.")

        # Let's force an update
        rmtree(str(home / "tpl-MNI152NLin2009cAsym"))
        updated = tfc.setup_home(force=True)
        out = capsys.readouterr()[0]
        assert updated is True
        assert out.startswith("Updating TEMPLATEFLOW_HOME using S3.")

    reload(tfc)
    assert tfc.TF_CACHED is True
    updated = tfc.setup_home()  # Templateflow is now cached
    out = capsys.readouterr()[0]
    assert not out.startswith("TemplateFlow was not cached")

    if use_datalad == "on":
        assert out.startswith("Updating TEMPLATEFLOW_HOME using DataLad")
        assert updated is True

    elif use_datalad == "off":
        # At this point, S3 should be up-to-date
        assert updated is False
        assert out.startswith("TEMPLATEFLOW_HOME directory (S3 type) was up-to-date.")

        # Let's force an update
        rmtree(str(home / "tpl-MNI152NLin2009cAsym"))
        updated = tfc.setup_home()
        out = capsys.readouterr()[0]
        assert updated is True
        assert out.startswith("Updating TEMPLATEFLOW_HOME using S3.")


def test_layout(monkeypatch, tmp_path):
    monkeypatch.setenv("TEMPLATEFLOW_USE_DATALAD", "off")

    lines = ("%s" % tfc.TF_LAYOUT).splitlines()
    assert lines[0] == "TemplateFlow Layout"
    assert lines[1] == " - Home: %s" % tfc.TF_HOME
    assert lines[2].startswith(" - Templates:")


def test_layout_errors(monkeypatch):
    """Check regression of #71."""
    import sys
    import builtins
    from importlib import __import__ as oldimport

    @tfc.requires_layout
    def myfunc():
        return "okay"

    def mock_import(name, globals=None, locals=None, fromlist=tuple(), level=0):
        if name == "bids":
            raise ModuleNotFoundError
        return oldimport(name, globals=globals, locals=locals, fromlist=fromlist, level=level)

    with monkeypatch.context() as m:
        m.setattr(tfc, "TF_LAYOUT", None)
        with pytest.raises(RuntimeError):
            myfunc()

        m.delitem(sys.modules, "bids")
        m.setattr(builtins, "__import__", mock_import)
        with pytest.raises(ImportError):
            myfunc()
