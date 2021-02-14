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
    file_split_period_ = file_path.split('.')
    if file_split_period_[-1] != 'json':
        raise ValueError('The supplied file extension is not a .json.')
    with open(file_path) as f_in:
        return json.load(f_in)


def js_dump(d: dict, file_path: str) -> None:
    """
    Dump a dictionary to a json file.

    Parameters
    ----------
    d: dict
        The dictionary that is being dumped
    file_path: str
        Path to where the dictionary is going to be dumped

    Returns
    -------
    None
    """
    # https://stackoverflow.com/a/26057360/11637415
    with open(file_path, 'w') as fp:
        json.dump(d, fp)


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
    return


def export_dict(d: dict, path_to_output: str, file_ext: str = None):
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
    # if there is no file extension provided, then check what is on the file path
    if file_ext is None:
        split_path = path_to_output.split('.')
        file_ext = split_path[-1]

    if file_ext == 'csv':
        pd.DataFrame(d).to_csv(path_to_output)
    elif file_ext == 'xlsx':
        pd.DataFrame(d).to_excel(path_to_output)
    elif file_ext == 'json':
        js_dump(d, path_to_output)
    else:
        raise ValueError('The file extension requested is not yet accounted for in this function.')