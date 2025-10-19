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
"""TemplateFlow's Python Client."""

from __future__ import annotations

import os
import sys
from json import loads
from pathlib import Path

from .conf.cache import CacheConfig, TemplateFlowCache


class TemplateFlowClient:
    def __init__(
        self,
        root: os.PathLike[str] | str | None = None,
        *,
        cache: TemplateFlowCache | None = None,
        **config_kwargs,
    ):
        if cache is None:
            if root:
                config_kwargs['root'] = root
            cache = TemplateFlowCache(CacheConfig(**config_kwargs))
        elif root or config_kwargs:
            raise ValueError(
                'If `cache` is provided, `root` and other config kwargs cannot be used.'
            )
        self.cache = cache

    def __getattr__(self, name: str):
        name = name.replace('ls_', 'get_')
        try:
            if name.startswith('get_') and name not in dir(self.cache.layout):
                return getattr(self.cache.layout, name)
        except AttributeError:
            pass
        msg = f"'{self.__class__.__name__}' object has no attribute '{name}'"
        raise AttributeError(msg) from None

    def ls(self, template, **kwargs) -> list[Path]:
        """
        List files pertaining to one or more templates.

        Parameters
        ----------
        template : str
            A template identifier (e.g., ``MNI152NLin2009cAsym``).

        Keyword Arguments
        -----------------
        resolution: int or None
            Index to an specific spatial resolution of the template.
        suffix : str or None
            BIDS suffix
        atlas : str or None
            Name of a particular atlas
        hemi : str or None
            Hemisphere
        space : str or None
            Space template is mapped to
        density : str or None
            Surface density
        desc : str or None
            Description field

        Examples
        --------

        .. testsetup::

            >>> client = TemplateFlowClient()

        >>> client.ls('MNI152Lin', resolution=1, suffix='T1w', desc=None)
        [PosixPath('.../tpl-MNI152Lin/tpl-MNI152Lin_res-01_T1w.nii.gz')]

        >>> client.ls('MNI152Lin', resolution=2, suffix='T1w', desc=None)
        [PosixPath('.../tpl-MNI152Lin/tpl-MNI152Lin_res-02_T1w.nii.gz')]

        >>> client.ls('MNI152Lin', suffix='T1w', desc=None)
        [PosixPath('.../tpl-MNI152Lin/tpl-MNI152Lin_res-01_T1w.nii.gz'),
         PosixPath('.../tpl-MNI152Lin/tpl-MNI152Lin_res-02_T1w.nii.gz')]

        >>> client.ls('fsLR', space=None, hemi='L', density='32k', suffix='sphere')
        [PosixPath('.../tpl-fsLR_hemi-L_den-32k_sphere.surf.gii')]

        >>> client.ls('fsLR', space='madeup')
        []

        """
        from bids.layout import Query

        # Normalize extensions to always have leading dot
        if 'extension' in kwargs:
            kwargs['extension'] = _normalize_ext(kwargs['extension'])

        return [
            Path(p)
            for p in self.cache.layout.get(
                template=Query.ANY if template is None else template, return_type='file', **kwargs
            )
        ]

    def get(self, template, raise_empty=False, **kwargs) -> list[Path]:
        """
        Pull files pertaining to one or more templates down.

        Parameters
        ----------
        template : str
            A template identifier (e.g., ``MNI152NLin2009cAsym``).
        raise_empty : bool, optional
            Raise exception if no files were matched

        Keyword Arguments
        -----------------
        resolution: int or None
            Index to an specific spatial resolution of the template.
        suffix : str or None
            BIDS suffix
        atlas : str or None
            Name of a particular atlas
        hemi : str or None
            Hemisphere
        space : str or None
            Space template is mapped to
        density : str or None
            Surface density
        desc : str or None
            Description field

        Examples
        --------

        .. testsetup::

            >>> client = TemplateFlowClient()

        >>> str(client.get('MNI152Lin', resolution=1, suffix='T1w', desc=None))
        '.../tpl-MNI152Lin/tpl-MNI152Lin_res-01_T1w.nii.gz'

        >>> str(client.get('MNI152Lin', resolution=2, suffix='T1w', desc=None))
        '.../tpl-MNI152Lin/tpl-MNI152Lin_res-02_T1w.nii.gz'

        >>> [str(p) for p in client.get('MNI152Lin', suffix='T1w', desc=None)]
        ['.../tpl-MNI152Lin/tpl-MNI152Lin_res-01_T1w.nii.gz',
         '.../tpl-MNI152Lin/tpl-MNI152Lin_res-02_T1w.nii.gz']

        >>> str(client.get('fsLR', space=None, hemi='L', density='32k', suffix='sphere'))
        '.../tpl-fsLR_hemi-L_den-32k_sphere.surf.gii'

        >>> client.get('fsLR', space='madeup')
        []

        >>> client.get('fsLR', raise_empty=True, space='madeup')
        Traceback (most recent call last):
        Exception:
        ...

        """
        # List files available
        out_file = self.ls(template, **kwargs)

        if raise_empty and not out_file:
            raise Exception('No results found')

        # Truncate possible S3 error files from previous attempts
        _truncate_s3_errors(out_file)

        # Try DataLad first
        dl_missing = [p for p in out_file if not p.is_file()]
        if self.cache.config.use_datalad and dl_missing:
            for filepath in dl_missing:
                _datalad_get(self.cache.config, filepath)
                dl_missing.remove(filepath)

        # Fall-back to S3 if some files are still missing
        s3_missing = [p for p in out_file if p.is_file() and p.stat().st_size == 0]
        for filepath in s3_missing + dl_missing:
            _s3_get(self.cache.config, filepath)

        not_fetched = [str(p) for p in out_file if not p.is_file() or p.stat().st_size == 0]

        if not_fetched:
            msg = 'Could not fetch template files: {}.'.format(', '.join(not_fetched))
            if dl_missing and not self.cache.config.use_datalad:
                msg += f"""\
    The $TEMPLATEFLOW_HOME folder {self.cache.config.root} seems to contain an initiated DataLad \
    dataset, but the environment variable $TEMPLATEFLOW_USE_DATALAD is not \
    set or set to one of (false, off, 0). Please set $TEMPLATEFLOW_USE_DATALAD \
    on (possible values: true, on, 1)."""

            if s3_missing and self.cache.config.use_datalad:
                msg += f"""\
    The $TEMPLATEFLOW_HOME folder {self.cache.layout.root} seems to contain an plain \
    dataset, but the environment variable $TEMPLATEFLOW_USE_DATALAD is \
    set to one of (true, on, 1). Please set $TEMPLATEFLOW_USE_DATALAD \
    off (possible values: false, off, 0)."""

            raise RuntimeError(msg)

        if len(out_file) == 1:
            return out_file[0]
        return out_file

    def templates(self, **kwargs) -> list[str]:
        """
        Return a list of available templates.

        Keyword Arguments
        -----------------
        resolution: int or None
            Index to an specific spatial resolution of the template.
        suffix : str or None
            BIDS suffix
        atlas : str
            Name of a particular atlas
        desc : str
            Description field

        Examples
        --------

        .. testsetup::

            >>> client = TemplateFlowClient()

        >>> base = ['MNI152Lin', 'MNI152NLin2009cAsym', 'NKI', 'OASIS30ANTs']
        >>> tpls = client.templates()
        >>> all([t in tpls for t in base])
        True

        >>> sorted(set(base).intersection(client.templates(suffix='PD')))
        ['MNI152Lin', 'MNI152NLin2009cAsym']
        """
        return sorted(self.get_templates(**kwargs))

    def get_metadata(self, template) -> dict[str, str]:
        """
        Fetch one file from one template.

        Parameters
        ----------
        template : str
            A template identifier (e.g., ``MNI152NLin2009cAsym``).

        Examples
        --------

        .. testsetup::

            >>> client = TemplateFlowClient()

        >>> client.get_metadata('MNI152Lin')['Name']
        'Linear ICBM Average Brain (ICBM152) Stereotaxic Registration Model'

        """
        tf_home = Path(self.cache.layout.root)
        filepath = tf_home / (f'tpl-{template}') / 'template_description.json'

        # Ensure that template is installed and file is available
        if not filepath.is_file():
            _datalad_get(filepath)
        return loads(filepath.read_text())

    def get_citations(self, template, bibtex=False) -> list[str]:
        """
        Fetch template citations

        Parameters
        ----------
        template : :obj:`str`
            A template identifier (e.g., ``MNI152NLin2009cAsym``).
        bibtex : :obj:`bool`, optional
            Generate citations in BibTeX format.

        """
        data = self.get_metadata(template)
        refs = data.get('ReferencesAndLinks', [])
        if isinstance(refs, dict):
            refs = list(refs.values())

        if not bibtex:
            return refs

        return [_to_bibtex(ref, template, self.cache.config.timeout).rstrip() for ref in refs]


