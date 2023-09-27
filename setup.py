#-*-*- encoding: utf-8 -*-*-
import os
import platform
import subprocess
from collections import OrderedDict

from setuptools import setup, Command,  find_packages
from setuptools.command.sdist import sdist
from setuptools.command.install import install

classifiers=[
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.9",
]

cp_license="BSD 2-Clause license"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='ll-oscilloscope-measurements',
      version='0.1.1',
      description="",
      long_description=long_description,
      long_description_content_type="text/markdown",
      project_urls=OrderedDict((
            ('Code', 'https://github.com/labsland/ll-oscilloscope-measurements'),
            ('Issue tracker', 'https://github.com/labsland/ll-oscilloscope-measurements/issues'),
      )),
      classifiers=classifiers,
      author='LabsLand',
      author_email='dev@labsland.com',
      url='https://github.com/labsland/ll-oscilloscope-measurements/',
      license=cp_license,
      py_modules=['ll_oscilloscope_measurements'],
      install_requires=['numpy', 'scipy'],
      extra_requires={
          'test': ['pytest']
      }
)

