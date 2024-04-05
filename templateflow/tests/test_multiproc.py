import os
from concurrent.futures import ProcessPoolExecutor

import pytest

CPUs = os.cpu_count() or 1


def _update():
    from templateflow.conf import update

    update(local=False, overwrite=True, silent=True)
    return True


@pytest.mark.skipif(CPUs < 2, reason='At least 2 CPUs are required')
def test_multi_proc_update(tmp_path, monkeypatch):
    tf_home = tmp_path / 'tf_home'
    monkeypatch.setenv('TEMPLATEFLOW_HOME', str(tf_home))

    futs = []
    with ProcessPoolExecutor(max_workers=2) as executor:
        for _ in range(2):
            futs.append(executor.submit(_update))

    for fut in futs:
        assert fut.result()
