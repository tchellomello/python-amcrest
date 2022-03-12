#!/usr/bin/env python
from setuptools import setup, find_packages


def readme():
    with open("README.rst") as desc:
        return desc.read()


setup(
    name="amcrest",
    version="1.9.5",
    description="Python wrapper implementation for Amcrest cameras.",
    long_description=readme(),
    author="Douglas Schilling Landgraf, Marcelo Moreira de Mello",
    author_email="dougsland@gmail.com, tchello.mello@gmail.com",
    url="http://github.com/tchellomello/python-amcrest",
    license="GPLv2",
    install_requires=[
        "argcomplete",
        "httpx",
        "requests",
        "typing_extensions",
        "urllib3",
    ],
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    package_data={"amcrest": ["py.typed"]},
    test_suite="tests",
    scripts=["cli/amcrest-cli", "tui/amcrest-tui"],
    zip_safe=True,
    keywords="amcrest camera python",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
