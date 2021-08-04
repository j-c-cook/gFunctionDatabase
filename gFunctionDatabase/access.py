# Jack C. Cook
# Tuesday, February 2, 2020

"""
**access.py**

A module that provides access to .json library files located in `Libraries/`
"""

import os
from . import fileio
from . import platform_specific
import warnings
import time
from . import handle_contents


class LibraryAccess:
    def __init__(self, lib_style='zoned', display=False):
        self.primary = {}
        self.secondary = {}
        self.library = {}  # holds the entirety of the library contents
        self.lib_style = lib_style  # the library style
        self.display = display  # whether or not to print out explanatory statements
        if lib_style is None:
            return
        else:
            self.load_library()  # apart of __init__, where a library is loaded

    def load_library(self):
        """
        Given the lib_style a library will be loaded into self.library

        Returns
        -------
        None
        """
        if self.display:
            print('Locating library...')

        slash = platform_specific.get_slash_style()  # get platform specific slash
        local_path = os.path.dirname(os.path.abspath(__file__))  # the path to this file
        if self.lib_style == 'zoned':
            additional_path = 'Libraries/zoned_rectangle_5m.json'
        elif self.lib_style == 'rectangle':
            additional_path = 'Libraries/rectangle_5m.json'
        elif self.lib_style == 'U':
            additional_path = 'Libraries/U_configurations_5m.json'
        elif self.lib_style == 'Open':
            additional_path = 'Libraries/Open_configurations_5m.json'
        else:
            raise ValueError('The requested library is not available.')
        path_to_lib: str = local_path + slash + additional_path

        if self.display:
            print('Loading library into memory...')

        tic = time.time()
        library: dict = fileio.js_r(path_to_lib)
        toc = time.time()

        if self.display:
            load_time = toc - tic
            print('Time to load library: {0:.4f} secs'.format(load_time))

        self.library = library  # this library is saved to the parent class

        return

    def primary_key_access(self, M: int, N: int):
        """
        This function will load what is found in the primary key into self.primary.

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
        library_boundaries = self.query_lib()
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

        pk_contents = self.library[key]  # contents of the pk

        if self.lib_style == 'rectangle':
            nbh = self.compute_nbh(N, M)

            bf = handle_contents.Borefield(self.library[key])

            self.primary[nbh] = {'Nx': M,
                                 'Ny': N,
                                 'lib_style': self.lib_style,
                                 'bf': bf}

        elif self.lib_style == 'U' or self.lib_style == 'Open':
            # there could be multiple u's
            for n in self.library[key]:
                bf = handle_contents.Borefield(self.library[key][n])
                nbh = len(bf.bore_locations)

                self.primary[nbh] = {'Nx': M,
                                     'Ny': N,
                                     'nested': n,
                                     'lib_style': self.lib_style,
                                     'bf': bf}

        elif self.lib_style == 'zoned':

            secondary_keys = list(pk_contents.keys())

            for _, sk in enumerate(secondary_keys):
                sk_split = sk.split('_')
                Nix = int(sk_split[0])
                Niy = int(sk_split[1])
                nbh = self.compute_nbh(N, M, Nix, Niy)
                bf = handle_contents.Borefield(pk_contents[sk])
                self.primary[nbh] = {'Nx': M,
                                     'Ny': N,
                                     'Nix': Nix,
                                     'Niy': Niy,
                                     'lib_style': self.lib_style,
                                     'bf': bf}

        return

    def query_lib(self):
        """
        It is helpful to know what has been computed in a library. The maximum number of boreholes. This function
        is prolific. <<<add more details on how this function is so great.>>>

        Returns
        -------
        library_boundaries: dict
            The boundaries. Explain further later.
        """

        if self.lib_style == 'rectangle' or self.lib_style == 'zoned' or self.lib_style == 'U' or \
                self.lib_style == 'Open':
            keys = list(self.library.keys())

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
            while key in self.library:
                start = (i, j)
                while key in self.library:
                    j += 1
                    key = self.create_key(i, j)
                stop = (i, j-1)
                library_boundaries[i] = [start, stop]
                i += 1
                j = i
                key = self.create_key(i, j)
        else:
            raise ValueError('The lib style given is not handled by this function')

        return library_boundaries

    def compute_nbh(self, Nx: int, Ny: int, Nix: int = None, Niy: int = None, nested: int = None):
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

        if self.lib_style == 'rectangle':
            nbh = Nx * Ny
        elif self.lib_style == 'U':
            raise ValueError('Equation not yet implemented.')
        elif self.lib_style == 'Open':
            raise ValueError('Equation not yet implemented.')
        elif self.lib_style == 'zoned':
            nbh = (2 * Nx + 2 * Ny - 4) + Nix * Niy
        else:
            raise ValueError('Library unavailable')

        return nbh

    def create_key(self, i: int, j: int):
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
        i, j = self.check_layout(j, i)
        return str(i) + '_' + str(j)

    @staticmethod
    def check_layout(M: int, N: int):
        """
        The fields in the library are all loaded such that N<M and the keys are N_M. If the value of N is not less
        than that of M, then they will be swapped.

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
