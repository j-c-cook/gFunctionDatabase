# Jack C. Cook
# Saturday, September 18, 2021

"""
Visualize coordinates for various configurations with a 7x10 layout.
"""

# Note: The coordinates are positioned as Ny > Nx.

import gFunctionDatabase as gfdb


def main():
    # Borefield to access is a 7x10
    N = 7
    M = 10
    key = gfdb.Management.retrieval.Retrieve.create_key(N, M)
    print('key: ' + key)

    # --------------------------------------------------------------------------
    # Visualize bore locations for configurations with one level
    # --------------------------------------------------------------------------

    # Access and then visualize the borehole locations for a
    # rectangular configuration
    r_configuration = 'rectangle'
    r = gfdb.Management.retrieval.Retrieve(r_configuration)
    library_boundaries = r.query_database()
    r_data = r.retrieve(N, M)
    bore_locations = r_data[list(r_data)[0]]['bore_locations']

    fig, ax = gfdb.Management.application.\
        GFunction.visualize_borefield(None, bore_locations=bore_locations)

    fig.savefig('rectangle.png')

    # Access and then visualize the borehole locations for a L configuration
    L_configuration = 'L'
    L = gfdb.Management.retrieval.Retrieve(L_configuration)
    library_boundaries = L.query_database()
    L_data = L.retrieve(N, M)
    bore_locations = L_data[list(L_data)[0]]['bore_locations']

    fig, ax = gfdb.Management.application. \
        GFunction.visualize_borefield(None, bore_locations=bore_locations)

    fig.savefig('L.png')

    # --------------------------------------------------------------------------
    # Visualize bore locations for configurations with two levels
    # --------------------------------------------------------------------------

    # Access and then visualize the borehole locations for a LopU configuration
    # Note: the LopU secondary key is of type "reduction", where the number
    # represents the number of points removed
    LopU_configuration = 'LopU'
    LopU = gfdb.Management.retrieval.Retrieve(LopU_configuration)
    LopU_data = LopU.retrieve(N, M)
    bore_locations = LopU_data[list(LopU_data)[0]]['bore_locations']

    fig, ax = gfdb.Management.application. \
        GFunction.visualize_borefield(None, bore_locations=bore_locations)

    fig.savefig('LopU.png')

    # Access and then visualize the borehole locations for a U configuration
    U_configuration = 'U'
    U = gfdb.Management.retrieval.Retrieve(U_configuration)
    U_data = U.retrieve(N, M)
    bore_locations = U_data[list(U_data)[0]]['bore_locations']

    fig, ax = gfdb.Management.application. \
        GFunction.visualize_borefield(None, bore_locations=bore_locations)

    fig.savefig('U.png')

    # Access and then visualize the borehole locations for a C configuration
    c_configuration = 'C'
    c = gfdb.Management.retrieval.Retrieve(c_configuration)
    c_data = c.retrieve(N, M)
    bore_locations = c_data[list(c_data)[0]]['bore_locations']

    fig, ax = gfdb.Management.application. \
        GFunction.visualize_borefield(None, bore_locations=bore_locations)

    fig.savefig('C.png')

    # Access and then visualize the borehole locations for an open rectangle
    # configuration
    Open_configuration = 'Open'
    Open = gfdb.Management.retrieval.Retrieve(Open_configuration)
    Open_data = Open.retrieve(N, M)
    bore_locations = Open_data[list(Open_data)[0]]['bore_locations']

    fig, ax = gfdb.Management.application. \
        GFunction.visualize_borefield(None, bore_locations=bore_locations)

    fig.savefig('Open.png')

    # Access zoned configuration
    zoned_configuration = 'zoned'
    zoned = gfdb.Management.retrieval.Retrieve(zoned_configuration)
    zoned_data = zoned.retrieve(N, M)
    bore_locations = zoned_data[list(zoned_data)[0]]['bore_locations']

    fig, ax = gfdb.Management.application. \
        GFunction.visualize_borefield(None, bore_locations=bore_locations)

    fig.savefig('zoned.png')


if __name__ == '__main__':
    main()
