"""TemplateFlow's Python Client."""
from json import loads
from pathlib import Path
import re
import sys

from .conf import TF_LAYOUT, TF_S3_ROOT, TF_USE_DATALAD


def get(template, raise_empty=False, **kwargs):
    """
    Fetch one file from one particular template.

    Parameters
    ----------
    template : str
        A template identifier (e.g., ``MNI152NLin2009cAsym``).
    raise_empty : bool, optional
        Raise exception if no files were matched

    Keyword Arguments
    -----------------
    resolution: int or None
        Index to an specific spatial resolution of the template.
    suffix : str or None
        BIDS suffix
    atlas : str or None
        Name of a particular atlas
    hemi : str or None
        Hemisphere
    space : str or None
        Space template is mapped to
    density : str or None
        Surface density
    desc : str or None
        Description field

    Examples
    --------
    >>> str(get('MNI152Lin', resolution=1, suffix='T1w'))  # doctest: +ELLIPSIS
    '.../tpl-MNI152Lin/tpl-MNI152Lin_res-01_T1w.nii.gz'

    >>> str(get('MNI152Lin', resolution=2, suffix='T1w'))  # doctest: +ELLIPSIS
    '.../tpl-MNI152Lin/tpl-MNI152Lin_res-02_T1w.nii.gz'

    >>> [str(p) for p in get(
    ...     'MNI152Lin', suffix='T1w')]  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    ['.../tpl-MNI152Lin/tpl-MNI152Lin_res-01_T1w.nii.gz',
     '.../tpl-MNI152Lin/tpl-MNI152Lin_res-02_T1w.nii.gz']

    >>> str(get('fsLR', space=None, hemi='L',
    ...         density='32k', suffix='sphere'))  # doctest: +ELLIPSIS
    '.../tpl-fsLR_hemi-L_den-32k_sphere.surf.gii'

    >>> get('fsLR', space='madeup')
    []

    >>> get('fsLR', raise_empty=True, space='madeup')  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    Exception:
    ...

    """
    out_file = [
        Path(p) for p in TF_LAYOUT.get(template=template, return_type="file", **kwargs)
    ]

    # Try DataLad first
    dl_missing = [p for p in out_file if not p.is_file()]
    if TF_USE_DATALAD and dl_missing:
        for filepath in dl_missing:
            _datalad_get(filepath)
            dl_missing.remove(filepath)

    # Fall-back to S3 if some files are still missing
    s3_missing = [p for p in out_file if p.is_file() and p.stat().st_size == 0]
    for filepath in s3_missing + dl_missing:
        _s3_get(filepath)

    not_fetched = [str(p) for p in out_file if not p.is_file() or p.stat().st_size == 0]

    if not_fetched:
        msg = "Could not fetch template files: %s." % ", ".join(not_fetched)
        if dl_missing and not TF_USE_DATALAD:
            msg += (
                """\
The $TEMPLATEFLOW_HOME folder %s seems to contain an initiated DataLad \
dataset, but the environment variable $TEMPLATEFLOW_USE_DATALAD is not \
set or set to one of (false, off, 0). Please set $TEMPLATEFLOW_USE_DATALAD \
on (possible values: true, on, 1)."""
                % TF_LAYOUT.root
            )

        if s3_missing and TF_USE_DATALAD:
            msg += (
                """\
The $TEMPLATEFLOW_HOME folder %s seems to contain an plain \
dataset, but the environment variable $TEMPLATEFLOW_USE_DATALAD is \
set to one of (true, on, 1). Please set $TEMPLATEFLOW_USE_DATALAD \
off (possible values: false, off, 0)."""
                % TF_LAYOUT.root
            )

        raise RuntimeError(msg)

    if not out_file and raise_empty:
        raise Exception("No results found")

    if len(out_file) == 1:
        return out_file[0]
    return out_file


