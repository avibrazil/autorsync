#!/usr/bin/env python

import distutils
import setuptools
from autorsync import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()





distutils.core.setup(
    name                    = "auto_remote_sync",
    version                 = __version__,

    python_requires         = '>=3.6',
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
                                "Development Status :: 5 - Production/Stable",
                                "Environment :: MacOS X",
                                "Environment :: Win32 (MS Windows)",
                                "Environment :: Console",
                                "Intended Audience :: System Administrators",
                                "Intended Audience :: End Users/Desktop",
                                "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
                                "Operating System :: MacOS",
                                "Operating System :: Microsoft :: Windows",
                                "Operating System :: POSIX",
                                "Operating System :: Unix",
                                "Topic :: System :: Archiving :: Backup",
                                "Topic :: System :: Recovery Tools"
    ],
)
