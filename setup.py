"""Installation script for 'fuzzy_fuss' package.

Disclaimer
----------
This script has been prepared following the instructions from:
https://packaging.python.org/tutorials/packaging-projects/
(as of 29.09.2019).
"""


import setuptools


setuptools.setup(
    name="fuzzy_fuss",
    version="0.0.1",
    author="Dominika Dlugosz",
    author_email="dominika.a.m.dlugosz@gmail.com",
    description="Little fuzzy logic toolbox",
    packages=['fuzzy_fuss'],
    python_requires='>=3.6',
    install_requires=['numpy>=1.16', 'matplotlib']
)
