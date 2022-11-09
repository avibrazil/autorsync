import setuptools
from autorsync import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autorsync",
    version=__version__,
    author="Avi Alkalay",
    author_email="avibrazil@gmail.com",
    description="Automate execution of various rsync commands based on profiles defined on a YAML configuration file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/avibrazil/autorsync",
    install_requires=['jinja2','pyyaml'],
    packages=setuptools.find_packages(),
    classifiers=[
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
    python_requires='>=3.0',
)
