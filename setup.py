from setuptools import setup

setup(name='amcrest',
      version='1.0.0',
      description='Python wrapper implementation for Amcrest cameras.',
      author='Douglas Schilling Landgraf, Marcelo Moreira de Mello',
      author_email='dougsland@gmail.com, tchello.mello@gmail.com',
      url='http://github.com/tchellomello/python-amcrest',
      license='GPLv2',
      install_requires=['requests'],
      packages=['src'],
      keywords="amcrest camera python",
      zip_safe=True)
