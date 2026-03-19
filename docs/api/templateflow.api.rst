templateflow.api module
=======================

``templateflow.api`` mirrors the long-standing global helpers while delegating
all heavy lifting to a shared :class:`templateflow.client.TemplateFlowClient`
instance.  The directives below document both the public functions and the
proxied client so that migration guides can reference consistent API signatures.

.. automodule:: templateflow.api
   :members: get, ls, templates, get_metadata, get_citations, TemplateFlowClient
   :imported-members:
   :member-order: bysource
