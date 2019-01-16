"""
Settings
"""
from os import getenv
from pathlib import Path

TF_DEFAULT_HOME = Path.home() / '.cache' / 'templateflow'
TF_HOME = Path(getenv('TEMPLATEFLOW_HOME', str(TF_DEFAULT_HOME)))
TF_GITHUB_SOURCE = 'https://github.com/templateflow/templateflow.git'
