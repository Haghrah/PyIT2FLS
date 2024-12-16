from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.build_py import build_py
import subprocess
import os


class CustomBuildExt(build_ext):
    def run(self):
        # Run the Makefile to build your C extension
        if not os.path.exists('build'):
            os.makedirs('build')
        subprocess.check_call(['make'])  # Adjust if your Makefile has specific targets
        super().run()


class CustomBuildPy(build_py):
    def run(self):
        # Ensure `make` runs before building Python package
        subprocess.check_call(['make'])
        super().run()

typreduction = Extension('typereduction', sources = ['typereduction/typereduction.c'])

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='typereduction',
      version='0.2.2',
      description='Implementation of CTypes-based type reduction algorithms for using with PyIT2FLS',
      long_description=long_description,
      long_description_content_type='text/markdown', 
      ext_modules = [typreduction], 
      url='https://github.com/Haghrah/PyIT2FLS/tree/master/typereduction',
      author='Amir Arslan Haghrah',
      author_email='arslan.haghrah@gmail.com',
      license='MIT',
      packages=['typereduction'],
      # zip_safe=False,
      )

