# Jack C. Cook
# Monday, September 27, 2021


def rectangle(Nx, Ny, Bx, By):
    # Create a list of (x, y) pairs for a rectangle
    r = []
    nbh = Nx * Ny
    for i in range(Nx):
        for j in range(Ny):
            r.append((i * Bx, j * By))
    assert len(r) == nbh
    return r


def open_rectangle(Nx, Ny, Bx, By):
    # Create a list of (x, y) pairs for an open rectangle
    open_r = []
    if Nx > 2 and Ny > 2:
        nbh = Ny * 2 + (Nx - 2) * 2
        for i in range(Nx):
            open_r.append((i * Bx, 0.))
        for j in range(1, Ny-1):
            open_r.append((0, j * By))
            open_r.append(((Nx-1) * Bx, j * By))
        for i in range(Nx):
            open_r.append((i * Bx, (Ny-1) * By))
    else:
        nbh = Nx * Ny
        open_r = rectangle(Nx, Ny, Bx, By)

    assert len(open_r) == nbh
    return open_r


def U_shape(Nx, Ny, Bx, By):
    # Create a list of (x, y) pairs for a U-shape
    U = []
    if Nx > 2 and Ny > 1:
        nbh = 2 * Ny + (Nx - 2)
        for i in range(Nx):
            U.append((i * Bx, 0.))
        for j in range(1, Ny):
            U.append((0., j * By))
    else:
        nbh = Nx * Ny
        U = rectangle(Nx, Ny, Bx, By)
    assert len(U) == nbh
    return U


def L_shape(Nx, Ny, Bx, By):
    nbh = Nx + Ny - 1
    L = []
    for i in range(Nx):
        L.append((i * Bx, 0.))
    for j in range(1, Ny):
        L.append((0., j * By))
    assert len(L) == nbh
    return L