def templates(**kwargs):
    """
    Returns a list of available templates.

    Keyword Arguments
    -----------------
    resolution: int or None
        Index to an specific spatial resolution of the template.
    suffix : str or None
        BIDS suffix
    atlas : str
        Name of a particular atlas
    desc : str
        Description field

    Examples
    --------
    >>> base = ['MNI152Lin', 'MNI152NLin2009cAsym', 'NKI', 'OASIS30ANTs']
    >>> tpls = templates()
    >>> all([t in tpls for t in base])
    True

    >>> templates(suffix='PD')
    ['MNI152Lin', 'MNI152NLin2009cAsym', 'MNI152NLin2009cSym', 'MNIInfant', 'MNIPediatricAsym']

    """
    return sorted(TF_LAYOUT.get_templates(**kwargs))


def get_metadata(template):
    """
    Fetch one file from one template.

    Parameters
    ----------
    template : str
        A template identifier (e.g., ``MNI152NLin2009cAsym``).

    Examples
    --------
    >>> get_metadata('MNI152Lin')['Name']
    'Linear ICBM Average Brain (ICBM152) Stereotaxic Registration Model'

    """

    tf_home = Path(TF_LAYOUT.root)
    filepath = tf_home / ("tpl-%s" % template) / "template_description.json"

    # Ensure that template is installed and file is available
    if not filepath.is_file():
        _datalad_get(filepath)
    return loads(filepath.read_text())


def get_citations(template, bibtex=False):
    """
    Fetch template citations

    Parameters
    ----------
    template : :obj:`str`
        A template identifier (e.g., ``MNI152NLin2009cAsym``).
    bibtex : :obj:`bool`, optional
        Generate citations in BibTeX format.

    """
    data = get_metadata(template)
    refs = data.get("ReferencesAndLinks", [])
    if isinstance(refs, dict):
        refs = [x for x in refs.values()]

    if not bibtex:
        return refs

    return [_to_bibtex(ref, template, idx).rstrip() for idx, ref in enumerate(refs, 1)]


def _datalad_get(filepath):
    if not filepath:
        return

    from datalad import api
    from datalad.support.exceptions import IncompleteResultsError

    try:
        api.get(str(filepath))
    except IncompleteResultsError as exc:
        if exc.failed[0]["message"] == "path not associated with any dataset":
            from .conf import TF_GITHUB_SOURCE

            api.install(path=TF_LAYOUT.root, source=TF_GITHUB_SOURCE, recursive=True)
            api.get(str(filepath))
        else:
            raise


def _s3_get(filepath):
    from sys import stderr
    from tqdm import tqdm
    import requests

    path = str(filepath.relative_to(TF_LAYOUT.root))
    url = "%s/%s" % (TF_S3_ROOT, path)

    print("Downloading %s" % url, file=stderr)
    # Streaming, so we can iterate over the response.
    r = requests.get(url, stream=True)

    # Total size in bytes.
    total_size = int(r.headers.get("content-length", 0))
    block_size = 1024
    wrote = 0
    if not filepath.is_file():
        filepath.unlink()

    with filepath.open("wb") as f:
        with tqdm(total=total_size, unit="B", unit_scale=True) as t:
            for data in r.iter_content(block_size):
                wrote = wrote + len(data)
                f.write(data)
                t.update(len(data))

    if total_size != 0 and wrote != total_size:
        raise RuntimeError("ERROR, something went wrong")


def _to_bibtex(doi, template, idx):
    try:
        from doi2bib.crossref import get_bib_from_doi
    except ImportError:
        print(
            "Cannot generate BibTeX citation, missing doi2bib dependency",
            file=sys.stderr,
        )
        return doi

    if "doi.org" not in doi:
        return doi
    bib = get_bib_from_doi(doi)[1]
    # replace identifier with template name
    m = re.search(r"([A-Z])\w+", bib)
    return bib.replace(m.group(), "%s%s" % (template.lower(), idx))
