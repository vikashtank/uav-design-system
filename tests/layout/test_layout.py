from os.path import join, exists, dirname, abspath
from os import makedirs
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../")  # so uggo thanks to atom runner
import unittest
import uav_design_system.layout as layout
import uav_design_system.layout as layout

class dummyMass(layout.IsArrangeable):
    pass

class TestArrangement(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_creation(self):

        component1 = dummyMass()
        component2 = dummyMass()

        arrangement = layout.Arrangement("arrangement1", component1, component2)
        self.assertEquals(arrangement.objects[0], component1)
        self.assertEquals(arrangement.objects[1], component2)

    def test_cog(self):
        pass


class TestComponent(unittest.TestCase):

    def setUp(self):
        self.geometry = layout.Cuboid(1,2,3)

    def tearDown(self):
        pass

    def test_cog(self):
        """
        test the center of gravity is initially the centroid
        """
        mass_object = layout.MassObject(self.geometry, 1, "name")
        self.assertEquals(mass_object.center_of_gravity, layout.Point(0.5, 1, 1.5))

    def test_set_cog(self):
        """
        test that the cog can be modified
        """
        mass_object = layout.MassObject(self.geometry, 1, "name")
        mass_object.center_of_gravity = layout.Point(1,2,3)
        self.assertEquals(mass_object.center_of_gravity, layout.Point(1,2,3))


    def test_default_location(self):
        """
        test the mass_object can be given a location
        """
        mass_object = layout.MassObject(self.geometry, 1, "name")
        self.assertEquals(mass_object.location, layout.Point(0,0,0))

    def test_location_setting(self):
        """
        test the mass_object can be given a location
        """
        mass_object = layout.MassObject(self.geometry, 1, "name")
        masss_object.location = layout.Point(1,2,3)
        self.assertEquals(mass_object.location, layout.Point(1,2,3))




if __name__ == "__main__":
    unittest.main()
