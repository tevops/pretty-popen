import setuptools

from src import PrettyPopen

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pretty_popen',
    version='0.0.1',
    author='tevops',
    author_email='tevos.matevosyan@gmail.com',
    description='sketch ',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/tevops/pretty-popen',
    project_urls={
        "Bug Tracker": "https://github.com/tevops/pretty-popen/issues"
    },
    license='MIT',
    packages=['toolbox'],
    install_requires=['PyYAML==6.0',
                      'setuptools==58.0.4']
)


