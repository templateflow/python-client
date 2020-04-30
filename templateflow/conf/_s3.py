"""Tooling to handle S3 downloads."""
from pathlib import Path
from tempfile import mkstemp
from pkg_resources import resource_filename

TF_SKEL_URL = (
    "https://raw.githubusercontent.com/templateflow/python-client/"
    "{release}/templateflow/conf/templateflow-skel.{ext}"
).format
TF_SKEL_PATH = Path(resource_filename("templateflow", "conf/templateflow-skel.zip"))
TF_SKEL_MD5 = Path(
    resource_filename("templateflow", "conf/templateflow-skel.md5")
).read_text()


def update(dest, local=True, overwrite=True, silent=False):
    """Update an S3-backed TEMPLATEFLOW_HOME repository."""
    skel_file = Path((_get_skeleton_file() if not local else None) or TF_SKEL_PATH)

    retval = _update_skeleton(skel_file, dest, overwrite=overwrite, silent=silent)
    if skel_file != TF_SKEL_PATH:
        skel_file.unlink()
    return retval


def _get_skeleton_file():
    import requests

    try:
        r = requests.get(TF_SKEL_URL(release="master", ext="md5", allow_redirects=True))
    except requests.exceptions.ConnectionError:
        return

    if not r.ok:
        return

    if r.content.decode().split()[0] != TF_SKEL_MD5:
        r = requests.get(TF_SKEL_URL(release="master", ext="zip", allow_redirects=True))
        if r.ok:
            from os import close

            fh, skel_file = mkstemp(suffix=".zip")
            Path(skel_file).write_bytes(r.content)
            close(fh)
            return skel_file


def _update_skeleton(skel_file, dest, overwrite=True, silent=False):
    from zipfile import ZipFile

    dest = Path(dest)
    dest.mkdir(exist_ok=True, parents=True)
    with ZipFile(skel_file, "r") as zipref:
        if overwrite:
            zipref.extractall(str(dest))
            return True

        allfiles = zipref.namelist()
        current_files = [s.relative_to(dest) for s in dest.glob("**/*")]
        existing = sorted(set(["%s/" % s.parent for s in current_files])) + [
            str(s) for s in current_files
        ]
        newfiles = sorted(set(allfiles) - set(existing))
        if newfiles:
            if not silent:
                print(
                    "Updating TEMPLATEFLOW_HOME using S3. Adding:\n%s" % '\n'.join(newfiles)
                )
            zipref.extractall(str(dest), members=newfiles)
            return True
    if not silent:
        print("TEMPLATEFLOW_HOME directory (S3 type) was up-to-date.")
    return False
