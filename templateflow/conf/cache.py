# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
#
# Copyright 2025 The NiPreps Developers <nipreps@gmail.com>
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
from __future__ import annotations

from dataclasses import dataclass, field
from functools import cache, cached_property
from pathlib import Path
from warnings import warn

from templateflow.conf.env import env_to_bool, get_templateflow_home

TYPE_CHECKING = False
if TYPE_CHECKING:
    from bids.layout import BIDSLayout


# The first CacheConfig is initialized during import, so we need a higher
# level of indirection for warnings to point to the user code.
# After that, we will set the stack level to point to the CacheConfig() caller.
STACKLEVEL = 6


@cache
def _have_datalad() -> bool:
    import importlib.util

    return importlib.util.find_spec('datalad') is not None


@dataclass
class CacheConfig:
    root: Path = field(default_factory=get_templateflow_home)
    origin: str = field(default='https://github.com/templateflow/templateflow.git')
    s3_root: str = field(default='https://templateflow.s3.amazonaws.com')
    use_datalad: bool = field(default_factory=env_to_bool('TEMPLATEFLOW_USE_DATALAD', False))
    autoupdate: bool = field(default_factory=env_to_bool('TEMPLATEFLOW_AUTOUPDATE', True))
    timeout: int = field(default=10)

    def __post_init__(self) -> None:
        global STACKLEVEL
        if self.use_datalad and not _have_datalad():
            self.use_datalad = False
            warn('DataLad is not installed ➔ disabled.', stacklevel=STACKLEVEL)
        STACKLEVEL = 3


@dataclass
class S3Manager:
    s3_root: str

    def install(self, path: Path, overwrite: bool, timeout: int) -> None:
        from ._s3 import update

        update(path, local=True, overwrite=overwrite, silent=True, timeout=timeout)

    def update(self, path: Path, local: bool, overwrite: bool, silent: bool, timeout: int) -> bool:
        from ._s3 import update as _update_s3

        return _update_s3(path, local=local, overwrite=overwrite, silent=silent, timeout=timeout)

    def wipe(self, path: Path) -> None:
        from shutil import rmtree

        def _onerror(func, path, excinfo):
            from pathlib import Path

            if Path(path).exists():
                print(f'Warning: could not delete <{path}>, please clear the cache manually.')

        rmtree(path, onerror=_onerror)


@dataclass
class DataladManager:
    source: str

    def install(self, path: Path, overwrite: bool, timeout: int) -> None:
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

    def wipe(self, path: Path) -> None:
        print('TemplateFlow is configured in DataLad mode, wipe() has no effect')


@dataclass
class TemplateFlowCache:
    config: CacheConfig
    precached: bool = field(init=False)
    manager: DataladManager | S3Manager = field(init=False)

    def __post_init__(self) -> None:
        self.manager = (
            DataladManager(self.config.origin)
            if self.config.use_datalad
            else S3Manager(self.config.s3_root)
        )
        # cache.cached checks live, precached stores state at init
        self.precached = self.cached

    @property
    def cached(self) -> bool:
        return self.config.root.is_dir() and any(self.config.root.iterdir())

    @cached_property
    def layout(self) -> BIDSLayout:
        import re

        from bids.layout.index import BIDSLayoutIndexer

        from .bids import Layout

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

    def ensure(self) -> None:
        if not self.cached:
            self.manager.install(
                self.config.root, overwrite=self.config.autoupdate, timeout=self.config.timeout
            )

    def update(self, local: bool = False, overwrite: bool = True, silent: bool = False) -> bool:
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

    def wipe(self) -> None:
        self.__dict__.pop('layout', None)  # Uncache property
        self.manager.wipe(self.config.root)
