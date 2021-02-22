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
    # show example of extracting features from a U configurationgmai
    # -------------- U-configuration Example ----------------
    path_to_file = 'Partial_Libraries/U_Output_Partial/U_7_x_12_3.json'
    data = gfl.fileio.js_r(path_to_file)
    bf = gfl.handle_contents.Borefield(data)
    u_info = gfl.featurerecognition.recognize_features(bf, lib_type='U')
    print(u_info)

    path_to_folder = 'Partial_Libraries/U_Output_Partial/'
    u_lib = gfl.folder_to_lib.FolderToLib(path_to_folder, lib_type='U')
    report_info = u_lib.create_report()
    gfl.fileio.export_dict(report_info, 'U_configruations.xlsx')
    u_lib_data = u_lib.create_lib_file()
    gfl.fileio.export_dict(u_lib_data, 'U_configurations_5m.json')
    # -----------------------------------------------------
    # ----------- Open-configuration Example --------------
    path_to_file = 'Partial_Libraries/Open_Output_Partial/ORect_7_x_7_3.json'
    data = gfl.fileio.js_r(path_to_file)
    bf = gfl.handle_contents.Borefield(data)
    O_info = gfl.featurerecognition.recognize_features(bf, lib_type='Open')
    print(O_info)

    path_to_folder = 'Partial_Libraries/Open_Output_Partial/'
    O_lib = gfl.folder_to_lib.FolderToLib(path_to_folder, lib_type='Open')
    report_info = O_lib.create_report()
    gfl.fileio.export_dict(report_info, 'Open_config_report.xlsx')
    O_lib_data = O_lib.create_lib_file()
    gfl.fileio.export_dict(O_lib_data, 'Open_configurations_5m.json')

    # -----------------------------------------------------

    # the following is depracated and needs updated
    # # --------------- Uniform field Example -------------------
    # # this is the same for rectangle, L, U, and Open rectangles
    # example_folder = 'Partial_Libraries/Rectangle_Output_Partial'
    # r_lib = gfl.folder_to_lib.FolderToLib(example_folder, lib_type='uniform')
    # report = r_lib.create_report()  # create a dialogue of what will be going into the lib file
    # gfl.fileio.export_dict(report, 'uniform.xlsx')  # export the report
    # r_lib_file = r_lib.create_lib_file()  #
    # gfl.fileio.export_dict(r_lib_file, 'rectangle_5m.json')
    # # -----------------------------------------------------
    # # --------------- Zoned Rectangle Example -------------
    # example_folder = 'Zoned_Rectangle_Outputs/'
    # gfl.fileio.create_dir_if_not(example_folder)
    # # provide a path to .json output files from cpgfunction
    # path_to_output = 'Partial_Libraries/Zoned_Rectangle_Output_Partial/'
    #
    # # Create an xlsx file detailing the contents of the output_folder/
    # zr_f_to_lib = gfl.folder_to_lib.FolderToLib(path_to_output, lib_type='zoned')
    # zr_report_info = zr_f_to_lib.create_report()
    # # export the contents to an excel file
    # gfl.fileio.export_dict(zr_report_info, example_folder + 'ZRect_Report.xlsx')
    # lib_file = zr_f_to_lib.create_lib_file()
    # gfl.fileio.export_dict(lib_file, example_folder + 'zoned_rectangle_example_lib.json')

    # -----------------------------------------------------


if __name__ == '__main__':
    main()
