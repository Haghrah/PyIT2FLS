# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'PyIT2FLS'
copyright = '2024, Amir Arslan Haghrah'
author = 'Amir Arslan Haghrah'
release = '0.8.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'sphinx_material'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_title = 'PyIT2FLS'

extensions = ['sphinx.ext.autodoc', ]

import os
import sys
sys.path.insert(0, os.path.abspath('../'))

html_theme_options = {
    # If False, expand all TOC entries
    'globaltoc_collapse': False,
    # If True, show hidden TOC entries
    'globaltoc_includehidden': False,
}









