#!/usr/bin/env python
"""Templateflow's setup script."""
import sys
from setuptools import setup


# Give setuptools a hint to complain if it's too old a version
# 30.3.0 allows us to put most metadata in setup.cfg
# Should match pyproject.toml
# setuptools >= 34.4 required by setuptools_scm
# 40.8.0 includes license_file, reducing MANIFEST.in requirements
#
# To install, 34.4.0 is enough, but if we're building an sdist, require 40.8.0
# This imposes a stricter rule on the maintainer than the user
# Keep the installation version synchronized with pyproject.toml
SETUP_REQUIRES = ['setuptools >= %s' % ("40.8.0" if "sdist" in sys.argv else "34.4")]
SETUP_REQUIRES += ["setuptools_scm >= 3.4", "toml"]
# This enables setuptools to install wheel on-the-fly
SETUP_REQUIRES += ["wheel"] if "bdist_wheel" in sys.argv else []

if __name__ == "__main__":
    """ Install entry-point """
    setup(
        name="templateflow", setup_requires=SETUP_REQUIRES,
    )
