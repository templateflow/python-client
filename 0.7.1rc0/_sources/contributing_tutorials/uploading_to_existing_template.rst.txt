.. _upload-to-existing:

Uploading files to an existing template space
=============================================

.. admonition :: Who is this tutorial for?

    First, this is intended for those wishing to upload templates to TemplateFlow.
    Second, this is for people who want to add to a template directory that already exists.
    TemplateFlow consists of multiple templates sorted by the space the template is in.
    If the space for you template does not exist, then you should follow :ref:`adding-new-template`.
    This tutorial assumes you have done all the steps in the preceding tutorial:
    :ref:`prerequisites-contributing`.

Big picture
~~~~~~~~~~~
Image files (e.g. NIfTI files) are hosted on OSF.
All other information (e.g. TSV, JSON files) will be hosted on github as regular files.

When you use TemplateFlow, the images are only downloaded when they are needed.
This can be done with DataLad, DataLad tracks a dataset and only downloads files when they are needed.
You can read more about DataLad `here <https://www.datalad.org>`__.

Thus, when uploading to an existing template, there are two different steps:

1. You need to place them on the OSF server.
2. you need to tell DataLad about the new items so the Github repo can track the new files.

Step 1: Placing the template on the OSF server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Go to the TemplateFlow directory you previously initialized.
Place the file you want to upload in directory and give them appropriate .

Let us say you want to upload:
`tpl-test/tpl-test_atlas-test1_dseg.nii.gz`, `tpl-test/tpl-test_atlas-test2_dseg.nii.gz`.

.. code-block:: bash

    export OSF_PASSWORD='<some-password>'
    osf upload tpl-test_atlas-test1_dseg.nii.gz tpl-test_atlas-test1_dseg.nii.gz

If you are overwriting an existing image, use the -f flag.

If you want to upload multiple images (let us say we have multiple atlases), use a for bash loop:

.. code-block:: bash

    ls tpl-test/*_atlas-test*_dseg.nii.gz | parallel -j8 'osf upload {} {}'

And this will iteratively upload all instances of the atlas to OSF.

Step 2: Telling DataLad where the files are
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Github is using DataLad to track the files.
You need to tell DataLad where the new files are.

To do this, run the following python script, changing the tqo required variables:

.. code-block:: python

    from pathlib import Path
    from datalad_osf.utils import url_from_key, json_from_url,
                                  get_osf_recursive, osf_to_csv

    ## VARIABLES THAT NEED TO BE CHANGED

    # THe template you are adding too
    subset = 'tpl-test'
    # A string that identifies your new nifit files
    # Leave as blank if you want all files added
    strinfile = 'atlas-test'

    ## OPTIONAL VARIABLES

    # Name of output file
    output_filename = 'new_files.csv'
    # templateflow project name
    key = 'ue5gx'

    ## Rest of script

    toplevel = json_from_url(url_from_key(key))
    for folder in toplevel['data']:
        if folder['attributes']['name'] == subset:
            url = folder['links']['move']
            break

    data = json_from_url(url)
    hits = ['name,link']
    for item in data['data']:
        name = item['attributes']['name']
        ext = ''.join(Path(name).suffixes)
        if strinfile in name and '.nii' in ext:
            print(item)
            link = item['links']['download']
            path = item['attributes']['materialized']
            hits.append(','.join((name, link)))
    Path(output_filename).write_text('\n'.join(hits))

Either run this script interactively or save the script as a python file (e.g. 'get_datalad_urls.py')
then run the file with `python get_datalad_urls.py`.

Note, the above script assumes there are no subdirectories within the template folder.
See end of tutorial for an example script when there are subdirectories within the template folder.

This script will produce a file called new_files.csv.

Finally, the contents of new_files.csv need to be uploaded via DataLad.

To do this first, move the local image file into a tmp folder.

.. code-block:: bash

    mv tpl-test/*_atlas-test*.nii.gz ~/tmp/

Then you add the new urls to DataLad. Add a message

.. code-block:: bash

    datalad addurls new_files.csv '{link}' '{name}' --message 'My test atlases'
    datalad publish

Example script when subdirectories are present
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from pathlib import Path
    from datalad_osf.utils import url_from_key, json_from_url, get_osf_recursive, osf_to_csv

    ## VARIABLES THAT NEED TO BE CHANGED

    # THe template you are adding too
    subset = 'tpl-test'
    # A string that identifies your new files
    strinfile = 'atlas-test'

    ## OPTIONAL VARIABLES

    # Name of output file
    output_filename = 'new_files.csv'
    # templateflow project name
    key = 'ue5gx'

    ## REST OF SCRIPT

    toplevel = json_from_url(url_from_key(key))
    for folder in toplevel['data']:
        if folder['attributes']['name'] == subset:
            url = folder['links']['move']
            break

    data = json_from_url(url)
    hits = ['name,link']
    for item in data['data']:
        if item['attributes']['kind'] == 'folder':
            subdata = json_from_url(item['links']['move'])
            for subitem in subdata['data']:
                if subitem['attributes']['kind'] == 'file':
                    name = subitem['attributes']['name']
                    ext = ''.join(Path(name).suffixes)
                    if strinfile in name and '.nii' in ext:
                        print(name)
                        link = subitem['links']['download']
                        path = subitem['attributes']['materialized']
                        hits.append(','.join((name, link)))
    Path(output_filename).write_text('\n'.join(hits))
