#!/usr/local/bin/python3
from setuptools import setup, find_packages

setup(
    name = "AdAnalytics",
    version = "0.1",
    packages = find_packages(),
    install_requires=open('./requirements.txt').read(),
    author = "Alexander Pushin",
    author_email = "private@apushin.com",
    entry_points={
        'console_scripts': [
            'run = src:run',
            'test_all = src.tests:test_all',
        ],
    },
    include_package_data=True,
)