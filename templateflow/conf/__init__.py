"""Configuration and settings."""
from os import getenv
from warnings import warn
from pathlib import Path

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

if not TF_HOME.exists() or not list(TF_HOME.iterdir()):
    TF_CACHED = False
    warn(
        """\
TemplateFlow: repository not found at %s. Populating a new TemplateFlow stub.
If the path reported above is not the desired location for TemplateFlow, \
please set the TEMPLATEFLOW_HOME environment variable.\
"""
        % TF_HOME,
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
    from .bids import Layout
    from bids.layout import BIDSLayoutIndexer

    global TF_LAYOUT
    TF_LAYOUT = Layout(
        TF_HOME,
        validate=False,
        config="templateflow",
        indexer=BIDSLayoutIndexer(
            validate=False,
            ignore=(
                ".git",
                ".datalad",
                ".gitannex",
                ".gitattributes",
                ".github",
                "scripts",
            ),
        ),
    )


try:
    init_layout()
except ImportError:
    pass
