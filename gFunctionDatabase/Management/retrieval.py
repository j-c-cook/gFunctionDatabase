from gFunctionDatabase import General
from . import data_definition

import logging


class BaseRetrieval(data_definition.BaseDefinition):
    """
    Base object for retrieving data from the database.
    """
    def __init__(self):
        super().__init__()

    def load_data(self, configuration):
        """
        This function takes in a configuration string argument, loads the
        specified database configuration file into memory and returns the entire
        file as a dictionary.

        Note
        ------
        There is no way to inject into a json file. When a library is opened,
        the entirety of the library is loaded into memory. For this reason, it
        is good practice to limit the number of database configuration files
        open at one time.

        Parameters
        ----------
        configuration : str
            A string defining the database configuration to be loaded.
            Options include: C, L, LopU, Open, U, rectangle, zoned

        Returns
        -------
        database : dict
            The contents of a database file is returned as a dictionary.
        """
        try:
            return General.fileio.js_r(self.registry[configuration])
        except KeyError:
            logger = logging.getLogger(__name__)
            logger.error('The requested configuration ' + configuration +
                         ' is not currently available. Please enter one of the '
                         'following configurations: C, L, LopU, Open, U, '
                         'rectangle, zoned')
            raise
