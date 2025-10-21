templateflow.client module
==========================

The client module provides the object-oriented entry point around the global
cache described in :mod:`templateflow.conf`.  Its documentation surfaces the
constructor, cache descriptor, and convenience methods so that downstream code
can migrate from the module-level API to the richer class interface.

.. automodule:: templateflow.client
   :members: TemplateFlowClient
   :undoc-members:
   :member-order: bysource

.. autoclass:: templateflow.client.TemplateFlowClient
   :members:
   :special-members: __init__, __repr__
   :member-order: bysource
   :show-inheritance:
