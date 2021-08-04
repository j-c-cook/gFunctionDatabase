# Jack C. Cook
# Wednesday, February 3, 2021

"""
**interpolation_1D.py**

This example focuses on 1D interpolation over B/H ratios
"""

import gFunctionDatabase as gfl
import matplotlib.pyplot as plt


def main():
    path_to_file: str = 'files/lib/7x10_B_5_nbh_70.json'  # give a path to a file containing computed g-functions
    data: dict = gfl.fileio.js_r(path_to_file)  # if we were to lookup in the library we would have this dict
    # pass the data into the borefield class
    bf = gfl.handle_contents.Borefield(data)
    # visualize this borefield
    fig_1, ax_1 = bf.visualize_borefield()
    fig_1.savefig('7x10_borefield.png')
    plt.close(fig_1)
    # visualize the g-functions
    fig_2, ax_2 = bf.visualize_g_functions()
    fig_2.savefig('7x10_g_functions.png')
    # dont close the figure yet so we can add on the interpolation curve

    # interpolate for a B/H value
    B: float = 8.
    H: float = 128.
    # the default for the kind of interpolation is
    g_interpolated, rb_interpolated, D_interpolated, H_eq = bf.g_function_interpolation(B/H)

    print('The interpolated g-function for a B/H = {}/{}:'.format(B, H))
    print(g_interpolated)
    print('rb = {0:.4f}\trb/H_eq = {1:.4f}'.format(rb_interpolated, rb_interpolated / H_eq))
    print('D = {0:.5f}\tD/H_eq = {1:.5f}'.format(D_interpolated, D_interpolated / H_eq))

    ax_2.plot(bf.log_time, g_interpolated, '^')
    fig_2.savefig('7x10_g_functions_w_interpolated.png')
    plt.close(fig_2)

    # Consider that the borehole radius of the design is different from the interpolated one
    rb_design = 0.075  # borehole radius (m)
    g_function_corrected = gfl.handle_contents.borehole_radius_correction(g_interpolated,
                                                                          rb_interpolated,
                                                                          rb_design)


if __name__ == '__main__':
    main()
