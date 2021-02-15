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


class ZonedRectangle:
    def __init__(self):
        self.primary = {}
        self.secondary = {}
        self.library = {}

    def primary_key_access(self, N: int, M: int):
        """
        This function will load what is found in the primary key into self.primary.

        Parameters
        ----------
        N: int
            Number of boreholes in the x-direction
        M: int
            Number of boreholes in the y-direction

        .. note::
                N > M

        Returns
        -------
        None

        """
        # see the documentation for the current range of the library
        # TODO: This is hardcoded, we could uses the query library function to get these constants.
        if N < 4 or M < 4:
            raise ValueError('This is not within the range of the zoned library.')
        if N > 28 or M > 32:
            raise ValueError('This is not within the range of the zoned library.')

        # make sure N is less than M
        if N > M:
            N, M = M, N
        assert N < M

        key = str(N) + '_' + str(M)

        pk_contents = self.library[key]  # contents of the pk

        secondary_keys = list(pk_contents.keys())

        for _, sk in enumerate(secondary_keys):
            sk_split = sk.split('_')
            Nix = int(sk_split[0])
            Niy = int(sk_split[1])
            nbh = self.compute_nbh(N, M, Nix, Niy)
            bf = handle_contents.Borefield(pk_contents[sk])
            self.primary[nbh] = {'Nx': N,
                                 'Ny': M,
                                 'Nix': Nix,
                                 'Niy': Niy,
                                 'bf': bf}

        return

    def primary_query(self):
        """
        Query what is loaded in primary.

        Returns
        -------

        """
        if len(list(self.primary.keys())) == 0:
            warnings.warn('No primary key values have been loaded.')

        return list(self.primary.keys())

    # def secondary_key_access(self):
    #     available_keys = self.primary_query()

    @staticmethod
    def compute_nbh(Nx: int, Ny: int, Nix: int, Niy: int):
        return (2 * Nx + 2 * Ny - 4) + Nix * Niy


class LibraryAccess(ZonedRectangle):
    def __init__(self, lib_style='zoned', display=False):
        if lib_style == 'zoned':
            ZonedRectangle.__init__(self)  # initialize parent
        else:
            warnings.warn('The requested library does not have a child access class being'
                          'initialized.')
        self.display = display
        self.lib_style = lib_style
        self.load_library()

    def load_library(self):
        if self.display:
            print('Locating library...')

        slash = platform_specific.get_slash_style()  # get platform specific slash
        local_path = os.path.dirname(os.path.abspath(__file__))  # the path to this file
        if self.lib_style == 'zoned':
            additional_path = 'Libraries/zoned_rectangle_5m.json'
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
