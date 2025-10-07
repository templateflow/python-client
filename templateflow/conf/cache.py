from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from warnings import warn

from .bids import Layout
from .env import env_to_bool, get_templateflow_home


@dataclass
class CacheConfig:
    root: Path = field(default_factory=get_templateflow_home)
    origin: str = field(default='https://github.com/templateflow/templateflow.git')
    http_root: str = field(default='https://templateflow.s3.amazonaws.com')
    use_datalad: bool = field(default_factory=env_to_bool('TEMPLATEFLOW_USE_DATALAD', False))
    autoupdate: bool = field(default_factory=env_to_bool('TEMPLATEFLOW_AUTOUPDATE', True))
    timeout: int = field(default=10)

    def __post_init__(self):
        if self.use_datalad:
            from importlib.util import find_spec

            self.use_datalad = find_spec('datalad') is not None


@dataclass
class S3Manager:
    http_root: str

    def install(self, path: Path, overwrite: bool, timeout: int):
        from ._s3 import update

        update(path, local=True, overwrite=overwrite, silent=True, timeout=timeout)

    def update(self, path: Path, local: bool, overwrite: bool, silent: bool, timeout: int) -> bool:
        from ._s3 import update as _update_s3

        return _update_s3(path, local=local, overwrite=overwrite, silent=silent, timeout=timeout)

    def wipe(self, path: Path):
        from shutil import rmtree

        def _onerror(func, path, excinfo):
            from pathlib import Path

            if Path(path).exists():
                print(f'Warning: could not delete <{path}>, please clear the cache manually.')

        rmtree(path, onerror=_onerror)


@dataclass
class DataladManager:
    source: str

    def install(self, path: Path, overwrite: bool, timeout: int):
        from datalad.api import install

        install(path=path, source=self.source, recursive=True)

    def update(self, path: Path, local: bool, overwrite: bool, silent: bool, timeout: int) -> bool:
        from datalad.api import update

        print('Updating TEMPLATEFLOW_HOME using DataLad ...')
        try:
            update(dataset=path, recursive=True, merge=True)
        except Exception as e:  # noqa: BLE001
            warn(
                f"Error updating TemplateFlow's home directory (using DataLad): {e}",
                stacklevel=2,
            )
            return False
        return True

    def wipe(self, path: Path):
        print('TemplateFlow is configured in DataLad mode, wipe() has no effect')


@dataclass
class TemplateFlowCache:
    config: CacheConfig
    precached: bool = field(init=False)
    manager: DataladManager | S3Manager = field(init=False)

    def __post_init__(self):
        self.manager = (
            DataladManager(self.config.origin)
            if self.config.use_datalad
            else S3Manager(self.config.http_root)
        )
        # cache.cached checks live, precached stores state at init
        self.precached = self.cached

    @property
    def cached(self) -> bool:
        return self.config.root.is_dir() and any(self.config.root.iterdir())

    @cached_property
    def layout(self) -> Layout:
        import re

        from bids.layout.index import BIDSLayoutIndexer

        self.ensure()
        return Layout(
            self.config.root,
            validate=False,
            config='templateflow',
            indexer=BIDSLayoutIndexer(
                validate=False,
                ignore=(re.compile(r'scripts/'), re.compile(r'/\.'), re.compile(r'^\.')),
            ),
        )

    def ensure(self):
        if not self.cached:
            self.manager.install(
                self.config.root, overwrite=self.config.autoupdate, timeout=self.config.timeout
            )

    def update(self, local: bool = False, overwrite: bool = True, silent: bool = False):
        if self.manager.update(
            self.config.root,
            local=local,
            overwrite=overwrite,
            silent=silent,
            timeout=self.config.timeout,
        ):
            self.__dict__.pop('layout', None)  # Uncache property
            return True
        return False

    def wipe(self):
        self.__dict__.pop('layout', None)  # Uncache property
        self.manager.wipe(self.config.root)
