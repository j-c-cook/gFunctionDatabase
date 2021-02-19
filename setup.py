# Jack C. Cook
# Tuesday, February 2, 2021

from setuptools import setup
import subprocess
import sys
import os

try:
    import git
except ModuleNotFoundError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'gitpython'])
    import git


def getreqs(fname):
    """
    Get the requirements list from the text file
    JCC 03.10.2020
    :param fname: the name of the requirements text file
    :return: a list of requirements
    """
    file = open(fname)
    data = file.readlines()
    file.close()
    return [data[i].replace('\n', '') for i in range(len(data))]


def pull_first():
    """This script is in a git directory that can be pulled."""
    cwd = os.getcwd()
    gitdir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(gitdir)
    g = git.cmd.Git(gitdir)
    try:
        g.execute(['git', 'lfs', 'pull'])
    except git.exc.GitCommandError:
        raise RuntimeError("Make sure git-lfs is installed!")
    os.chdir(cwd)

pull_first()

# read the contents of your README file
# https://packaging.python.org/guides/making-a-pypi-friendly-readme/#including-your-readme-in-your-package-s-metadata
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='gFunctionLibrary',
      install_requires=['matplotlib', 'numpy', 'Pillow', 'scipy', 'pandas', 'natsort'],
      url='https://github.com/j-c-cook/gFunctionLibrary',
      download_url='https://github.com/j-c-cook/gFunctionLibrary/archive/v0.1.8.tar.gz',
      long_description=long_description,
      long_description_content_type='text/markdown',
      version='0.1.8',
      packages=['gFunctionLibrary'],
      include_package_data=True,
      author='Jack C. Cook',
      author_email='jack.cook@okstate.edu',
      description='A submodule of the GLHE Design Tool, containing libraries of '
                  'g-functions, access and accurate interpolation')
