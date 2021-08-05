import gFunctionDatabase as gfdb

import logging


class _BaseRetrieval(gfdb.DatabaseManagement.data_definition._BaseDefinition):
    """
    Base object for retrieving data from the database.
    """
    def __init__(self):
        super().__init__()

    def load_data(self, configuration):
        try:
            return gfdb.General.fileio.js_r(self.registry[configuration])
        except KeyError:
            logger = logging.getLogger(__name__)
            logger.error('The requested configuration ' + configuration +
                         ' is not currently available. Please enter one of the '
                         'following configurations: L, LopU, Open, U, rectangle'
                         ', zoned')
            raise
