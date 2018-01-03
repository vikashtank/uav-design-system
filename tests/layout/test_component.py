from os.path import join, exists, dirname, abspath
from os import makedirs
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../")  # so uggo thanks to atom runner
import unittest
from uav_design_system import layout, athena_vortex_lattice as avl


class TestCreateFoamWing(unittest.TestCase):
    """
    tests the create foam wing method in the StructureFactory class
    """

    def setUp(self):
        surface = avl.Surface(name = "test_surface")

        # add five square sections side by side to form a rectangular surface
        for i in range(5):
            section = avl.Section("", 1)
            section.translation_bias(0, i, 0)
            surface.add_section(section)

        foam_factory = layout.StructureFactory(layout.StructuralModelType.HOLLOWFOAM)
        self.structural_model = foam_factory(surface, wall_thickness = 1)

    def tearDown(self):
        pass

    def test_structural_factory_foam(self):
        """
        tests that the stuctural factory produces the correct structural model
        for the foam model and returns the correct centers of gravity
        """
        self.assertTrue(isinstance(self.structural_model, layout.StructuralModel))
        self.assertEqual(len(self.structural_model.objects), 4)

        for index, section in enumerate(self.structural_model.objects):
            point = layout.Point(0.5, index + 0.5, 1)
            self.assertEqual(section.center_of_gravity_global.x, point.x)
            self.assertEqual(section.center_of_gravity_global.y, point.y)
            self.assertEqual(section.center_of_gravity_global.z, point.z)


    def test_total_mass(self):
        density = 5
        thickness = 1
        number_of_sections = 4
        self.assertEqual(self.structural_model.total_mass, density * 2 *
                         thickness * number_of_sections)


if __name__ == "__main__":
    unittest.main()
