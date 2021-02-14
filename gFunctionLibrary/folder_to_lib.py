# Friday, February 5, 2020

"""
**folder_to_lib.py**

This module will be where the functions for taking path/to/folder outputs from cpgfunction are combined
into a library.json file
"""

import os
from . import platform_specific
from . import fileio


class Decipherkey:
    def __init__(self):
        a = 1

    @staticmethod
    def zoned_rectangle(file_name: str):
        """
        Given a filename.json which is a filename associated with a zoned rectangle,
        return the Nx, Ny, Nix, Niy values.

        Returns
        -------
        key_contents: dict
            A dictionary containing the deciphered key with the following primary keys

            Nx: int
                Number of boreholes in the x-direction
            Ny: int
                Number of boreholes in the y-direction
            Nix: int
                Number of interior boreholes in the x-direction
            Niy: int
                Number of interior boreholes in the y-direction
        """
        # split the file by period
        split_file_period = file_name.split('.')
        # if the file extension is not provided, and just the string, then handle it
        if split_file_period[-1] == 'json':
            _key = split_file_period[-2]
        else:
            _key = split_file_period[-1]

        slash = platform_specific.get_slash_style()  # get the \ or / slash

        split_key_by_slash = _key.split(slash)  # split the path by that slash

        key = split_key_by_slash[-1]  # the raw key

        split_key_by_underscore = key.split('_')

        Nx = int(split_key_by_underscore[1])
        Ny = int(split_key_by_underscore[3])
        Nix = int(split_key_by_underscore[4])
        Niy = int(split_key_by_underscore[6])

        key_contents = {'Nx': Nx, 'Ny': Ny, 'Nix': Nix, 'Niy': Niy}

        return key_contents


class FolderToLib(Decipherkey):
    def __init__(self, path_to_folder, lib_type='zoned'):
        super().__init__()
        self.path_to_folder = path_to_folder
        self.lib_type = lib_type

    def create_report(self):
        files = os.listdir(self.path_to_folder)  # get a list of the files

        report_info: dict = {'file_path': []}  # place to hold the information for the report

        for _, file in enumerate(files):

            # handle zoned rectangles
            if 'zoned' in self.lib_type:
                key_contents = self.zoned_rectangle(file)
            else:
                raise ValueError('The library type input is not currently handled by this object.')

            # loop through the dictionary containing the keys and append to the report_info dictionary
            for key in key_contents:
                # if any of the keys returned in key_contents are not in the report dictionary, put them there
                if key not in report_info:
                    report_info[key] = []
                report_info[key].append(key_contents[key])
            report_info['file_path'].append(self.path_to_folder + platform_specific.get_slash_style()
                                            + file)

        return report_info

    def create_lib_file(self):

        library_file = {}

        report_info = self.create_report()

        file_paths: list = report_info['file_path']
        del report_info['file_path']

        keys = list(report_info.keys())
        n_rows = len(report_info[keys[0]])

        for i in range(n_rows):

            if 'zoned' in self.lib_type:
                Nx = report_info['Nx'][i]
                Ny = report_info['Ny'][i]
                Nix = report_info['Nix'][i]
                Niy = report_info['Niy'][i]
                file_path = file_paths[i]
                # the primary key in the zoned rectangle lib file
                primary_key = str(Nx) + '_' + str(Ny)
                if primary_key not in library_file:
                    library_file[primary_key] = {}
                # the secondary key in the zoned rectangle lib file
                secondary_key = str(Nix) + '_' + str(Niy)

                # read the cpgfunction output into a dictionary
                cpgf_output = fileio.js_r(file_path)

                library_file[primary_key][secondary_key] = cpgf_output
            else:
                raise ValueError('The library type input is not currently handled by this object.')

        return library_file
