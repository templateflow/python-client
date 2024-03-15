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
"""The TemplateFlow Python Client command-line interface (CLI)."""
from __future__ import annotations

import json
from pathlib import Path

import click
from click.decorators import FC, Option, _param_memo

from templateflow import __package__, api
from templateflow._loader import Loader as _Loader
from templateflow.conf import TF_HOME, TF_USE_DATALAD

load_data = _Loader(__package__)

ENTITY_SHORTHANDS = {
    # 'template': ('--tpl', '-t'),
    'resolution': ('--res', ),
    'density': ('--den', ),
    'atlas': ('-a', ),
    'suffix': ('-s', ),
    'desc': ('-d', '--description'),
    'extension': ('--ext', '-x'),
    'label': ('-l', ),
    'segmentation': ('--seg', ),
}
ENTITY_EXCLUDE = {'template', 'description'}
TEMPLATE_LIST = api.get_templates()


def _nulls(s):
    return None if s == 'null' else s


def entity_opts():
    """Attaches all entities as options to the command."""

    entities = json.loads(
        Path(load_data('conf/config.json')).read_text()
    )['entities']

    args = [
        (
            f"--{e['name']}",
            *ENTITY_SHORTHANDS.get(e['name'], ())
        )
        for e in entities if e['name'] not in ENTITY_EXCLUDE
    ]

    def decorator(f: FC) -> FC:
        for arg in reversed(args):
            _param_memo(f, Option(arg, type=str, default=''))
        return f

    return decorator


@click.group()
@click.version_option(message='TemplateFlow Python Client %(version)s')
def main():
    """The TemplateFlow Python Client command-line interface (CLI)."""
    pass


@main.command()
def config():
    """Print-out configuration."""
    click.echo(f"""Current TemplateFlow settings:

    TEMPLATEFLOW_HOME={TF_HOME}
    TEMPLATEFLOW_USE_DATALAD={'on' if TF_USE_DATALAD else 'off'}
""")


@main.command()
def wipe():
    """Wipe out a local S3 (direct-download) TemplateFlow Archive."""
    click.echo(f'This will wipe out all data downloaded into {TF_HOME}.')

    if click.confirm('Do you want to continue?'):
        value = click.prompt(
            f'Please write the path of your local archive ({TF_HOME})',
            default='(abort)',
            show_default=False,
        )
        if value.strip() == str(TF_HOME):
            from templateflow.conf import wipe

            wipe()
            click.echo(f'{TF_HOME} was wiped out.')
            return
    click.echo(f'Aborted! {TF_HOME} WAS NOT wiped out.')


@main.command()
def update():
    """Update the local TemplateFlow Archive."""
    from templateflow.conf import update as _update

    click.echo(
        f'Successfully updated local TemplateFlow Archive: {TF_HOME}.'
        if _update()
        else 'TemplateFlow Archive not updated.'
    )


@main.command()
@entity_opts()
@click.argument('template', type=click.Choice(TEMPLATE_LIST))
def ls(template, **kwargs):
    """List the assets corresponding to template and optional filters."""
    entities = {k: _nulls(v) for k, v in kwargs.items() if v != ''}
    click.echo(
        '\n'.join(f'{match}' for match in api.ls(template, **entities))
    )


@main.command()
@entity_opts()
@click.argument('template', type=click.Choice(TEMPLATE_LIST))
def get(template, **kwargs):
    """Fetch the assets corresponding to template and optional filters."""
    entities = {k: _nulls(v) for k, v in kwargs.items() if v != ''}
    click.echo(
        '\n'.join(f'{match}' for match in api.get(template, **entities))
    )


if __name__ == '__main__':
    """ Install entry-point """
    main()
