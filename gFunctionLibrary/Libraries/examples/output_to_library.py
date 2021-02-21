# Jack C. Cook
# Wednesday, February 10, 2021

"""
output_to_library.py

This will exemplify the methods for interacting with cppgfunction output folders
for the following libraries:/media/jackcook/SHARED/Documents/Oklahoma_State/Masters/Research/cpgfunction/README.md
- Zoned Rectangles
"""

import gFunctionLibrary as gfl


def main():
    # --------------- Rectangle Example -------------------
    example_folder = '/media/jackcook/SHARED/Documents/Oklahoma_State/Masters/Research/ORNL_Design_Tool_Projects/' \
                     'gFunctionLibrary/Library_Backup/Library_Combined/Rectangle_1650_5m_Corrected'
    r_lib = gfl.folder_to_lib.FolderToLib(example_folder, lib_type='uniform')
    report = r_lib.create_report()  # create a dialogue of what will be going into the lib file
    gfl.fileio.export_dict(report, 'uniform.xlsx')  # export the report
    r_lib_file = r_lib.create_lib_file()  #
    gfl.fileio.export_dict(r_lib_file, 'rectangle_5m.json')

    # -----------------------------------------------------
    # --------------- Zoned Rectangle Example -------------
    example_folder = 'Zoned_Rectangle_Outputs/'
    gfl.fileio.create_dir_if_not(example_folder)
    # provide a path to .json output files from cpgfunction
    path_to_output = 'Partial_Libraries/Zoned_Rectangle_Output_Partial/'

    # Create an xlsx file detailing the contents of the output_folder/
    zr_f_to_lib = gfl.folder_to_lib.FolderToLib(path_to_output, lib_type='zoned')
    zr_report_info = zr_f_to_lib.create_report()
    # export the contents to an excel file
    gfl.fileio.export_dict(zr_report_info, example_folder + 'ZRect_Report.xlsx')
    lib_file = zr_f_to_lib.create_lib_file()
    gfl.fileio.export_dict(lib_file, example_folder + 'zoned_rectangle_example_lib.json')

    # -----------------------------------------------------


if __name__ == '__main__':
    main()