def _datalad_get(config: CacheConfig, filepath: Path) -> None:
    if not filepath:
        return

    from datalad import api
    from datalad.support.exceptions import IncompleteResultsError

    try:
        api.get(filepath, dataset=config.root)
    except IncompleteResultsError as exc:
        if exc.failed[0]['message'] == 'path not associated with any dataset':
            api.install(path=config.root, source=config.origin, recursive=True)
            api.get(filepath, dataset=config.root)
        else:
            raise


def _s3_get(config: CacheConfig, filepath: Path) -> None:
    from sys import stderr
    from urllib.parse import quote

    import requests
    from tqdm import tqdm

    path = quote(filepath.relative_to(config.root).as_posix())
    url = f'{config.s3_root}/{path}'

    print(f'Downloading {url}', file=stderr)
    # Streaming, so we can iterate over the response.
    r = requests.get(url, stream=True, timeout=config.timeout)
    if r.status_code != 200:
        raise RuntimeError(f'Failed to download {url} with status code {r.status_code}')

    # Total size in bytes.
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024
    wrote = 0
    if not filepath.is_file():
        filepath.unlink()

    with filepath.open('wb') as f:
        with tqdm(total=total_size, unit='B', unit_scale=True) as t:
            for data in r.iter_content(block_size):
                wrote = wrote + len(data)
                f.write(data)
                t.update(len(data))

    if total_size != 0 and wrote != total_size:
        raise RuntimeError('ERROR, something went wrong')


