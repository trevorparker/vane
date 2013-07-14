import sys
import os
import vane
from distutils.core import setup

setup(
    name=vane.__title__,
    version=vane.__version__,
    author=vane.__author__,
    author_email='trevor@trevorparker.com',
    package_dir={'vane': 'vane'},
    packages=['vane'],
    scripts=['bin/weather-now'],
    url='https://github.com/trevorparker/vane',
    license=vane.__license__,
    description='Simple weather utilities in Python',
    install_requires=['requests']
)
