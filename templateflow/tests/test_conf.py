from pathlib import Path

import pytest

from .. import api, conf


@pytest.mark.skipif(conf.TF_USE_DATALAD, reason='S3 only')
def test_update_s3(tmp_path):
    conf.TF_HOME = tmp_path / 'templateflow'
    conf.TF_HOME.mkdir(exist_ok=True)

    # replace TF_SKEL_URL with the path of a legacy skeleton
    _skel_url = conf._s3.TF_SKEL_URL
    conf._s3.TF_SKEL_URL = (
        'https://github.com/templateflow/python-client/raw/0.5.0/'
        'templateflow/conf/templateflow-skel.{ext}'.format
    )
    # initialize templateflow home, making sure to pull the legacy skeleton
    conf.update(local=False)
    # ensure we can grab a file
    assert Path(api.get('MNI152NLin2009cAsym', resolution=2, desc='brain', suffix='mask')).exists()
    # and ensure we can't fetch one that doesn't yet exist
    assert not api.get('Fischer344', hemi='L', desc='brain', suffix='mask')

    # refresh the skeleton using the most recent skeleton
    conf._s3.TF_SKEL_URL = _skel_url
    conf.update(local=True, overwrite=True)
    assert Path(api.get('Fischer344', hemi='L', desc='brain', suffix='mask')).exists()
