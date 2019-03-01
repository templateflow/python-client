"""
Settings
"""
from os import getenv
from pathlib import Path
from .bids import Layout

TF_DEFAULT_HOME = Path.home() / '.cache' / 'templateflow'
TF_HOME = Path(getenv('TEMPLATEFLOW_HOME', str(TF_DEFAULT_HOME)))
TF_GITHUB_SOURCE = 'https://github.com/templateflow/templateflow.git'

if not TF_HOME.exists():
    try:
        from datalad.api import install
    except ImportError:
        raise RuntimeError("""\
'TemplateFlow repository not found at path %s, and DataLad/git-annex are not \
installed.
Please download TemplateFlow manually from \
https://files.osf.io/v1/resources/ue5gx/providers/osfstorage/?zip= \
and place all templates under the path indicated above.""" % TF_HOME)
    else:
        TF_HOME.parent.mkdir(exist_ok=True, parents=True)
        install(path=str(TF_HOME), source=TF_GITHUB_SOURCE, recursive=True)

TF_LAYOUT = Layout(
    TF_HOME, validate=False, config='templateflow',
    exclude=['.git', '.datalad', '.gitannex', '.gitattributes', 'scripts'])
