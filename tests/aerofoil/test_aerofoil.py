from os.path import join, exists, dirname, abspath
from os import makedirs
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../")  # so uggo thanks to atom runner
import unittest
from uav_design_system import aerofoil
import numpy as np


class Test(unittest.TestCase):

    def setUp(self):
        nodes1 = np.asfortranarray([[0, 0], [0.5, 0], [1, 0]])
        nodes2 = np.asfortranarray([[0, 0], [0.5, 0.5], [1, 1]])

        p_surface = aerofoil.Surface(nodes1, degree = 1)
        s_surface = aerofoil.Surface(nodes2, degree = 1)
        self.aerofoil = aerofoil.Aerofoil(s_surface, p_surface)

    def tearDown(self):
        pass

    def test_get_top_bottom(self):

        y_pressure, y_suction = self.aerofoil.get_maxmin_y(0.5, x0 = np.float(0.2))

        self.assertEqual(y_pressure, 0)
        self.assertEqual(y_suction, 0.5)

    def test_get_top_bottom_dev(self):

        aero = aerofoil.Aerofoil.develop_aerofoil(0.2, 0.2, 0.2, 0.2, 0.2)
        y_pressure, y_suction = aero.get_maxmin_y(0.5, x0 = np.float(0.2))
        self.assertAlmostEqual(y_pressure, 0.0712798523671)
        self.assertAlmostEqual(y_suction, 0.156091116794)


if __name__ == "__main__":
    unittest.main()
