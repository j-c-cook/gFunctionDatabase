# Jack C. Cook
# 7/1/20

import pandas as pd
from .Gen_Field import FieldGenerator
from .system import syscheck, check_output_dirs


def read_excel(path):
    df = pd.read_excel(path)
    dictionary = df.to_dict('list')
    return dictionary


class BatchProcess:
    def __init__(self, generator_description_path: str, output_path='Output'):
        """
        This is an object to take what is in the excel file for generating borehole fields and use the
        FieldGenerator object to export the fields
        :param generator_description_path:
        :param output_path:
        """
        slash = syscheck()
        check_output_dirs(output_path)
        dnary = read_excel(generator_description_path)
        self.__setup__(dnary)
        self.borefields = []
        for i in range(len(self.BottomY)):
            fgen = FieldGenerator(BottomY=self.BottomY[i], LeftX=self.LeftX[i], TopY=self.TopY[i],
                                  RightX=self.RightX[i], SpaceX=self.SpaceX[i], SpaceY=self.SpaceY[i],
                                  DistanceX=self.DistanceX[i], DistanceY=self.DistanceY[i],
                                  D=self.D[i], H=self.H[i], inclination=self.inclination[i],
                                  direction=self.direction[i], Name=output_path + slash + self.Name[i])
            fgen.__export_field__()
            self.borefields.append(fgen.borehole_locations)
            del fgen

    def __setup__(self, dnary):
        for key in dnary:
            setattr(self, key, dnary[key])
