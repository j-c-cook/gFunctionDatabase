# Jack C. Cook
# Saturday, February 6, 2021

import gFunctionLibrary as gfl
from natsort import natsorted
from PIL import Image
import os


def main():
    # Zoned Rectangle example: 7x12 field
    # ------- Inputs --------
    Nx = 7  # number of boreholes in the x-direction
    Ny = 12  # number of boreholes in the y-direction
    B = 5  # uniform spacing around outer perimeter
    # -----------------------
    z_rectangles = gfl.coordinate_generator.ZonedRectangle(Nx=Nx, Ny=Ny, B=B)
    # Plot all of the borefields created, will be saved in /ZRect/Plots/
    z_rectangles.visualize_coordinates('ZRect/Plots/', plot_ext='png')
    print(z_rectangles.coordinates)

    # Create csv files
    z_rectangles.export_coordinates('ZRect/CSVs/')

    # create a .gif from the plots we created
    # Source: https://stackoverflow.com/a/57751793/11637415
    # Note: Pillow wanted pngs for creating the gif
    file_plot_names = os.listdir('ZRect/Plots/')
    # we need to reverse the order to start from less zone to more zone, we'll use natsort to do it
    # # sort the keys by order from largest to smallest
    file_plot_names = natsorted(file_plot_names)
    file_plot_names_sorted = list(reversed(file_plot_names))
    print(file_plot_names_sorted)
    frames = []
    for file in file_plot_names_sorted:
        frames.append(Image.open('ZRect/Plots/' + file))

    frames[0].save(fp='ZRect/ZRect.gif', format='GIF', append_images=frames[0:],
                   save_all=True, duration=800, loop=0)


if __name__ == '__main__':
    main()
