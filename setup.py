#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" templateflow setup script """
from setuptools.command.install import install
from setuptools.command.develop import develop


def make_cmdclass(basecmd):
    """Decorate setuptools commands."""
    base_run = basecmd.run

    def new_run(self):
        from templateflow.conf import update_home
        update_home()
        base_run(self)

    basecmd.run = new_run
    return basecmd


@make_cmdclass
class CheckHomeDevCommand(develop):
    pass

@make_cmdclass
class CheckHomeProdCommand(install):
    pass


if __name__ == '__main__':
    """ Install entry-point """
    from setuptools import setup, find_packages
    from versioneer import get_cmdclass, get_version

    from templateflow.__about__ import (
        __packagename__,
        __author__,
        __email__,
        __maintainer__,
        __license__,
        __description__,
        __longdesc__,
        __url__,
        DOWNLOAD_URL,
        CLASSIFIERS,
        REQUIRES,
        SETUP_REQUIRES,
        LINKS_REQUIRES,
        TESTS_REQUIRES,
        EXTRA_REQUIRES,
    )

    setup(
        name=__packagename__,
        version=get_version(),
        description=__description__,
        long_description=__longdesc__,
        author=__author__,
        author_email=__email__,
        maintainer=__maintainer__,
        maintainer_email=__email__,
        license=__license__,
        url=__url__,
        download_url=DOWNLOAD_URL,
        classifiers=CLASSIFIERS,
        packages=find_packages(exclude=['*.tests']),
        zip_safe=False,
        # Dependencies handling
        setup_requires=SETUP_REQUIRES,
        install_requires=list(set(REQUIRES)),
        dependency_links=LINKS_REQUIRES,
        tests_require=TESTS_REQUIRES,
        extras_require=EXTRA_REQUIRES,
        # Data
        include_package_data=True,
        package_data={__packagename__: [
            'conf/config.json',
            'conf/templateflow-skel.zip'
        ]},
        cmdclass=get_cmdclass(cmdclass={
            'develop': CheckHomeDevCommand,
            'install': CheckHomeProdCommand,
        }),
    )
