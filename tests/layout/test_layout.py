from os.path import join, exists, dirname, abspath
from os import makedirs
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../")  # so uggo thanks to atom runner
import unittest
import uav_design_system.layout as layout

class DummyMass(layout.IsArrangeable):
    pass

class TestArrangement(unittest.TestCase):

    def setUp(self):
        geometry = layout.Cuboid(1,2,3)
        mass1 = layout.MassObject(geometry, 1, "name")
        mass2 = layout.MassObject(geometry, 2, "name")
        mass3 = layout.MassObject(geometry, 3, "name")
        mass4 = layout.MassObject(geometry, 4, "name")
        self.mass_list = [mass1, mass2, mass3, mass4]

    def tearDown(self):
        pass

    def test_creation(self):

        component1 = DummyMass()
        component2 = DummyMass()

        arrangement = layout.Arrangement("arrangement1", component1, component2)
        self.assertEqual(arrangement.objects[0], component1)
        self.assertEqual(arrangement.objects[1], component2)

    def test_all_mass_objects(self):
        """
        tests obtaining all mass objects within an arrangement, without nested
        arrangements
        """
        arrangement = layout.Arrangement("arrangement1", *self.mass_list)
        mass_list = arrangement.all_mass_objects

        self.assertEqual(len(mass_list), len(self.mass_list))
        for i in range(len(self.mass_list)):
            self.assertEqual(mass_list[i], self.mass_list[i])

    def test_all_mass_objects_nested(self):
        """
        tests obtaining all mass objects within an arrangement, with nested
        arrangements
        """
        sub_arrangement = layout.Arrangement("arrangement1", *self.mass_list)
        arrangement = layout.Arrangement("arrangement2", sub_arrangement)
        mass_list = arrangement.all_mass_objects

        self.assertEqual(len(mass_list), len(self.mass_list))
        for i in range(len(self.mass_list)):
            self.assertEqual(mass_list[i], self.mass_list[i])


    def test_create_mass_list(self):
        arrangement = layout.Arrangement("arrangement1", *self.mass_list)
        expected_list = ["6   0.5   1.0   1.5    6.5   5.0   2.5",
                         "12   0.5   1.0   1.5    13.0   10.0   5.0",
                         "18   0.5   1.0   1.5    19.5   15.0   7.5",
                         "24   0.5   1.0   1.5    26.0   20.0   10.0"]
        self.assertEqual(arrangement.avl_mass_list, expected_list)

    def test_center_of_gravity(self):
        """
        tests the calculation of the center of gravity
        """
        arrangement = layout.Arrangement("arrangement1", *self.mass_list)
        self.assertEqual(arrangement.center_of_gravity, 0.5)

    def test_total_mass(self):
        arrangement = layout.Arrangement("arrangement1", *self.mass_list)
        self.assertEqual(arrangement.total_mass, 60)

    def test_total_mass_nested(self):
        arrangement = layout.Arrangement("arrangement1", *self.mass_list[0:2])
        arrangement2 = layout.Arrangement("arrangement2", *self.mass_list[2:])
        arrangement3 = layout.Arrangement("arrangement3", arrangement,
                                                          arrangement2,
                                                          self.mass_list[0])

        self.assertEqual(arrangement3.total_mass, 66)


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
        self.assertEqual(mass_object.center_of_gravity,
                          layout.Point(0.5, 1, 1.5))

    def test_set_cog(self):
        """
        test that the cog can be modified
        """
        mass_object = layout.MassObject(self.geometry, 1, "name")
        mass_object.center_of_gravity = layout.Point(1,2,3)
        self.assertEqual(mass_object.center_of_gravity, layout.Point(1,2,3))
        self.assertEqual(mass_object.center_of_gravity_global,
                          layout.Point(1,2,3))

    def test_default_location(self):
        """
        test the mass_object can be given a location
        """
        mass_object = layout.MassObject(self.geometry, 1, "name")
        self.assertEqual(mass_object.location, layout.Point(0,0,0))

    def test_location_setting(self):
        """
        test the mass_object can be given a location and cog change
        """
        mass_object = layout.MassObject(self.geometry, 1, "name")
        mass_object.location = layout.Point(1,2,3)
        self.assertEqual(mass_object.location, layout.Point(1,2,3))
        self.assertEqual(mass_object.center_of_gravity_global,
                          layout.Point(1.5, 3, 4.5))

    def test_create_mass_string(self):
        """
        test the create mass string method works with a shifted mass
        """
        mass_object = layout.MassObject(self.geometry, 1, "name")
        mass_object.location = layout.Point(1,1,1) # apply shift

        expected_string = "6   1.5   2.0   2.5    6.5   5.0   2.5"
        self.assertEqual(mass_object.avl_mass_string, expected_string)


if __name__ == "__main__":
    unittest.main()
