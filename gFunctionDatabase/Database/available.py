# Jack C. Cook
# Wednesday, August 4, 2021

from gFunctionDatabase import General
import os


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
        gfdb.Database.available.find_data_files()

    """
    # get forward or backward slash based on OS
    slash = General.platform_specific.get_slash_style()
    # get the path to the current file
    path_to_database = os.path.dirname(os.path.abspath(__file__)) + slash
    # get a list of files from current path with file_ext of json
    available_data_files = General.fileio.list_directory_files(
        path_to_database, file_ext=file_ext)
    return path_to_database, available_data_files
