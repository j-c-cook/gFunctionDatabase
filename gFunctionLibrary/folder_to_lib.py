# Friday, February 5, 2020

"""
**folder_to_lib.py**

This module will be where the functions for taking path/to/folder outputs from cpgfunction are combined
into a library.json file
"""

import os
from . import platform_specific
from . import fileio
from . import handle_contents
from . import featurerecognition
from . import access


class RecognizeFeatures:
    # TODO: this should take in the lib_style and a borefield object
    def __init__(self, bf: handle_contents.Borefield, lib_style: str):
        """
        Get information about a field by feature recognition.

        Parameters
        ----------
        bf: handle_contents.borefield
            A borefield object
        lib_style: str
            The library style:
            - "rectangle"
            - "L"
            - "U"
            - "Open"
            - "zoned"
        """
        self.bf = bf
        self.lib_style = lib_style

        a = 1

    @staticmethod
    def uniform_layout(path_to_file: str):

        data: dict = fileio.js_r(path_to_file)  # read the data into a dictionary
        bf = handle_contents.Borefield(data)  # load a borefield object using the dictionary
        x, y = list(zip(*bf.bore_locations))  # separate coordinates into x and y lists
        features = featurerecognition.FeatureRecognition(x, y)
        return features

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


class FolderToLib(RecognizeFeatures):
    """


    Parameters
    ----------
    path_to_folder
    lib_type: str
        - zoned
        - uniform (same for the following)
            - rectangle
            - L
            - U
            - Open
    """
    def __init__(self, path_to_folder, lib_type='zoned'):
        # super().__init__()
        self.path_to_folder = path_to_folder
        self.lib_type = lib_type

    def create_report(self):
        """
        Each library has different information stored in the report. This library uses the recognize features
        function to develop reports based on the given library type.

        Returns
        -------
        report_info: dict
            A report containing information associated with the library style
        """
        files = os.listdir(self.path_to_folder)  # get a list of the files
        slash = platform_specific.get_slash_style()
        path_to_folder_split = self.path_to_folder.split(slash)
        if path_to_folder_split[-1] == '':
            del path_to_folder_split[-1]

        report_info: dict = {'file_path': []}  # place to hold the information for the report

        for i, file in enumerate(files):
            path_to_file_list = path_to_folder_split + [file]
            path_to_file = slash.join(path_to_file_list)
            report_info['file_path'].append(path_to_file)
            data: dict = fileio.js_r(path_to_file)
            bf = handle_contents.Borefield(data)
            # get the relevant information
            relevant_info = featurerecognition.recognize_features(bf, self.lib_type)

            # load the relevant information into the report_info dictionary
            for key in relevant_info:
                if not key in report_info:
                    report_info[key] = []
                report_info[key].append(relevant_info[key])

        return report_info

    def create_lib_file(self):
        """
        This uses the information in the report to create a library file

        Returns
        -------
        library_file: dict
            A library file to be used stored for use in the package.
        """
        lib_info = access.LibraryAccess(lib_style=None, display=False)

        library_file = {}

        report_info = self.create_report()

        file_paths: list = report_info['file_path']
        del report_info['file_path']

        keys = list(report_info.keys())
        n_rows = len(report_info[keys[0]])

        for i in range(n_rows):
            file_path = file_paths[i]
            Nx = report_info['Nx'][i]
            Ny = report_info['Ny'][i]
            # create a key for the library
            key = lib_info.create_key(Nx, Ny)
            # if the key is not in the library file dictionary, then key it
            if key in library_file:
                pass
            else:
                library_file[key] = {}

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
            elif 'uniform' in self.lib_type:
                # store these as MXN where M < N
                n = int(report_info['Nx'][i])
                m = int(report_info['Ny'][i])
                if n < m:  # swap if necessary
                    m, n = n, m
                key = str(m) + '_' + str(n)

                # read the cpgfunction output into a dictionary
                file_path = file_paths[i]
                cpgf_output = fileio.js_r(file_path)

                library_file[key] = cpgf_output
            elif 'U' in self.lib_type or 'Open' in self.lib_type:
                nested = report_info['nested'][i]
                library_file[key][nested] = fileio.js_r(file_path)
            else:
                raise ValueError('The library type input is not currently handled by this object.')

        return library_file
