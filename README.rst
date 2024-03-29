A Python client to query TemplateFlow
=====================================

|Zenodo| |preprint| |CircleCI| |Build Status| |Pypi|

Reference anatomies of the brain and corresponding atlases play a central role in experimental
neuroimaging workflows and are the foundation for reporting standardized results.
The choice of such references —i.e., templates— and atlases is one relevant source of methodological
variability across studies, which has recently been brought to attention as an important challenge
to reproducibility in neuroscience.
*TemplateFlow* is a publicly available framework for human and nonhuman brain models.
The framework combines an open database with software for access, management, and vetting,
allowing scientists to distribute their resources under *FAIR* —findable, accessible, interoperable,
reusable— principles.
*TemplateFlow* supports a multifaceted insight into brains across species, and enables multiverse
analyses testing whether results generalize across standard references, scales, and in the long term,
species, thereby contributing to increasing the reliability of neuroimaging results.

Publishing resources in the *TemplateFlow* Archive
--------------------------------------------------
Please check the `Contributing section of the TemplateFlow website
<https://www.templateflow.org/contributing/submission/>`__.

License information
-------------------
*TemplateFlow* adheres to the 
`general licensing guidelines <https://www.nipreps.org/community/licensing/>`__
of the *NiPreps framework*.

License
~~~~~~~
Copyright (c) 2021, the *NiPreps* Developers.

The *TemplateFlow* Python Client is
licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
`http://www.apache.org/licenses/LICENSE-2.0
<http://www.apache.org/licenses/LICENSE-2.0>`__.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Acknowledgements
----------------
This work is steered and maintained by the `NiPreps Community <https://www.nipreps.org>`__.
The development of this resource was supported by
the Laura and John Arnold Foundation (RAP and KJG),
the NIBIB (R01EB020740, SSG; 1P41EB019936-01A1SSG, YOH),
the NIMH (RF1MH121867, RAP, OE; R24MH114705 and R24MH117179, RAP; 1RF1MH121885 SSG),
NINDS (U01NS103780, RAP), and NSF (CRCNS 1912266, YOH).
OE acknowledges financial support from the SNSF Ambizione project
“*Uncovering the interplay of structure, function, and dynamics of
brain connectivity using MRI*” (grant number 
`PZ00P2_185872 <http://p3.snf.ch/Project-185872>`__).

.. |Zenodo| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.2583289.svg
   :target: https://doi.org/10.5281/zenodo.2583289
.. |CircleCI| image:: https://circleci.com/gh/templateflow/python-client/tree/master.svg?style=shield
   :target: https://circleci.com/gh/templateflow/python-client/tree/master
.. |Build Status| image:: https://github.com/templateflow/python-client/workflows/Python%20package/badge.svg
   :target: https://github.com/templateflow/python-client/actions?query=workflow%3A%22Python+package%22
.. |Pypi| image:: https://img.shields.io/pypi/v/templateflow.svg
   :target: https://pypi.python.org/pypi/templateflow/
.. |preprint| image:: https://img.shields.io/badge/doi-10.1101%2F2021.02.10.430678-blue.svg
   :target: https://doi.org/10.1101/2021.02.10.430678