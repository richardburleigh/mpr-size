import os

import pkg_resources
from setuptools import setup, find_packages

setup(
    name="mprsize",
    py_modules=["mprsize"],
    version="0.1",
    description="A simple Python tool to extract object sizes from Mendix MPR files and export them into Excel reports.",
    author="Richard Burleigh <richard.burleigh@mendix.com>",
    packages=find_packages(),
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
        )
    ],
    entry_points = {
        'console_scripts': ['mprsize=mprsize.analyzer:cli'],
    },
    include_package_data=True
)