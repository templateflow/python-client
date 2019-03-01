"""
Settings
"""
from os import getenv
from pathlib import Path
from .bids import Layout

TF_DEFAULT_HOME = Path.home() / '.cache' / 'templateflow'
TF_HOME = Path(getenv('TEMPLATEFLOW_HOME', str(TF_DEFAULT_HOME)))
TF_GITHUB_SOURCE = 'https://github.com/templateflow/templateflow.git'

TF_LAYOUT = Layout(
    TF_HOME, validate=False, config='templateflow',
    exclude=['.git', '.datalad', '.gitannex', '.gitattributes', 'scripts'])
