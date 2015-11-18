#!/usr/bin/python3
from setuptools import setup, find_packages

setup(
        name = "gitmagic",
        version = "0.1",
        packages = find_packages(),
        scripts = ['git-magic-fixup'],
        install_requires = ['GitPython>=1.0.1'],
        )
