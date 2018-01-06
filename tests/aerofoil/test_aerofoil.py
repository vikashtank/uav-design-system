from os.path import join, exists, dirname, abspath
from os import makedirs
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../")  # so uggo thanks to atom runner
import unittest
from uav_design_system import aerofoil, layout
import numpy as np

class TestAerofoil(unittest.TestCase):

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

    def test_fits_false(self):
        rectangle = layout.Rectangle(1, 1)
        self.assertFalse(self.aerofoil.check_fits(rectangle))

        rectangle = layout.Rectangle(0.5, 0.5)
        rectangle.location = layout.Point2D(0.5, 0.5)
        self.assertFalse(self.aerofoil.check_fits(rectangle))

        rectangle = layout.Rectangle(0.5, 0.5)
        rectangle.location = layout.Point2D(0.75, 0)
        self.assertFalse(self.aerofoil.check_fits(rectangle))

    def test_fits_false_outrange(self):

        rectangle = layout.Rectangle(0.5, 0.5)
        rectangle.location = layout.Point2D(1, 0)
        self.assertFalse(self.aerofoil.check_fits(rectangle))

        rectangle = layout.Rectangle(0.5, 0.5)
        rectangle.location = layout.Point2D(2, 0)
        self.assertFalse(self.aerofoil.check_fits(rectangle))

    def test_fits_true(self):

        rectangle = layout.Rectangle(0.3, 0.3)
        rectangle.location = layout.Point2D(0.5, 0.1)
        self.assertTrue(self.aerofoil.check_fits(rectangle))

        rectangle = layout.Rectangle(0.5, 0.5)
        rectangle.location = layout.Point2D(0.75, 0.25)
        self.assertTrue(self.aerofoil.check_fits(rectangle))

    def test_fits_true_real_aerofoil(self):
        aero = aerofoil.Aerofoil.develop_aerofoil(0.2, -0.2, 0.2, 0.2, 0.2)
        rectangle = layout.Rectangle(0.1, 0.1)
        rectangle.location = layout.Point2D(0.1, 0.05)
        self.assertTrue(aero.check_fits(rectangle))


class TestSurface(unittest.TestCase):

    def setUp(self):
        nodes1 = np.asfortranarray([[0, 0], [0.5, 0], [1, 0]])
        nodes2 = np.asfortranarray([[0, 0], [0.5, 0.5], [1, 1]])

        self.p_surface = aerofoil.Surface(nodes1, degree = 1)
        self.s_surface = aerofoil.Surface(nodes2, degree = 1)

    def test_get_xy_coords_flat(self):
        """
        tests get xy coordinares for a flat line
        """
        x, y= self.p_surface.get_xy_coords(num_points = 101)
        for i in range(100):
            self.assertAlmostEqual(x[i], 0.01*i)
            self.assertEqual(y[i], 0)

    def test_get_xy_coords_slope(self):
        """
        tests get xy coordinares for a sloped line
        """
        x, y= self.s_surface.get_xy_coords(num_points = 101)
        for i in range(100):
            self.assertAlmostEqual(x[i], 0.01 * i)
            self.assertAlmostEqual(y[i], 0.01 * i)




if __name__ == "__main__":
    unittest.main()
