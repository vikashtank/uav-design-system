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

    def test_interias(self):
        self.assertEquals(self.cuboid.inertia_xx, 25/12)
        self.assertEquals(self.cuboid.inertia_yy, 20/12)
        self.assertEquals(self.cuboid.inertia_zz, 13/12)


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_cog(self):
        pass

    def test_location(self):
        pass



if __name__ == "__main__":
    unittest.main()
