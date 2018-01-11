from os.path import join, exists, dirname, abspath
from os import makedirs
from shutil import rmtree
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../")  # so uggo thanks to atom runner
import unittest
from uav_design_system.athena_vortex_lattice import AVLRunner as AVL
import json


def get_resource_content(file_name):
    """
    function to retrieve data from files in the resource folder for these tests
    """
    resources_directory = join(this_directory, "resources", "results_resources")
    with open(join(resources_directory, file_name)) as open_file:
        return open_file.read()


class Test(unittest.TestCase):

    def setUp(self):
        self.content = json.loads(get_resource_content("avl_output.json"))
        

    def test_get_cl(self):
        print(self.content["total_forces"])



if __name__ == "__main__":
    unittest.main()
