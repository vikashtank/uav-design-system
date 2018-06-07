from os.path import join, exists, dirname, abspath
from os import makedirs
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../../")  # so uggo thanks to atom runner
import unittest
import uav_design_system.aerodynamics.athena_vortex_lattice as avl
from uav_design_system import aerofoil
import shutil


def get_resource_content(file_name):
    """
    function to retrieve data from files in the resource folder for these tests
    """
    resources_directory = join(this_directory, "resources", "surface_resources")
    with open(join(resources_directory, file_name)) as open_file:
        return open_file.read()


class TestSurface(unittest.TestCase):

    def setUp(self):
        """
        create surface class
        """
        self.aerofoil = aerofoil.Aerofoil.develop_aerofoil(0.2, 0.2, 0.2, 0.2, 0.2)
        self.surface = avl.Surface("wing")
        self.surface.define_mesh()
        self.control_surface = avl.ControlSurface("elevator", 0.6, [0,0.1,0],
                            avl.ControlDeflectionType.SYMMETRIC)

        for i in range(5):
            section = self.surface.add_section(2)
            section.aerofoil = self.aerofoil
            section.translation_bias(0, i, 0)

    def tearDown(self):
        pass

    def test_len(self):
        self.assertEqual(len(self.surface), 5)

    def test_add_control_surface_all(self):
        """
        tests that the control surfaces can be applies to sections
        """
        self.surface.add_control_surface(self.control_surface, 0, 4)

        for section in self.surface:
            self.assertTrue(section.control_surface is self.control_surface)

    def test_add_control_surface(self):
        """
        tests that the control surfaces are only applied to the specific section
        """

        self.surface.add_control_surface(self.control_surface, 0, 1)

        self.assertTrue(self.surface[0].control_surface is self.control_surface)
        self.assertTrue(self.surface[1].control_surface is self.control_surface)

        with self.assertRaises(avl.NoControlSurfaceError):
            hasattr(self.surface[2], 'control_surface')

    def test_add_control_surface_failure(self):
        """
        tests failure when a contrl surfaces is added to a section that doesnt
        exist
        """

        with self.assertRaises(avl.NoSectionError):
            self.surface.add_control_surface(self.control_surface, 5, 5)

        with self.assertRaises(avl.NoSectionError):
            self.surface.add_control_surface(self.control_surface, 0, 5)

    def test_surface_area(self):
        """
        test the calculation of the wing area with 2 sections
        """
        self.assertEqual(self.surface.area, 8)

    def test_surface_area_reflect(self):
        """
        test the calculation of the wing area with 2 sections with a reflected
        surface
        """
        self.surface.reflect_surface = True
        self.assertEqual(self.surface.area, 16)

    def test_cord(self):
        """
        test surface cord property
        """
        self.assertEqual(self.surface.cord, 2)

    def test_span(self):
        """
        test surface span property
        """
        self.assertEqual(self.surface.span, 4)

    def test_span_reflected(self):
        """
        test surface span property with a reflected surface
        """
        self.surface.reflect_surface = True
        self.assertEqual(self.surface.span, 8)

    def test_get_plot_coords(self):

        expected_x_coords = [0, 0, 0, 0, 0, 2, 2, 2, 2, 2]
        expected_y_coords = [0, 1, 2, 3, 4, 4, 3, 2, 1, 0]
        expected_z_coords = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        x, y, z = self.surface.get_plot_coordinates()
        self.assertEqual(x, expected_x_coords)
        self.assertEqual(y, expected_y_coords)
        self.assertEqual(z, expected_z_coords)

    def test_get_plot_coords_reflected(self):

        self.surface.reflect_surface = True

        expected_x_coords = [0, 0, 0, 0, 0, 2, 2, 2, 2, 2,
                             2, 2, 2, 2, 2, 0, 0, 0, 0, 0]
        expected_y_coords = [0, 1, 2, 3, 4, 4, 3, 2, 1, 0,
                             0, -1, -2, -3, -4, -4, -3, -2, -1, 0]
        expected_z_coords = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        x, y, z = self.surface.get_plot_coordinates()
        self.assertEqual(x, expected_x_coords)
        self.assertEqual(y, expected_y_coords)
        self.assertEqual(z, expected_z_coords)


