DataLad
=======
The *TemplateFlow* Archive is an infrastructure reliant on DataLad.
Therefore, it is possible (and recommended for those who want to
leverage the power of DataLad) to access the Archive using just
DataLad.

Installing the Archive
----------------------
The archive is indexed by a superdataset, which can be installed with::

  $ datalad install -r https://github.com/templateflow/templateflow.git

or just::

  $ datalad install -r ///templateflow

Please note the ``-r`` modifier, which will automatically install all the
subdatasets.
In this case, subdatasets (sub-folders) are the individual templates
(signified by the ``tpl-`` prefix).
If the operation finished successfully, you should be able to change directories
into templateflow and see something like::

  $ cd templateflow/
  $ ls -lh
  total 76K
  -rw-rw-r--  1 oesteban oesteban  122 Sep  8 10:42 dataset_description.json
  drwxrwxr-x  4 oesteban oesteban 4.0K Sep  8 10:43 tpl-fsaverage
  drwxrwxr-x  5 oesteban oesteban 4.0K Sep  8 10:43 tpl-fsLR
  drwxrwxr-x  5 oesteban oesteban 4.0K Sep  8 10:42 tpl-MNI152Lin
  drwxrwxr-x  5 oesteban oesteban  16K Sep  8 10:42 tpl-MNI152NLin2009cAsym
  drwxrwxr-x  5 oesteban oesteban 4.0K Sep  8 10:42 tpl-MNI152NLin2009cSym
  drwxrwxr-x  5 oesteban oesteban  12K Sep  8 10:42 tpl-MNI152NLin6Asym
  drwxrwxr-x  5 oesteban oesteban 4.0K Sep  8 10:42 tpl-MNI152NLin6Sym
  drwxrwxr-x 16 oesteban oesteban 4.0K Sep  8 10:43 tpl-MNIInfant
  drwxrwxr-x 11 oesteban oesteban 4.0K Sep  8 10:43 tpl-MNIPediatricAsym
  drwxrwxr-x  5 oesteban oesteban 4.0K Sep  8 10:43 tpl-NKI
  drwxrwxr-x  4 oesteban oesteban 4.0K Sep  8 10:43 tpl-OASIS30ANTs
  drwxrwxr-x  4 oesteban oesteban 4.0K Sep  8 10:43 tpl-PNC
  drwxrwxr-x  5 oesteban oesteban 4.0K Sep  8 10:43 tpl-WHS

.. important ::

   The DataLad install operation DOES NOT download the data.
   Please see how to get the data below.

Accessing templates
-------------------
Before going ahead, make sure you understand how DataLad works.
Once the TemplateFlow superdataset has been installed, as well as all or
some of the subdatasets, it is possible to access data.
For example, pulling down all T1-weighted NIfTI images of all datasets
would look like::

  $ find . -name "*_T1w.nii.gz" -exec datalad get {} +

Let's unpack what happened.
DataLad (or more precisely, the *git-annex* working under the hood)
replaces large files with symbolic links which point to files that
permit the location of the actual resource.
This technique ("annexing" to git) permits keeping the actual files
outside the version control system that (unless set up with some
special extension such as LFS) is not adequate to track large data
files.
Because annexed files are indeed in the file tree, it is possible to
search with tools like ``find`` or ``tree``::

  $ tree tpl-MNI152Lin
  tpl-MNI152Lin
  ├── CHANGES
  ├── LICENSE
  ├── scripts
  │   ├── headmask.py
  │   ├── normalize.py
  │   └── sanitize.py
  ├── template_description.json
  ├── tpl-MNI152Lin_res-01_desc-brain_mask.nii.gz -> .git/annex/objects/J4/J9/URL-s131839--https&c%%files.osf.io%v1%resourc-4a92beb360af57cc397642c99e4f34ee/URL-s131839--https&c%%files.osf.io%v1%resourc-4a92beb360af57cc397642c99e4f34ee
  ├── tpl-MNI152Lin_res-01_desc-head_mask.nii.gz -> .git/annex/objects/j3/Jw/URL-s168509--https&c%%files.osf.io%v1%resourc-2e366aff039e485ce73875dd1fc912fd/URL-s168509--https&c%%files.osf.io%v1%resourc-2e366aff039e485ce73875dd1fc912fd
  ├── tpl-MNI152Lin_res-01_PD.nii.gz -> .git/annex/objects/5m/4z/URL-s10250635--https&c%%files.osf.io%v1%resourc-d38cc6938c26e9389a1a9acf03f5a4b6/URL-s10250635--https&c%%files.osf.io%v1%resourc-d38cc6938c26e9389a1a9acf03f5a4b6
  ├── tpl-MNI152Lin_res-01_T1w.nii.gz -> .git/annex/objects/pM/Fm/URL-s10669511--https&c%%files.osf.io%v1%resourc-2e59511114a1686f937e0127af887b83/URL-s10669511--https&c%%files.osf.io%v1%resourc-2e59511114a1686f937e0127af887b83
  ├── tpl-MNI152Lin_res-01_T2w.nii.gz -> .git/annex/objects/63/jK/URL-s10096230--https&c%%files.osf.io%v1%resourc-7ee9c493542a55d96d28d55d57a3ee52/URL-s10096230--https&c%%files.osf.io%v1%resourc-7ee9c493542a55d96d28d55d57a3ee52
  ├── tpl-MNI152Lin_res-02_desc-brain_mask.nii.gz -> .git/annex/objects/vj/pW/URL-s25649--https&c%%files.osf.io%v1%resourc-ebe0f869bd33c9dd7d983a73f7704326/URL-s25649--https&c%%files.osf.io%v1%resourc-ebe0f869bd33c9dd7d983a73f7704326
  ├── tpl-MNI152Lin_res-02_desc-head_mask.nii.gz -> .git/annex/objects/7q/gF/URL-s32857--https&c%%files.osf.io%v1%resourc-4c79972ef82dfaa9070522b558a8411c/URL-s32857--https&c%%files.osf.io%v1%resourc-4c79972ef82dfaa9070522b558a8411c
  ├── tpl-MNI152Lin_res-02_PD.nii.gz -> .git/annex/objects/1m/jq/URL-s1411464--https&c%%files.osf.io%v1%resourc-95c7dabef32603e9f1d4f3f9cb92b800/URL-s1411464--https&c%%files.osf.io%v1%resourc-95c7dabef32603e9f1d4f3f9cb92b800
  ├── tpl-MNI152Lin_res-02_T1w.nii.gz -> .git/annex/objects/Wf/Fx/URL-s1448817--https&c%%files.osf.io%v1%resourc-2ba5a81206dff8bbf84fb319ed1d7201/URL-s1448817--https&c%%files.osf.io%v1%resourc-2ba5a81206dff8bbf84fb319ed1d7201
  └── tpl-MNI152Lin_res-02_T2w.nii.gz -> .git/annex/objects/X8/Fv/URL-s1375781--https&c%%files.osf.io%v1%resourc-6f1f3ad0441ef1200307a70b32b4f303/URL-s1375781--https&c%%files.osf.io%v1%resourc-6f1f3ad0441ef1200307a70b32b4f303
  
  1 directory, 16 files

If your terminal has advanced coloring, you will also see that only the two
links ending with ``_T1w.nii.gz`` are not "broken" links.
This is because we did ``datalad get`` on both of them in the previous step.
DataLad only pulls the actual file objects when they are requested.
