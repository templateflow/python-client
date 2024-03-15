"""Test _version.py."""
import sys
from importlib.metadata import PackageNotFoundError
from importlib import reload
import templateflow


def test_version_scm0(monkeypatch):
    """Retrieve the version via setuptools_scm."""

    class _version:
        __version__ = "10.0.0"

    monkeypatch.setitem(sys.modules, "templateflow._version", _version)
    reload(templateflow)
    assert templateflow.__version__ == "10.0.0"


def test_version_scm1(monkeypatch):
    """Retrieve the version via importlib.metadata."""
    monkeypatch.setitem(sys.modules, "templateflow._version", None)

    def _ver(name):
        return "success"

    monkeypatch.setattr("importlib.metadata.version", _ver)
    reload(templateflow)
    assert templateflow.__version__ == "success"


def test_version_scm2(monkeypatch):
    """Check version could not be interpolated."""
    monkeypatch.setitem(sys.modules, "templateflow._version", None)

    def _raise(name):
        raise PackageNotFoundError("No get_distribution mock")

    monkeypatch.setattr("importlib.metadata.version", _raise)
    reload(templateflow)
    assert templateflow.__version__ == "0+unknown"
