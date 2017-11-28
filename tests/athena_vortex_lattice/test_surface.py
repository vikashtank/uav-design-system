from os.path import join, exists, dirname, abspath
from os import makedirs
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../")  # so uggo thanks to atom runner
import unittest
import uav_design_system.athena_vortex_lattice as avl

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
            section = avl.Section("", 0)
            self.surface.add_section(section)



    def tearDown(self):
        pass

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
        self.assertFalse(hasattr(self.surface[2], 'control_surface'))

    def test_surface_area(self):
        """
        test the calculation of the wing area with 2 sections
        """
        surface = avl.Surface("surface1")
        section1 = avl.Section("", 10)
        section2 = avl.Section("", 2)
        section2.translation_bias(0, 10, 0)

        surface.add_section(section1)
        surface.add_section(section2)

        self.assertEqual(surface.area, 60)

    def test_surface_area_multi(self):
        """
        calculations of the wing area with multiple sections
        """
        surface = avl.Surface("surface1")
        section1 = avl.Section("", 10)
        section2 = avl.Section("", 2)
        section2.translation_bias(0, 10, 0)
        section3 = avl.Section("", 2)
        section3.translation_bias(0, 20, 0)

        surface.add_section(section1, section2, section3)

        self.assertEqual(surface.area, 60 + 10*2)




    def test_section_to_string(self):
        """
        tests that the correct AVL string is produced by the surface
        """
        section = avl.Section("hello", 5)
        string = str(section)
        expected_string = """#    Xle         Yle         Zle         chord       angle   Nspan  Sspace
SECTION
     0     0     0     5         0

AFIL
hello
"""

        self.assertEqual(string, expected_string)


    def test_section_to_string_control(self):
        """
        tests that the correct AVL string is produced by the surface
        """
        section = avl.Section("hello", 5)
        control_surface = avl.ControlSurface("elevator", 0.8, [0, 1, 0], avl.ControlDeflectionType.SYMMETRIC)
        section._add_control_surface(control_surface)

        string = str(section)
        expected_string = """#    Xle         Yle         Zle         chord       angle   Nspan  Sspace
SECTION
     0     0     0     5         0
CONTROL
elevator  1  0.8   0 1 0   1
AFIL
hello
"""

        self.assertEqual(string, expected_string)

    def test_control_surface_string(self):
        """
        tests that the control surface class str method creates the appropriate
        string
        """
        control_surface = avl.ControlSurface("elevator", 0.8, [0,1,0], avl.ControlDeflectionType.SYMMETRIC)
        string = str(control_surface)
        expected_string = "elevator  1  0.8   0 1 0   1"
        self.assertEqual(string, expected_string)




if __name__ == "__main__":
    unittest.main()
