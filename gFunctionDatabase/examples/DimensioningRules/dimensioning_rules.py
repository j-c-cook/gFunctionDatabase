# Jack C. Cook
# Tuesday, February 2, 2020

# Updated Monday, September 27 to include live calculated g-functions using the
# UBHWT g-function computed by pygfunction

"""
**dimensioning_rules.py**

The following goals will be accomplished in this example:
    1) proof that g-functions vary based on ln(t/ts), B/H, D/H, and rb/H
    2) proof that interpolation over B/H is accurate
"""

import matplotlib.pyplot as plt
import gFunctionDatabase as gfdb


def tabulate_dimensionless_ratios(D_values: list, H_values: list,
                                  r_b_values: list, B: float):
    print('$B$ (m)\t$D$ (m)\t$H$ (m)\t$r_b$ (m)\t$B/H$\t$D/H$\t$r_b/H$')
    for i in range(len(D_values)):
        D = D_values[i]
        H = H_values[i]
        r_b = r_b_values[i]
        string = '{0}\t{1}\t{2}\t{3}\t{4:.4f}\t{5:.4f}\t{6:.4f}'.\
            format(B, D, H, r_b, B/H, D/H, r_b/H)
        print(string)


def main():
    # Prove that the g-functions vary based on ln(t/ts), B/H, D/H,
    # and rb/H visually and mathematically

    log_time = gfdb.utilities.Eskilson_log_times()

    # Part A) Compute and plot the g-functions for a uniform temperature
    # boundary condition, for a layout of 7x10 and uniform spacing of B=5m
    Nx = 7
    Ny = 10
    B = 5
    D_values = [0.16667, 0.25, 0.5, 1., 2., 4., 8.]
    H_values = [8., 12., 24., 48., 96., 192., 384.]
    r_b_values = [0.004, 0.006, 0.012, 0.024, 0.048, 0.096, 0.192]
    nSegments = [12] * len(D_values)
    alpha = 1.0e-06
    tabulate_dimensionless_ratios(D_values, H_values, r_b_values, B)

    # Compute g-functions
    r_coodinates = gfdb.coordinates.rectangle(Nx, Ny, B, B)
    g_data = gfdb.Management.application.\
        uniform_temperature_uniform_segment_lengths(D_values, H_values,
                                                    r_b_values, B, log_time,
                                                    alpha, r_coodinates,
                                                    nSegments)
    GFunction_input = gfdb.Management.application.GFunction.\
        configure_database_file_for_usage(g_data)
    GFunction_5m = gfdb.Management.application.GFunction(**GFunction_input)
    fig_1, ax_1 = GFunction_5m.visualize_g_functions()

    # Part B) Annotate the plot with the borehole layout and the D/H, rb/H
    # add in a sub axes plot with the borehole layout
    sub_axes = plt.axes([.0, .47, .5, .5])
    x, y = list(zip(*GFunction_5m.bore_locations))
    sub_axes.scatter(x, y)
    sub_axes.set_aspect('equal')
    sub_axes.axis('off')
    # annotate the layout with B spacings
    sub_axes.annotate(text='', xy=(0, 0), xytext=(5, 0),
                      arrowprops=dict(arrowstyle='<->'))
    sub_axes.annotate(text='', xy=(0, 0), xytext=(0, 5),
                      arrowprops=dict(arrowstyle='<->'))
    ax_1.text(-7.8, 53, 'B')
    ax_1.text(-8.5, 62, 'B')
    # add in text for D/H and rb/H
    ax_1.text(-3.5, 124, '$\dfrac{r_b}{H}$=0.0005', fontsize=12)
    ax_1.text(-3.5, 111, '$\dfrac{D}{H}$=0.02083', fontsize=12)

    fig_1.savefig('g-functions_7_10.png')

    # Part C) Compute and plot the g-functions for a uniform temperature
    # boundary condition, for a layout of 7x10 and B=20m
    B = 20.
    D_values = [0.66667, 1., 2., 4., 8.]
    H_values = [32., 48., 96., 192., 384.]
    r_b_values = [0.016, 0.024, 0.048, 0.096, 0.192]
    nSegments = [12] * len(D_values)
    alpha = 1.0e-06
    tabulate_dimensionless_ratios(D_values, H_values, r_b_values, B)

    # Compute g-functions
    r_coodinates = gfdb.coordinates.rectangle(Nx, Ny, B, B)
    g_data = gfdb.Management.application. \
        uniform_temperature_uniform_segment_lengths(D_values, H_values,
                                                    r_b_values, B, log_time,
                                                    alpha, r_coodinates,
                                                    nSegments)
    GFunction_input = gfdb.Management.application.GFunction. \
        configure_database_file_for_usage(g_data)
    GFunction_20m = gfdb.Management.application.GFunction(**GFunction_input)

    # Part D) Determine the error between the g-functions with the same
    # dimensionless values
    keys_5m = list(reversed(list(GFunction_5m.g_lts.keys())))
    keys_5m = keys_5m[2:]
    print('The heights that will be used in the from the 5m library file:')
    print(keys_5m)
    print('The heights that will be used in the from the 20m library file:')
    keys_20m = list(reversed(list(GFunction_20m.g_lts.keys())))
    print(keys_20m)

    mean_percent_errors = []
    for i in range(len(keys_5m)):
        mean_percent_error = \
            gfdb.statistics.mpe(GFunction_5m.g_lts[keys_5m[i]],
                                GFunction_20m.g_lts[keys_20m[i]])
        mean_percent_errors.append(mean_percent_error)
    print('Mean percent errors between g-functions')
    print(mean_percent_errors)
    print('Min MPE: {}\tMax MPE: {}'.format(min(mean_percent_errors),
                                            max(mean_percent_errors)))
    print('$B$ (m)\t$H_0$ (m)\t$H_1$ (m)\t$H_2$ (m)\t$H_3$ (m)\t$H_4$ (m)')
    string_5m = ''
    for i in range(len(keys_5m)):
        string_5m += '\t' + str(int(keys_5m[i]))
    print('5' + string_5m)
    string_20m = ''
    for i in range(len(keys_20m)):
        string_20m += '\t' + str(int(keys_20m[i]))
    print('20' + string_20m)
    string_mpe = ''
    for i in range(len(mean_percent_errors)):
        string_mpe += '\t{0:.2E}'.format(mean_percent_errors[i])
    print(r'\textbf{MPE (\%)}' + string_mpe)


if __name__ == '__main__':
    main()
