Installation
============
*TemplateFlow Client* is distributed via *Pypi* and can easily be installed
within your Python distribution with::

  python -m pip install templateflow

Alternatively, you can install the bleeding-edge version of the software
directly from the GitHub repo with::

  python -m pip install git+https://github.com/templateflow/python-client.git@master

To verify the installation, you can run the following command::

  python -c "import templateflow as tf; print(tf.__version__)"

You should see the version number.

Settings
--------
The *TemplateFlow Client* has two modes of operation: (a) based on
`DataLad <https://datalad.org>`__, or (b) direct downloads from Amazon S3.

By default, the client will operate in direct download mode (b) which is
more lightweight and comes with some limitations, as all the advanced
version control management afforded by DataLad will not be available.

For the most part, and considering that templates/atlases do not substantially
change over time, the direct download mode should be sufficient to anyone
developing new pipelines and tools, as it will provided the latest version
of any available template set.

**TemplateFlow "home" folder**.
The lazy-loading implementation of the client requires some folder on the host
where template resources can be stored (therefore, write permissions are
required). By default, the home folder will be ``$HOME/.cache/templateflow``.
This setting can be overridden by defining the environment variable ``TEMPLATEFLOW_HOME``
before running the client, for example::

  $ export TEMPLATEFLOW_HOME=$DATA/.templateflow

**Configuring the operation mode**.
By default, the client will operate without DataLad (and hence, without version control).
To set up the DataLad mode, make sure DataLad is installed and functioning on your host,
and then::

  $ export TEMPLATEFLOW_USE_DATALAD=on

It is recommended that the ``$TEMPLATEFLOW_HOME`` folder is wiped out before running the
client again, in case the tool has already been operated in direct download mode::

  $ rm -r ${TEMPLATEFLOW_HOME:-$HOME/.cache/templateflow}

**Naming conventions**.
Naming conventions for templates and atlases are available within the
`Contributing section of the TemplateFlow website
<https://www.templateflow.org/contributing/naming/>`__.

Developers
----------
Advanced users and developers who plan to contribute with bugfixes, documentation,
etc. can first clone our Git repository::

  git clone https://github.com/templateflow/python-client.git templateflow

and install the tool in *editable* mode::

  cd templateflow
  python -m pip install -e .
