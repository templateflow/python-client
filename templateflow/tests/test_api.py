import pytest

from .. import api


# test setup to avoid cluttering pytest parameterize
mni2009_urls = [
    'https://doi.org/10.1016/j.neuroimage.2010.07.033',
    'https://doi.org/10.1016/S1053-8119(09)70884-5',
    'http://nist.mni.mcgill.ca/?p=904',
    'https://doi.org/10.1007/3-540-48714-X_16'
]

mni2009_fbib = (
    '@article{mni152nlin2009casym1,\n'
    '\tdoi = {10.1016/j.neuroimage.2010.07.033},\n'
    '\turl = {https://doi.org/10.1016%2Fj.neuroimage.2010.07.033},\n'
    '\tyear = 2011,\n'
    '\tmonth = {jan},\n'
    '\tpublisher = {Elsevier {BV}},\n'
    '\tvolume = {54},\n'
    '\tnumber = {1},\n'
    '\tpages = {313--327},\n'
    '\tauthor = {Vladimir Fonov and Alan C. Evans and Kelly Botteron and C. '
    'Robert Almli and Robert C. McKinstry and D. Louis Collins},\n'
    '\ttitle = {Unbiased average age-appropriate atlases for pediatric studies},\n'
    '\tjournal = {{NeuroImage}}\n}'
)

mni2009_lbib = (
    '@incollection{mni152nlin2009casym4,\n'
    '\tdoi = {10.1007/3-540-48714-x_16},\n'
    '\turl = {https://doi.org/10.1007%2F3-540-48714-x_16},\n'
    '\tyear = 1999,\n'
    '\tpublisher = {Springer Berlin Heidelberg},\n'
    '\tpages = {210--223},\n'
    '\tauthor = {D. Louis Collins and Alex P. Zijdenbos and Wim F. C. '
    "Baar{\\'{e}} and Alan C. Evans},\n"
    '\ttitle = {{ANIMAL}$\\mathplus${INSECT}: Improved Cortical Structure '
    'Segmentation},\n'
    '\tbooktitle = {Lecture Notes in Computer Science}\n}'
 )

fslr_urls = [
    'https://doi.org/10.1093/cercor/bhr291',
    'https://github.com/Washington-University/HCPpipelines/tree/master/global/templates'
]

fslr_fbib = (
    '@article{fslr1,\n'
    '\tdoi = {10.1093/cercor/bhr291},\n'
    '\turl = {https://doi.org/10.1093%2Fcercor%2Fbhr291},\n'
    '\tyear = 2011,\n'
    '\tmonth = {nov},\n'
    '\tpublisher = {Oxford University Press ({OUP})},\n'
    '\tvolume = {22},\n'
    '\tnumber = {10},\n'
    '\tpages = {2241--2262},\n'
    '\tauthor = {D. C. Van Essen and M. F. Glasser and D. L. Dierker and J. '
    'Harwell and T. Coalson},\n'
    '\ttitle = {Parcellations and Hemispheric Asymmetries of Human Cerebral '
    'Cortex Analyzed on Surface-Based Atlases},\n'
    '\tjournal = {Cerebral Cortex}\n}'
)

fslr_lbib = 'https://github.com/Washington-University/HCPpipelines/tree/master/global/templates'


@pytest.mark.parametrize('template,urls,fbib,lbib', [
    ('MNI152NLin2009cAsym', mni2009_urls, mni2009_fbib, mni2009_lbib),
    ('fsLR', fslr_urls, fslr_fbib, fslr_lbib),
    ('fsaverage', [], None, None)
])
def test_citations(tmp_path, template, urls, fbib, lbib):
    assert api.get_citations(template) == urls
    bibs = api.get_citations(template, bibtex=True)
    if bibs:
        assert bibs[0] == fbib
        assert bibs[-1] == lbib
    else:
        # no citations currently
        assert template == 'fsaverage'
