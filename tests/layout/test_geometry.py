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
        self.assertEquals(self.cuboid.centroid, geometry.Point(1, 1.5, 2))

    def test_inertias(self):
        self.assertEquals(self.cuboid.inertia_xx, 25/12)
        self.assertEquals(self.cuboid.inertia_yy, 20/12)
        self.assertEquals(self.cuboid.inertia_zz, 13/12)


class TestCylinder(unittest.TestCase):

    def setUp(self):
        self.cylinder = geometry.Cylinder(1, 10)

    def tearDown(self):
        pass

    def test_volume(self):
        pass

    def test_centroid(self):
        self.assertEquals(self.cylinder.centroid, geometry.Point(0, 0, 5))

    def test_inertias(self):
        self.assertAlmostEquals(self.cylinder.inertia_xx, 103/12)
        self.assertAlmostEquals(self.cylinder.inertia_yy, 103/12)
        self.assertAlmostEquals(self.cylinder.inertia_zz, 0.5)

class TestPoint(unittest.TestCase):

    def test_equals(self):

        point1 = geometry.Point(1,2,3)
        point2 = geometry.Point(1,2,3)
        self.assertEquals(point1, point2)

    def test_add(self):

        point1 = geometry.Point(1,2,3)
        point2 = geometry.Point(1,2,3)
        point3 = point1 + point2
        self.assertEquals(point3.x, 2)
        self.assertEquals(point3.y, 4)
        self.assertEquals(point3.z, 6)





if __name__ == "__main__":
    unittest.main()
