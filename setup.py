#!/usr/bin/python3
from setuptools import setup, find_packages

setup(
        name = "gitmagic",
        version = "0.3",
        packages = find_packages(),
        description = 'All the magical things that git misses.',
        scripts = ['git-magic-fixup'],
        install_requires = ['GitPython>=1.0.1'],
        url = 'https://github.com/balabit/git-magic',
        maintainer = 'Peter Hajdu',
        maintainer_email = 'peter.ferenc.hajdu@gmail.com',
        download_url = 'https://github.com/balabit/git-magic/tarball/0.3',
        keywords = ['git', 'magic', 'fixup'],
        )
