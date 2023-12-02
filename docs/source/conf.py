# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


# -- Path setup --------------------------------------------------------------
# Ensure that the package is in the path
import os
import sys
sys.path.insert(0, os.path.abspath('../..')) # TODO: Change to pathlib?


project = 'chromex'
copyright = '2023, Daniel P. Henderson'
author = 'Daniel P. Henderson'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    # other extensions here
]

autodoc_default_options = {
    'private-members': True,
}

# Intersphinx configuration
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'selenium': ('https://selenium-python.readthedocs.io/', None),
    # You can add more mappings for other projects here
}


templates_path = ['_templates']
exclude_patterns = []

# Since we are using sphinx.ext.todo
todo_include_todos = True 

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
