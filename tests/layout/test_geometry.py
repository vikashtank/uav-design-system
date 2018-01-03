from os.path import join, exists, dirname, abspath
from os import makedirs
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../")  # so uggo thanks to atom runner
import unittest
import uav_design_system.layout as geometry


class TestCuboid(unittest.TestCase):

    def setUp(self):
        self.cuboid = geometry.Cuboid(2, 3, 4)

    def tearDown(self):
        pass

    def test_centroid(self):
        self.assertEqual(self.cuboid.centroid, geometry.Point(1, 1.5, 2))

    def test_inertias(self):
        self.assertEqual(self.cuboid.inertia_xx, 25/12)
        self.assertEqual(self.cuboid.inertia_yy, 20/12)
        self.assertEqual(self.cuboid.inertia_zz, 13/12)

    def test_reflect_y(self):
        self.assertEqual(self.cuboid.reflect_y().centroid,
                         geometry.Point(1, -1.5, 2))


class TestCylinder(unittest.TestCase):

    def setUp(self):
        self.cylinder = geometry.Cylinder(1, 10)

    def tearDown(self):
        pass

    def test_volume(self):
        pass

    def test_centroid(self):
        self.assertEqual(self.cylinder.centroid, geometry.Point(0, 5, 0))

    def test_inertias(self):
        self.assertAlmostEqual(self.cylinder.inertia_xx, 103/12)
        self.assertAlmostEqual(self.cylinder.inertia_yy, 0.5)
        self.assertAlmostEqual(self.cylinder.inertia_zz, 103/12)

    def test_reflect_y(self):
        self.assertEqual(self.cylinder.reflect_y().centroid,
                         geometry.Point(0, -5, 0))


class TestTrapeziumPlate(unittest.TestCase):

    def setUp(self):
        self.trapezium = geometry.TrapeziumPlate(6, 4, 0, 5, 1)
        self.cuboid = geometry.Cuboid(5, 5, 1)

    def tearDown(self):
        pass

    def test_volume(self):
        self.assertEqual(self.trapezium.volume, 25)

    def test_centroid(self):
        """
        test if the correct centroid is calculated
        """
        self.assertAlmostEqual(self.trapezium.centroid.x, 38/15)
        self.assertAlmostEqual(self.trapezium.centroid.y, 7/3)
        self.assertAlmostEqual(self.trapezium.centroid.z, 0.5)

    def test_centroid_square(self):
        """
        test method still works if the trapezium is a square
        """
        self.trapezium = geometry.TrapeziumPlate(5,5, 0, 5, 1)
        self.assertAlmostEqual(self.trapezium.centroid.x, 2.5)
        self.assertAlmostEqual(self.trapezium.centroid.y, 2.5)
        self.assertAlmostEqual(self.trapezium.centroid.z, 0.5)

    def test_centroid_flipped(self):
        """
        test if the correct centroid is calculated when the first side is
        smaller than the second
        """
        self.trapezium = geometry.TrapeziumPlate(4, 6, 0, 5, 1)
        self.assertAlmostEqual(self.trapezium.centroid.z, 0.5)
        self.assertAlmostEqual(self.trapezium.centroid.x, 38/15)
        self.assertAlmostEqual(self.trapezium.centroid.y, 5 - 7/3)

    def test_inertias(self):
        """
        check the trapezium inertias are equivilent to a cuboid
        """
        self.assertAlmostEqual(self.trapezium.inertia_xx, self.cuboid.inertia_xx)
        self.assertAlmostEqual(self.trapezium.inertia_yy, self.cuboid.inertia_yy)
        self.assertAlmostEqual(self.trapezium.inertia_zz, self.cuboid.inertia_zz)

    def test_reflect_y(self):

        self.assertEqual(self.trapezium.reflect_y().centroid,
                         geometry.Point(38/15, -7/3, 0.5))

class TestPoint(unittest.TestCase):

    def test_equals(self):

        point1 = geometry.Point(1, 2, 3)
        point2 = geometry.Point(1, 2, 3)
        self.assertEqual(point1, point2)

    def test_add(self):

        point1 = geometry.Point(1, 2, 3)
        point2 = geometry.Point(1, 2, 3)
        point3 = point1 + point2
        self.assertEqual(point3.x, 2)
        self.assertEqual(point3.y, 4)
        self.assertEqual(point3.z, 6)

    def test_reflect_y(self):
        point1 = geometry.Point(1, 2, 3)
        self.assertEqual(point1.reflect_y(),
                         geometry.Point(1, -2, 3))





if __name__ == "__main__":
    unittest.main()
