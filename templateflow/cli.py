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
from acres import Loader as _Loader
from click.decorators import FC, Option, _param_memo

from templateflow.client import TemplateFlowClient

load_data = _Loader(__spec__.parent)

ENTITY_SHORTHANDS = {
    # 'template': ('--tpl', '-t'),
    'resolution': ('--res',),
    'density': ('--den',),
    'atlas': ('-a',),
    'suffix': ('-s',),
    'desc': ('-d', '--description'),
    'extension': ('--ext', '-x'),
    'label': ('-l',),
    'segmentation': ('--seg',),
}
ENTITY_EXCLUDE = {'template', 'description'}

CLIENT = TemplateFlowClient()
CACHE = CLIENT.cache
CONFIG = CACHE.config
CACHE.ensure()

TEMPLATE_LIST = [d.name[4:] for d in CONFIG.root.iterdir() if d.name.startswith('tpl-')]


def _nulls(s):
    return None if s == 'null' else s


def entity_opts():
    """Attaches all entities as options to the command."""

    entities = json.loads(load_data('conf/config.json').read_text())['entities']

    args = [
        (f'--{e["name"]}', *ENTITY_SHORTHANDS.get(e['name'], ()))
        for e in entities
        if e['name'] not in ENTITY_EXCLUDE
    ]

    def decorator(f: FC) -> FC:
        for arg in reversed(args):
            _param_memo(f, Option(arg, type=str, default=[], multiple=True))
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

    TEMPLATEFLOW_HOME={CONFIG.root}
    TEMPLATEFLOW_USE_DATALAD={'on' if CONFIG.use_datalad else 'off'}
    TEMPLATEFLOW_AUTOUPDATE={'on' if CONFIG.autoupdate else 'off'}
""")


@main.command()
def wipe():
    """Wipe out a local S3 (direct-download) TemplateFlow Archive."""
    click.echo(f'This will wipe out all data downloaded into {CONFIG.root}.')

    if click.confirm('Do you want to continue?'):
        value = click.prompt(
            f'Please write the path of your local archive ({CONFIG.root})',
            default='(abort)',
            show_default=False,
        )
        if value.strip() == str(CONFIG.root):
            from templateflow.conf import wipe

            wipe()
            click.echo(f'{CONFIG.root} was wiped out.')
            return
    click.echo(f'Aborted! {CONFIG.root} WAS NOT wiped out.')


@main.command()
@click.option('--local', is_flag=True)
@click.option('--overwrite/--no-overwrite', default=True)
def update(local, overwrite):
    """Update the local TemplateFlow Archive."""
    from templateflow.conf import update as _update

    click.echo(
        f'Successfully updated local TemplateFlow Archive: {CONFIG.root}.'
        if _update(local=local, overwrite=overwrite)
        else 'TemplateFlow Archive not updated.'
    )


@main.command()
@entity_opts()
@click.argument('template', type=click.Choice(TEMPLATE_LIST))
def ls(template, **kwargs):
    """List the assets corresponding to template and optional filters."""
    entities = {k: _nulls(v) for k, v in kwargs.items() if v != ''}
    click.echo('\n'.join(f'{match}' for match in CLIENT.ls(template, **entities)))


@main.command()
@entity_opts()
@click.argument('template', type=click.Choice(TEMPLATE_LIST))
def get(template, **kwargs):
    """Fetch the assets corresponding to template and optional filters."""
    entities = {k: _nulls(v) for k, v in kwargs.items() if v != ''}
    paths = CLIENT.get(template, **entities)
    filenames = [str(paths)] if isinstance(paths, Path) else [str(file) for file in paths]
    click.echo('\n'.join(filenames))


if __name__ == '__main__':
    """ Install entry-point """
    main()
