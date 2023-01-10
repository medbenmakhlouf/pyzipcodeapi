from codecs import open
from os import path

from setuptools import find_packages, setup

__version__ = "2.0.0"

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pyzipcodeapi",
    version=__version__,
    description="Py ZipCodeApi will make it easier for you to use the different options in ZipCodeAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/medbenmakhlouf/pyzipcodeapi",
    download_url="https://github.com/medbenmakhlouf/pyzipcodeapi/tarball/" + __version__,
    license="BSD",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
    ],
    keywords=["api", "zipcode"],
    packages=find_packages(exclude=["docs", "tests*"]),
    include_package_data=True,
    author="Mohamed Ben Makhlouf",
    author_email="med.b.makhlouf@gmail.com",
)
