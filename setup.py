#!/usr/bin/env python3
import setuptools
from __version__ import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pretty_popen',
    version=__version__,
    author='tevops',
    package_dir={'': 'src'},
    author_email='tevos.matevosyan@gmail.com',
    description='Popen made pretty',
    packages=setuptools.find_namespace_packages(where='src'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/tevops/pretty-popen',
    project_urls={
        "Bug Tracker": "https://github.com/tevops/pretty-popen/issues"
    },
    install_requires=['setuptools'],
    license='MIT'
)