def _to_bibtex(doi: str, template: str, timeout: float) -> str:
    if 'doi.org' not in doi:
        return doi

    # Is a DOI URL
    import requests

    response = requests.post(
        doi,
        headers={'Accept': 'application/x-bibtex; charset=utf-8'},
        timeout=timeout,
    )
    if not response.ok:
        print(
            f'Failed to convert DOI <{doi}> to bibtex, returning URL.',
            file=sys.stderr,
        )
        return doi

    # doi.org may not honor requested charset, to safeguard force a bytestream with
    # response.content, then decode into UTF-8.
    bibtex = response.content.decode()

    # doi.org / crossref may still point to the no longer preferred proxy service
    return bibtex.replace('http://dx.doi.org/', 'https://doi.org/')


def _normalize_ext(value):
    """
    Normalize extensions to have a leading dot.

    Examples
    --------
    >>> _normalize_ext(".nii.gz")
    '.nii.gz'
    >>> _normalize_ext("nii.gz")
    '.nii.gz'
    >>> _normalize_ext(("nii", ".nii.gz"))
    ['.nii', '.nii.gz']
    >>> _normalize_ext(("", ".nii.gz"))
    ['', '.nii.gz']
    >>> _normalize_ext((None, ".nii.gz"))
    [None, '.nii.gz']
    >>> _normalize_ext([])
    []

    """

    if not value:
        return value

    if isinstance(value, str):
        return f'{"" if value.startswith(".") else "."}{value}'
    return [_normalize_ext(v) for v in value]


def _truncate_s3_errors(filepaths):
    """
    Truncate XML error bodies saved by previous versions of TemplateFlow.

    Parameters
    ----------
    filepaths : list of Path
        List of file paths to check and truncate if necessary.
    """
    for filepath in filepaths:
        if filepath.is_file(follow_symlinks=False) and 0 < filepath.stat().st_size < 1024:
            with open(filepath, 'rb') as f:
                content = f.read(100)
            if content.startswith(b'<?xml') and b'<Error><Code>' in content:
                filepath.write_bytes(b'')  # Truncate file to zero bytes
