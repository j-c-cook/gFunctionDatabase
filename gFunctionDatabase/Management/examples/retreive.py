# Jack C. Cook
# Thursday, September 16, 2021

import gFunctionDatabase as gfdb


def main():
    # Borefield to access is a 7x10
    N = 7
    M = 10
    key = gfdb.Management.retrieval.Retrieve.create_key(N, M)
    print('key: ' + key)

    # --------------------------------------------------------------------------
    # Access configurations with one level
    # --------------------------------------------------------------------------

    # Access rectangular configurations
    r_configuration = 'rectangle'
    r = gfdb.Management.retrieval.Retrieve(r_configuration)
    library_boundaries = r.query_database()
    r_data = r.retrieve(N, M)
    print(r_data)
    # if the level is 1, then the data returned from retrieve(N, M) will just
    # have one configuration in it
    r_level = r.levels[r_configuration]

    # Access C configuration
    c_configuration = 'C'
    c = gfdb.Management.retrieval.Retrieve(c_configuration)
    library_boundaries = c.query_database()
    c_data = c.retrieve(N, M)
    print(c_data)

    # Access L configuration
    L_configuration = 'L'
    L = gfdb.Management.retrieval.Retrieve(L_configuration)
    library_boundaries = L.query_database()
    L_data = L.retrieve(N, M)
    print(L_data)

    # --------------------------------------------------------------------------
    # Access configurations with two levels
    # --------------------------------------------------------------------------

    # Access LopU configuration
    LopU_configuration = 'LopU'
    LopU = gfdb.Management.retrieval.Retrieve(LopU_configuration)
    LopU_data = LopU.retrieve(N, M)
    print(LopU_data)

    # Access Open rectangle configuration
    Open_configuration = 'Open'
    Open = gfdb.Management.retrieval.Retrieve(Open_configuration)
    Open_data = Open.retrieve(N, M)
    print(Open_data)

    # Access U configurations
    U_configuration = 'U'
    U = gfdb.Management.retrieval.Retrieve(U_configuration)
    U_data = U.retrieve(N, M)
    print(U_data)

    # Access zoned configuration
    zoned_configuration = 'zoned'
    zoned = gfdb.Management.retrieval.Retrieve(zoned_configuration)
    zoned_data = zoned.retrieve(N, M)
    print(zoned_data)


if __name__ == '__main__':
    main()

