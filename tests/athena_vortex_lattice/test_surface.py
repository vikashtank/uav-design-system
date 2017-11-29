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
hello"""

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
hello"""

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

    def test_cord(self):
        """
        test surface cord property
        """
        surface = avl.Surface("surface1")
        section1 = avl.Section("", 10)
        section2 = avl.Section("", 2)
        section2.translation_bias(0, 10, 0)
        surface.add_section(section1, section2)

        self.assertEqual(surface.cord, 10)

    def test_span(self):
        """
        test surface span property
        """
        surface = avl.Surface("surface1")
        section1 = avl.Section("", 10)
        section2 = avl.Section("", 2)
        section2.translation_bias(0, 12, 0)
        surface.add_section(section1, section2)

        self.assertEqual(surface.span, 12)

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


        expected_string = """all
0.0                      Mach
0     0     0.0          iYsym  iZsym  Zsym
60.0 10  10          Sref   Cref   Bref   reference area, chord, span
0 0   0          Xref   Yref   Zref   moment reference location (arb.)
0.020                    CDoref
#
#==============================================================
#
SURFACE
surface1
20  1.0  30  1.0  !  Nchord   Cspace   Nspan  Sspace
#
# reflect image wing about y=0 plane
YDUPLICATE
     0
#
# twist angle bias for whole surface
ANGLE
     0
#
# x,y,z bias for whole surface
TRANSLATE
    0     0     0
#--------------------------------------------------------------
#    Xle         Yle         Zle         chord       angle   Nspan  Sspace
SECTION
     0     0     0     10         0

AFIL
aerofoil_file
#-----------------------
#    Xle         Yle         Zle         chord       angle   Nspan  Sspace
SECTION
     0     10     0     2         0

AFIL
aerofoil_file
#-----------------------"""

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
    surface.add_control_surface(control_surface, 0, 0)
    surface.add_section(section1, section2)


    expected_string = """all
0.0                      Mach
0     0     0.0          iYsym  iZsym  Zsym
60.0 10  10          Sref   Cref   Bref   reference area, chord, span
0 0   0          Xref   Yref   Zref   moment reference location (arb.)
0.020                    CDoref
#
#==============================================================
#
SURFACE
surface1
20  1.0  30  1.0  !  Nchord   Cspace   Nspan  Sspace
#
# reflect image wing about y=0 plane
YDUPLICATE
 0
#
# twist angle bias for whole surface
ANGLE
 0
#
# x,y,z bias for whole surface
TRANSLATE
0     0     0
#--------------------------------------------------------------
#    Xle         Yle         Zle         chord       angle   Nspan  Sspace
SECTION
 0     0     0     10         0
CONTROL
elevator  1.0  0.8   0. 1. 0.   1.0
AFIL
aerofoil_file
#-----------------------
#    Xle         Yle         Zle         chord       angle   Nspan  Sspace
SECTION
 0     10     0     2         0

AFIL
aerofoil_file
#-----------------------"""

    self.assertEqual(str(surface).strip(), expected_string.strip())

if __name__ == "__main__":
    unittest.main()
