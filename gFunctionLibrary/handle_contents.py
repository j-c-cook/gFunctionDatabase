# Jack C. Cook
# Tuesday, February 2, 2021

"""
**handle_contents.py**

A module that handles the contents of the g-function library
"""

import matplotlib.pyplot as plt
import math
from scipy.interpolate import interp1d, lagrange


class Borefield:
    """
    An object that keeps the data for a specific borefield g-function calculation in order

    Parameters
    ----------
    data: dict
        A dictionary which is in the output format of cpgfunction.
    """
    def __init__(self, data: dict):
        self.bore_locations: list = []  # (x, y) coordinates of boreholes
        self.g: dict = {}  # g-functions keyed by height
        self.r_bs: dict = {}  # r_b (borehole radius) value keyed by height
        self.Ds: dict = {}  # D (burial depth) value keyed by height
        self.log_time: list = []  # ln(t/ts) values that apply to all the heights
        self.time: dict = {}  # the time values in years
        self.B: float = math.nan  # a B spacing in the borefield
        self.read_cpgfunction_output(data)

        self.interpolation_table: dict = {}  # an interpolation table for B/H ratios, D, r_b

    def read_cpgfunction_output(self, data) -> None:
        """
        This method is called upon initialization of the object.

        Read the cpgfunction output dictionary into the borefield class for easy access of information

        Parameters
        ----------
        data: dict
            A dictionary which is in the output format of cpgfunction.

        Returns
        -------
            None
        """
        self.log_time = data['logtime']

        self.bore_locations = data['bore_locations']  # store the bore locations in the object
        g_values: dict = data['g']  # pull the g-functions into the g_values
        g_tmp: dict = {}  # a temporary g-function dictionary that might be out of order
        Ds_tmp: dict = {}  # a temporary burial depth dictionary that may be out of order
        r_bs_tmp: dict = {}  # the borehole radius dictionary that may be out of order
        t_tmp: dict = {}
        for key in g_values:
            # do the g-function dictionary
            key_split = key.split('_')
            # get the current height
            # TODO: change this to a rounded float to n decimal places
            height = int(float((key_split[1])))
            # create a g-function list associated with this height key
            g_tmp[height] = g_values[key]
            # create a r_b value associated with this height key
            r_b = float(key_split[2])
            r_bs_tmp[height] = r_b
            try:  # the D value is recently added to the key value for the saved g-functions computed
                D = float(key_split[3])
                Ds_tmp[height] = D
            except:
                pass

            # do the time dictionary
            time_arr: list = []
            for _, log_time in enumerate(self.log_time):
                alpha = 1.0e-06
                t_seconds = height ** 2 / 9 / alpha * math.exp(log_time)
                t_year = t_seconds / 60 / 24 / 365
                time_arr.append(t_year)
            t_tmp[height] = time_arr

        self.B = float(list(g_values.keys())[0].split('_')[0])  # every B-spacing should be the same for each file

        keys = sorted(list(g_tmp.keys()), key=int)  # sort the heights in order

        self.g = {key: g_tmp[key] for key in keys}  # fill the g-function dictionary with sorted heights
        try:
            self.Ds = {key: Ds_tmp[key] for key in keys}  # fill the burial depth dictionary with sorted heights
        except:
            pass
        self.r_bs = {key: r_bs_tmp[key] for key in keys}
        self.time = {key: t_tmp[key] for key in keys}  # fill the time array for yearly points

        return

    def g_function_interpolation(self, B_over_H: float, kind='cubic'):
        """
        Interpolate a range of g-functions for a specific B/H ratio

        Parameters
        ----------
        B_over_H: float
            A B/H ratio
        kind: str
            Could be 'linear', 'quadratic', 'cubic', etc.
            default: 'cubic'

        Returns
        -------
        **g-function: list**
            A list of the g-function values for each ln(t/ts)
        **rb: float**
            A borehole radius value that is interpolated for
        **D: float**
            A burial depth that is interpolated for
        **H_eq: float**
            An equivalent height

            .. math::

                H_{eq} = \dfrac{B_{field}}{B/H}
        """
        # the g-functions are stored in a dictionary based on heights, so an equivalent height can be found
        H_eq = 1 / B_over_H * self.B
        # if the interpolation table is not yet know, build it
        if len(self.interpolation_table) == 0:
            # create an interpolation for the g-function which takes the height (or equivilant height) as an input
            # the g-function needs to be interpolated at each point in dimensionless time
            self.interpolation_table['g'] = []
            for i, lntts in enumerate(self.log_time):
                x = []
                y = []
                for key in self.g:
                    height_value = float(key)
                    g_value = self.g[key][i]
                    x.append(height_value)
                    y.append(g_value)
                if kind == 'lagrange':
                    f = lagrange(x, y)
                else:
                    f = interp1d(x, y, kind=kind)
                self.interpolation_table['g'].append(f)
            # create interpolation tables for 'D' and 'r_b' by height
            keys = list(self.r_bs.keys())
            height_values: list = []
            rb_values: list = []
            D_values: list = []
            for h in keys:
                height_values.append(float(h))
                rb_values.append(self.r_bs[h])
                try:
                    D_values.append(self.Ds[h])
                except:
                    pass
            if kind == 'lagrange':
                rb_f = lagrange(height_values, rb_values)
            else:
                rb_f = interp1d(height_values, rb_values, kind=kind)  # interpolation function for rb values by H equivalent
            self.interpolation_table['rb'] = rb_f
            try:
                if kind == 'lagrange':
                    D_f = lagrange(height_values, D_values)
                else:
                    D_f = interp1d(height_values, D_values, kind=kind)
                self.interpolation_table['D'] = D_f
            except:
                pass

        # create the g-function by interpolating at each ln(t/ts) value
        rb_value = self.interpolation_table['rb'](H_eq)
        try:
            D_value = self.interpolation_table['D'](H_eq)
        except:
            D_value = None
        g_function: list = []
        for i in range(len(self.log_time)):
            f = self.interpolation_table['g'][i]
            g = f(H_eq).tolist()
            g_function.append(g)
        return g_function, rb_value, D_value, H_eq

    def visualize_g_functions(self):
        """
        Visualize the g-functions.

        Returns
        -------
        **fig, ax**
            Figure and axes information.
        """
        fig, ax = plt.subplots()

        ax.set_xlim([-8.8, 3.9])
        ax.set_ylim([-2, 139])

        ax.text(2.75, 135, 'B/H')

        keys = reversed(list(self.g.keys()))

        for key in keys:
            ax.plot(self.log_time, self.g[key], label=str(int(self.B)) + '/' + str(key))
            x_n = self.log_time[-1]
            y_n = self.g[key][-1]
            if key == 8:
                ax.annotate(str(round(float(self.B) / float(key), 4)), xy=(x_n - .4, y_n - 5))
            else:
                ax.annotate(str(round(float(self.B) / float(key), 4)), xy=(x_n-.4, y_n+1))

        handles, labels = ax.get_legend_handles_labels()

        legend = fig.legend(handles=handles, labels=labels, title='B/H'.rjust(5) + '\nLibrary',
                            bbox_to_anchor=(1, 1.0))
        fig.gca().add_artist(legend)

        ax.set_ylabel('g')
        ax.set_xlabel('ln(t/t$_s$)')
        ax.grid()
        ax.set_axisbelow(True)
        fig.subplots_adjust(left=0.09, right=0.835, bottom=0.1, top=.99)

        return fig, ax

    def visualize_borefield(self):
        """
        Visualize the (x,y) coordinates.

        Returns
        -------
        **fig, ax**
            Figure and axes information.
        """
        fig, ax = plt.subplots(figsize=(3.5,5))

        x, y = list(zip(*self.bore_locations))

        ax.scatter(x, y)

        ax.set_xlabel('x (m)')
        ax.set_ylabel('y (m)')

        ax.set_aspect('equal')
        fig.tight_layout()

        return fig, ax
