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
        self.levels = {
            'rectangle': 1,
            'L': 1,
            'U': 2,
            'LopU': 2,
            'Open': 2,
            'C': 2,
            'zoned': 2}
        # Defines the number of keys for primary and secondary values in
        # each configuration
        # the secondary types:
        #   r: reduction
        #   t: thickness
        #   pair: (x, y) pair
        self.secondary_type = {
            'rectangle': None,
            'L': None,
            'U': 't',
            'LopU': 'r',
            'C': 't',
            'Open': 't',
            'zoned': 'pair'}

    def compute_nbh(self, configuration, Nx: int, Ny: int, Nix: int = None,
                    Niy: int = None, nested: int = None):
        """
        Compute the number of boreholes in a borefield

        Parameters
        ----------
        Nx: int
            Number of boreholes in the x-direction
        Ny: int
            Number of boreholes in the y-direction
        Nix: int (optional)
            Number of boreholes x-direction in the interior rectangle
        Niy: int (optional)
            Number of boreholes in the y-direction in the interior rectangle
        nested: int (optional)
            The number of nested shapes, ie. 2 for a double U

        Returns
        -------
        nbh: int
            Number of boreholes in the field
        """

        if configuration == 'rectangle':
            nbh = Nx * Ny
        elif configuration == 'U':
            raise ValueError('Equation not yet implemented.')
        elif configuration == 'Open':
            raise ValueError('Equation not yet implemented.')
        elif configuration == 'zoned':
            nbh = (2 * Nx + 2 * Ny - 4) + Nix * Niy
        else:
            raise ValueError('Library unavailable')

        return nbh


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