class TestSurfaceWrite(unittest.TestCase):

    def setUp(self):
        self.aerofoil = aerofoil.Aerofoil.develop_aerofoil(0.2, 0.2, 0.2, 0.2, 0.2)
        self.surface = avl.Surface("surface1")
        self.surface.define_mesh(20, 30, 1.0, 1.0)

        section1 = self.surface.add_section(10)
        section1.aerofoil = self.aerofoil

        section2 = self.surface.add_section(2)
        section2.aerofoil = self.aerofoil

        section2.translation_bias(0, 10, 0)

        self.control_surface = avl.ControlSurface("elevator",
                                                  0.8,
                                                  [0, 1, 0],
                                                  avl.ControlDeflectionType.SYMMETRIC)

    def test_avl_write(self):
        """
        tests the avl file is correctl written from the surface class
        """

        self.surface.reflect_surface = True
        expected_string = get_resource_content("surface.txt")
        self.maxDiff = None
        self.assertEqual(self.surface._to_avl_string().strip(),
                         expected_string.strip())

    def test_avl_write_no_duplicate(self):
        """
        tests the avl file is correctl written from the surface class
        """
        expected_string = get_resource_content("surface_no_dup.txt")
        self.maxDiff = None
        self.assertEqual(self.surface._to_avl_string().strip(),
                         expected_string.strip())

    def test_avl_write_with_controls(self):
        """
        tests the avl file is correctl written from the surface class
        """

        self.surface.add_control_surface(self.control_surface, 0, 0)
        expected_string = get_resource_content("surface_control.txt")
        self.surface.reflect_surface = True
        self.maxDiff = None
        self.assertEqual(self.surface._to_avl_string().strip(),
                         expected_string.strip())


class TestSection(unittest.TestCase):

        def setUp(self):
            self.aerofoil = aerofoil.Aerofoil.develop_aerofoil(0.2, 0.2, 0.2, 0.2, 0.2)
            self.section = avl.Section(5)
            self.control_surface = avl.ControlSurface("elevator",
                                                       0.8,
                                                       [0, 1, 0],
                                                       avl.
                                                       ControlDeflectionType.
                                                       SYMMETRIC)

        def test_section_to_string(self):
            """
            tests that the correct AVL string is produced by the surface
            """
            string = self.section._to_avl_string("")

            expected_string = get_resource_content("section_to_string.txt")

            self.assertEqual(string.strip(), expected_string.strip())

        def test_control_surface_missing(self):
            """
            test correct error is thrown when the control surface has not been set
            """
            with self.assertRaises(avl.NoControlSurfaceError):
                self.section.control_surface

        def test_control_surface(self):
            """
            test correct error is thrown when the control surface has not been set
            """
            self.section.control_surface = self.control_surface
            self.assertEqual(self.section.control_surface, self.control_surface)

        def test_aerofoil(self):

            self.section.aerofoil = self.aerofoil
            self.assertEqual(self.section.aerofoil, self.aerofoil)

        def test_aerofoil_missing(self):

            with self.assertRaises(avl.NoAerofoilError):
                self.section.aerofoil

        def test_section_to_string_control(self):
            """
            tests that the correct AVL string is produced by the surface
            """
            self.section.control_surface = self.control_surface
            string = self.section._to_avl_string("")
            expected_string = get_resource_content("section_to_control.txt")

            self.assertEqual(string.strip(), expected_string.strip())

        def test_leading_edge_coordinates(self):
            self.assertEqual((0, 0, 0), self.section.leading_edge_coordinates)

        def test_trailing_edge_coordinates(self):
            self.assertEqual((5, 0, 0), self.section.trailing_edge_coordinates)


class TestControlSurface(unittest.TestCase):

        def test_control_surface_string(self):
            """
            tests that the control surface class str method creates the appropriate
            string
            """
            control_surface = avl.ControlSurface("elevator",
                                                 0.8,
                                                 [0,1,0],
                                                 avl.ControlDeflectionType.
                                                                    SYMMETRIC)
            string = control_surface.to_avl_string()
            expected_string = "elevator  1  0.8   0 1 0   1"
            self.assertEqual(string, expected_string)






if __name__ == "__main__":
    unittest.main()
