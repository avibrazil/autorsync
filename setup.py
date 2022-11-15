#!/usr/bin/env python

import distutils
import setuptools
from autorsync import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()





distutils.core.setup(
    name                    = "autorsync",
    version                 = __version__,

    python_requires         = '>=3.0',
    install_requires        = ['jinja2','pyyaml'],
    packages                = setuptools.find_packages(),
    scripts                 = ['scripts/autorsync'],

    description             = "Automate execution of various rsync commands based " +
                              "on profiles defined on a YAML configuration file",
    long_description        = long_description,
    long_description_content_type = "text/markdown",

    author                  = "Avi Alkalay",
    author_email            = "avi@unix.sh",
    url                     = "https://github.com/avibrazil/autorsync",

    classifiers             = [
                                "Programming Language :: Python :: 3",
                                "Operating System :: OS Independent",
                                "Development Status :: 4 - Beta",
                                "Environment :: MacOS X",
                                "Environment :: Console",
                                "Environment :: Linux",
                                "Intended Audience :: Sysadmins",
                                "Intended Audience :: End Users/Desktop",
                                "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
                                "Operating System :: MacOS",
                                "Operating System :: iOS",
                                "Operating System :: Microsoft :: Windows",
                                "Operating System :: POSIX",
                                "Operating System :: Unix",
                                "Topic :: System :: Archiving :: Backup",
                                "Topic :: System :: Recovery Tools"
    ],
)
