from os.path import join, exists, dirname, abspath
from os import makedirs
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../")  # so uggo thanks to atom runner
import unittest
import uav_design_system.optimisation as opt

class TestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_(self):
        pass


if __name__ == "__main__":
    unittest.main()
