#!/usr/bin/env python
"""Templateflow's setup script."""
import sys
from setuptools import setup


# Give setuptools a hint to complain if it's too old a version
# 30.3.0 allows us to put most metadata in setup.cfg
# Should match pyproject.toml
SETUP_REQUIRES = [
    "setuptools >= 42.0",
    "setuptools_scm >= 3.4",
    "setuptools_scm_git_archive",
    "toml",
]
# This enables setuptools to install wheel on-the-fly
SETUP_REQUIRES += ["wheel"] if "bdist_wheel" in sys.argv else []

if __name__ == "__main__":
    """ Install entry-point """
    setup(
        name="templateflow",
        setup_requires=SETUP_REQUIRES,
    )
