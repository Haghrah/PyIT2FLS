from setuptools import setup


from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='pyit2fls',
      version='0.7.9',
      description='Type 1 and Interval Type 2 Fuzzy Logic Systems in Python',
      long_description=long_description,
      long_description_content_type='text/markdown', 
      url='https://github.com/Haghrah/PyIT2FLS',
      author='Amir Arslan Haghrah',
      author_email='arslan.haghrah@gmail.com',
      license='MIT',
      packages=['pyit2fls'],
      install_requires=['numpy', 'scipy', 'matplotlib', ],
      python_requires='>=3.6',
      zip_safe=False)
