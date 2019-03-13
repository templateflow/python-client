"""
Settings
"""
from os import getenv
from warnings import warn
from pathlib import Path
from pkg_resources import resource_filename
from .bids import Layout

TF_DEFAULT_HOME = Path.home() / '.cache' / 'templateflow'
TF_HOME = Path(getenv('TEMPLATEFLOW_HOME', str(TF_DEFAULT_HOME)))
TF_GITHUB_SOURCE = 'https://github.com/templateflow/templateflow.git'
TF_S3_ROOT = 'https://templateflow.s3.amazonaws.com'
TF_USE_DATALAD = getenv('TEMPLATEFLOW_USE_DATALAD', 'false').lower() in (
    'true', 'on', '1')

_msg = """\
TemplateFlow: repository not found at %s. Populating a TemplateFlow stub.
If the path reported above is not the desired location for TemplateFlow, \
please set the TEMPLATEFLOW_HOME environment variable.
""" % TF_HOME

if not TF_HOME.exists() or not list(TF_HOME.iterdir()):
    warn(_msg, ResourceWarning)
    if TF_USE_DATALAD:
        try:
            from datalad.api import install
        except ImportError:
            TF_USE_DATALAD = False
        else:
            TF_HOME.parent.mkdir(exist_ok=True, parents=True)
            install(path=str(TF_HOME), source=TF_GITHUB_SOURCE, recursive=True)

    if not TF_USE_DATALAD:
        from zipfile import ZipFile
        TF_HOME.mkdir(exist_ok=True, parents=True)
        with ZipFile(resource_filename('templateflow',
                                       'conf/templateflow-skel.zip'), 'r') as zipref:
            zipref.extractall(str(TF_HOME))

TF_LAYOUT = Layout(
    TF_HOME, validate=False, config='templateflow',
    exclude=['.git', '.datalad', '.gitannex', '.gitattributes', 'scripts'])
