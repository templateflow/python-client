# A Python client to query TemplateFlow

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2583289.svg)](https://doi.org/10.5281/zenodo.2583289)
[![CircleCI](https://circleci.com/gh/templateflow/python-client/tree/master.svg?style=shield)](https://circleci.com/gh/templateflow/python-client/tree/master)
[![Build Status](https://travis-ci.org/templateflow/python-client.svg?branch=master)](https://travis-ci.org/templateflow/python-client)
[![Pypi](https://img.shields.io/pypi/v/templateflow.svg)](https://pypi.python.org/pypi/templateflow/)

Group inference and reporting of neuroimaging studies require that individual's
features are spatially aligned into a common frame where their location can be
called standard.
To that end, a multiplicity of brain templates with anatomical annotations
(i.e., atlases) have been published.
However, a centralized resource that allows programmatic access to templates is
lacking.
TemplateFlow is a modular, version-controlled resource that allows researchers
to use templates "off-the-shelf" and share new ones.