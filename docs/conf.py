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
sys.path.insert(0, os.path.abspath('../'))


# -- Project information -----------------------------------------------------

project = 'gFunctionLibrary'
copyright = '2021, Jack C. Cook'
author = 'Jack C. Cook'

# The full version, including alpha/beta/rc tags
release = '0.0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.mathjax',
              'sphinx.ext.viewcode',
              'sphinx.ext.githubpages',
              'sphinxcontrib.bibtex',
              # 'sphinxcontrib.inlinesyntaxhighlight',
              # 'cloud_sptheme.ext.index_styling',
              # 'cloud_sptheme.ext.relbar_toc',
              # 'cloud_sptheme.ext.issue_tracker',
              'numpydoc',
              'sphinx.ext.napoleon']
            # 'cloud_sptheme.ext.escaped_samp_]
bibtex_bibfiles=['references.bib']

# Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
try:
    import cloud_sptheme as csp
except:
    print('unable to import cloud_sptheme as csp; try a "pip install cloud_sptheme"')

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'cloud'

# set the theme path to point to cloud's theme data
html_theme_path = [csp.get_theme_dir()]

# [optional] set some of the options listed above...
html_theme_options = {"roottarget": "index",
                       "max_width": "13in",
                       "logotarget": "index",
                       "googleanalytics_id": "UA-53205480-2",
                       "default_layout_text_size": "85%"}
                       # "table_style_default_align": "left"



# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

numfig = True
