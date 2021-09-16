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


class Retrieve(BaseRetrieval):
    def __init__(self, configuration):
        super().__init__()
        self.configuration = configuration
        self.data = self.load_data(configuration)

    def query_database(self):
        """
            It is helpful to know what has been computed in a library. The maximum
            number of boreholes. This function
            is prolific. <<<add more details on how this function is so great.>>>

            Returns
            -------
            library_boundaries: dict
                The boundaries. Explain further later.
        """

        if self.configuration in self.levels:
            keys = list(self.data.keys())

            # find the starting x and y point
            x = []
            y = []
            for key in keys:
                _x, _y = key.split('_')
                x.append(int(_x))
                y.append(int(_y))

            # query...
            library_boundaries = {}
            i = min(x)
            j = min(y)
            key = self.create_key(i, j)
            while key in self.data:
                start = (i, j)
                while key in self.data:
                    j += 1
                    key = self.create_key(i, j)
                stop = (i, j - 1)
                library_boundaries[i] = [start, stop]
                i += 1
                j = i
                key = self.create_key(i, j)
        else:
            raise ValueError(
                'The lib style given is not handled by this function')

        return library_boundaries

    def retrieve(self, N, M):
        """
        This function returns a unimodal list of values given NxM.

        Parameters
        ----------
        M: int
            Number of boreholes in the x-direction
        N: int
            Number of boreholes in the y-direction

        .. note::
                N < M

        Returns
        -------
        None

        """
        # see the documentation for the current range of the library
        library_boundaries = self.query_database()
        N, M = self.check_layout(M, N)

        keys = sorted(list(library_boundaries.keys()), key=int)
        first_key = keys[0]
        last_key = keys[-1]

        # make sure the number in the y-direction is in available in the library
        if first_key <= N <= last_key:
            pass
        else:
            raise ValueError('The field is not in the library')
        # make sure the number in the x-direction is available in the library
        x_min = library_boundaries[N][0][1]
        x_max = library_boundaries[N][1][1]
        if x_min <= M <= x_max:
            pass
        else:
            raise ValueError('The field is not in the library')

        key = self.create_key(N, M)

        # get the number of levels
        levels = self.levels[self.configuration]

        content = self.data[key]  # contents of the pk

        if levels == 1:
            data = {self.configuration + '_' + key: content}
        elif levels == 2:
            data = {}
            # Make sure the list is unimodal starting from lowest heat rise to
            # largest
            sec_type = self.secondary_type[self.configuration]
            if sec_type == 'r':
                # sec type reduction
                keys = list(reversed(list(content.keys())))
            elif sec_type == 't':
                keys = list(content.keys())
            elif sec_type == 'pair':
                keys = list(content.keys())

            for _key in keys:
                data[self.configuration + '_' + key + '_' + sec_type +
                     '_' + str(_key)] = content[str(_key)]

        else:
            raise ValueError('The requested configuration is not properly'
                             'configured.')

        return data

    # def count_boreholes(self):
    #     """
    #     Compute the number of boreholes in a borefield
    #
    #     Parameters
    #     ----------
    #     Nx: int
    #         Number of boreholes in the x-direction
    #     Ny: int
    #         Number of boreholes in the y-direction
    #     Nix: int (optional)
    #         Number of boreholes x-direction in the interior rectangle
    #     Niy: int (optional)
    #         Number of boreholes in the y-direction in the interior rectangle
    #     nested: int (optional)
    #         The number of nested shapes, ie. 2 for a double U
    #
    #     Returns
    #     -------
    #     nbh: int
    #         Number of boreholes in the field
    #     """
    #
    #     Nx = None
    #     Ny = None
    #     Nix = None
    #     Niy = None
    #     thickness = None
    #     reduced = None
    #
    #     return self.compute_nbh(
    #         self.configuration, Nx, Ny, Nix, Niy, reduced, thickness)

    @classmethod
    def create_key(cls, i: int, j: int):
        """
        Given an i and a j create the standard `i_j` key for the library

        Parameters
        ----------
        i: int
            Number of boreholes in the x-direction
        j: int
            Number of boreholes in the y-direction

        Returns
        -------
        key: str
            i_j
        """
        i, j = cls.check_layout(j, i)
        return str(i) + '_' + str(j)

    @staticmethod
    def check_layout(M: int, N: int):
        """
        The fields in the library are all loaded such that N<M and the keys are
        N_M. If the value of N is not less than that of M, then they will be
        swapped.

        Parameters
        ----------
        N: int
            The number of boreholes in the x-direction
        M: int
            The number of boreholes in the y-direction

        Returns
        -------
        (N, M): tuple
            A tuple of N and M, where N is less than M.
        """
        if N > M:
            M, N = N, M
        return N, M
