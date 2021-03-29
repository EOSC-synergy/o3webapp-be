# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - 2019 Karlsruhe Institute of Technology - Steinbuch Centre for Computing
# This code is distributed under the GNU GPLv3 License
# Please, see the LICENSE file
#

import unittest

class TestPackageMethods(unittest.TestCase):
    """ Class to unit tests
    """
    # Placeholder for tests
    def setUp(self):
        self.FakeTest = True

    def test_faketest_type(self):
        """Test of the variable FakeTest
        """
        self.assertTrue(type(self.FakeTest) is bool)



