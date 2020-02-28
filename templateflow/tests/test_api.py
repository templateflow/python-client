from .. import api


def test_citations(tmp_path):
    cits = api.get_citations('MNI152NLin2009cAsym')
    assert cits == [
        'https://doi.org/10.1016/j.neuroimage.2010.07.033',
        'https://doi.org/10.1016/S1053-8119(09)70884-5'
    ]

    bibs = api.get_citations('MNI152NLin2009cAsym', bibtex=True)
    assert bibs == """\
@article{Fonov_2011,\n\tdoi = {10.1016/j.neuroimage.2010.07.033},\
\n\turl = {https://doi.org/10.1016%2Fj.neuroimage.2010.07.033},\
\n\tyear = 2011,\n\tmonth = {jan},\n\tpublisher = {Elsevier {BV}},\
\n\tvolume = {54},\n\tnumber = {1},\n\tpages = {313--327},\
\n\tauthor = {Vladimir Fonov and Alan C. Evans and Kelly Botteron \
and C. Robert Almli and Robert C. McKinstry and D. Louis Collins},\
\n\ttitle = {Unbiased average age-appropriate atlases for pediatric studies},\
\n\tjournal = {{NeuroImage}}\n}\n\
@article{Fonov_2009,\n\tdoi = {10.1016/s1053-8119(09)70884-5},\
\n\turl = {https://doi.org/10.1016%2Fs1053-8119%2809%2970884-5},\
\n\tyear = 2009,\n\tmonth = {jul},\n\tpublisher = {Elsevier {BV}},\
\n\tvolume = {47},\n\tpages = {S102},\
\n\tauthor = {VS Fonov and AC Evans and RC McKinstry and CR Almli and DL Collins},\
\n\ttitle = {Unbiased nonlinear average age-appropriate brain templates from birth to adulthood},\
\n\tjournal = {{NeuroImage}}\n}"""

    assert api.get_citations('fsaverage') is None
