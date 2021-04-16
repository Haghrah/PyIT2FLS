from distutils.core import setup, Extension
setup(name='typereduction', version='0.1.0',  \
      ext_modules=[Extension('typereduction', ['typereduction.c'])])
