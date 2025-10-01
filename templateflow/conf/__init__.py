"""Configuration and settings."""

import re
from contextlib import suppress
from functools import wraps
from os import getenv
from pathlib import Path
from warnings import warn

from acres import Loader

load_data = Loader(__spec__.name)


def _env_to_bool(envvar: str, default: bool) -> bool:
    """Check for environment variable switches and convert to booleans."""
    switches = {
        'on': {'true', 'on', '1', 'yes', 'y'},
        'off': {'false', 'off', '0', 'no', 'n'},
    }

    val = getenv(envvar, default)
    if isinstance(val, str):
        if val.lower() in switches['on']:
            return True
        elif val.lower() in switches['off']:
            return False
        else:
            # TODO: Create templateflow logger
            print(
                f'{envvar} is set to unknown value <{val}>. '
                f'Falling back to default value <{default}>'
            )
            return default
    return bool(val)


TF_DEFAULT_HOME = Path.home() / '.cache' / 'templateflow'
TF_HOME = Path(getenv('TEMPLATEFLOW_HOME', str(TF_DEFAULT_HOME))).absolute()
TF_GITHUB_SOURCE = 'https://github.com/templateflow/templateflow.git'
TF_S3_ROOT = 'https://templateflow.s3.amazonaws.com'
TF_USE_DATALAD = _env_to_bool('TEMPLATEFLOW_USE_DATALAD', False)
TF_AUTOUPDATE = _env_to_bool('TEMPLATEFLOW_AUTOUPDATE', True)
TF_CACHED = True
TF_GET_TIMEOUT = 10

if TF_USE_DATALAD:
    try:
        from datalad.api import install
    except ImportError:
        warn('DataLad is not installed ➔ disabled.', stacklevel=2)
        TF_USE_DATALAD = False

if not TF_USE_DATALAD:
    from templateflow.conf._s3 import update as _update_s3


def _init_cache():
    global TF_CACHED

    if not TF_HOME.exists() or not list(TF_HOME.iterdir()):
        TF_CACHED = False
        warn(
            f"""\
TemplateFlow: repository not found at <{TF_HOME}>. Populating a new TemplateFlow stub.
If the path reported above is not the desired location for TemplateFlow, \
please set the TEMPLATEFLOW_HOME environment variable.""",
            ResourceWarning,
            stacklevel=2,
        )
        if TF_USE_DATALAD:
            TF_HOME.parent.mkdir(exist_ok=True, parents=True)
            install(path=str(TF_HOME), source=TF_GITHUB_SOURCE, recursive=True)
        else:
            _update_s3(TF_HOME, local=True, overwrite=TF_AUTOUPDATE, silent=True)


_init_cache()


def requires_layout(func):
    """Decorate function to ensure ``TF_LAYOUT`` is correctly initiated."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        from templateflow.conf import TF_LAYOUT

        if TF_LAYOUT is None:
            from bids import __version__

            raise RuntimeError(f'A layout with PyBIDS <{__version__}> could not be initiated')
        return func(*args, **kwargs)

    return wrapper


def update(local=False, overwrite=True, silent=False):
    """Update an existing DataLad or S3 home."""
    if TF_USE_DATALAD:
        success = _update_datalad()
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

    if TF_USE_DATALAD:
        print('TemplateFlow is configured in DataLad mode, wipe() has no effect')
        return

    import importlib
    from shutil import rmtree

    from templateflow import api

    def _onerror(func, path, excinfo):
        from pathlib import Path

        if Path(path).exists():
            print(f'Warning: could not delete <{path}>, please clear the cache manually.')

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

    print('Updating TEMPLATEFLOW_HOME using DataLad ...')
    try:
        update(dataset=str(TF_HOME), recursive=True, merge=True)
    except Exception as e:  # noqa: BLE001
        warn(
            f"Error updating TemplateFlow's home directory (using DataLad): {e}",
            stacklevel=2,
        )
        return False
    return True


TF_LAYOUT = None


def init_layout():
    from bids.layout.index import BIDSLayoutIndexer

    from templateflow.conf.bids import Layout

    global TF_LAYOUT
    TF_LAYOUT = Layout(
        TF_HOME,
        validate=False,
        config='templateflow',
        indexer=BIDSLayoutIndexer(
            validate=False,
            ignore=(
                re.compile(r'scripts/'),
                re.compile(r'/\.'),
                re.compile(r'^\.'),
            ),
        ),
    )


with suppress(ImportError):
    init_layout()
