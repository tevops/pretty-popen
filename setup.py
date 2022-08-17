#!/usr/bin/env python3
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as requirements_file:
    packages = requirements_file.read().splitlines()

setuptools.setup(
    name='pretty_popen',
    version='0.0.1',
    author='tevops',
    author_email='tevos.matevosyan@gmail.com',
    description='Popen made pretty',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/tevops/pretty-popen',
    project_urls={
        "Bug Tracker": "https://github.com/tevops/pretty-popen/issues"
    },
    license='MIT',
    packages=packages
)
