#!/usr/bin/python3
from setuptools import setup, find_packages

setup(
        name = "gitmagic",
        version = "0.1",
        packages = find_packages(),
        description = 'All the magical things that git misses.',
        scripts = ['git-magic-fixup'],
        install_requires = ['GitPython>=1.0.1'],
        url = 'https://github.com/peterhajdu/gitmagic',
        maintainer = 'Peter Hajdu',
        maintainer_email = 'peter.ferenc.hajdu@gmail.com',
        download_url = 'https://github.com/peterhajdu/gitmagic/tarball/0.1',
        keywords = ['git', 'magic', 'fixup'],
        )