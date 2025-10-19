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
"""Extending pyBIDS for querying TemplateFlow."""

from acres import Loader
from bids.layout import BIDSLayout, add_config_paths

load_data = Loader(__spec__.parent)

add_config_paths(templateflow=load_data('config.json'))


class Layout(BIDSLayout):
    def __repr__(self):
        # A tidy summary of key properties
        s = """\
TemplateFlow Layout
 - Home: {}
 - Templates: {}.""".format(self.root, ', '.join(sorted(self.get_templates())))
        return s
