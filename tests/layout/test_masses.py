from os.path import join, exists, dirname, abspath
from os import makedirs
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../")  # so uggo thanks to atom runner
import unittest
from uav_design_system import layout
import copy

class DummyMass(layout.IsArrangeable):
    pass

class TestArrangement(unittest.TestCase):

    def setUp(self):
        geometry = layout.Cuboid(1,2,3)
        self.mass1 = layout.MassObject(geometry, 1, "name1")
        self.mass2 = layout.MassObject(geometry, 2, "name2")
        self.mass3 = layout.MassObject(geometry, 3, "name3")
        self.mass4 = layout.MassObject(geometry, 4, "name4")
        self.mass_list = [self.mass1, self.mass2, self.mass3, self.mass4]

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

    def test_all_mass_objects_not_clones(self):
        """
        tests the all mass objects method does not clone the masses it outputs
        """
        arrangement = layout.Arrangement("arrangement1", *self.mass_list)
        mass_list = arrangement.all_mass_objects

        for i in range(len(mass_list)):

            self.assertEqual(id(mass_list[i]), id(self.mass_list[i]))

    def test_all_mass_objects_nested_twice(self):
        """
        tests obtaining all mass objects within an arrangement, with nested
        arrangements
        """
        sub_arrangement = layout.Arrangement("arrangement1", *[self.mass1,
                                                              self.mass2,
                                                              ])
        sub_arrangement2 = layout.Arrangement("arrangement2", *[self.mass3,
                                                               self.mass4,
                                                               ])
        arrangement = layout.Arrangement("arrangement3", *[sub_arrangement,
                                                          sub_arrangement2,
                                                          ])

        mass_list = arrangement.all_mass_objects

        self.assertEqual(len(mass_list), len(self.mass_list))
        for i in range(len(self.mass_list)):
            self.assertEqual(mass_list[i], self.mass_list[i])

    def test_all_mass_objects_nested(self):
        """
        tests obtaining all mass objects within an arrangement, with nested
        arrangements all with their own locations
        """
        sub_arrangement = layout.Arrangement("arrangement1", *self.mass_list)
        sub_arrangement.location = layout.Point(0, 0, 1)
        arrangement = layout.Arrangement("arrangement2", sub_arrangement)
        mass_list = arrangement.all_mass_objects

        self.assertEqual(len(mass_list), len(self.mass_list))
        for i in range(len(self.mass_list)):
            self.assertEqual(mass_list[i], self.mass_list[i])

    def test_getitem(self):
        arrangement = layout.Arrangement("arrangement1", *self.mass_list)
        self.assertEqual(arrangement["name1"][0],  self.mass1)

    def test_getitem_missing(self):
        arrangement = layout.Arrangement("arrangement1", *self.mass_list)

        with self.assertRaises(KeyError):
            self.assertEqual(arrangement["name"], self.mass1)

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
        self.assertEqual(arrangement.center_of_gravity,
                         layout.Point(0.5, 1, 1.5))

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

    def test_clone(self):
        """
        test clone method
        """
        arrangement = layout.Arrangement("arrangement1", *self.mass_list)

        arrangement_clone = arrangement.clone()

        self.assertEqual(arrangement.center_of_gravity,
                        arrangement_clone.center_of_gravity)

    def test_reflect_y(self):
        """
        tests that the y refelection method creates a new arrangement reflected
        in the y axis
        """
        arrangement = layout.Arrangement("arrangement1", *self.mass_list)

        # create expected reflected coordinates for center of gravity
        x = arrangement.center_of_gravity.x
        y = -1 * arrangement.center_of_gravity.y
        z = arrangement.center_of_gravity.z
        reflected_cog = layout.Point(x, y, z)

        arrangement_reflect = arrangement.clone(reflect_y = True)

        self.assertEqual(arrangement_reflect.center_of_gravity.x, reflected_cog.x)
        self.assertEqual(arrangement_reflect.center_of_gravity.y, reflected_cog.y)
        self.assertEqual(arrangement_reflect.center_of_gravity.z, reflected_cog.z)

    def test_reflect_y_offset(self):
        """
        tests that the y refelection method creates a new arrangement reflected
        in the y axis
        """
        arrangement = layout.Arrangement("arrangement1", *self.mass_list)

        # offset the masses within the arrangement
        for mass in self.mass_list:
            mass.location = layout.Point(0, 10, 0)

        arrangement_reflect = arrangement.clone(reflect_y = True)

        self.assertEqual(arrangement_reflect.center_of_gravity.x, 0.5)
        self.assertEqual(arrangement_reflect.center_of_gravity.y, -11)
        self.assertEqual(arrangement_reflect.center_of_gravity.z, 1.5)

    def test_len(self):
        arrangement = layout.Arrangement("arrangement1", *self.mass_list)
        self.assertEqual(len(arrangement), 4)

    def test_flatten_arrangement_1layer(self):
        """
        test flatten maintains arrangement when the arrangement only contains
        one layer of masses
        """
        arrangement = layout.Arrangement("arrangement1", *self.mass_list)
        flattened_arrangement = arrangement.flatten()
        mass_list = flattened_arrangement.all_mass_objects

        for i in range(len(mass_list)):
            self.assertEqual(mass_list[i], self.mass_list[i])

    def test_flatten_arrangement_2layer(self):
        """
        test flatten maintains arrangement when the arrangement only contains
        multiple layers of masses
        """
        arrangement = layout.Arrangement("arrangement1", *self.mass_list[0:2])
        arrangement2 = layout.Arrangement("arrangement2", *self.mass_list[2:])
        arrangement3 = layout.Arrangement("arrangement3", arrangement,
                                                          arrangement2,
                                                          self.mass_list[0])
        flattened_arrangement = arrangement3.flatten()
        mass_list = flattened_arrangement.all_mass_objects
        expected_mass_list = self.mass_list + [self.mass1]

        self.assertEqual(len(flattened_arrangement), 5)
        for i in range(len(mass_list)):
            self.assertEqual(mass_list[i], expected_mass_list[i])

    def test_flatten_arrangement_clones(self):
        """
        tests the  method clones the masses it outputs
        """
        arrangement = layout.Arrangement("arrangement1", *self.mass_list)
        flattened_arrangement = arrangement.flatten()
        mass_list = flattened_arrangement.all_mass_objects
        self.assertEqual(len(flattened_arrangement), 4)
        for i in range(len(mass_list)):
            self.assertNotEqual(id(mass_list[i]), id(self.mass_list[i]))

    def test_flatten_arrangement_2layer_locations(self):
        """
        test flatten applies correct locations
        """
        arrangement = layout.Arrangement("arrangement1", *self.mass_list[0:2])
        arrangement.location = layout.Point(0, 0, 1)
        arrangement2 = layout.Arrangement("arrangement2", *self.mass_list[2:])
        arrangement2.location = layout.Point(0, 0, 2)
        arrangement3 = layout.Arrangement("arrangement3", arrangement,
                                                          arrangement2,
                                                          self.mass_list[0])
        arrangement3.location = layout.Point(1, 7, 0)

        flattened_arrangement = arrangement3.flatten()
        mass_list = flattened_arrangement.all_mass_objects
        expected_mass_list = self.mass_list + [self.mass1]

        self.assertEqual(mass_list[0].location, layout.Point(1, 7 , 1))
        self.assertEqual(mass_list[1].location, layout.Point(1, 7 , 1))
        self.assertEqual(mass_list[2].location, layout.Point(1, 7 , 2))
        self.assertEqual(mass_list[3].location, layout.Point(1, 7 , 2))
        self.assertEqual(mass_list[4].location, layout.Point(1, 7 , 0))

    def test_flatten_arrangement_2layer_locations_complicated(self):
        """
        test flatten applies correct locations
        """
        self.mass1.location = layout.Point(4, -5, 6)
        self.mass2.location = layout.Point(3, 2, 1)

        arrangement = layout.Arrangement("arrangement1", *[self.mass1, self.mass2])
        arrangement.location = layout.Point(3, -2, 7)
        arrangement2 = layout.Arrangement("arrangement2", *[self.mass3, self.mass4])
        arrangement2.location = layout.Point(-5, 0, 12)
        arrangement3 = layout.Arrangement("arrangement3", arrangement,
                                                          arrangement2,
                                                          self.mass1)
        arrangement3.location = layout.Point(1, 7, 0)

        flattened_arrangement = arrangement3.flatten()
        mass_list = flattened_arrangement.all_mass_objects
        expected_mass_list = self.mass_list + [self.mass1]

        self.assertEqual(mass_list[0].location, layout.Point(8, 0 , 13))
        self.assertEqual(mass_list[1].location, layout.Point(7, 7 , 8))
        self.assertEqual(mass_list[2].location, layout.Point(-4, 7 , 12))
        self.assertEqual(mass_list[3].location, layout.Point(-4, 7 , 12))
        self.assertEqual(mass_list[4].location, layout.Point(5, 2, 6))

class TestMassObject(unittest.TestCase):

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

    def test_equal(self):
        mass1 = layout.MassObject(self.geometry, 1, "name")
        mass2 = layout.MassObject(self.geometry, 1, "name")
        self.assertEqual(mass1, mass2)


if __name__ == "__main__":
    unittest.main()
