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

fsaverage_fbib = """\
@article{Fischl_1999,
\tdoi = {10.1002/(sici)1097-0193(1999)8:4<272::aid-hbm10>3.0.co;2-4},
\turl = {https://doi.org/10.1002%2F%28sici%291097-0193%281999%298%3A4%3C272%3A%3Aaid-hbm10%3E3.0.co%3B2-4},
\tyear = 1999,
\tpublisher = {Wiley},
\tvolume = {8},
\tnumber = {4},
\tpages = {272--284},
\tauthor = {Bruce Fischl and Martin I. Sereno and Roger B.H. Tootell and Anders M. Dale},
\ttitle = {High-resolution intersubject averaging and a coordinate system for the cortical surface},
\tjournal = {Human Brain Mapping}
}"""

@pytest.mark.parametrize(
    "template,urls,fbib,lbib",
    [
        ("MNI152NLin2009cAsym", mni2009_urls, mni2009_fbib, mni2009_lbib),
        ("fsLR", fslr_urls, fslr_fbib, fslr_lbib),
        ("fsaverage", ["https://doi.org/10.1002/(sici)1097-0193(1999)8:4%3C272::aid-hbm10%3E3.0.co;2-4"], fsaverage_fbib, None),
    ],
)
def test_citations(tmp_path, template, urls, fbib, lbib):
    """Check the correct composition of citations."""
    assert api.get_citations(template) == urls
    bibs = api.get_citations(template, bibtex=True)
    if bibs:
        assert "".join(bibs[0]) == fbib
        assert len(bibs) == 1 if lbib is None else "".join(bibs[-1]) == lbib
    else:
        # no citations currently
        assert False


def test_pybids_magic_get():
    """Check automatic entity expansion of the layout."""
    assert sorted(api.ls_atlases()) == sorted(api.TF_LAYOUT.get_atlases())
    assert sorted(api.ls_atlases(template="MNI152NLin6ASym")) == sorted(
        api.TF_LAYOUT.get_atlases(template="MNI152NLin6ASym")
    )

    with pytest.raises(TypeError):
        api.ls_atlases("MNI152NLin6ASym")
