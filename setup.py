#!/usr/bin/env python
"""Templateflow's setup script."""
import sys
from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop

# Give setuptools a hint to complain if it's too old a version
# 30.3.0 allows us to put most metadata in setup.cfg
# Should match pyproject.toml
SETUP_REQUIRES = ["setuptools >= 42.0", "setuptools_scm >= 3.4", "toml"]
# This enables setuptools to install wheel on-the-fly
SETUP_REQUIRES += ["wheel"] if "bdist_wheel" in sys.argv else []


def make_cmdclass(basecmd):
    """Decorate setuptools commands."""
    base_run = basecmd.run

    def new_run(self):
        from templateflow.conf import setup_home

        setup_home()
        base_run(self)

    basecmd.run = new_run
    return basecmd


@make_cmdclass
class CheckHomeDevCommand(develop):
    pass


@make_cmdclass
class CheckHomeProdCommand(install):
    pass


if __name__ == "__main__":
    """ Install entry-point """
    setup(
        name="templateflow",
        setup_requires=SETUP_REQUIRES,
        cmdclass={"develop": CheckHomeDevCommand, "install": CheckHomeProdCommand},
    )
