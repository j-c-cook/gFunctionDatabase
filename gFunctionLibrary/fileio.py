# Jack C. Cook
# Tuesday, February 2, 2020

"""
**fileio.py**

A module for handling data entering (input) or leaving (output).
"""

import json


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
