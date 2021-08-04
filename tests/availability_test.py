import unittest

import gFunctionDatabase as gfdb
from natsort.natsort import natsorted


def get_current_available_data_files():
    _, available_data_files = gfdb.Database.available.find_data_files()
    return natsorted(available_data_files)


class TestAvailableData(unittest.TestCase):

    def setUp(self):
        self.available_data_files = \
            ['L_configurations_5m.json', 'LopU_configurations_5m.json',
             'Open_configurations_5m.json', 'U_configurations_5m.json',
             'rectangle_5m.json', 'zoned_rectangle_5m.json']

    def test_available(self):
        available_data_files = get_current_available_data_files()
        self.assertEqual(available_data_files, self.available_data_files)


if __name__ == '__main__':
    unittest.main()
