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
    resources_directory = join(this_directory, "resources", "plane_resources")
    with open(join(resources_directory, file_name)) as open_file:
        return open_file.read()


class TestPlane(unittest.TestCase):

    def setUp(self):

        # create wing with aerofoil
        self.aerofoil = aerofoil.Aerofoil.develop_aerofoil(0.2, 0.2, 0.2, 0.2, 0.2)
        self.surface = avl.Surface("surface1")
        self.surface.define_mesh(20, 30, 1.0, 1.0)
        section1 = avl.Section(10)
        section1.aerofoil = self.aerofoil
        section2 = avl.Section(2)
        section2.aerofoil = self.aerofoil
        section2.translation_bias(0, 10, 0)
        self.surface.add_section(section1, section2)

        self.plane = avl.Plane("plane1", self.surface)

    def test_main_surface_property(self):
        self.assertEqual(self.plane.main_surface, self.surface)

    def test_reference_string(self):
        expected_string = get_resource_content("ref_string.txt")
        self.maxDiff = None
        actual_string = self.plane._ref_string
        self.assertEqual(expected_string.strip(), actual_string.strip())


class TestSurfaceDump(unittest.TestCase):

    def setUp(self):
        self.temp_dir = join(this_directory, "temp")
        makedirs(self.temp_dir)

        # create wing with aerofoil
        self.aerofoil = aerofoil.Aerofoil.develop_aerofoil(0.2, 0.2, 0.2, 0.2, 0.2)
        self.surface = avl.Surface("surface1")
        self.surface.define_mesh(20, 30, 1.0, 1.0)

        section1 = avl.Section(10)
        section1.aerofoil = self.aerofoil

        section2 = avl.Section(2)
        section2.aerofoil = self.aerofoil

        section2.translation_bias(0, 10, 0)

        self.surface.add_section(section1, section2)

        self.plane = avl.Plane("plane1", self.surface)

        self.control_surface = avl.ControlSurface("elevator",
                                                  0.8,
                                                  [0, 1, 0],
                                                  avl.ControlDeflectionType.SYMMETRIC)


    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_dump(self):

        avl_file, aero_files = self.plane.dump_avl_files(self.temp_dir)
        self.assertTrue(exists(join(self.temp_dir, "surf0_sec0_af.txt")))
        self.assertTrue(exists(join(self.temp_dir, "surf0_sec1_af.txt")))
        self.assertTrue(exists(join(self.temp_dir, "plane1.avl")))

    def test_dump_returns(self):

        avl_file, aero_files = self.plane.dump_avl_files(self.temp_dir)
        self.assertEqual(avl_file, join(self.temp_dir, "plane1.avl"))
        self.assertEqual(len(aero_files), 2)
        self.assertEqual(aero_files[0], join(self.temp_dir, "surf0_sec0_af.txt"))
        self.assertEqual(aero_files[1], join(self.temp_dir, "surf0_sec1_af.txt"))


    def test_dump_file_content(self):
        """
        tests the avl file is correctl written from the surface class
        """
        self.surface.reflect_surface = True
        expected_string = get_resource_content("surface.txt")
        self.maxDiff = None
        self.assertEqual(self.plane._to_avl_string.strip(),
                         expected_string.strip())

    def test_avl_write_no_duplicate(self):
        """
        tests the avl file is correctl written from the surface class
        """
        expected_string = get_resource_content("surface_no_dup.txt")
        self.maxDiff = None
        self.assertEqual(self.plane._to_avl_string.strip(),
                         expected_string.strip())

    def test_dump_file_content_control_surfaces(self):
        """
        tests the avl file is correctl written from the surface class
        """

        self.surface.add_control_surface(self.control_surface, 0, 0)
        expected_string = get_resource_content("surface_control.txt")
        self.surface.reflect_surface = True
        self.maxDiff = None
        self.assertEqual(self.plane._to_avl_string.strip(),
                         expected_string.strip())

    def test_mulitple_surfaces(self):
        # create and add second surface
        tail_surface = avl.Surface("tail")
        section1 = avl.Section(1)
        section2 = avl.Section(1)
        section2.translation_bias(0, 5, 0)
        tail_surface.add_section(section1, section2)
        tail_surface.define_translation_bias(10, 0, 0)
        self.plane.append(tail_surface)
        expected_string = get_resource_content("surface_multiple.txt")
        self.assertEqual(self.plane._to_avl_string.strip(),
                         expected_string.strip())



if __name__ == "__main__":
    unittest.main()
