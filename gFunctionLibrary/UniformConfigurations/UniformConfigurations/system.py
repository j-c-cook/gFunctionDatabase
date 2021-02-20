# Jack Cook
# Thursday, October 17, 2019

# TODO: everything pertaining to the system

from sys import platform
import os


def syscheck():
    if "darwin" in platform or "linux" in platform:
        slash = r'/'
    elif platform == "win32" or platform == "win64":
        slash = '\\'
    return slash


def check_output_dirs(output_location):
    if not os.path.exists(output_location):
        os.makedirs(output_location)
