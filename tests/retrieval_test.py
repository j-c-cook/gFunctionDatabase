import unittest

import gFunctionDatabase as gfdb


class TestRetrieval(unittest.TestCase):

    def setUp(self):
        # Note: The rectangle cases contain more NxM layouts than the other
        # cases. This is an artifact of the maximum dimensions of all cases
        # is 32x32, but the rectangle cases contain fields like 1x99.
        self.configuration_count = {'C': 465, 'L': 495, 'LopU': 465,
                                    'Open': 871, 'U': 1177, 'rectangle': 1651,
                                    'zoned': 410}

    def test_configuration_count(self):
        current_configuration_count = {}
        base_retrieval = \
            gfdb.DatabaseManagement.retrieval.BaseRetrieval()
        for key in base_retrieval.levels:
            configuration = base_retrieval.load_data(key)
            count = len(list(configuration.keys()))
            current_configuration_count[key] = count
            del configuration
        self.assertEqual(current_configuration_count, self.configuration_count)
