"""
"""
from os.path import join, exists, dirname, abspath
from os import makedirs, remove
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../")  # so uggo thanks to atom runner
import unittest
from uav_design_system import layout
from uav_design_system.aerodynamics import athena_vortex_lattice as avl


def get_resource_content(file_name):
    """
    function to retrieve data from files in the resource folder for these tests
    """
    resources_directory = join(this_directory, "resources")
    with open(join(resources_directory, file_name)) as open_file:
        return open_file.read()

class TestAthenaApi(unittest.TestCase):


    def _create_structure(self):
        surface = avl.Surface(name = "test_surface")

        for i in range(5):
            section = avl.Section(1)
            section.translation_bias(0, i, 0)
            surface.add_section(section)

        foam_factory = layout.StructureFactory(layout.StructuralModelType.HOLLOWFOAM)

        return foam_factory(surface, wall_thickness = 1)


    def setUp(self):
        self.file_name = join(this_directory, "test.txt")
        self.properties = {"gravity": 9.81, "density": 1.225}

        self.structure = self._create_structure()

    def tearDown(self):
        remove(self.file_name)

    def test_make_mass_file(self):

        layout.create_mass_file(self.file_name, self.structure , self.properties)
        self.assertTrue(exists(self.file_name))


    def test_contents_mass_file(self):

        layout.create_mass_file(self.file_name, self.structure , self.properties)

        expected_content = get_resource_content("mass_file.txt")

        with open(self.file_name) as open_file:
            actual_content = open_file.read()
        self.assertEqual(expected_content.strip(), actual_content.strip())


if __name__ == "__main__":
    unittest.main()
