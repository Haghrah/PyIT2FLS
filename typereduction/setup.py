from distutils.core import setup, Extension

typreduction = Extension('typereduction',
                         sources = ['typereduction/typereduction.c'])

setup(name='typereduction',
      version='0.2.0',
      description='CTypes base type reduction algorithms for using with PyIT2FLS',
      ext_modules = [typreduction], 
      url='https://github.com/Haghrah/PyIT2FLS/typereduction',
      author='Amir Arslan Haghrah',
      author_email='arslan.haghrah@gmail.com',
      license='MIT',
      packages=['typereduction'],
      )

