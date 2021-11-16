"""Test citations."""
import pytest

from .. import api


# test setup to avoid cluttering pytest parameterize
mni2009_urls = [
    "https://doi.org/10.1016/j.neuroimage.2010.07.033",
    "https://doi.org/10.1016/S1053-8119(09)70884-5",
    "http://nist.mni.mcgill.ca/?p=904",
    "https://doi.org/10.1007/3-540-48714-X_16",
]

mni2009_fbib = """\
@article{Fonov_2011,
\tdoi = {10.1016/j.neuroimage.2010.07.033},
\turl = {https://doi.org/10.1016%2Fj.neuroimage.2010.07.033},
\tyear = 2011,
\tmonth = {jan},
\tpublisher = {Elsevier {BV}},
\tvolume = {54},
\tnumber = {1},
\tpages = {313--327},
\tauthor = {Vladimir Fonov and Alan C. Evans and Kelly Botteron and C. Robert \
Almli and Robert C. McKinstry and D. Louis Collins},
\ttitle = {Unbiased average age-appropriate atlases for pediatric studies},
\tjournal = {{NeuroImage}}
}"""

mni2009_lbib = """\
@incollection{Collins_1999,
\tdoi = {10.1007/3-540-48714-x_16},
\turl = {https://doi.org/10.1007%2F3-540-48714-x_16},
\tyear = 1999,
\tpublisher = {Springer Berlin Heidelberg},
\tpages = {210--223},
\tauthor = {D. Louis Collins and Alex P. Zijdenbos and Wim F. C. Baar{\\'{e}} and Alan C. Evans},
\ttitle = {{ANIMAL}$\\mathplus${INSECT}: Improved Cortical Structure Segmentation},
\tbooktitle = {Lecture Notes in Computer Science}
}"""

fslr_urls = [
    "https://doi.org/10.1093/cercor/bhr291",
    "https://github.com/Washington-University/HCPpipelines/tree/master/global/templates",
]

fslr_fbib = """\
@article{Van_Essen_2011,
\tdoi = {10.1093/cercor/bhr291},
\turl = {https://doi.org/10.1093%2Fcercor%2Fbhr291},
\tyear = 2011,
\tmonth = {nov},
\tpublisher = {Oxford University Press ({OUP})},
\tvolume = {22},
\tnumber = {10},
\tpages = {2241--2262},
\tauthor = {D. C. Van Essen and M. F. Glasser and D. L. Dierker and J. Harwell and T. Coalson},
\ttitle = {Parcellations and Hemispheric Asymmetries of Human Cerebral Cortex Analyzed on \
Surface-Based Atlases},
\tjournal = {Cerebral Cortex}
}"""

fslr_lbib = (
    "https://github.com/Washington-University/HCPpipelines/tree/master/global/templates"
)


@pytest.mark.parametrize(
    "template,urls,fbib,lbib",
    [
        ("MNI152NLin2009cAsym", mni2009_urls, mni2009_fbib, mni2009_lbib),
        ("fsLR", fslr_urls, fslr_fbib, fslr_lbib),
        ("fsaverage", [], None, None),
    ],
)
def test_citations(tmp_path, template, urls, fbib, lbib):
    """Check the correct composition of citations."""
    assert api.get_citations(template) == urls
    bibs = api.get_citations(template, bibtex=True)
    if bibs:
        assert "".join(bibs[0]) == fbib
        assert "".join(bibs[-1]) == lbib
    else:
        # no citations currently
        assert template == "fsaverage"
