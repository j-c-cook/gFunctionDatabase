# Jack C. Cook
# Saturday, February 13, 2021

"""
access_library.py

Provide an example on how to access the following libraries:
- zoned rectangle
"""

import gFunctionLibrary as gfl


def main():
    # ----- Zoned Rectangle Library Access Example ------
    n = 4
    m = 5

    # load up the library into memory
    zr_lib = gfl.access.LibraryAccess(lib_style='zoned', display=True)
    zr_lib.primary_key_access(n, m)
    print(zr_lib.primary)
    print(zr_lib.primary_query())
    # ---------------------------------------------------

    a = 1


if __name__ == '__main__':
    main()
