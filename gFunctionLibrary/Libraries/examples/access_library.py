# Jack C. Cook
# Saturday, February 13, 2021

"""
access_library.py

Provide an example on how to access the following libraries:
- zoned rectangle
"""

import gFunctionLibrary as gfl


def main():
    m = 5  # the x-direction
    n = 4  # the y-direction
    # ------- Rectangle Library Access Example ----------

    r_lib = gfl.access.LibraryAccess(lib_style='rectangle', display=True)
    # # find out what is available in the rectangle library
    library_boundaries = r_lib.query_lib()
    for key in library_boundaries:
        start = library_boundaries[key][0]
        stop = library_boundaries[key][1]
        # print('({0}, {1}) -> ({2}, {3})'.format(str(start[0]).zfill(2), str(start[1]).zfill(2),
        #                                         str(stop[0]).zfill(2), str(stop[1]).zfill(2)))
    r_lib.primary_key_access(m, n)
    print(r_lib.primary)
    # ---------------------------------------------------
    # ----- U configuration Library Access Example ------
    u_lib = gfl.access.LibraryAccess(lib_style='U', display=True)
    u_lib.primary_key_access(m, n)
    print(u_lib.primary)
    # ---------------------------------------------------
    # ----- Open rectangle Library Access Example ------
    o_lib = gfl.access.LibraryAccess(lib_style='Open', display=True)
    o_lib.primary_key_access(m, n)
    print(o_lib.primary)
    # ---------------------------------------------------
    # ----- Zoned Rectangle Library Access Example ------

    # load up the library into memory
    zr_lib = gfl.access.LibraryAccess(lib_style='zoned', display=True)
    zr_lib.primary_key_access(m, n)
    print(zr_lib.primary)
    # ---------------------------------------------------

    a = 1


if __name__ == '__main__':
    main()
