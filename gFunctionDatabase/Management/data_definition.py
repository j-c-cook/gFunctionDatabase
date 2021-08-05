from gFunctionDatabase import Data

from natsort.natsort import natsorted


class BaseDefinition(Data.available.Configuration):
    """
    This is the base class for the data definition module. This will be the base
    class for all objects in this module, and likely other modules.
    """
    def __init__(self):
        super().__init__()
        self.registry = self.register_database()

    @staticmethod
    def register_database():
        """
        This registers the available databases into the database instance of
        this object.

        Returns
        -------
        registry : dict
            A dictionary with the keys being L, LopU, Open, U, rectangle and
            zoned. The values for each dictionary is the full file path to the
            configuration json.
        """
        registry = {}

        path_to_database, available_data_files = \
            Data.available.find_data_files()

        available_data_files_sorted = natsorted(available_data_files)

        data_file_keys = [f.split('_')[0] for f in available_data_files_sorted]

        for i in range(len(data_file_keys)):
            registry[data_file_keys[i]] = \
                path_to_database + available_data_files_sorted[i]

        return registry
