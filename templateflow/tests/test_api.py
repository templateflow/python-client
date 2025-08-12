# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
#
# Copyright 2024 The NiPreps Developers <nipreps@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# We support and encourage derived works from this project, please read
# about our expectations at
#
#     https://www.nipreps.org/community/licensing/
#
"""Test citations."""

import pytest

from templateflow import api


class Bibtex:
    def __init__(self, bibtex):
        self.text = bibtex
        self.url_only = False
        self.etype = None
        self.citekey = None
        self.pairs = {}

        # DOI could not be converted
        if self.text.startswith('http'):
            self.url_only = True
        else:
            self._parse_bibtex()

    def _parse_bibtex(self):
        import re

        try:
            self.etype = re.search(r'@(\w+)', self.text).group(1)
        except AttributeError as err:
            raise TypeError(f'Invalid bibtex: {self.text}') from err
        try:
            self.citekey = re.search(r'@[^{]*{([^,\s]+)', self.text).group(1)
        except AttributeError as err:
            raise TypeError(f'Invalid bibtex: {self.text}') from err
        self.pairs = dict(re.findall(r'(\w+)=(\{[^{}]+\})', self.text))

    def get(self, val):
        return self.pairs.get(val)

    def __str__(self):
        return self.text

    def __repr__(self):
        return (
            f'@{self.etype}{{{self.citekey}, '
            f'{", ".join([f"{key} = {val}" for key, val in self.pairs.items()])}}}'
        )

    def __eq__(self, other):
        if isinstance(other, Bibtex):
            if self.url_only and self.text == other.text:
                return True
            if (
                self.etype == other.etype
                and self.citekey == other.citekey
                and self.pairs == other.pairs
            ):
                return True
        return False

    def assert_same(self, other):
        """Convenience method to find deviations between two Bibtex objects"""
        assert isinstance(other, Bibtex)
        assert self.etype == other.etype, 'Mismatched entry types'
        assert self.citekey == other.citekey, 'Mismatched citekeys'
        for key in self.pairs.keys():
            assert key in other.pairs, f'Key ({key}) missing from other'
            assert self.pairs[key] == other.pairs[key], (
                f'Key ({key}) mismatched\n\n{self.pairs[key]}\n\n{other.pairs[key]}'
            )

        for key in other.pairs.keys():
            assert key in self.pairs, f'Key ({key}) missing from pairs'

        assert self.pairs == other.pairs, 'Dictionaries do not match'


# test setup to avoid cluttering pytest parameterize
mni2009_urls = [
    'https://doi.org/10.1016/j.neuroimage.2010.07.033',
    'https://doi.org/10.1016/S1053-8119(09)70884-5',
    'http://nist.mni.mcgill.ca/?p=904',
    'https://doi.org/10.1007/3-540-48714-X_16',
]

mni2009_fbib = """\
@article{Fonov_2011,
DOI={10.1016/j.neuroimage.2010.07.033},
url={https://doi.org/10.1016/j.neuroimage.2010.07.033},
year={2011},
publisher={Elsevier BV},
ISSN={1053-8119},
volume={54},
number={1},
pages={313–327},
author={Fonov, Vladimir and Evans, Alan C. and Botteron, Kelly and Almli, C. Robert \
and McKinstry, Robert C. and Collins, D. Louis},
title={Unbiased average age-appropriate atlases for pediatric studies},
journal={NeuroImage}
}"""

mni2009_lbib = """\
@inbook{Collins_1999,
DOI={10.1007/3-540-48714-x_16},
url={https://doi.org/10.1007/3-540-48714-X_16},
year={1999},
publisher={Springer Berlin Heidelberg},
pages={210–223},
ISBN={9783540487142},
ISSN={0302-9743}
author={Collins, D. Louis and Zijdenbos, Alex P. and Baaré, Wim F. C. and Evans, Alan C.},
title={ANIMAL+INSECT: Improved Cortical Structure Segmentation},
booktitle={Information Processing in Medical Imaging}
}"""

fslr_urls = [
    'https://doi.org/10.1093/cercor/bhr291',
    'https://github.com/Washington-University/HCPpipelines/tree/master/global/templates',
]

fslr_fbib = """\
@article{Van_Essen_2011,
DOI={10.1093/cercor/bhr291},
ISSN={1460-2199},
url={https://doi.org/10.1093/cercor/bhr291},
year={2011},
publisher={Oxford University Press (OUP)},
volume={22},
number={10},
pages={2241–2262},
author={Van Essen, D. C. and Glasser, M. F. and Dierker, D. L. and Harwell, J. and Coalson, T.},
title={Parcellations and Hemispheric Asymmetries of Human Cerebral Cortex Analyzed on \
Surface-Based Atlases},
journal={Cerebral Cortex}
}"""

fslr_lbib = 'https://github.com/Washington-University/HCPpipelines/tree/master/global/templates'

fsaverage_fbib = """\
@article{Fischl_1999,
DOI={10.1002/(sici)1097-0193(1999)8:4<272::aid-hbm10>3.0.co;2-4},
ISSN={1097-0193},
url={https://doi.org/10.1002/(sici)1097-0193(1999)8:4<272::aid-hbm10>3.0.co;2-4},
year={1999},
publisher={Wiley},
volume={8},
number={4},
pages={272–284},
author={Fischl, Bruce and Sereno, Martin I. and Tootell, Roger B.H. and Dale, Anders M.},
title={High-resolution intersubject averaging and a coordinate system for the cortical surface},
journal={Human Brain Mapping}
}"""


@pytest.mark.parametrize(
    ('template', 'urls', 'fbib', 'lbib'),
    [
        ('MNI152NLin2009cAsym', mni2009_urls, mni2009_fbib, mni2009_lbib),
        ('fsLR', fslr_urls, fslr_fbib, fslr_lbib),
        (
            'fsaverage',
            ['https://doi.org/10.1002/(sici)1097-0193(1999)8:4%3C272::aid-hbm10%3E3.0.co;2-4'],
            fsaverage_fbib,
            None,
        ),
    ],
)
def test_citations(tmp_path, template, urls, fbib, lbib):
    """Check the correct composition of citations."""
    assert api.get_citations(template) == urls
    bibs = api.get_citations(template, bibtex=True)
    if bibs:
        bib0 = Bibtex(bibs[0])
        exp0 = Bibtex(fbib)
        assert bib0 == exp0
        if lbib is not None:
            bib1 = Bibtex(bibs[-1])
            exp1 = Bibtex(lbib)
            assert bib1 == exp1
        else:
            assert len(bibs) == 1

    else:
        pytest.fail('no citations currently')


def test_pybids_magic_get():
    """Check automatic entity expansion of the layout."""
    assert sorted(api.ls_atlases()) == sorted(api.TF_LAYOUT.get_atlases())
    assert sorted(api.ls_atlases(template='MNI152NLin6ASym')) == sorted(
        api.TF_LAYOUT.get_atlases(template='MNI152NLin6ASym')
    )

    with pytest.raises(TypeError):
        api.ls_atlases('MNI152NLin6ASym')

    # Existing layout.get_* should not be bubbled to the layout
    # (that means, raise an AttributeError instead of a BIDSEntityError)
    with pytest.raises(AttributeError):
        _ = api.get_fieldmap
