templateflow.conf package
=========================

``templateflow.conf`` centralizes configuration state for both the legacy module
level helpers (``update``/``wipe``) and the newer :class:`~templateflow.conf.cache.TemplateFlowCache`
object.  The documentation below highlights the migration path so that users can
incrementally adopt the cache classes without losing backwards-compatible entry
points.

.. automodule:: templateflow.conf
   :members: requires_layout, setup_home, update, wipe
   :imported-members:
   :member-order: bysource

Cache management classes
------------------------

.. automodule:: templateflow.conf.cache
   :members: CacheConfig, TemplateFlowCache, S3Manager, DataladManager
   :special-members: __init__
   :undoc-members:
   :member-order: bysource
