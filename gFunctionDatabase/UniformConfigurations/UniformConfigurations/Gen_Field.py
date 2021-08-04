# Jack C. Cook
# 7/1/20

# Original: Thursday, December 12, 2019
# Modification for ease of use by all July 1, 2020

import matplotlib.pyplot as plt
import pandas as pd


def generate_pairs(self):
    """
    This function makes use off all the methods inside of FieldGenerator
    A list of (x, y) pairs are generated
    :return: a list of (x, y) pairs defining the borehole field
    """
    object_methods = [method_name for method_name in dir(self)
                      if callable(getattr(self, method_name)) and not method_name.startswith("__")]
    pairs_list = []
    for i in range(len(object_methods)):
        pair_func = getattr(self, object_methods[i])
        new_pairs = pair_func()
        pairs_list.extend(new_pairs)
    return pairs_list


class FieldGenerator:
    def __init__(self, BottomY=0, LeftX=0, TopY=0, RightX=0, SpaceX=0, SpaceY=0, DistanceX=0, DistanceY=0,
                 D=0, H=0, inclination=0, direction=0, Name='noname'):
        """
        Create any Line, L, U, Open rect, rect
        :param BottomY: The number of rows from the bottom of the field
        :param LeftX: the number of boreholes in the x-direction heading left starting from the far right of the field
        :param TopY: the number of rows from the top heading in the y direction down
        :param RightX: the number of rows from the right of the field heading in the x direction to the right
        :param SpaceX: the spacing of the borehole field in the x-direction
        :param SpaceY: the spacing of the borehole field in the y-direction
        :param DistanceX: the total distance in the x direction of the field
        :param DistanceY: the total distance in the y direction of the field
        """
        self.BottomY: int = BottomY
        self.LeftX: int = LeftX
        self.TopY: int = TopY
        self.RightX: int = RightX
        self.SpaceX: float = SpaceX
        self.SpaceY: float = SpaceY
        self.DistanceX: float = DistanceX
        self.DistanceY: float = DistanceY
        pairs_list = generate_pairs(self)
        self.borehole_locations = list(set(pairs_list))
        self.D = D
        self.H = H
        self.inclination = inclination
        self.direction = direction
        self.path = Name

    def bottom_left(self):
        """
        This is the bottom left corner control
        :return: list of (x, y) coordinates with origin as bottom left corner
        """
        if self.SpaceX == 0:
            return []
        else:
            Nx = int(self.DistanceX / self.SpaceX) + 1
            return [(i * self.SpaceX, j * self.SpaceY) for j in range(self.BottomY) for i in range(Nx)]

    def bottom_right(self):
        """
        The bottom right corner
        :return: list of (x, y) coordinates with origin of the bottom right corner
        """
        if self.SpaceY == 0:
            return []
        else:
            Ny = int(self.DistanceY / self.SpaceY) + 1
            xes = [i * self.SpaceX for i in range(self.RightX)]
            return [(self.DistanceX - xes[i], j * self.SpaceY) for j in range(Ny) for i in range(len(xes))]

    def top_right(self):
        """
        The control of the top right corner
        :return: list of (x, y) coordinates with origin at the top right
        """
        if self.SpaceX == 0:
            return []
        else:
            Nx = int(self.DistanceX / self.SpaceX) + 1
            yes = [j * self.SpaceY for j in range(self.TopY)]
            return [(i * self.SpaceX, self.DistanceY - yes[j]) for j in range(len(yes)) for i in range(Nx)]

    def top_left(self):
        """
        The control of the top left corner
        :return: list of (x, y) coordinates with origin at the top left
        """
        if self.SpaceY == 0:
            return []
        else:
            Ny = int(self.DistanceY / self.SpaceY) + 1
            yes = [i * self.SpaceY for i in range(Ny)]
            return [(i * self.SpaceX, yes[j]) for j in range(len(yes)) for i in range(self.LeftX)]

    def __display_field__(self, path: str = None, show_plot: bool = False, save_plot: bool = False):
        """
        Plot a field of boreholes, choose to either save to path, show the plot, or never see the plot at all
        :param path: an optional path to save the plot
        :param show_plot: an optional argument to show the plot
        :return: None
        """
        if show_plot is False:
            plt.switch_backend('agg')  # make compatible for non display CPU's (ie. Linux cluster)

        x_locations, y_locations = list(zip(*self.borehole_locations))
        fig, ax = plt.subplots()
        ax.scatter(x_locations, y_locations)

        if save_plot is True:
            fig.savefig(self.path + '.pdf')

        if show_plot is True:
            fig.show()

        plt.close(fig)  # close out the figure, make nullptr
        return

    def __export_field__(self, units: str = 'm'):
        location_dictionary = {}
        x_locations, y_locations = list(zip(*self.borehole_locations))
        location_dictionary['x(' + units + ')'] = x_locations
        location_dictionary['y(' + units + ')'] = y_locations
        location_dictionary['z(' + units + ')'] = [self.D] * len(x_locations)
        location_dictionary['length(' + units + ')'] = [self.H] * len(x_locations)
        location_dictionary['inclination angle - from vertical'] = [self.inclination] * len(x_locations)
        location_dictionary['direction angle - CW from N'] = [self.direction] * len(x_locations)

        path = self.path

        if '.' in path:
            path_split = path.split('.')
            path_extension = path_split[-1]
            file_path = path_split[0:len(path_split)-1]
            file_path = '.'.join(file_path)
        else:
            file_path = path
            path_extension = 'csv'  # default extension

        acceptable_extensions = ['txt', 'json', 'xlsx', 'csv']

        if path_extension not in acceptable_extensions:
            raise ValueError('Not an acceptable path extension, please use one of: ' + ' '.join(acceptable_extensions))

        file_path_output = file_path + '.' + path_extension

        if path_extension == 'xlsx':
            pd.DataFrame(location_dictionary).to_excel(file_path_output)
        elif path_extension == 'csv':
            pd.DataFrame(location_dictionary).to_csv(file_path_output)
        else:
            raise ValueError('Either you did not provide an appropriate extension style or this code is incomplete.')