class ZonedRectangle(object):
    """
        A class for control of zoned rectangles.

        Original implementation by Jeffrey D. Spitler in VBA.

        Parameters
        ----------
        Nx: int
            Number of boreholes on perimeter in x direction
        Ny: int
            Number of boreholes on perimeter in y direction
        B: float
            Spacing of perimeter boreholes (m)
        Nix: int, optional
            Number of interior borehole in the x direction Nix < (Nx-2);
            if Nix=Nx-2 that would be a regular uniform rectangle
        Niy: int, optional
            Number of interior boreholes in the y direction Niy < (Ny-2);
            if Niy=Ny-2, that would be a regular uniform rectangle

            .. note::
                Assumptions/Limitations/Comments:

                1. We assume on the perimeter uniform spacing; the same in both
                directions.
                2. The interior spacing in each direction if uniform (but may be
                different in the x and y directions). It is set, so that in each
                direction, the spacing between the interior boreholes is the
                same as the spacing from the outermost interior borehole and the
                perimeter. Interior boreholes are not usually aligned with the
                perimeter boreholes.

        Raises
        --------
        ValueError
            if the optional Nix is provided and `Nix > (Nx-2)`
            if the optional Niy is provided and `Niy > (Ny-2)`
    """
    def __init__(self, Nx: int, Ny: int, B: float, Nix: int = None,
                 Niy: int = None):
        self.Nx = Nx
        self.Ny = Ny
        self.B = B
        self.coordinates = {}
        if Nix is None:
            self.Nix = Nx - 2
        else:
            if Nix > (Nx-2):
                raise ValueError('To many interior x boreholes.')
        if Niy is None:
            self.Niy = Ny - 2
        else:
            if Niy > (Ny-2):
                raise ValueError('Too many interior y boreholes.')
        if Nix is None and Niy is None:
            self.z_rect_control()  # generate all of the zoned rectangles

    def coordinate(self, i: int, j: int):
        """
        Given and i and a j value, return the x and y coordinate based on the
        equal B spacing in the field.

        Parameters
        ----------
        i: int
            the iterator i in a for loop, corresponding to the x-coordinate
        j: int
            the iterator j in a for loop, corresponding to the y-coordinate

        Returns
        -------
        (x, y): tuple
            A tuple containing the x and y coordinate for this i and j
        """
        x = (i - 1) * self.B
        y = (j - 1) * self.B
        return x, y

    def hash_key(self):
        """
        This function will query the self for Nx, Ny, Nix and Niy values

        Returns
        -------
        key: str
            'ZRect_Nx_x_Ny_Nix_x_Niy'
        """
        key = 'ZRect_' + str(self.Nx) + '_x_' + str(self.Ny) + '_' + \
              str(self.Nix) + '_x_' + str(self.Niy)
        return key

    def gen_z_rect(self):
        key = self.hash_key()
        # Create a list of (x, y) coordinates
        current_coordinates = []

        # 1) Create the top and bottom rows
        for i in range(1, self.Nx+1):
            # create bottom row
            j = 1
            x, y = self.coordinate(i, j)
            current_coordinates.append((x, y))
            # create top row
            j = self.Ny
            x, y = self.coordinate(i, j)
            current_coordinates.append((x, y))

        # 2) Create the left and right columns, excluding the corners
        for j in range(2, self.Ny):
            # create the left column
            i = 1
            x, y = self.coordinate(i, j)
            current_coordinates.append((x, y))
            # create the right column
            i = self.Nx
            x, y = self.coordinate(i, j)
            current_coordinates.append((x, y))

        # 3) Create the interior coordinates
        Bx = (self.Nx - 1) * self.B / (self.Nix + 1)
        By = (self.Ny - 1) * self.B / (self.Niy + 1)

        for i in range(1, self.Nix+1):
            for j in range(1, self.Niy+1):
                x = i * Bx
                y = j * By
                current_coordinates.append((x, y))
        self.coordinates[key] = current_coordinates

    def reduce_i_rect(self):
        """
        Determines the internal rectangle row or column reduction
        that keeps the x and y spacing the most uniform, and updates
        the correct new value of Nix and Niy in self.

        Returns
        -------
        finished: bool
            This method will return a true or false value. If the value is
            false, continue creating rectangles, if it is true then no more
            zoned rectangles can be generated.
        """
        finished = False
        # tentative values
        Nixm1 = self.Nix - 1
        Niym1 = self.Niy - 1

        if Nixm1 == 0 and Niym1 == 0:
            finished = True  # no further reductions can be made
        elif Nixm1 == 0:
            self.Niy = Niym1  # reduce in the y-direction
            if self.Niy == 1:
                finished = True
        elif Niym1 == 0:
            self.Nix = Nixm1
            if self.Nix == 1:
                finished = True
        else:
            # general case where we can reduce in either direction
            # current x spacing
            x_spacing_c = (self.Nx - 1) * self.B / (self.Nix + 1)
            # current y spacing
            y_spacing_c = (self.Ny - 1) * self.B / (self.Niy + 1)
            # x spacing if we reduce one column
            x_spacing_t = (self.Nx - 1) * self.B / self.Nix
            # y spacing if we reduce one row
            y_spacing_t = (self.Ny - 1) * self.B / self.Niy

            # possible outcomes
            # ratio (fraction) if we reduce one column
            f_x = x_spacing_t / y_spacing_c
            if f_x < 1:
                f_x = 1 / f_x
            # ratio (fraction) if we reduce one row
            f_y = x_spacing_c / y_spacing_t
            if f_y < 1:
                f_y = 1 / f_y
            d_f_x = f_x - 1  # distance of ratio from 1 if we reduce one column
            d_f_y = f_y - 1  # distance of ratio from 1 if wer reduce one row
            if d_f_x > d_f_y:
                self.Niy = Niym1
            else:
                self.Nix = Nixm1

        return finished

    def z_rect_control(self):
        """
        This function is called if the optional inputs Nix and Niy are not
        provided. This will create all of the zoned rectangles given Nx, Ny and
        B. A while loop continuously calls
        :func:`gFunctionDatabase.coordinate_generator.ZonedRectangle.reduce_i_rect`
        until all of the zoned rectangles have been created.

        Returns
        -------
        None
            The coordinates are stored in self.coordinates(), an instance of
            :func:`gFunctionDatabase.coordinate_generator.CoordinateGeneratorBase`
            made available because Base is a child.

        """
        # while we are still able to create more zoned rectangles, create zoned
        # rectangles self.gen_z_rect()
        # if this was not commented out then we would create the square first
        unfinished: bool = True
        while unfinished:
            finished: bool = self.reduce_i_rect()
            self.gen_z_rect()
            if finished is True:
                unfinished = False
