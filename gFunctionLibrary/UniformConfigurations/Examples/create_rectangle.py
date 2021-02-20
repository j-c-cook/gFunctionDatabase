# Jack C. Cook
# 7/1/20

# Creating borehole fields in an rectangular configuration
"""
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
"""

import Create_Rectangular_Fields as fieldgen


def main():
    # Four boreholes in a line
    # -------- inputs ----------
    BottomY = 10  # nrows in Y from bottom
    LeftX = 10    # nrows in x from left
    TopY = 0     # nrows in y from top
    RightX = 0   # nrows in x from right

    SpaceX = 5   # borehole spacing in the x
    SpaceY = 5   # borehole spacing in the y

    DistanceX = (LeftX - 1) * SpaceX  # total distance covered in the x
    DistanceY = (BottomY - 1) * SpaceY  # total distance covered in the y

    # --------------------------

    fgen = fieldgen.Gen_Field.FieldGenerator(BottomY=BottomY, LeftX=LeftX, SpaceX=SpaceX, SpaceY=SpaceY,
                                             DistanceX=DistanceX, DistanceY=DistanceY, RightX=RightX,
                                             TopY=TopY, Name='rectangle')
    print(fgen.borehole_locations)
    fgen.__display_field__(show_plot=True, save_plot=True)
    fgen.__export_field__()


if __name__ == '__main__':
    main()
