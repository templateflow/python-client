
TemplateFlow Naming
===================

.. admonition :: Who is this tutorial for?

	Anyone trying to understand the naming structure in TemplateFlow.

Naming information
~~~~~~~~~~~~~~~~~~
TemplateFlow generally follows the `BIDS naming structure <https://bids-specification.readthedocs.io/en/derivatives/>`__, but has a few deviations (e.g. the ``tpl`` key).
Here we outline the most common names that are found in TemplateFlow.

Common key names using in TemplateFlow:

=====  =====
Key    Description
=====  =====
tpl    The space of the template.
res    Resolution index. See ``template_description.json`` within each template for more information about what the index specifies.
atlas  Name of an atlas.
desc   Additional information about the file to differentiate it from other files.
=====  =====

Common suffixes used in TemplateFlow:

=======    ============
Suffix     Description
=======    ============
dseg       discrete segmentation
pseg       probability segmentation
mask       binary mask
xfm        transform file
T2w        T2 weighted image
T1w        T1 weighted image
=======    ============

Common file-formats used in TemplateFlow:

==========   =======
Extension    Description
==========   =======
.nii.gz      Image
.tsv         Tabular information
.json        Meta-information
.h5          Transform file
==========   =======

Thus a template with the following name: ``tpl-test_res-01_atlas-myatlas_desc-200nodes_dseg.nii.gz``
would be a NIfTI image containing discrete segmentation of "myatlas" which contains 200nodes.
And it is in the template space "test".
The resolution information will be found in the dataset_description.json file under '01'.
