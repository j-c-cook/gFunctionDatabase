# Jack C. Cook
# Tuesday, February 2, 2020

"""
**fileio.py**

A module for handling data entering (input) or leaving (output).
"""

import json
import os
import pandas as pd


def js_r(file_path: str) -> dict:
    """
    Read a .json file into a dictionary

    Parameters
    ----------
    file_path: str
        the path to the .json file
    Returns
    -------
    the .json file in dictionary format
    """
    with open(file_path) as f_in:
        return json.load(f_in)


def create_dir_if_not(path_to_folder: str):
    """
    Create a directory if it does not exist.

    Parameters
    ----------
    path_to_folder: str
        A file path (absolute or relative) to a folder that may or may not exist yet

    Returns
    -------
    None
    """
    # https://www.tutorialspoint.com/How-can-I-create-a-directory-if-it-does-not-exist-using-Python
    if not os.path.exists(path_to_folder):
        os.makedirs(path_to_folder)


def export_dict(d: dict, path_to_output: str, file_ext: str):
    """
    Export a dictionary based on its file extension.

    Parameters
    ----------
    d: dict
        A python dictionary
    path_to_output: str
        The output path of the dictionary
    file_ext: str
        The file extension to be exported, ie. csv, json, xlsx

    Returns
    -------
    None
    """
    if file_ext == 'csv':
        pd.DataFrame(d).to_csv(path_to_output)
    else:
        raise ValueError('The file extension requested is not yet accounted for in this function.')