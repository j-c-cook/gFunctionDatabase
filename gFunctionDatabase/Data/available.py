# Jack C. Cook
# Wednesday, August 4, 2021

from gFunctionDatabase import General
import os


class Configuration:
    """
    This object serves as the base object for several of the g-function database
    management modules. The two instances of this object define the number of
    json levels and the number of keys used on each level.
    """
    def __init__(self):
        # Define the number of levels in the json file
        self.levels = {'C': 1, 'L': 1, 'LopU': 2, 'Open': 2, 'U': 2,
                       'rectangle': 1, 'zoned': 2}
        # Reusable dictionaries for the number of primary and secondary keys
        two_and_none = {'primary': 2, 'secondary': None}
        two_and_one = {'primary': 2, 'secondary': 1}
        two_and_two = {'primary': 2, 'secondary': 2}
        # Defines the number of keys for primary and secondary values in
        # each configuration
        self.number_of_keys = {'L': two_and_none,
                               'rectangle': two_and_none,
                               'LopU': two_and_one,
                               'Open': two_and_one,
                               'U': two_and_one,
                               'zoned': two_and_two}


def find_data_files(file_ext='json'):
    """
    This function finds the path and the available database data files.

    Parameters
    ----------
    file_ext : str (optional)
        This argument is the string of the file extension to be searched for.
        Given that this database contains only json files, it defaults to
        'json'.

    Returns
    -------
    (path_to_database, available_data_files) : tuple
        A tuple containing the path to the database and the available json
        data files.

    Examples
    ---------
    >>> import gFunctionDatabase as gfdb
    >>> path_to_database, available_data_files = \
        gfdb.Data.available.find_data_files()
    """
    # get forward or backward slash based on OS
    slash = General.platform_specific.get_slash_style()
    # get the path to the current file
    path_to_database = os.path.dirname(os.path.abspath(__file__)) + slash
    # get a list of files from current path with file_ext of json
    available_data_files = General.fileio.list_directory_files(
        path_to_database, file_ext=file_ext)
    return path_to_database, available_data_files
