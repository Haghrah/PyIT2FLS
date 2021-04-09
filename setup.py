from setuptools import setup

setup(name='pyit2fls',
      version='0.6.2',
      description='Interval Type 2 Fuzzy Logic Systems in Python',
      url='https://github.com/Haghrah/PyIT2FLS',
      author='Amir Arslan Haghrah',
      author_email='arslan.haghrah@gmail.com',
      license='GPL-3.0',
      packages=['pyit2fls'],
      install_requires=['numpy', 'scipy', 'matplotlib', ],
      python_requires='>=3.6',
      zip_safe=False)
