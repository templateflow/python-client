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
    'true', 'on', '1', 'yes', 'y')
TF_CACHED = True

if not TF_HOME.exists() or not list(TF_HOME.iterdir()):
    TF_CACHED = False
    warn("""\
TemplateFlow: repository not found at %s. Populating a new TemplateFlow stub.
If the path reported above is not the desired location for TemplateFlow, \
please set the TEMPLATEFLOW_HOME environment variable.\
""" % TF_HOME, ResourceWarning)
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


def update_home(force=False):
    """Update an existing DataLad or S3 home."""
    if not force and not TF_CACHED:
        print("""\
TemplateFlow was not cached (TEMPLATEFLOW_HOME=%s), \
a fresh initialization was done.""" % TF_HOME)
        return False

    if TF_USE_DATALAD:
        from datalad.api import update
        print("Updating TemplateFlow's HOME using DataLad ...")
        try:
            update(str(TF_HOME), recursive=True, merge=True)
        except Exception as e:
            warn("""Error updating TemplateFlow's home directory (using DataLad):
%s""" % str(e))
        return True

    # This is an S3 type of installation
    from zipfile import ZipFile
    with ZipFile(resource_filename('templateflow',
                                   'conf/templateflow-skel.zip'), 'r') as zipref:
        allfiles = zipref.namelist()
        current_files = [s.relative_to(TF_HOME) for s in TF_HOME.glob('**/*')]
        existing = sorted(set(['%s/' % s.parent for s in current_files])) + \
            [str(s) for s in current_files]
        newfiles = sorted(set(allfiles) - set(existing))
        if newfiles:
            print("Updating TemplateFlow's HOME using S3. "
                  "Adding: \n%s" % "\n".join(newfiles))
            zipref.extractall(str(TF_HOME), members=newfiles)
            return True

    print("TemplateFlow's HOME directory (S3 type) was up-to-date.")
    return False


TF_LAYOUT = Layout(
    str(TF_HOME), validate=False, config='templateflow',
    ignore=['.git', '.datalad', '.gitannex', '.gitattributes', 'scripts'])
