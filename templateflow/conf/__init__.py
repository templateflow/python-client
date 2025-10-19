"""Configuration and settings."""

from functools import wraps
from warnings import warn

from acres import Loader

from .cache import CacheConfig, TemplateFlowCache

load_data = Loader(__spec__.name)

_cache = TemplateFlowCache(config=CacheConfig())


def __getattr__(name: str):
    if name == 'TF_HOME':
        return _cache.config.root
    elif name == 'TF_GITHUB_SOURCE':
        return _cache.config.origin
    elif name == 'TF_S3_ROOT':
        return _cache.config.s3_root
    elif name == 'TF_USE_DATALAD':
        return _cache.config.use_datalad
    elif name == 'TF_AUTOUPDATE':
        return _cache.config.autoupdate
    elif name == 'TF_CACHED':
        return _cache.precached
    elif name == 'TF_GET_TIMEOUT':
        return _cache.config.timeout
    elif name == 'TF_LAYOUT':
        return _cache.layout
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


if not _cache.precached:
    warn(
        f"""\
TemplateFlow: repository not found at <{_cache.config.root}>. Populating a new TemplateFlow stub.
If the path reported above is not the desired location for TemplateFlow, \
please set the TEMPLATEFLOW_HOME environment variable.""",
        ResourceWarning,
        stacklevel=2,
    )
    _cache.ensure()


def requires_layout(func):
    """Decorate function to ensure ``TF_LAYOUT`` is correctly initiated."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if _cache.layout is None:
            from bids import __version__

            raise RuntimeError(f'A layout with PyBIDS <{__version__}> could not be initiated')
        return func(*args, **kwargs)

    return wrapper


update = _cache.update
wipe = _cache.wipe


def setup_home(force=False):
    """Initialize/update TF's home if necessary."""
    if not force and not _cache.precached:
        print(
            f"""\
TemplateFlow was not cached (TEMPLATEFLOW_HOME={_cache.config.root}), \
a fresh initialization was done."""
        )
        return False
    return _cache.update(local=True, overwrite=False)
