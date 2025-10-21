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

Managing client configuration
-----------------------------
The ``templateflow`` CLI transparently manipulates the same cache configuration used
by :class:`templateflow.client.TemplateFlowClient`.  Running ``templateflow config``
exposes the options stored in the underlying :class:`templateflow.conf.cache.CacheConfig`
instance::

        $ templateflow config show
        TEMPLATEFLOW_HOME=/home/user/.cache/templateflow
        TEMPLATEFLOW_USE_DATALAD=0
        TEMPLATEFLOW_AUTOUPDATE=1
        TEMPLATEFLOW_GET_TIMEOUT=10

Changing a value updates the cached client configuration immediately. For example,
enabling the DataLad backend is equivalent to instantiating a client with
``TemplateFlowClient(use_datalad=True)`` because the command mutates the
``CacheConfig`` object used by the global client::

        $ templateflow config set TEMPLATEFLOW_USE_DATALAD 1
        Updated TEMPLATEFLOW_USE_DATALAD → 1 (DataLad downloads will be used on next access)

When the CLI is invoked afterwards, the cache will be re-initialized using
``use_datalad=True`` without requiring any additional Python code.  The same
mechanism applies to paths (``TEMPLATEFLOW_HOME``), origins, and timeout
settings provided via ``templateflow config``.

Updating an existing cache
--------------------------
The :mod:`templateflow.conf` module exposes an ``update`` helper that the CLI
mirrors through ``templateflow update``.  Executing the command instructs the
underlying :class:`templateflow.conf.cache.TemplateFlowCache` instance to refresh
its content using the currently selected backend::

        $ templateflow update --silent
        Cache mode: S3
        Cache root: /home/user/.cache/templateflow
        TemplateFlow cache is up to date

If ``TEMPLATEFLOW_USE_DATALAD`` (or ``--use-datalad``) is enabled, the command
delegates to :class:`templateflow.conf.cache.DataladManager` and performs a
recursive ``datalad update``.  Otherwise the S3 manager fetches new or changed
files while keeping existing downloads intact.

Wiping the cache
----------------
The ``templateflow wipe`` command is a thin wrapper around
:meth:`templateflow.conf.cache.TemplateFlowCache.wipe`.  It clears the local cache
and invalidates the in-memory layout so that subsequent ``templateflow`` CLI
calls or new :class:`templateflow.client.TemplateFlowClient` instances trigger a clean re-install::

        $ templateflow wipe
        Removing cache at /home/user/.cache/templateflow …
        Cache cleared; next access will reinstall the archive

In DataLad mode the wipe operation reports that no deletion occurs because
``TemplateFlowCache`` delegates to :class:`~templateflow.conf.cache.DataladManager`,
preserving the working tree.  This makes it safe to toggle between backends via
``templateflow config`` without unintentionally removing a managed repository.
