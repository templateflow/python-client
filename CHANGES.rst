24.2.0 (March 18, 2024)
=======================
Minor release including a new command line interface for the Client.

* ENH: Add a command line interface (#123)
* MAINT: Update *DataLad*'s pinned version (#128)
* MAINT: Revise failing *Pypi* deployment and ``twine check`` (#127)
* MAINT: Generate a requirements file with ``test`` dependencies (#125)
* MAINT: Add codespell and make it fix some typos (#121)
* MAINT: Revise code style according to ruff (#124)
* MAINT: Add license header in all Python files (#122)
* MAINT: Migrate to hatchling packaging (#120)
* MAINT: Run ruff and address some issues (#119)
* MAINT: Finalize migration of package build to PEP517/8 (#117)

24.1.0 (March 15, 2024)
=======================
Minor release updating *PyBIDS*'s configuration to enable new entities
that allow the selection of recently added *FreeSurfer*'s surface parcellations in
`templateflow/tpl-fsaverage#5 <https://github.com/templateflow/tpl-fsaverage/pull/5>`__.

* ENH: Add `seg-<label>` and `scale-<number>` entities (#114)

24.0.0 (March 4, 2024)
======================
Minor release to update skeleton to include recently added templates.

* CI: Add manual trigger, bump action versions (#113)

23.1.0 (October 12, 2023)
=========================
Minor release including support for Python 3.12.

Python 3.7 support has been removed.

* FIX: Use Path.as_posix() and f-strings to build correct URLs on Windows (#107)
* MNT: Python 3.12 support, drop Python 3.7 and pkg_resources (#109)

23.0.0 (February 2, 2023)
=========================
Minor release including additional API features and an updated skeleton.

* FIX: Preempt ``BIDSLayout`` from indexing dot-folders (#99)
* ENH: Make sure existing ``layout.get_*`` are not bubbled in (#102)
* ENH: Allow access to PyBIDS' magic ``get_*`` (#101)
* ENH: Add an ``api.ls()`` function to list (without getting) files (#97)
* MAINT: Discontinue legacy docker runners of CircleCI (#104)
* MAINT: Rotate CircleCI secrets and setup up org-level context (#103)
* MAINT: Fix docs build environment in CircleCI (#96)

0.8.1 (May 7, 2022)
===================
Patch release updating the S3 skeleton to include the fixed version of ``tpl-MouseIn``.

0.8.0 (March 31, 2022)
======================
Minor release including the feedback received through peer-review of the preprint.
Please note that this release is supported by Python +3.7.

* FIX: Normalize extensions for leading dot & update doctests to new resources (#92)
* ENH: Add a ``wipe()`` utility to clear up the cache (#91)
* DOC: Update notebooks submodule (#94)
* MAINT: Drop Python 3.6 (#93)

0.7.2 (November 16, 2021)
=========================
Patch release with a substantially documentation update, as well as usage improvements.
Additionally, new surface meshes were added for the `fsLR` template.

* DOC: Substantial update and re-structuring to the documentation (#77) (#79)
* FIX: layout is ``None`` when PyBIDS not correctly installed (#72)
* FIX: Drop ``doi2bib`` and query doi.org directly (#76)
* MAINT: Pin ``setuptools >=45``, new dependency as of ``setuptools_scm>=6.0.1`` (#73)

0.7.1 (December 9, 2020)
========================
Patch release with improvements to the template fetching experience.
With thanks to Lea Waller for the contribution.

* FIX: Use ``BIDSLayoutIndexer`` when initiating ``BIDSLayout`` (#61)
* FIX: Display correct units when downloading templates (#63)
* FIX: GitHub Actions build (#64)
* ENH: Add option to raise exception on empty ``get`` queries (#57)
* ENH: Ensure templates layout is re-indexed when updated (#59)

0.7.0 - Withdrawn
=================
Release 0.7.0 was withdrawn because of inconsistencies in deployment.

0.6.3 (July 06, 2020)
=====================
Patch release including an updated PyBIDS configuration file for the PyBIDS 0.11.x series.

* FIX: Include leading dots in extensions (#56)

0.6.2 (May 09, 2020)
====================
Patch release including some minimal improvements to package building and CI.

* MAINT: Some additional distribution improvements (#51)


0.6.1 (May 09, 2020)
====================
Patch release to generate and distribute wheels.

* MAINT: Run ``black`` (#50)
* MAINT: Distribute wheel + Revise CI framework (#49)


0.6.0 (May 1st, 2020)
=====================
Minor release in preparation of a new CalVer versioning following the lead of *fMRIPrep*.
This release contains a fair amount of maintenance work to ensure synchronicity with the TemplateFlow Archive (https://github.com/templateflow/templateflow). These maintenance actions drive the development towards establishing a peer-reviewed, lightweight template submission protocol. The release includes an update mechanism, enabling users of the *S3-backed mode of operation* (default) to update their local Archive structure without reinstalling the client. This feature is enabled by default on import time, to disable it make sure you export ``TEMPLATEFLOW_AUTOUPDATE=off``.
With thanks to Yarik for a datalad-related bug-fix.
With thanks to V. Fonov for contributing with the new ``tpl-MNI152NLin2009cSym``.

* FIX: Provide path to the dataset as ``dataset`` argument (#48)
* ENH: Run an automatic S3-skeleton update on import by default (#45)
* ENH: Update the internal index of *TemplateFlow* (#40)
* ENH: Automatic generation of template citations (#35)
* MAINT: Set-up a GitHub action to test installation alternatives (see #23).
* MAINT: Migrate to ``setuptools_scm`` (#42)
* MAINT: Run ``black`` on the whole tree (#41)
* MAINT: Transfer the burden of keeping the S3-skeleton updated over to the archive (#39)

0.5.2 (March 20, 2020)
======================
Patch release in the 0.5 series, adding a soft brainmask for numerical stability in
floating-point rounding of atlas-based brain-extraction methods using the
``MNI152NLin2009cAsym`` template.

0.5.1 (March 20, 2020)
======================
Patch of the new 0.5.x series, including a `new rodent template
<https://github.com/templateflow/tpl-WHS/tree/eee3069910cdaa2a4a7e2f880485ad0e67f031d3>`__
and file fixes for ``fsaverage`` and ``fsLR`` templates.
With thanks to E. MacNicol for contributing the new ``tpl-WHS``.

* MAINT: Drop Python 3.5 (#36)

0.5.0 (March 12, 2020)
======================
This release has been removed and should not be used.

Version 0.4.2 (January 28, 2020)
================================
Patch release including a bugfix, adding a DataLad pin, and making PyBIDS pin more flexible.

  * MAINT: Update PyBIDS pin and DataLad pin
  * FIX: Density key (#31)

Version 0.4.1 (July 22, 2019)
=============================
First release after a deep revision of the tests and the continuous integration setup.
Also includes minor reliability improvements over the previous release and some bugfixes.

* MAINT: Testing Automatically update CHANGES after merge (51988f8) (#27)
* MAINT: Enable code coverage collection (#25)
* MAINT: Switch to a ``setup.cfg``-style of installation (#24)
* FIX: Check and update ``$HOME`` if needed with every installation (#20)
* FIX: Do not merge branches into master when pushing back skell (#19)
* FIX: Commit newly generated S3 skeletons back to repo (#17)
* FIX: Add ``extension`` entity for selection (#16) @effigies

Version 0.4.0 (July 9, 2019)
============================
* MAINT: Use PyBIDS 0.9.x (#15) @effigies

Version 0.3.0 (June 4, 2019)
============================
* ENH: Add ``MNIInfant`` template.

Version 0.2.0 (June 4, 2019)
============================
* ENH: Added ``MNIPediatricAsym`` template.
* ENH: Updated spec to allow several *cohorts* (``cohort-``).

Version 0.1.9 (May 28, 2019)
============================
* ENH: Added the `Schaefer 2018 atlas <https://github.com/ThomasYeoLab/CBIG/tree/master/stable_projects/brain_parcellation/Schaefer2018_LocalGlobal/Parcellations/MNI>`__) to ``MNI152NLin6Asym``.
* ENH: Mapped the Schaefer atlas and the Harvard-Oxford atlas into ``MNI152NLin2009cAsym``.

Version 0.1.8 (May 9, 2019)
===========================
* ENH: Added FSL's Harvard-Oxford template to ``MNI152NLin6Asym``.

Version 0.1.7 (April 3, 2019)
=============================
* ENH: New release including bugfixes for ``MNI152NLin2009cAsym`` (particularly https://github.com/templateflow/tpl-MNI152NLin2009cAsym/commit/6e6d5915c7d8055d4af5efbf5e5457a0ab3246b9)

Version 0.1.6 (March 29, 2019)
==============================
* ENH: Finish adding ``MNI152NLin6Sym`` after curation of NIfTI volumes and exporting to S3.

Version 0.1.5 (March 29, 2019)
==============================
* ENH: Add volumetric data to the ``fsLR`` template.
* ENH: Rename the segmentation of subcortical structures to be consistent with the new files.

Version 0.1.4 (March 28, 2019)
==============================
* ENH: New release to include the new ``MNI152NLin6Asym`` template (the default MNI template of FSL).

Version 0.1.3 (March 14, 2019)
==============================
* FIX: Update TemplateFlow skeleton to include ``tpl-fsaverage/tpl-fsaverage_dseg.tsv``, after TemplateFlow update.

Version 0.1.2 (March 12, 2019)
==============================
* FIX: ``api.get`` - robuster fetcher algorithm (allows S3 download on DL repos) and better error messages (#10)

Version 0.1.1 (March 12, 2019)
==============================
* FIX: Require environment variable to use DataLad (#8)

Version 0.1.0.post1 (March 05, 2019)
====================================
* ENH: Testing a better ``.zenodo.json`` settings.

Version 0.1.0 (March 05, 2019)
==============================
* ENH: First minimally functional TemplateFlow client release.

Version 0.0.5.post1 (March 04, 2019)
====================================
Hotfix release to retrieve correct version when pip installed.

* MAINT: Add a ``.zenodo.json`` file.

Version 0.0.5 (March 04, 2019)
==============================
* ENH: Datalad-free alternative for TemplateFlow (#7)
* ENH: Use a BIDSLayout to index TemplateFlow (#6)

Version 0.0.4 (January 18, 2019)
================================
* ENH: Add a ``get_metadata`` utility

Version 0.0.3 (January 16, 2019)
================================
* ENH: Add ``api.templates()`` + one doctest

Version 0.0.2 (January 16, 2019)
================================
* ENH: Add one doctest

Version 0.0.1 (January 16, 2019)
================================
* ENH: First functional release
