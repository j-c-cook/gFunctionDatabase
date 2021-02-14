# Jack C. Cook
# Thursday, October 17, 2019

# Modified: Sunday, September 20, 2020
# Modified: Wednesday, February 10, 2021

"""
platform_specific.py

Almost all things in python are platform independent, however the "slash"
in file paths is different on Unix and windows. Therefore, a function that
"splits by the slash" must be aware of the platform.
"""

from sys import platform


def get_slash_style() -> str:
    """
    Determine whether the slash should be forwards or backwards based on the system being used

    Returns
    -------
    slash: str
        a forward or backwards slash

    """

    forward_slash_platforms = ['darwin', 'linux']
    backward_slash_platforms = ['win32', 'win64']

    if platform not in forward_slash_platforms and platform not in backward_slash_platforms:
        print('Your platform is {}, please consider modifying this function'.format(platform))
        raise ValueError('The current platform is unknown to this function.')

    forward_slash = False
    backward_slash = False

    for i in range(len(forward_slash_platforms)):
        if forward_slash_platforms[i] in platform:
            forward_slash = True

    for i in range(len(backward_slash_platforms)):
        if backward_slash_platforms[i] in platform:
            backward_slash = True

    if forward_slash is True and backward_slash is True:
        raise ValueError('The slash check function improperly determined that both slash styles can be used.')

    if forward_slash is False and backward_slash is False:
        raise ValueError('The slash check function needs to be modified to check for the following system: ' + platform)

    if forward_slash is True:
        return r'/'

    if backward_slash is True:
        return '\\'
