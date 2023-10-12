"""Configuration and settings."""
from os import getenv
import re
from warnings import warn
from pathlib import Path
from contextlib import suppress
from functools import wraps
from .._loader import Loader

load_data = Loader(__package__)

TF_DEFAULT_HOME = Path.home() / ".cache" / "templateflow"
TF_HOME = Path(getenv("TEMPLATEFLOW_HOME", str(TF_DEFAULT_HOME)))
TF_GITHUB_SOURCE = "https://github.com/templateflow/templateflow.git"
TF_S3_ROOT = "https://templateflow.s3.amazonaws.com"
TF_USE_DATALAD = getenv("TEMPLATEFLOW_USE_DATALAD", "false").lower() in (
    "true",
    "on",
    "1",
    "yes",
    "y",
)
TF_CACHED = True


def _init_cache():
    global TF_HOME, TF_CACHED, TF_USE_DATALAD

    if not TF_HOME.exists() or not list(TF_HOME.iterdir()):
        TF_CACHED = False
        warn(
            f"""\
TemplateFlow: repository not found at <{TF_HOME}>. Populating a new TemplateFlow stub.
If the path reported above is not the desired location for TemplateFlow, \
please set the TEMPLATEFLOW_HOME environment variable.""",
            ResourceWarning,
        )
        if TF_USE_DATALAD:
            try:
                from datalad.api import install
            except ImportError:
                TF_USE_DATALAD = False
            else:
                TF_HOME.parent.mkdir(exist_ok=True, parents=True)
                install(path=str(TF_HOME), source=TF_GITHUB_SOURCE, recursive=True)

        if not TF_USE_DATALAD:
            from ._s3 import update as _update_s3

            _update_s3(TF_HOME, local=True, overwrite=True)


_init_cache()


def requires_layout(func):
    """Decorate function to ensure ``TF_LAYOUT`` is correctly initiated."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        from templateflow.conf import TF_LAYOUT

        if TF_LAYOUT is None:
            from bids import __version__

            raise RuntimeError(
                f"A layout with PyBIDS <{__version__}> could not be initiated"
            )
        return func(*args, **kwargs)

    return wrapper


def update(local=False, overwrite=True, silent=False):
    """Update an existing DataLad or S3 home."""
    if TF_USE_DATALAD and _update_datalad():
        success = True
    else:
        from ._s3 import update as _update_s3

        success = _update_s3(TF_HOME, local=local, overwrite=overwrite, silent=silent)

    # update Layout only if necessary
    if success and TF_LAYOUT is not None:
        init_layout()
        # ensure the api uses the updated layout
        import importlib
        from .. import api

        importlib.reload(api)
    return success


def wipe():
    """Clear the cache if functioning in S3 mode."""
    global TF_USE_DATALAD, TF_HOME

    if TF_USE_DATALAD:
        print("TemplateFlow is configured in DataLad mode, wipe() has no effect")
        return

    import importlib
    from shutil import rmtree
    from templateflow import api

    def _onerror(func, path, excinfo):
        from pathlib import Path

        if Path(path).exists():
            print(
                f"Warning: could not delete <{path}>, please clear the cache manually."
            )

    rmtree(TF_HOME, onerror=_onerror)
    _init_cache()

    importlib.reload(api)


def setup_home(force=False):
    """Initialize/update TF's home if necessary."""
    if not force and not TF_CACHED:
        print(
            f"""\
TemplateFlow was not cached (TEMPLATEFLOW_HOME={TF_HOME}), \
a fresh initialization was done."""
        )
        return False
    return update(local=True, overwrite=False)


def _update_datalad():
    from datalad.api import update

    print("Updating TEMPLATEFLOW_HOME using DataLad ...")
    try:
        update(dataset=str(TF_HOME), recursive=True, merge=True)
    except Exception as e:
        warn(f"Error updating TemplateFlow's home directory (using DataLad): {e}")
    return True


TF_LAYOUT = None


def init_layout():
    from templateflow.conf.bids import Layout
    from bids.layout.index import BIDSLayoutIndexer

    global TF_LAYOUT
    TF_LAYOUT = Layout(
        TF_HOME,
        validate=False,
        config="templateflow",
        indexer=BIDSLayoutIndexer(
            validate=False,
            ignore=(
                re.compile(r"scripts/"),
                re.compile(r"/\."),
                re.compile(r"^\."),
            ),
        ),
    )


with suppress(ImportError):
    init_layout()
