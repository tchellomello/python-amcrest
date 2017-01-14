#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='amcrest',
      version='1.1.0',
      description='Python wrapper implementation for Amcrest cameras.',
      author='Douglas Schilling Landgraf, Marcelo Moreira de Mello',
      author_email='dougsland@gmail.com, tchello.mello@gmail.com',
      url='http://github.com/tchellomello/python-amcrest',
      license='GPLv2',
      install_requires=['requests', 'argcomplete'],
      package_dir={'': 'src'},
      packages=find_packages('src'),
      include_package_data=True,
      scripts=['cli/amcrest-cli'],
      keywords="amcrest camera python",
      zip_safe=True)
