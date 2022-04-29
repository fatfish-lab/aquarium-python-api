# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Aquarium python package'
copyright='2021, Fatfish Lab'
author='Fatfish Lab'

# The full version, including alpha/beta/rc tags
release='1.0.6'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions=[
    "sphinx.ext.autodoc",
    "myst_parser",
    "sphinx_copybutton"
]

# Add any paths that contain templates here, relative to this directory.
templates_path=['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns=[]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_title=''
html_theme='furo'
html_logo="_static/logo.png"
html_favicon='_static/favicon.png'
html_theme_config={
    "light_css_variables": {
        "color-brand-primary": "#339af0",
        "color-brand-content": "#339af0",
    },
    "dark_css_variables": {
        "fcolor-brand-primary": "#339af0",
        "color-brand-content": "#339af0",
    },
    "sidebar_hide_name": True
}
pygments_style="monokai"
add_module_names=False
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path=['_static']


# -- Options for Markdown files ----------------------------------------------
myst_enable_extensions=[
    "colon_fence",
    "deflist"
]
myst_heading_anchors=3
