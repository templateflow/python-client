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
