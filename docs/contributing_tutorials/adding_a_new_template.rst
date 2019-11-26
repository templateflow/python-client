Creating a new template space
###############################################

Who is this tutorial for
============================

First, this is intended for those wishing to add templates to TemplateFlow.
Second, this is for people who want to add a template directory that does not already exists.
TemplateFlow consists of multiple templates sorted by the space the template is in.
This tutorial tells you how to add a new template space.

If the space for you template already exists, then you should follow the tutorial: :ref: `uploading_to_existing_templates`.

This tutorial assumes you have done all the steps in the preceding tutorial: :ref: `prerequisites_to_contributing`.

__Note__ at present, this tutorial will require writing access to the TemplateFlow repo.
If you do not have access here, it may be best to open up an issue asking for a template space to be created.

Big picture
===============

Image files (e.g. nifti files) are hosted on OSF and linked to Github.

You will need to publish the directory to OSF and create a link to it to Github.
This link can be done with DataLad, DataLad tracks a dataset and only downloads files when they are needed.
You can read more about DataLad [`Link <FIXLINK>`_].

Step 1: create a new dataset
=============================

First make sure you are in your local templateflow directory.
If you do not have a local templateflow copy, run:

::.
    git clone https://github.com/templateflow/templateflow/
    cd templateflow

Now set the variable ``TEMPLATENAME`` to whatever your template will be called.
Also set your Github username to the variable ``GITHUBUSERNAME``.
Finally, write a description of your template.

::.
    TEMPALTENAME='tpl-test'
    GITHUBUSERNAME='yourusername'
    TEMPALTEDESCRIPTION="This is a test template"
    GITHUBREPO='templateflow'

At the moment, always keep templateflow as GITHUBREPO, this may be changed in the future 

With these variables set you can then run the following code with no modifications:

::.
    datalad create -d . -D "$TEMPALTEDESCRIPTION" $TEMPALTENAME
    cd $TEMPALTENAME
    datalad create-sibling-github --github-organization $GITHUBREPO --github-login $GITHUBUSERNAME --access-protocol ssh $TEMPALTENAME
    cd ..
    sed -i -e "s/url = .\/$TEMPALTENAME/url = https:\/\/github.com\/$GITHUBREPO\/$TEMPLATENAME/g" .gitmodules
    datalad save -m "set the github repo url for new template ``$TEMPLATENAME``"
    datalad publish

You will be asked to enter your github username and password while running this code.

Explanation of above code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After running, this code will create an empty datalad folder called ``tpl-test`` (or whatever TEMPLATENAME is set to).
It will then change into that directory, upload the template to github.
It will then return to the templateflow directory.

The 5th line in the above code edits the file .gitmodules to replace:

::.
    [submodule "tpl-test"]
            path = tpl-test
            url = ./tpl-test

with:

::.
    [submodule "tpl-test"]
            path = tpl-test
            url = https://github.com/templateflow/tpl-test

I.e. it adds a full url link to the.
The final two lines upload this change.

Step 2: Add a template_description.json
========================================

Within this directory we place a template_description.json which is needed in all templates.
The json file contains the following:

::.
    {
        "Authors": ["Noone"],
        "Acknowledgements": "Curated and added to TemplateFlow by Thompson WH",
        "BIDSVersion": "1.1.0",
        "HowToAcknowledge": "You should not use this template",
        "Identifier": "test",
        "License": "See LICENSE file",
        "Name": "A test template to for testing.",
        "RRID": "SCR_002823",
        "ReferencesAndLinks": [
            "Link to article if there is one"],
        "TemplateFlowVersion": "1.0.0",
        "res": {
            "01": {
            "origin": [-91.0, -126.0, -72.0],
            "shape": [182, 218, 182],
            "zooms": [1.0, 1.0, 1.0]
            }
        }
    }

Add all the necessary information into the .json file.
Then open a pull request on github to submit this information.
