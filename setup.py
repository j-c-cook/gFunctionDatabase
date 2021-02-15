# Jack C. Cook
# Tuesday, February 2, 2021

from setuptools import setup


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
    

setup(name='gFunctionLibrary',
      install_requires=getreqs('requirements.txt'),
      version='0.1.1',
      packages=['gFunctionLibrary'],
      include_package_data=True,
      author='Jack C. Cook',
      author_email='jack.cook@okstate.edu',
      description='A submodule of the GLHE Design Tool, containing libraries of '
                  'g-functions, access and accurate interpolation')
