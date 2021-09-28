# Jack C. Cook
# Tuesday, September 28, 2021

import gFunctionDatabase as gfdb
import matplotlib.pyplot as plt


def main():
    # Ensure that the interpolation procedure implemented is accurate

    # The configuration used in this example is a 7x10 with uniform spacing
    Nx = 7
    Ny = 10

    # Use Eskilson's 27 logarithmic times
    log_time = gfdb.utilities.Eskilson_log_times()

    # Part A) Compute a g-function for B/H of 0.0625, B/H=8/128
    B = 8.
    D_values = [2.6624]
    H_values = [128.]
    r_b_values = [0.064]
    nSegments = [12] * len(D_values)
    alpha = 1.0e-06

    # Get the (x, y) rectangular coordinates
    r_coodinates = gfdb.coordinates.rectangle(Nx, Ny, B, B)
    g_data = gfdb.Management.application. \
        uniform_temperature_uniform_segment_lengths(D_values, H_values,
                                                    r_b_values, B, log_time,
                                                    alpha, r_coodinates,
                                                    nSegments)
    GFunction_input = gfdb.Management.application.GFunction. \
        configure_database_file_for_usage(g_data)
    GFunction_8m = gfdb.Management.application.GFunction(**GFunction_input)

    # Part B) Compute 5 g-function curves for B/H curves with a B spacing of 5m
    B = 5.
    D_values = [0.5, 1., 2., 4., 8.]
    H_values = [24., 48., 96., 192., 384.]
    r_b_values = [0.012, 0.024, 0.048, 0.096, 0.192]
    nSegments = [12] * len(D_values)
    r_coodinates = gfdb.coordinates.rectangle(Nx, Ny, B, B)
    g_data = gfdb.Management.application. \
        uniform_temperature_uniform_segment_lengths(D_values, H_values,
                                                    r_b_values, B, log_time,
                                                    alpha, r_coodinates,
                                                    nSegments)
    GFunction_input = gfdb.Management.application.GFunction. \
        configure_database_file_for_usage(g_data)
    GFunction_5m = gfdb.Management.application.GFunction(**GFunction_input)

    # Part C) Plot the g-function curves
    fig, ax = GFunction_5m.visualize_g_functions()
    height_0 = list(GFunction_8m.g_lts.keys())[0]
    line, = ax.plot(GFunction_8m.log_time, GFunction_8m.g_lts[height_0],
            ls=(0, (3, 5, 1, 5)),
            label=str(int(GFunction_8m.B)) + '/' + str(int(height_0)), zorder=2)

    # Annotate the plot with the borehole layout and the D/H, rb/H
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
    ax.text(-7.8, 53, 'B')
    ax.text(-8.5, 62, 'B')
    # add in text for D/H and rb/H
    ax.text(-3.5, 124, '$\dfrac{r_b}{H}$=0.0005', fontsize=12)
    ax.text(-3.5, 111, '$\dfrac{D}{H}$=0.02083', fontsize=12)

    # Make the legend for the reference g-function curve
    lines = [line]
    second_legend = fig.legend(handles=lines,
                                 title='B/H'.rjust(8) + '\n' + 'Reference',
                                 bbox_to_anchor=(1.005, 0.6))
    fig.gca().add_artist(second_legend)

    # Part D) Interpolate for a B/H = 0.0625
    B: float = 8.
    H: float = 128.
    B_over_H: float = B / H
    interpolation_kinds = ['linear', 'quadratic', 'cubic', 'lagrange']
    # Store the g-function interpolated with different procedures
    g_functions = []
    for kind in interpolation_kinds:
        g_function, rb_value, D_value, H_eq = \
            GFunction_5m.g_function_interpolation(B_over_H, kind=kind)
        # this needs reset to recompute the table with a new kind
        GFunction_5m.interpolation_table = {}
        g_functions.append(g_function)
    mean_percentage_errors = []
    for i in range(len(g_functions)):
        MPE = gfdb.statistics.mpe(GFunction_8m.g_lts[height_0], g_functions[i])
        mean_percentage_errors.append(MPE)
    print('The errors associated with different interpolation methods:')
    for i in range(len(interpolation_kinds)):
        print('\t{0}:\t{1:.2f}%'.format(interpolation_kinds[i],
                                        mean_percentage_errors[i]))
    mean_percent_errors_abs = list(map(abs, mean_percentage_errors))
    idx = mean_percent_errors_abs.index(min(mean_percent_errors_abs))
    print('{} interpolation is the most accurate'.format(
        interpolation_kinds[idx]))
    g_function = g_functions[idx]
    line, = ax.plot(log_time, g_function, marker='^', zorder=0, color='C9',
                       markersize=5, ls='None', label='0.0625')
    lines = [line]
    third_legend = fig.legend(handles=lines,
                              title='B/H'.rjust(10) + '\nInterpolated',
                              bbox_to_anchor=(1.005, 0.2))
    fig.gca().add_artist(third_legend)

    fig.savefig('interpolation.png')

    # Now check to see the accuracy of interpolation with reduced curves
    # first remove the highest height, then the lowest height, then the highest
    # height
    print('#Ref g-functions\tLinear\tQuadratic\tCubic\tLagrange')
    sign = 1
    for _ in range(4):
        g_functions = []
        for kind in interpolation_kinds:
            g_function, rb_value, D_value, H_eq = \
                GFunction_5m.g_function_interpolation(B_over_H, kind=kind)
            # this needs reset to recompute the table with a new kind
            GFunction_5m.interpolation_table = {}
            g_functions.append(g_function)
        mean_percentage_errors = ''
        for i in range(len(g_functions)):
            MPE = gfdb.statistics.mpe(GFunction_8m.g_lts[height_0],
                                      g_functions[i])
            mean_percentage_errors += '\t' + str(round(MPE, 3))
        # Get number of height values still in GFunction
        height_values = list(GFunction_5m.g_lts.keys())
        # Add to the table
        print(str(len(height_values)) + mean_percentage_errors)

        if sign == 1:
            # remove max height
            h = max(height_values)
        else:
            # remove min height
            h = min(height_values)
        del GFunction_5m.g_lts[h]
        del GFunction_5m.r_b_values[h]
        del GFunction_5m.D_values[h]
        sign *= -1


if __name__ == '__main__':
    main()
