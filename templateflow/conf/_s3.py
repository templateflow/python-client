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
"""Tooling to handle S3 downloads."""

from pathlib import Path
from tempfile import mkstemp

from acres import Loader

load_data = Loader(__spec__.parent)

TF_SKEL_URL = (
    'https://raw.githubusercontent.com/templateflow/python-client/'
    '{release}/templateflow/conf/templateflow-skel.{ext}'
).format


def update(dest, local=True, overwrite=True, silent=False, *, timeout: int):
    """Update an S3-backed TEMPLATEFLOW_HOME repository."""
    skel_zip = load_data('templateflow-skel.zip')
    skel_file = Path((_get_skeleton_file(timeout) if not local else None) or skel_zip)

    retval = _update_skeleton(skel_file, dest, overwrite=overwrite, silent=silent)
    if skel_file != skel_zip:
        skel_file.unlink()
    return retval


def _get_skeleton_file(timeout: int):
    import requests

    try:
        r = requests.get(
            TF_SKEL_URL(release='master', ext='md5'),
            allow_redirects=True,
            timeout=timeout,
        )
    except requests.exceptions.ConnectionError:
        return

    if not r.ok:
        return

    md5 = load_data.readable('templateflow-skel.md5').read_bytes()
    if r.content != md5:
        r = requests.get(
            TF_SKEL_URL(release='master', ext='zip'),
            allow_redirects=True,
            timeout=timeout,
        )
        if r.ok:
            from os import close

            fh, skel_file = mkstemp(suffix='.zip')
            Path(skel_file).write_bytes(r.content)
            close(fh)
            return skel_file


def _update_skeleton(skel_file, dest, overwrite=True, silent=False):
    from zipfile import ZipFile

    dest = Path(dest)
    dest.mkdir(exist_ok=True, parents=True)
    with ZipFile(skel_file, 'r') as zipref:
        allfiles = sorted(zipref.namelist())

        if overwrite:
            newfiles = allfiles
        else:
            current_files = [s.relative_to(dest) for s in dest.glob('**/*')]
            existing = sorted({f'{s.parent}/' for s in current_files}) + [
                str(s) for s in current_files
            ]
            newfiles = sorted(set(allfiles) - set(existing))

        if newfiles:
            if not silent:
                print('Updating TEMPLATEFLOW_HOME using S3. Adding:')

            for fl in newfiles:
                if not silent:
                    print(fl)
                localpath = dest / fl
                if localpath.exists():
                    continue
                try:
                    zipref.extract(fl, path=dest)
                except FileExistsError:
                    # If there is a conflict, do not clobber
                    pass
            return True
    if not silent:
        print('TEMPLATEFLOW_HOME directory (S3 type) was up-to-date.')
    return False
