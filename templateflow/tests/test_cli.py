from pathlib import Path

import click.testing

from .. import cli


def test_ls_one():
    runner = click.testing.CliRunner()

    result = runner.invoke(cli.main, ['ls', 'MNI152Lin', '--res', '1', '-s', 'T1w'])

    # One result
    lines = result.stdout.strip().splitlines()
    assert len(lines) == 1

    assert 'tpl-MNI152Lin/tpl-MNI152Lin_res-01_T1w.nii.gz' in lines[0]

    path = Path(lines[0])

    assert path.exists()


def test_ls_multi():
    runner = click.testing.CliRunner()

    result = runner.invoke(cli.main, ['ls', 'MNI152Lin', '--res', '1', '-s', 'T1w', '-s', 'T2w'])

    # Two results
    lines = result.stdout.strip().splitlines()
    assert len(lines) == 2

    assert 'tpl-MNI152Lin/tpl-MNI152Lin_res-01_T1w.nii.gz' in lines[0]
    assert 'tpl-MNI152Lin/tpl-MNI152Lin_res-01_T2w.nii.gz' in lines[1]

    paths = [Path(line) for line in lines]

    assert all(path.exists() for path in paths)


def test_get_one():
    runner = click.testing.CliRunner()

    result = runner.invoke(cli.main, ['get', 'MNI152Lin', '--res', '1', '-s', 'T1w'])

    # One result, possible download status before
    lines = result.stdout.strip().splitlines()[-2:]

    assert 'tpl-MNI152Lin/tpl-MNI152Lin_res-01_T1w.nii.gz' in lines[0]

    path = Path(lines[0])

    stat_res = path.stat()
    assert stat_res.st_size == 10669511


def test_get_multi():
    runner = click.testing.CliRunner()

    result = runner.invoke(cli.main, ['get', 'MNI152Lin', '--res', '1', '-s', 'T1w', '-s', 'T2w'])

    # Two result, possible download status before
    lines = result.stdout.strip().splitlines()[-3:]

    assert 'tpl-MNI152Lin/tpl-MNI152Lin_res-01_T1w.nii.gz' in lines[0]
    assert 'tpl-MNI152Lin/tpl-MNI152Lin_res-01_T2w.nii.gz' in lines[1]

    paths = [Path(line) for line in lines]

    stats = [path.stat() for path in paths]
    assert [stat_res.st_size for stat_res in stats] == [10669511, 10096230]
