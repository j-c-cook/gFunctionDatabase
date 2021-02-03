# Jack C. Cook
# Tuesday, February 2, 2020

"""
**dimensioning_rules.py**

The following goals will be accomplished in this example:
    1) proof that g-functions vary based on ln(t/ts), B/H, D/H, and rb/H
    2) proof that interpolation over B/H is accurate
"""

import gFunctionLibrary as gfl
import matplotlib.pyplot as plt


def main():
    # Part 1) Prove that the g-functions vary based on ln(t/ts), B/H, D/H, and rb/H visually and mathematically
    # Part A) Collect and plot the g-functions for a library file for a 7x10 borefield where B=5
    path_to_lib_files: str = 'files/lib/'  # each of the files in here have g-functions like will be stored in lookup
    bf_5m_lib = gfl.handle_contents.Borefield(gfl.fileio.js_r(path_to_lib_files + '7x10_B_5_nbh_70.json'))
    fig_1, ax_1 = bf_5m_lib.visualize_g_functions()

    # Part B) Collect the g-functions for the library file for a 7x10 borefield where B=20
    #         Determine the error when computing B/H values
    bf_20m_lib = gfl.handle_contents.Borefield(gfl.fileio.js_r(path_to_lib_files + '7x10_B_20_nbh_70.json'))
    # If Eskilson was right, and the dimensioning rules are accurate, then the following mean percent errors will be ~0
    keys_5m = list(reversed(list(bf_5m_lib.g.keys())))
    keys_5m = keys_5m[2:]
    print('The heights that will be used in the from the 5m library file:')
    print(keys_5m)
    print('The heights that will be used in the from the 20m library file:')
    keys_20m = list(reversed(list(bf_20m_lib.g.keys())))
    print(keys_20m)

    mean_percent_errors = []
    for i in range(len(keys_5m)):
        mean_percent_error = gfl.statistics.mpe(bf_5m_lib.g[keys_5m[i]], bf_20m_lib.g[keys_20m[i]])
        mean_percent_errors.append(mean_percent_error)
    print('Mean percent errors between g-functions')
    print(mean_percent_errors)

    # Part C) Plot the g-functions for the B=20 7x10 borefield
    lines = []
    for i, key in enumerate(keys_20m):
        line, = ax_1.plot(bf_20m_lib.log_time, bf_20m_lib.g[key], marker='o', ls='None', color='C' + str(i + 2),
                          markersize=3,
                          label=str(int(bf_20m_lib.B)) + '/' + str(key))
        lines.append(line)

    # Part D) Plot a B/H of 0.0625 which is 8/128 and 5/8
    path_to_computed = 'files/computed/'
    bf_computed_5m = gfl.handle_contents.Borefield(gfl.fileio.js_r(path_to_computed + '7x10_B_5_nbh_70.json'))
    bf_computed_8m = gfl.handle_contents.Borefield(gfl.fileio.js_r(path_to_computed + '7x10_B_8_nbh_70.json'))
    line_7, = ax_1.plot(bf_computed_5m.log_time, bf_computed_5m.g[80], ls=(0, (3, 5, 1, 5)),
                        label=str(int(bf_computed_5m.B)) + '/' + str(80), zorder=2)
    line_8, = ax_1.plot(bf_computed_5m.log_time, bf_computed_8m.g[128], ls='dashed',
                        label=str(int(bf_computed_5m.B)) + '/' + str(128), zorder=1)
    lines.append(line_7)
    lines.append(line_8)
    second_legend = fig_1.legend(handles=lines,
                                 title='B/H'.rjust(8) + '\nComputed', bbox_to_anchor=(1.005, 0.6))
    fig_1.gca().add_artist(second_legend)

    # Part E) Annotate the plot with the borehole layout and the D/H, rb/H
    # add in a sub axes plot with the borehole layout
    sub_axes = plt.axes([.0, .47, .5, .5])
    x, y = list(zip(*bf_5m_lib.bore_locations))
    sub_axes.scatter(x, y)
    sub_axes.set_aspect('equal')
    sub_axes.axis('off')
    # annotate the layout with B spacings
    sub_axes.annotate(text='', xy=(0, 0), xytext=(5, 0), arrowprops=dict(arrowstyle='<->'))
    sub_axes.annotate(text='', xy=(0, 0), xytext=(0, 5), arrowprops=dict(arrowstyle='<->'))
    ax_1.text(-7.8, 53, 'B')
    ax_1.text(-8.5, 62, 'B')
    # add in text for D/H and rb/H
    ax_1.text(-3.5, 124, '$\dfrac{r_b}{H}$=0.0005', fontsize=12)
    ax_1.text(-3.5, 111, '$\dfrac{D}{H}$=0.02083', fontsize=12)

    fig_1.savefig('dimensioning_rules_figure_01.png')

    # Part F) Interpolate for a B/H = 0.0625
    B: float = 8.
    H: float = 128.
    B_over_H: float = B / H
    interpolation_kinds = ['linear', 'quadratic', 'cubic']
    g_functions = []
    for kind in interpolation_kinds:
        g_function = bf_5m_lib.g_function_interpolation(B_over_H, kind=kind)
        bf_5m_lib.interpolation_table = {}  # this needs reset to recompute the table with a new kind
        g_functions.append(g_function)
    mean_percentage_errors = []
    for i in range(len(g_functions)):
        MPE = gfl.statistics.mpe(bf_computed_5m.g[80], g_functions[i])
        mean_percentage_errors.append(MPE)
    print('The errors associated with different interpolation methods:')
    for i in range(len(interpolation_kinds)):
        print('\t{0}:\t{1:.2f}%'.format(interpolation_kinds[i], mean_percentage_errors[i]))
    mean_percent_errors_abs = list(map(abs, mean_percentage_errors))
    idx = mean_percent_errors_abs.index(min(mean_percent_errors_abs))
    print(idx)
    g_function = g_functions[idx]
    line_10, = ax_1.plot(bf_5m_lib.log_time, g_function, marker='^', zorder=0, color='C9', markersize=5, ls='None',
                         label='0.0625')

    third_legend = fig_1.legend(handles=[line_10],
                                title='B/H'.rjust(10) + '\nInterpolated', bbox_to_anchor=(1.005, 0.2))
    fig_1.gca().add_artist(third_legend)

    fig_1.savefig('dimensioning_rules_figure_02.png')
    plt.close(fig_1)


if __name__ == '__main__':
    main()
