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
``TemplateFlowClient`` is the central entry point for configuring how the
archive is cached and updated.  Each constructor argument mirrors an
environment variable (when available) and exposes its live value through the
metadata descriptors defined in :mod:`templateflow.conf`.

.. list-table:: ``TemplateFlowClient`` configuration
   :header-rows: 1

   * - Argument
     - Environment variable
     - Default
     - Metadata descriptor
   * - ``root``
     - ``TEMPLATEFLOW_HOME``
     - ``platformdirs.user_cache_dir('templateflow')`` (e.g., ``~/.cache/templateflow``)
     - ``templateflow.conf.TF_HOME``
   * - ``use_datalad``
     - ``TEMPLATEFLOW_USE_DATALAD``
     - ``False`` (automatically disabled if DataLad is not installed)
     - ``templateflow.conf.TF_USE_DATALAD``
   * - ``autoupdate``
     - ``TEMPLATEFLOW_AUTOUPDATE``
     - ``True``
     - ``templateflow.conf.TF_AUTOUPDATE``
   * - ``timeout``
     - *(none)*
     - ``10`` seconds
     - ``templateflow.conf.TF_GET_TIMEOUT``
   * - ``origin`` (DataLad)
     - *(none)*
     - ``https://github.com/templateflow/templateflow.git``
     - ``templateflow.conf.TF_GITHUB_SOURCE``
   * - ``s3_root`` (direct download)
     - *(none)*
     - ``https://templateflow.s3.amazonaws.com``
     - ``templateflow.conf.TF_S3_ROOT``

Cache location
~~~~~~~~~~~~~~
The client stores downloads in a writable cache that defaults to the
platform-specific ``TEMPLATEFLOW_HOME`` directory.  You can point the CLI to a
different location by exporting the environment variable before invoking any
command; the current value is always available through
``templateflow.conf.TF_HOME``.

.. code-block:: console

   $ export TEMPLATEFLOW_HOME=$DATA/.templateflow
   $ templateflow config

.. code-block:: python

   from templateflow.client import TemplateFlowClient

   client = TemplateFlowClient(root="/data/templateflow")
   print(client.cache.config.root)

If you switch between cache locations, wipe the previous cache (``templateflow
wipe`` or :func:`templateflow.conf.wipe`) to avoid mixing S3 and DataLad
layouts.

DataLad mode
~~~~~~~~~~~~
Two backends are available: a lightweight S3 mirror and a DataLad dataset.
Setting ``TEMPLATEFLOW_USE_DATALAD=on`` switches the CLI into DataLad mode
(automatically falling back to S3 if DataLad is missing).  The active backend
can be inspected via ``templateflow.conf.TF_USE_DATALAD``.

.. code-block:: console

   $ export TEMPLATEFLOW_USE_DATALAD=on
   $ templateflow config

.. code-block:: python

   from templateflow.client import TemplateFlowClient

   client = TemplateFlowClient(root="/data/tf-datalad", use_datalad=True)
   client.cache.ensure()
   print(client.cache.config.use_datalad)

When switching from the default S3 mode to DataLad, start with an empty cache
directory (for example by deleting ``$TEMPLATEFLOW_HOME``) so that git-annex can
initialise cleanly.

S3 origins
~~~~~~~~~~
S3-backed installations download assets from the ``s3_root`` mirror referenced
in the configuration.  The CLI always reports the active mirror through the
``templateflow.conf.TF_S3_ROOT`` descriptor.

.. code-block:: console

   $ python - <<'PY'
   from templateflow.conf import TF_S3_ROOT
   print(TF_S3_ROOT)
   PY

.. code-block:: python

   from templateflow.client import TemplateFlowClient

   mirror = TemplateFlowClient(s3_root="https://my-mirror.s3.amazonaws.com")
   print(mirror.cache.config.s3_root)

To use a custom DataLad remote, pass ``origin=...`` when constructing the
client and call :func:`templateflow.conf.update` to refresh the cache metadata.

Autoupdates, timeouts, and cache metadata
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Automatic cache refreshes are controlled by ``autoupdate``.  Disable them for
air-gapped deployments with ``TEMPLATEFLOW_AUTOUPDATE=off`` or by creating the
client with ``autoupdate=False``; the current flag is exported as
``templateflow.conf.TF_AUTOUPDATE``.

Network operations time out after 10 seconds by default.  Provide a different
``timeout`` when constructing ``TemplateFlowClient`` and inspect the value via
``templateflow.conf.TF_GET_TIMEOUT``.

Whenever the cache contents change outside the client (for example, when
switching mirrors or pulling updates with DataLad), rebuild the BIDS layout by
calling :func:`templateflow.conf.update` or ``TemplateFlowClient.cache.update``.
The layout object is exposed as ``templateflow.conf.TF_LAYOUT`` and is
invalidated automatically whenever :func:`templateflow.conf.update` succeeds,
ensuring that new metadata descriptors are reflected in subsequent queries.

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
