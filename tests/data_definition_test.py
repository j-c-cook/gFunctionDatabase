import unittest

import gFunctionDatabase as gfdb


def get_current_registry():
    data_definition_base = \
        gfdb.DatabaseManagement.data_definition.BaseDefinition()
    return data_definition_base.registry


class TestDataDefinition(unittest.TestCase):

    def setUp(self):
        self.registry_keys = ['L', 'LopU', 'Open', 'U', 'rectangle', 'zoned']

    def test_registry_keys(self):
        available_registry_keys = list(get_current_registry().keys())
        self.assertEqual(available_registry_keys, self.registry_keys)
