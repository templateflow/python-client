"""
TemplateFlow's Python Client
"""
from pathlib import Path
from json import loads
from .conf import TF_LAYOUT


def get(template, **kwargs):
    """
    Fetch one file from one template

    >>> str(get('MNI152Lin', resolution=1, suffix='T1w'))  # doctest: +ELLIPSIS
    '.../tpl-MNI152Lin/tpl-MNI152Lin_res-01_T1w.nii.gz'

    >>> str(get('MNI152Lin', resolution=2, suffix='T1w'))  # doctest: +ELLIPSIS
    '.../tpl-MNI152Lin/tpl-MNI152Lin_res-02_T1w.nii.gz'

    >>> [str(p) for p in get(
    ...     'MNI152Lin', suffix='T1w')]  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    ['.../tpl-MNI152Lin/tpl-MNI152Lin_res-01_T1w.nii.gz',
     '.../tpl-MNI152Lin/tpl-MNI152Lin_res-02_T1w.nii.gz']

    """
    out_file = [Path(p) for p in TF_LAYOUT.get(
        template=template, return_type='file', **kwargs)]

    for filepath in [p for p in out_file if not p.is_file()]:
        _datalad_get(filepath)

    if len(out_file) == 1:
        return out_file[0]
    return out_file


def templates(**kwargs):
    """
    Returns a list of available templates

    >>> base = ['MNI152Lin', 'MNI152NLin2009cAsym', 'NKI', 'OASIS30ANTs']
    >>> tpls = templates()
    >>> all([t in tpls for t in base])
    True

    >>> templates(suffix='PD')
    ['MNI152Lin', 'MNI152NLin2009cAsym']

    """
    return sorted(TF_LAYOUT.get_templates(**kwargs))


def get_metadata(template):
    """
    Fetch one file from one template

    >>> get_metadata('MNI152Lin')['Name']
    'Linear ICBM Average Brain (ICBM152) Stereotaxic Registration Model'

    """

    tf_home = Path(TF_LAYOUT.root)
    filepath = tf_home / ('tpl-%s' % template) / 'template_description.json'

    # Ensure that template is installed and file is available
    if not filepath.is_file():
        _datalad_get(filepath)
    return loads(filepath.read_text())


def _datalad_get(filepath):
    if not filepath:
        return

    from datalad import api
    from datalad.support.exceptions import IncompleteResultsError

    try:
        api.get(str(filepath))
    except IncompleteResultsError as exc:
        if exc.failed[0]['message'] == 'path not associated with any dataset':
            from .conf import TF_GITHUB_SOURCE
            api.install(path=TF_LAYOUT.root, source=TF_GITHUB_SOURCE, recursive=True)
            api.get(str(filepath))
        else:
            raise
