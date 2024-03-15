Using the client with the Command-line interface (CLI)
======================================================

.. click:: templateflow.cli:main
  :prog: templateflow
  :nested: full

Examples
--------
Listing all the compressed NIfTI files in ``fsaverage``::

	$ templateflow ls fsaverage -x .nii.gz
	~/.cache/templateflow/tpl-fsaverage/tpl-fsaverage_res-01_den-41k_T1w.nii.gz
	~/.cache/templateflow/tpl-fsaverage/tpl-fsaverage_res-01_desc-brain_mask.nii.gz
	~/.cache/templateflow/tpl-fsaverage/tpl-fsaverage_res-01_T1w.nii.gz
