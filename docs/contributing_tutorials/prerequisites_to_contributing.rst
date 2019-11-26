
Prerequisites to contributing templates to TemplateFlow
############################################################

Who is this tutorial for?
=================================

Have a template that you would like to see on TemplateFlow? Great!
Contributions are welcome.
This document goes through some of the prerequisites needed to submit a template.
Once you have these prerequisites achieved.

Are you allowed to share the template?
==========================================

Templates have a licence which specifies the terms that they can be shared.
TemplateFlow can only include templates that allow for redistribution.
It is okay if the template requires attribution, but you need to make sure to add the attribution information.

What type of contribution are you making?
============================================

There are three different types of contributions you can make to TemplateFlow.

**A new template space**.
This contribution involves adding a new space that does not currently exist.
Let us say you have made a new pediatric space that you transform your images to; this would be a new template space.
All the different MNI templates are each considered their own template space.
Currently this requires writing permissions to the TemplateFlow repo.
For now, if you do not have access open up an issue in the templateflow repo to say which template spaces should be added.

**Nifti images within an existing template space**.
This contribution involves adding to a template space that currently exists.
An example of this would be adding a nifti file that is an atlas.
You need to know which template space your atlas is in (Note: there are multiple MNI spaces).

**Meta information**.
This contribution involves additional information about existing templates.
These will generally be in .json or .tsv files.
There are also transform files which help translate between templates.

There are tutorials for each of these three different types of contributions.

Prerequisites for uploading nifti files
=====================================================

Aside from typical requirements (python3, git, pip), some prerequisites need addressing before you can upload a template (i.e. any image file).

1. Getting access to the OSF repository. Create an issue stating you would like to access to the OSF repo. You need an account at: `osf.io <https://osf.io>`_
2. Download the OSF client: ``pip install osfclient``.
3. Install `DataLad <https://www.datalad.org>`_. See the `installation page <https://www.datalad.org/get_DataLad.html>`_ for more details.
4. You also need TemplateFlows DataLad/osf tools. To install these type in a terminal: ``pip install git+https://github.com/TemplateFlow/DataLad-osf``.

After installing these tools, you are ready to upload a template.

If you only plan to contribute metadata (e.g. json files and tsv files), then these three steps are not needed.

Initializing the TemplateFlow OSF directory
==================================================

Once you have the prerequisites set up, you can initialize the OSF directory onto your computer.

In a new directory type:

.. code-clock:: bash
    
    osf init

This will prompt you for your username and TemplateFlow project number.
This project number is ``ue5gx``.

You can check that your directory has been correctly set up by typing:

.. code-clock:: bash

    osf ls

You should see the contents of the OSF project folder appear in the console.
