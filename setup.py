# -*- coding: utf-8 -*-
"""
setup.py
"""

import re

from setuptools import find_packages, setup

with open("kompozit/kompozit.py", encoding="utf-8") as file:
    REGEX_VERSION = r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]'
    version = re.search(REGEX_VERSION, file.read(), re.MULTILINE).group(1)  # type: ignore[union-attr]

with open("README.md", encoding="utf-8") as file:
    readme = file.read()

setup(
    name="kompozit",
    version=version,
    packages=find_packages(),
    description="Declarative Configuration Management Tool for Docker Compose.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="veerendra2",
    author_email="vk.tyk23@simplelogin.com",
    url="https://github.com/veerendra2/kompozit",
    download_url=f"https://github.com/veerendra2/kompozit/archive/{version}.tar.gz",
    project_urls={
        "Documentation": "https://veerendra2.gitbook.io/kompozit",
    },
    keywords=["gitops", "cicd", "docker-compose", "configuration management"],
    license="Apache License",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Utilities",
    ],
    install_requires=[
        "deepmerge==2.0",
        "jsonpatch==1.33",
        "PyYAML==6.0.3",
    ],
    python_requires=">=3.9",
    entry_points={"console_scripts": ["kompozit = kompozit.kompozit:main"]},
)
