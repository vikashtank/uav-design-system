from os.path import join, exists, dirname, abspath
from os import makedirs
from shutil import rmtree
this_directory = dirname(abspath(__file__))
import sys
sys.path.append(this_directory + "/../../")  # so uggo thanks to atom runner
import unittest
import uav_design_system.athena_vortex_lattice as AVL
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
        self.result_api = AVL.AVLResults(self.content)

    def test_alpha(self):
        self.assertEqual(self.result_api.alpha, 1.28763)

    def test_cl(self):
        self.assertEqual(self.result_api.cl, 0.16549)

    def test_cd(self):
        self.assertEqual(self.result_api.cd, 0.00193)

    def test_efficiency(self):
        self.assertEqual(self.result_api.efficiency, 0.8828)

    def test_elevator(self):
        self.assertEqual(self.result_api.elevator_deflection, 2.81795)

    def test_y_distribution(self):
        actual_list = self.result_api.y_distribution
        self.assertEqual(len(actual_list), 60)
        self.assertEqual(actual_list[0], 0.0006)
        self.assertEqual(actual_list[1], 0.0053)
        self.assertEqual(actual_list[2], 0.0148)
        self.assertEqual(actual_list[29], 0.8494)
        self.assertEqual(actual_list[30], -0.0006)
        self.assertEqual(actual_list[59], -0.8494)

    def test_cl_distrbution(self):
        actual_list = list(self.result_api.cl_distribution)

        self.assertEqual(len(actual_list), 60)
        self.assertEqual(actual_list[0], 0.0618)
        self.assertEqual(actual_list[1], 0.0626)
        self.assertEqual(actual_list[2], 0.0638)
        self.assertEqual(actual_list[29], 0.0620)
        self.assertEqual(actual_list[30], 0.0618)
        self.assertEqual(actual_list[59], 0.0620)

if __name__ == "__main__":
    unittest.main()
