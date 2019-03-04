#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" templateflow setup script """


def main():
    """ Install entry-point """
    from os import path as op
    from inspect import getfile, currentframe
    from setuptools import setup, find_packages
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

    pkg_data = {'templateflow': [
        'conf/config.json',
        'conf/templateflow-skel.zip'
    ]}

    root_dir = op.dirname(op.abspath(getfile(currentframe())))
    version = None
    cmdclass = {}
    if op.isfile(op.join(root_dir, __packagename__, 'VERSION')):
        with open(op.join(root_dir, __packagename__, 'VERSION')) as vfile:
            version = vfile.readline().strip()
        pkg_data[__packagename__].insert(0, 'VERSION')

    if version is None:
        import versioneer
        version = versioneer.get_version()
        cmdclass = versioneer.get_cmdclass()

    setup(
        name=__packagename__,
        version=version,
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
        package_data=pkg_data,
        include_package_data=True,
        cmdclass=cmdclass,
    )


if __name__ == '__main__':
    main()
