from setuptools import setup, find_packages

setup(
    name="sfdata",
    version='0.4.1',
    url="https://github.com/paulscherrerinstitute/sf_datafiles",
    description="SwissFEL Data Files",
    author="Paul Scherrer Institute",
    packages=find_packages(),
    py_modules=["sfdstats"]
)


