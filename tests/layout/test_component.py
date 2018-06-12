from os.path import join, exists, dirname, abspath
from os import makedirs
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../")  # so uggo thanks to atom runner
import unittest
from uav_design_system import layout
from uav_design_system.aerodynamics import athena_vortex_lattice as avl
from matplotlib import pyplot as plt

class TestCreateFoamWing(unittest.TestCase):
    """
    tests the create foam wing method in the StructureFactory class
    """

    def setUp(self):
        self.surface = avl.Surface(name = "test_surface")

        # add five square sections side by side to form a rectangular surface
        for i in range(5):
            section = self.surface.add_section(1)
            section.translation_bias(0, i, 0)


        self.foam_factory = layout.StructureFactory(layout.StructuralModelType.HOLLOWFOAM)
        self.structural_model = self.foam_factory(self.surface, wall_thickness = 1)

    def tearDown(self):
        pass

    def test_return_type(self):
        """
        tests the correct object type and size is returned
        """
        self.assertTrue(isinstance(self.structural_model, layout.StructuralModel))
        self.assertEqual(len(self.structural_model.objects), 4)

    def test_structural_factory_foam(self):
        """
        tests that the stuctural factory produces the correct structural model
        for the foam model and returns the correct centers of gravity
        """

        for index, section in enumerate(self.structural_model.objects):
            point = layout.Point(0.5, index + 0.5, 1)
            self.assertEqual(section.center_of_gravity_global.x, point.x)
            self.assertEqual(section.center_of_gravity_global.y, point.y)
            self.assertEqual(section.center_of_gravity_global.z, point.z)

    def test_total_mass(self):
        density = 36
        thickness = 1
        number_of_sections = 4
        self.assertEqual(self.structural_model.mass, density * 2 *
                         thickness * number_of_sections)


class TestCreateFoamWingTrapezium(unittest.TestCase):

    def setUp(self):
        self.surface = avl.Surface(name = "test_surface")

        # add five square sections side by side to form a rectangular surface
        for i in range(5):
            section = avl.Section(1)
            section.translation_bias(-i, i, 0)
            self.surface.add_section(section)

        foam_factory = layout.StructureFactory(layout.StructuralModelType.HOLLOWFOAM)
        self.structural_model = foam_factory(self.surface, wall_thickness = 1)

    def _test_plot(self):
        """
        test the plots of the structural model overlap the plots of the surface
        """
        for mass in self.structural_model.flatten().all_mass_objects:
            x, y = mass.geometry.project_xy.plot_coordinates
            plt.plot(x, y)
            cg_x = mass.center_of_gravity_global.x
            cg_y = mass.center_of_gravity_global.y
            plt.plot(cg_x, cg_y, "*")

        x, y, _ = self.surface.get_plot_coordinates()
        plt.plot(x, y, "r--")
        plt.show()

class TestFoamSection(unittest.TestCase):

    def setUp(self):
        self.section = layout.FoamSection(10, 5, 2.5, 10, 1)

    def test_location_default(self):
        self.assertEqual(self.section.location, layout.Point(0, 0, 0))

    def test_location_set(self):
        self.section.location = layout.Point(1, 7, -3)
        self.assertEqual(self.section.location, layout.Point(1, 7, -3))


if __name__ == "__main__":
    unittest.main()
