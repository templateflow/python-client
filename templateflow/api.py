"""
TemplateFlow's Python Client
"""

from datalad import api
from datalad.support.exceptions import IncompleteResultsError
from .conf import TF_HOME


def get(template_id, suffix):
    """
    Fetch one file from one template

    >>> get('MNI152Lin', 'res-01_T1w.nii.gz')  # doctest: +ELLIPSIS
    '.../tpl-MNI152Lin/tpl-MNI152Lin_res-01_T1w.nii.gz'
    """
    if suffix.startswith('_'):
        suffix = suffix[1:]

    filename = 'tpl-%s_%s' % (template_id, suffix)
    filepath = str(TF_HOME / ('tpl-%s' % template_id) / filename)

    try:
        out_file = api.get(filepath)
    except IncompleteResultsError as exc:
        if exc.failed[0]['message'] == 'path not associated with any dataset':
            from .conf import TF_GITHUB_SOURCE
            api.install(path=str(TF_HOME), source=TF_GITHUB_SOURCE, recursive=True)
            out_file = api.get(filepath)
        else:
            raise

    out_file = [p['path'] for p in out_file]
    if len(out_file) == 1:
        return out_file[0]
    return out_file
