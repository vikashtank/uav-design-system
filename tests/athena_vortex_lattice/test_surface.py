from os.path import join, exists, dirname, abspath
from os import makedirs
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../")  # so uggo thanks to atom runner
import unittest
import uav_design_system.athena_vortex_lattice as avl


def get_resource_content(file_name):
    """
    function to retrieve data from files in the resource folder for these tests
    """
    resources_directory = join(this_directory, "resources", "surface_resources")
    with open(join(resources_directory, file_name)) as open_file:
        return open_file.read()


class Test(unittest.TestCase):

    def setUp(self):
        """
        create surface class
        """

        self.surface = avl.Surface("wing")
        self.surface.define_mesh()
        self.control_surface = avl.ControlSurface("elevator", 0.6, [0,0.1,0],
                            avl.ControlDeflectionType.SYMMETRIC)

        for i in range(5):
            section = avl.Section("", 2)
            section.translation_bias(0, i, 0)
            self.surface.add_section(section)

    def tearDown(self):
        pass

    def test_len(self):
        self.assertEqual(len(self.surface), 5)

    def test_add_control_surface_all(self):
        """
        tests that the control surfaces can be applies to sections
        """
        self.surface.add_control_surface(self.control_surface, 0, 5)

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

    def test_surface_area(self):
        """
        test the calculation of the wing area with 2 sections
        """
        self.assertEqual(self.surface.area, 8)

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

    def _test_get_plot_coords(self):

        surface = avl.Surface("surface1")
        section1 = avl.Section("", 10)
        section2 = avl.Section("", 2)
        section2.translation_bias(0, 10, 0)

        surface.add_section(section1)
        surface.add_section(section2)

        expected_x_coords = []
        expected_y_coords = []
        x, y = surface.get_plot_coordinates()
        self.assertEqual(x, expected_x_coords)
        self.assertEqual(y, expected_y_coords)

    def test_avl_write(self):
        """
        tests the avl file is correctl written from the surface class
        """
        surface = avl.Surface("surface1")
        surface.define_mesh(20, 30, 1.0, 1.0)
        section1 = avl.Section("aerofoil_file", 10)
        section2 = avl.Section("aerofoil_file", 2)
        section2.translation_bias(0, 10, 0)
        surface.add_section(section1, section2)

        expected_string = get_resource_content("surface.txt")

        self.assertEqual(str(surface).strip(), expected_string.strip())


    def test_avl_write_with_controls(self):
        """
        tests the avl file is correctl written from the surface class
        """
        surface = avl.Surface("surface1")
        surface.define_mesh(20, 30, 1.0, 1.0)
        section1 = avl.Section("aerofoil_file", 10)
        section2 = avl.Section("aerofoil_file", 2)
        control_surface = avl.ControlSurface("elevator", 0.8, [0, 1, 0], avl.ControlDeflectionType.SYMMETRIC)
        section2.translation_bias(0, 10, 0)
        surface.add_section(section1, section2)
        surface.add_control_surface(control_surface, 0, 0)
        expected_string = get_resource_content("surface_control.txt")
        self.assertEqual(str(surface).strip(), expected_string.strip())


class TestSection(unittest.TestCase):

        def setUp(self):
            self.section = avl.Section("hello", 5)
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
            string = self.section.to_avl_string()

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


        def test_section_to_string_control(self):
            """
            tests that the correct AVL string is produced by the surface
            """
            self.section.control_surface = self.control_surface
            string = self.section.to_avl_string()
            expected_string = get_resource_content("section_to_control.txt")


            self.assertEqual(string.strip(), expected_string.strip())

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
