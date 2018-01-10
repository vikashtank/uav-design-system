from os.path import join, exists, dirname, abspath
from os import makedirs, remove
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../")  # so uggo thanks to atom runner
import unittest
from uav_design_system import aerofoil, layout
import numpy as np
from matplotlib import pyplot as plt

class TestAerofoil(unittest.TestCase):

    def setUp(self):
        self.nodes1 = np.asfortranarray([[0, 0], [0.5, 0], [1, 0]])
        self.nodes2 = np.asfortranarray([[0, 0], [0.5, 0.5], [1, 1]])

        p_surface = aerofoil.Surface(self.nodes1, degree = 1)
        s_surface = aerofoil.Surface(self.nodes2, degree = 1)
        self.aerofoil = aerofoil.Aerofoil(s_surface, p_surface)

    def tearDown(self):
        pass

    def test_get_top_bottom(self):
        """
        test function returns the upper surface y and lower surface y from a
        x coordinate
        """
        y_pressure, y_suction = self.aerofoil.get_maxmin_y(0.5, x0 = np.float(0.2))

        self.assertEqual(y_pressure, 0)
        self.assertEqual(y_suction, 0.5)

    def test_get_top_bottom_dev(self):

        aero = aerofoil.Aerofoil.develop_aerofoil(0.2, 0.2, 0.2, 0.2, 0.2)
        y_pressure, y_suction = aero.get_maxmin_y(0.5, x0 = np.float(0.2))
        self.assertAlmostEqual(y_pressure, 0.0712798523671)
        self.assertAlmostEqual(y_suction, 0.156091116794)

    def test_fits_false(self):
        """
        tests that the rectangle does not fit inside the aerofoil
        """
        rectangle = layout.Rectangle(1, 1)
        self.assertFalse(self.aerofoil.check_fits(rectangle))

        rectangle = layout.Rectangle(0.5, 0.5)
        rectangle.location = layout.Point2D(0.5, 0.5)
        self.assertFalse(self.aerofoil.check_fits(rectangle))

        rectangle = layout.Rectangle(0.5, 0.5)
        rectangle.location = layout.Point2D(0.75, 0)
        self.assertFalse(self.aerofoil.check_fits(rectangle))

    def test_fits_false_outrange(self):
        """
        tests function returns false when the rectangle is not within the x
        range of the aerofoil
        """
        rectangle = layout.Rectangle(0.5, 0.5)
        rectangle.location = layout.Point2D(1, 0)
        self.assertFalse(self.aerofoil.check_fits(rectangle))

        rectangle = layout.Rectangle(0.5, 0.5)
        rectangle.location = layout.Point2D(2, 0)
        self.assertFalse(self.aerofoil.check_fits(rectangle))

    def test_fits_true(self):
        """
        tests where rectangles do fit inside a dummy aerofoil class
        """
        rectangle = layout.Rectangle(0.3, 0.3)
        rectangle.location = layout.Point2D(0.5, 0.1)
        self.assertTrue(self.aerofoil.check_fits(rectangle))

        rectangle = layout.Rectangle(0.5, 0.5)
        rectangle.location = layout.Point2D(0.75, 0.25)
        self.assertTrue(self.aerofoil.check_fits(rectangle))

    def test_fits_true_real_aerofoil(self):
        """
        test rectangle fits into an actual aerofoil shape
        """
        aero = aerofoil.Aerofoil.develop_aerofoil(0.2, -0.2, 0.2, 0.2, 0.2)
        rectangle = layout.Rectangle(0.1, 0.1)
        rectangle.location = layout.Point2D(0.1, 0.05)
        self.assertTrue(aero.check_fits(rectangle))

    def test_multiply(self):
        """
        tests aerofoil can be scaled by multiplication
        """
        new_aerofoil  = self.aerofoil * 3
        ps_nodes = new_aerofoil.pressure_surface.nodes
        ss_nodes = new_aerofoil.suction_surface.nodes

        for i in range(3):
            for j in [0, 1]:
                self.assertEqual(ps_nodes[i][j], self.nodes1[i][j] * 3)

        for i in range(3):
            for j in [0, 1]:
                self.assertEqual(ss_nodes[i][j], self.nodes2[i][j] * 3)

class TestAerofoilWrite(unittest.TestCase):

    def setUp(self):
        self.aerofoil = aerofoil.Aerofoil.develop_aerofoil(0.2, 0.2, 0.2, 0.2, 0.2)
        self.test_file = join(this_directory, "test_file.txt")

    def tearDown(self):
        remove(self.test_file)

    def test_write(self):

        with open(self.test_file, "w") as open_file:
            self.aerofoil.write(open_file)

        self.assertTrue(exists(self.test_file))


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

    def test_multiply(self):
        """
        test surface can be scaled by multiplication
        """
        new_surface = self.p_surface * 2
        expected_nodes = np.asfortranarray([[0, 0], [1, 0], [2, 0]])

        for i in range(3):
            for j in [0, 1]:
                self.assertEqual(new_surface.nodes[i][j], expected_nodes[i][j])


        new_surface = self.p_surface * 3
        expected_nodes = np.asfortranarray([[0, 0], [1.5, 0], [3, 0]])

        for i in range(3):
            for j in [0, 1]:
                self.assertEqual(new_surface.nodes[i][j], expected_nodes[i][j])



if __name__ == "__main__":
    unittest.main()
